"""出題用チャートを生成する。"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def create_candlestick_chart(
    prices: pd.DataFrame,
    title: str = "Chart A",
    show_ma25: bool = False,
    show_ma50: bool = False,
    show_ma75: bool = False,
) -> go.Figure:
    """会社名を伏せたローソク足チャートを生成する。

    Args:
        prices: 日付インデックスとOHLCV列を持つデータ。
        title: チャートに表示するタイトル。
        show_ma25: 25日移動平均線を表示するか。
        show_ma50: 50日移動平均線を表示するか。
        show_ma75: 75日移動平均線を表示するか。

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
            name="",
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    moving_average_specs = (
        (25, "MA25", "#2563EB", show_ma25),
        (50, "MA50", "#F59E0B", show_ma50),
        (75, "MA75", "#7C3AED", show_ma75),
    )
    for window, label, color, is_visible in moving_average_specs:
        if not is_visible:
            continue
        moving_average = prices["Close"].rolling(
            window=window,
            min_periods=1,
        ).mean()
        figure.add_trace(
            go.Scatter(
                x=prices.index,
                y=moving_average,
                mode="lines",
                name=label,
                line={"width": 2, "color": color},
                hovertemplate=f"{label}: %{{y:,.2f}}円<extra></extra>",
            ),
            row=1,
            col=1,
        )
    figure.add_trace(
        go.Bar(
            x=prices.index,
            y=prices["Volume"],
            name="",
            showlegend=False,
        ),
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

    figure.update_layout(
        title=title,
        showlegend=show_ma25 or show_ma50 or show_ma75,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
    )
    figure.update_xaxes(rangebreaks=rangebreaks, rangeslider_visible=False)
    return figure


def create_review_chart(
    display_data: pd.DataFrame,
    future_data: pd.DataFrame,
    base_date: pd.Timestamp,
    title: str = "Chart A - Review",
    show_ma25: bool = False,
    show_ma50: bool = False,
    show_ma75: bool = False,
) -> go.Figure:
    """観察期間と将来期間を連結した結果確認用チャートを生成する。

    Args:
        display_data: 200共通取引日分の観察用OHLCVデータ。
        future_data: 20共通取引日分の将来OHLCVデータ。
        base_date: 観察期間の最終日。
        title: チャートに表示するタイトル。
        show_ma25: 25日移動平均線を表示するか。
        show_ma50: 50日移動平均線を表示するか。
        show_ma75: 75日移動平均線を表示するか。

    Returns:
        220共通取引日のローソク足と出来高を持つPlotly Figure。

    Raises:
        ValueError: 必須列、件数、日付、期間境界が要件を満たさない場合。
    """
    frames = (
        ("display_data", display_data, 200),
        ("future_data", future_data, 20),
    )
    validated: list[pd.DataFrame] = []
    for name, prices, expected_length in frames:
        missing_columns = [
            column for column in REQUIRED_COLUMNS if column not in prices
        ]
        if missing_columns:
            missing = ", ".join(missing_columns)
            raise ValueError(f"{name}に必要な列がありません: {missing}")
        if len(prices) != expected_length:
            raise ValueError(f"{name}は{expected_length}件である必要があります。")

        copied = prices.copy(deep=True)
        try:
            dates = pd.DatetimeIndex(
                pd.to_datetime(copied.index, errors="raise")
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"{name}に日付へ変換できないインデックスが含まれています。"
            ) from error
        if dates.isna().any():
            raise ValueError(f"{name}の日付インデックスにNaTが含まれています。")
        if dates.tz is not None:
            dates = dates.tz_localize(None)

        copied.index = dates
        if not copied.index.is_monotonic_increasing:
            raise ValueError(f"{name}の日付インデックスが昇順ではありません。")
        if copied.index.has_duplicates:
            raise ValueError(f"{name}の日付インデックスに重複があります。")
        validated.append(copied)

    display_copy, future_copy = validated
    try:
        normalized_base_date = pd.Timestamp(base_date)
    except (TypeError, ValueError) as error:
        raise ValueError("base_dateを日付として扱えません。") from error
    if pd.isna(normalized_base_date):
        raise ValueError("base_dateにNaTは使用できません。")
    if normalized_base_date.tz is not None:
        normalized_base_date = normalized_base_date.tz_localize(None)

    if display_copy.index[-1] != normalized_base_date:
        raise ValueError("display_dataの最終日とbase_dateが一致しません。")
    if future_copy.index[0] <= normalized_base_date:
        raise ValueError("future_dataはbase_dateより後に開始する必要があります。")
    if not display_copy.index.intersection(future_copy.index).empty:
        raise ValueError("display_dataとfuture_dataの日付が重複しています。")

    combined_data = pd.concat(
        [display_copy, future_copy],
        axis=0,
        copy=True,
    )
    if len(combined_data) != 220:
        raise ValueError("連結後のデータは220件である必要があります。")
    if not combined_data.index.is_monotonic_increasing:
        raise ValueError("連結後の日付インデックスが昇順ではありません。")
    if combined_data.index.has_duplicates:
        raise ValueError("連結後の日付インデックスに重複があります。")

    boundary_x = display_copy.index[-1] + (
        future_copy.index[0] - display_copy.index[-1]
    ) / 2
    future_last_half_width = (
        future_copy.index[-1] - future_copy.index[-2]
    ) / 2
    background_x0 = boundary_x
    background_x1 = future_copy.index[-1] + future_last_half_width

    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.03,
    )
    figure.add_trace(
        go.Candlestick(
            x=combined_data.index,
            open=combined_data["Open"],
            high=combined_data["High"],
            low=combined_data["Low"],
            close=combined_data["Close"],
            name="",
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    moving_average_specs = (
        (25, "MA25", "#2563EB", show_ma25),
        (50, "MA50", "#F59E0B", show_ma50),
        (75, "MA75", "#7C3AED", show_ma75),
    )
    for window, label, color, is_visible in moving_average_specs:
        if not is_visible:
            continue
        moving_average = combined_data["Close"].rolling(
            window=window,
            min_periods=1,
        ).mean()
        figure.add_trace(
            go.Scatter(
                x=combined_data.index,
                y=moving_average,
                mode="lines",
                name=label,
                line={"width": 2, "color": color},
                hovertemplate=f"{label}: %{{y:,.2f}}円<extra></extra>",
            ),
            row=1,
            col=1,
        )
    figure.add_trace(
        go.Bar(
            x=combined_data.index,
            y=combined_data["Volume"],
            name="",
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    figure.add_vrect(
        x0=background_x0,
        x1=background_x1,
        fillcolor="lightgray",
        opacity=0.15,
        layer="below",
        line_width=0,
        row="all",
        col=1,
    )
    figure.add_vline(
        x=boundary_x,
        line_dash="dash",
        line_color="gray",
        line_width=1,
        row="all",
        col=1,
    )

    total_count = len(combined_data)
    boundary_paper_x = len(display_copy) / total_count
    future_center_paper_x = (
        len(display_copy) + len(future_copy) / 2
    ) / total_count
    figure.add_annotation(
        x=boundary_paper_x - 0.01,
        y=1.02,
        xref="paper",
        yref="paper",
        text="ここまで見て予測",
        showarrow=False,
        xanchor="right",
        yanchor="bottom",
    )
    figure.add_annotation(
        x=future_center_paper_x,
        y=1.02,
        xref="paper",
        yref="paper",
        text="予測対象期間",
        showarrow=False,
        xanchor="center",
        yanchor="bottom",
    )

    calendar_dates = pd.date_range(
        start=combined_data.index.min(),
        end=combined_data.index.max(),
        freq="D",
    )
    non_trading_dates = calendar_dates.difference(combined_data.index)
    rangebreaks = [dict(values=non_trading_dates)]

    figure.update_layout(
        title=title,
        showlegend=show_ma25 or show_ma50 or show_ma75,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
    )
    figure.update_xaxes(rangebreaks=rangebreaks, rangeslider_visible=False)
    return figure
