"""Stock TrainerのStreamlitエントリーポイント。"""

import streamlit as st

from data.downloader import download_daily_prices
from data.nikkei225 import NIKKEI_225_TICKERS
from game.question_generator import (
    CASH_OPTION_LABEL,
    generate_game_question,
    select_random_tickers,
)
from ui.charts import create_candlestick_chart, create_review_chart


CHART_TITLES = ("Chart A", "Chart B", "Chart C")
CHART_CARD_KEYS = ("chart_card_a", "chart_card_b", "chart_card_c")
CHART_BUTTON_KEYS = ("select_chart_a", "select_chart_b", "select_chart_c")
ERROR_MESSAGE = "問題データを生成できませんでした。時間をおいて再度お試しください。"
RESULT_ERROR_MESSAGE = "結果を表示できませんでした。時間をおいて再度お試しください。"


def initialize_session_state() -> None:
    """回答に必要なSession Stateを既存値を保ったまま初期化する。"""
    if "answer_choice" not in st.session_state:
        st.session_state.answer_choice = None
    if "selected_label" not in st.session_state:
        st.session_state.selected_label = None
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "current_view" not in st.session_state:
        st.session_state.current_view = (
            "result" if st.session_state.submitted else "question"
        )


def normalize_session_state() -> None:
    """回答状態の矛盾を補正し、表示画面を有効な値へ統一する。"""
    if not st.session_state.submitted:
        st.session_state.selected_label = None
        st.session_state.current_view = "question"
        return

    if st.session_state.selected_label is None:
        st.session_state.update(
            {
                "answer_choice": None,
                "selected_label": None,
                "submitted": False,
                "current_view": "question",
            }
        )
        return

    st.session_state.answer_choice = st.session_state.selected_label
    st.session_state.current_view = "result"


def select_answer(label: str) -> None:
    """回答確定前の選択中ラベルを保存する。"""
    if not st.session_state.submitted:
        st.session_state.answer_choice = label


def format_return_percent(value: float) -> str:
    """騰落率を符号付き小数第2位の表示文字列へ変換する。"""
    rounded = round(value, 2)
    if rounded == 0:
        return "0.00%"
    return f"{rounded:+.2f}%"


def format_price(value: float) -> str:
    """価格を3桁区切り、小数第2位、円表記へ変換する。"""
    return f"{value:,.2f}円"


def main() -> None:
    """3銘柄のチャートと回答UIを表示する。"""
    st.title("Stock Trainer")
    initialize_session_state()
    normalize_session_state()

    try:
        if "game_question" not in st.session_state:
            selected_tickers = select_random_tickers(NIKKEI_225_TICKERS)
            price_frames = tuple(
                download_daily_prices(ticker, period="5y")
                for ticker in selected_tickers
            )
            question = generate_game_question(selected_tickers, price_frames)
            st.session_state.game_question = question

        question = st.session_state.game_question
    except Exception:
        st.error(ERROR_MESSAGE)
        return

    if st.session_state.current_view == "result":
        try:
            review_figures = tuple(
                create_review_chart(
                    chart.display_data,
                    chart.future_data,
                    chart.base_date,
                    title=f"{chart.label} - Review",
                )
                for chart in question.charts
            )
            common_chart = question.charts[0]
            base_date_text = common_chart.base_date.strftime("%Y-%m-%d")
            evaluation_date_text = common_chart.evaluation_date.strftime(
                "%Y-%m-%d"
            )
            comparison_texts = tuple(
                (
                    f"基準日終値：{format_price(chart.base_close)}",
                    f"評価日終値：{format_price(chart.future_close)}",
                    "騰落率："
                    f"{format_return_percent(chart.future_return_percent)}",
                )
                for chart in question.charts
            )
            answer_text = f"あなたの回答：{st.session_state.selected_label}"
            correct_text = f"正解：{question.correct_label}"
            is_correct = (
                st.session_state.selected_label == question.correct_label
            )
            result_text = "正解！" if is_correct else "不正解"
            cash_return_text = "現金で保有：0.00%"
            cash_result_text = (
                "3つのChartがすべて0%以下だったため、"
                "現金保有が最も良い結果でした。"
                if question.correct_label == CASH_OPTION_LABEL
                else None
            )
        except Exception:
            st.error(RESULT_ERROR_MESSAGE)
            return

        st.header("結果発表")
        st.write(f"基準日：{base_date_text}")
        st.write(
            f"評価日：{evaluation_date_text}"
            "（20共通取引日後・おおむね約1か月後）"
        )
        st.write(answer_text)
        st.write(correct_text)
        st.write(result_text)
        st.write(cash_return_text)
        if cash_result_text is not None:
            st.write(cash_result_text)

        for chart, figure, comparison in zip(
            question.charts,
            review_figures,
            comparison_texts,
            strict=True,
        ):
            st.write(chart.label)
            for text in comparison:
                st.write(text)
            st.plotly_chart(figure, use_container_width=True)

        if st.button("次の問題", key="next_question"):
            try:
                next_tickers = select_random_tickers(NIKKEI_225_TICKERS)
                next_price_frames = tuple(
                    download_daily_prices(ticker, period="5y")
                    for ticker in next_tickers
                )
                next_question = generate_game_question(
                    next_tickers,
                    next_price_frames,
                )
                tuple(
                    create_candlestick_chart(
                        chart.display_data,
                        title=chart.label,
                    )
                    for chart in next_question.charts
                )
            except Exception:
                st.error(ERROR_MESSAGE)
            else:
                st.session_state.update(
                    {
                        "game_question": next_question,
                        "answer_choice": None,
                        "selected_label": None,
                        "submitted": False,
                        "current_view": "question",
                    }
                )
                st.rerun()
        return

    try:
        figures = tuple(
            create_candlestick_chart(
                chart.display_data,
                title=chart.label,
            )
            for chart in question.charts
        )
        common_chart = question.charts[0]
        display_start_text = common_chart.display_data.index[0].strftime(
            "%Y-%m-%d"
        )
        base_date_text = common_chart.base_date.strftime("%Y-%m-%d")
    except Exception:
        st.error(ERROR_MESSAGE)
        return

    selected_card_key = None
    if st.session_state.answer_choice in CHART_TITLES:
        selected_index = CHART_TITLES.index(st.session_state.answer_choice)
        selected_card_key = CHART_CARD_KEYS[selected_index]
    elif st.session_state.answer_choice == CASH_OPTION_LABEL:
        selected_card_key = "cash_option_card"

    selected_card_css = ""
    if selected_card_key is not None:
        selected_card_css = f"""
        .st-key-{selected_card_key} {{
            background-color: #F3F8FF;
            border: 2px solid #4A90E2;
            box-shadow: 0 4px 12px rgba(74, 144, 226, 0.15);
        }}
        """

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-color: #F6F8FB;
        }}
        .st-key-chart_card_a,
        .st-key-chart_card_b,
        .st-key-chart_card_c,
        .st-key-cash_option_card {{
            background-color: #FFFFFF;
            border: 1px solid #D9E2EC;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
        }}
        {selected_card_css}
        .st-key-submit_answer button {{
            background-color: #2F6FB2;
            color: #FFFFFF;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.write(f"観察期間：{display_start_text} ～ {base_date_text}")
    st.write(f"基準日（予測時点）：{base_date_text}")
    st.write("観察データ：120共通取引日（おおむね約6か月）")

    for chart, figure, card_key, button_key in zip(
        question.charts,
        figures,
        CHART_CARD_KEYS,
        CHART_BUTTON_KEYS,
        strict=True,
    ):
        with st.container(key=card_key):
            select_column, chart_column = st.columns(
                [1.5, 8.5],
                vertical_alignment="center",
            )
            with select_column:
                selection_mark = (
                    "●"
                    if st.session_state.answer_choice == chart.label
                    else "○"
                )
                st.button(
                    f"{selection_mark} {chart.label}",
                    key=button_key,
                    on_click=select_answer,
                    args=(chart.label,),
                    width="stretch",
                )
            with chart_column:
                st.plotly_chart(figure, use_container_width=True)

    st.write(
        "📈 あなたが利用できる情報はここまでです。"
        "この先約1か月（20共通取引日）の値動きを予測してください。"
    )
    st.write(
        "3つとも上昇しないと予想する場合は、"
        f"「{CASH_OPTION_LABEL}」を選択してください。"
    )

    with st.container(key="cash_option_card"):
        cash_selection_mark = (
            "●"
            if st.session_state.answer_choice == CASH_OPTION_LABEL
            else "○"
        )
        st.button(
            f"{cash_selection_mark} どれにも投資しない",
            key="select_cash_option",
            on_click=select_answer,
            args=(CASH_OPTION_LABEL,),
        )
        st.write("現金で保有する（騰落率 0.00%）")
        st.caption("3つとも上昇しないと思う場合はこちら")

    if st.button("回答する", key="submit_answer"):
        if st.session_state.answer_choice is None:
            st.warning("1つ選択してください。")
        else:
            st.session_state.update(
                {
                    "selected_label": st.session_state.answer_choice,
                    "submitted": True,
                    "current_view": "result",
                }
            )
            st.rerun()


if __name__ == "__main__":
    main()
