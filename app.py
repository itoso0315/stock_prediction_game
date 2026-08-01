"""Stock TrainerのStreamlitエントリーポイント。"""

import streamlit as st

from data.downloader import download_daily_prices
from data.nikkei225 import NIKKEI_225_TICKERS
from game.question_generator import generate_game_question, select_random_tickers
from ui.charts import create_candlestick_chart, create_review_chart


CHART_TITLES = ("Chart A", "Chart B", "Chart C")
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
        except Exception:
            st.error(RESULT_ERROR_MESSAGE)
            return

        st.header("結果発表")
        st.write(f"基準日：{base_date_text}")
        st.write(
            f"評価日：{evaluation_date_text}"
            "（20共通取引日後・おおむね約1か月後）"
        )
        is_correct = st.session_state.selected_label == question.correct_label
        st.write(f"あなたの回答：{st.session_state.selected_label}")
        st.write(f"正解：{question.correct_label}")
        st.write("正解！" if is_correct else "不正解")

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

    st.write(f"観察期間：{display_start_text} ～ {base_date_text}")
    st.write(f"基準日（予測時点）：{base_date_text}")
    st.write("観察データ：120共通取引日（おおむね約6か月）")

    for chart, figure in zip(question.charts, figures, strict=True):
        st.plotly_chart(figure, use_container_width=True)
        st.button(
            f"{chart.label}を選ぶ",
            key=f"select_{chart.label.lower().replace(' ', '_')}",
            disabled=False,
            on_click=select_answer,
            args=(chart.label,),
        )

    st.write(
        "📈 あなたが利用できる情報はここまでです。"
        "この先約1か月（20共通取引日）の値動きを予測してください。"
    )

    if st.session_state.answer_choice is not None:
        st.write(f"選択中：{st.session_state.answer_choice}")

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
