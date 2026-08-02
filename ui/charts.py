# Chart helper module for candlestick and review charts
import pandas as pd
import plotly.graph_objs as go

def _get_dates(price_df):
    """Return chart dates from a Date column or the DataFrame index."""
    if "Date" in price_df.columns:
        return price_df["Date"]
    return price_df.index

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
    fig = go.Figure()
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
        )
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
            )
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
            )
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
            )
        )
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            x=0,
            xanchor="left",
            y=1,
            yanchor="top",
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=350,
    )
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
    fig = go.Figure()
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
        )
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
        )
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
            )
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
            )
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
            )
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
        )
        fig.add_vline(
            x=base_date,
            line=dict(color="black", width=2, dash="dash"),
            annotation_text="予想時点",
            annotation_position="top left",
        )
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            x=0,
            xanchor="left",
            y=1,
            yanchor="top",
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=350,
    )
    return fig
