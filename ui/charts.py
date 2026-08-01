"""出題用チャートを生成する。"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def create_candlestick_chart(
    prices: pd.DataFrame,
    title: str = "Chart A",
) -> go.Figure:
    """会社名を伏せたローソク足チャートを生成する。

    Args:
        prices: 日付インデックスとOHLCV列を持つデータ。
        title: チャートに表示するタイトル。

    Returns:
        指定されたタイトルを持つPlotly Figure。

    Raises:
        ValueError: 必要な価格列が存在しない、またはデータが空の場合。
    """
    if prices.empty:
        raise ValueError("チャート用の株価データが空です。")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in prices]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"チャート生成に必要な列がありません: {missing}")

    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.03,
    )
    figure.add_trace(
        go.Candlestick(
            x=prices.index,
            open=prices["Open"],
            high=prices["High"],
            low=prices["Low"],
            close=prices["Close"],
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Bar(x=prices.index, y=prices["Volume"]),
        row=2,
        col=1,
    )

    trading_dates = pd.DatetimeIndex(pd.to_datetime(prices.index)).normalize()
    calendar_dates = pd.date_range(
        start=trading_dates.min(),
        end=trading_dates.max(),
        freq="D",
    )
    non_trading_dates = calendar_dates.difference(trading_dates)
    rangebreaks = [dict(values=non_trading_dates)]

    figure.update_layout(title=title, showlegend=False)
    figure.update_xaxes(rangebreaks=rangebreaks, rangeslider_visible=False)
    return figure
