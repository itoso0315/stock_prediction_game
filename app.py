"""Stock TrainerのStreamlitエントリーポイント。"""

import streamlit as st

from data.downloader import download_daily_prices
from data.nikkei225 import NIKKEI_225_TICKERS
from game.question_generator import generate_game_question, select_random_tickers
from ui.charts import create_candlestick_chart


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


def main() -> None:
    """3銘柄のチャートと回答UIを表示する。"""
    st.title("Stock Trainer")
    initialize_session_state()

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

    if st.session_state.submitted:
        try:
            figures = tuple(
                create_candlestick_chart(
                    chart.display_data,
                    title=chart.label,
                )
                for chart in question.charts
            )
            future_figures = tuple(
                create_candlestick_chart(
                    chart.future_data,
                    title=f"{chart.label} - Result",
                )
                for chart in question.charts
            )
        except Exception:
            st.error(RESULT_ERROR_MESSAGE)
            return

        for chart, figure in zip(question.charts, figures, strict=True):
            st.plotly_chart(figure, use_container_width=True)
            st.button(
                f"{chart.label}を選ぶ",
                key=f"select_{chart.label.lower().replace(' ', '_')}",
                disabled=True,
                on_click=select_answer,
                args=(chart.label,),
            )

        is_correct = st.session_state.selected_label == question.correct_label
        st.write(f"あなたの回答：{st.session_state.selected_label}")
        st.write(f"正解：{question.correct_label}")
        st.write("正解！" if is_correct else "不正解")

        for chart, figure in zip(question.charts, future_figures, strict=True):
            st.write(
                f"{chart.label}：{format_return_percent(chart.future_return_percent)}"
            )
            st.plotly_chart(figure, use_container_width=True)
        return

    try:
        figures = tuple(
            create_candlestick_chart(
                chart.display_data,
                title=chart.label,
            )
            for chart in question.charts
        )
    except Exception:
        st.error(ERROR_MESSAGE)
        return

    for chart, figure in zip(question.charts, figures, strict=True):
        st.plotly_chart(figure, use_container_width=True)
        st.button(
            f"{chart.label}を選ぶ",
            key=f"select_{chart.label.lower().replace(' ', '_')}",
            disabled=False,
            on_click=select_answer,
            args=(chart.label,),
        )

    if st.session_state.answer_choice is not None:
        st.write(f"選択中：{st.session_state.answer_choice}")

    if st.button("回答する", key="submit_answer"):
        if st.session_state.answer_choice is None:
            st.warning("1つ選択してください。")
        else:
            st.session_state.selected_label = st.session_state.answer_choice
            st.session_state.submitted = True
            st.rerun()


if __name__ == "__main__":
    main()
