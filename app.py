"""Stock TrainerのStreamlitエントリーポイント。"""

import streamlit as st

from data.downloader import download_daily_prices
from data.nikkei225 import NIKKEI_225_TICKERS
from game.question_generator import select_random_tickers
from ui.charts import create_candlestick_chart


CHART_TITLES = ("Chart A", "Chart B", "Chart C")
ERROR_MESSAGE = "チャートを表示できませんでした。時間をおいて再度お試しください。"


def main() -> None:
    """3銘柄のローソク足チャートを縦方向に表示する。"""
    st.title("Stock Trainer")

    try:
        selected_tickers = select_random_tickers(NIKKEI_225_TICKERS)
        for ticker, title in zip(selected_tickers, CHART_TITLES, strict=True):
            prices = download_daily_prices(ticker, period="6mo")
            figure = create_candlestick_chart(prices, title=title)
            st.plotly_chart(figure, use_container_width=True)
    except Exception:
        st.error(ERROR_MESSAGE)


if __name__ == "__main__":
    main()
