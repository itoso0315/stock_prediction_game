"""Stock TrainerのStreamlitエントリーポイント。"""

import streamlit as st

from data.downloader import download_daily_prices
from data.nikkei225 import NIKKEI_225_TICKERS
from game.question_generator import generate_game_question, select_random_tickers
from ui.charts import create_candlestick_chart


CHART_TITLES = ("Chart A", "Chart B", "Chart C")
ERROR_MESSAGE = "問題データを生成できませんでした。時間をおいて再度お試しください。"


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
        figures = tuple(
            create_candlestick_chart(
                chart.display_data,
                title=chart.label,
            )
            for chart in question.charts
        )
        for chart, figure in zip(question.charts, figures, strict=True):
            st.plotly_chart(figure, use_container_width=True)
            st.button(
                f"{chart.label}を選ぶ",
                key=f"select_{chart.label.lower().replace(' ', '_')}",
                disabled=st.session_state.submitted,
                on_click=select_answer,
                args=(chart.label,),
            )
    except Exception:
        st.error(ERROR_MESSAGE)
        return

    if st.session_state.submitted:
        st.write(f"回答：{st.session_state.selected_label}")
        return

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
