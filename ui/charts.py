# Chart helper module for candlestick and review charts
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def _get_dates(price_df):
    """Return chart dates from a Date column or the DataFrame index."""
    if "Date" in price_df.columns:
        return price_df["Date"]
    return price_df.index


def _volume_colors(price_df):
    """Return red/green volume colors matching bullish/bearish candles."""
    return [
        "red" if close >= open_price else "green"
        for open_price, close in zip(price_df["Open"], price_df["Close"])
    ]

def create_candlestick_chart(
    price_df,
    title="",
    show_ma25=False,
    show_ma50=False,
    show_ma75=False,
):
    """
    Generate a Plotly candlestick chart with optional moving averages.
    price_df: pd.DataFrame with columns ['Date','Open','High','Low','Close']
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.78, 0.22],
    )
    fig.add_trace(
        go.Candlestick(
            x=_get_dates(price_df),
            open=price_df["Open"],
            high=price_df["High"],
            low=price_df["Low"],
            close=price_df["Close"],
            name="Candlestick",
            showlegend=False,
            increasing_line_color="red",
            increasing_fillcolor="red",
            decreasing_line_color="green",
            decreasing_fillcolor="green",
        ),
        row=1,
        col=1,
    )
    if show_ma25:
        ma25 = price_df["Close"].rolling(window=25).mean()
        fig.add_trace(
            go.Scatter(
                x=_get_dates(price_df),
                y=ma25,
                mode="lines",
                name="MA25",
                line=dict(color="orange", width=1),
            ),
            row=1,
            col=1,
        )
    if show_ma50:
        ma50 = price_df["Close"].rolling(window=50).mean()
        fig.add_trace(
            go.Scatter(
                x=_get_dates(price_df),
                y=ma50,
                mode="lines",
                name="MA50",
                line=dict(color="green", width=1),
            ),
            row=1,
            col=1,
        )
    if show_ma75:
        ma75 = price_df["Close"].rolling(window=75).mean()
        fig.add_trace(
            go.Scatter(
                x=_get_dates(price_df),
                y=ma75,
                mode="lines",
                name="MA75",
                line=dict(color="purple", width=1),
            ),
            row=1,
            col=1,
        )
    fig.add_trace(
        go.Bar(
            x=_get_dates(price_df),
            y=price_df["Volume"],
            marker_color=_volume_colors(price_df),
            opacity=0.35,
            name="Volume",
            showlegend=False,
        ),
        row=2,
        col=1,
    )
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            x=0,
            xanchor="left",
            y=1,
            yanchor="top",
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=430,
    )
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    return fig

def create_review_chart(
    display_data,
    future_data,
    base_date=None,
    title="",
    show_ma25=False,
    show_ma50=False,
    show_ma75=False,
):
    """
    Generate a review chart with historical and future data.
    display_data: pd.DataFrame (past data)
    future_data: pd.DataFrame (future data)
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.78, 0.22],
    )
    # Historical data
    fig.add_trace(
        go.Candlestick(
            x=_get_dates(display_data),
            open=display_data["Open"],
            high=display_data["High"],
            low=display_data["Low"],
            close=display_data["Close"],
            name="Past",
            showlegend=False,
            increasing_line_color="red",
            increasing_fillcolor="red",
            decreasing_line_color="green",
            decreasing_fillcolor="green",
        ),
        row=1,
        col=1,
    )
    # Future data
    fig.add_trace(
        go.Candlestick(
            x=_get_dates(future_data),
            open=future_data["Open"],
            high=future_data["High"],
            low=future_data["Low"],
            close=future_data["Close"],
            name="Future",
            showlegend=False,
            increasing_line_color="red",
            increasing_fillcolor="red",
            decreasing_line_color="green",
            decreasing_fillcolor="green",
        ),
        row=1,
        col=1,
    )
    # Moving averages on the combined data
    # Keep the original date index when Date is stored in the index. Resetting it
    # makes Plotly interpret the moving-average x values as epoch-based dates.
    combined = pd.concat([display_data, future_data])
    if show_ma25:
        ma25 = combined["Close"].rolling(window=25).mean()
        fig.add_trace(
            go.Scatter(
                x=_get_dates(combined),
                y=ma25,
                mode="lines",
                name="MA25",
                line=dict(color="orange", width=1),
            ),
            row=1,
            col=1,
        )
    if show_ma50:
        ma50 = combined["Close"].rolling(window=50).mean()
        fig.add_trace(
            go.Scatter(
                x=_get_dates(combined),
                y=ma50,
                mode="lines",
                name="MA50",
                line=dict(color="green", width=1),
            ),
            row=1,
            col=1,
        )
    if show_ma75:
        ma75 = combined["Close"].rolling(window=75).mean()
        fig.add_trace(
            go.Scatter(
                x=_get_dates(combined),
                y=ma75,
                mode="lines",
                name="MA75",
                line=dict(color="purple", width=1),
            ),
            row=1,
            col=1,
        )
    for prices in (display_data, future_data):
        fig.add_trace(
            go.Bar(
                x=_get_dates(prices),
                y=prices["Volume"],
                marker_color=_volume_colors(prices),
                opacity=0.35,
                name="Volume",
                showlegend=False,
            ),
            row=2,
            col=1,
        )
    # Optionally, add a vertical line for base_date
    if base_date is not None:
        display_dates = _get_dates(display_data)
        past_start = (
            display_dates.iloc[0]
            if isinstance(display_dates, pd.Series)
            else display_dates[0]
        )
        fig.add_vrect(
            x0=past_start,
            x1=base_date,
            fillcolor="lightgray",
            opacity=0.18,
            layer="below",
            line_width=0,
            row="all",
            col=1,
        )
        fig.add_vline(
            x=base_date,
            line=dict(color="black", width=2, dash="dash"),
            row="all",
            col=1,
        )
        fig.add_annotation(
            x=base_date,
            y=1,
            xref="x",
            yref="y domain",
            text="予想時点",
            showarrow=False,
            xanchor="right",
            yanchor="bottom",
        )
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            x=0,
            xanchor="left",
            y=1,
            yanchor="top",
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=430,
    )
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    return fig
