"""出題用チャートを生成する。"""

import pandas as pd
import plotly.graph_objects as go


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close"]


def create_candlestick_chart(prices: pd.DataFrame) -> go.Figure:
    """会社名を伏せたローソク足チャートを生成する。

    Args:
        prices: 日付インデックスとOpen、High、Low、Close列を持つデータ。

    Returns:
        タイトルが「Chart A」のPlotly Figure。

    Raises:
        ValueError: 必要な価格列が存在しない、またはデータが空の場合。
    """
    if prices.empty:
        raise ValueError("チャート用の株価データが空です。")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in prices]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"チャート生成に必要な列がありません: {missing}")

    figure = go.Figure(
        data=[
            go.Candlestick(
                x=prices.index,
                open=prices["Open"],
                high=prices["High"],
                low=prices["Low"],
                close=prices["Close"],
            )
        ]
    )
    figure.update_layout(title="Chart A", xaxis_rangeslider_visible=False)
    return figure
