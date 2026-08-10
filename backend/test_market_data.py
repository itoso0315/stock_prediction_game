from unittest.mock import patch

import pandas as pd

from backend.market_data import fetch_candles, fetch_chart_data, fetch_future_candles


def test_fetch_candles_returns_latest_120_days_through_base_date():
    index = pd.bdate_range("2023-09-01", periods=189)
    prices = pd.DataFrame(
        {
            "Open": range(100, 289),
            "High": range(102, 291),
            "Low": range(99, 288),
            "Close": range(101, 290),
            "Volume": range(1000, 1189),
        },
        index=index,
    )
    base_date = index[-1].date().isoformat()

    with patch("backend.market_data.yf.download", return_value=prices) as download:
        candles = fetch_candles("7203.T", base_date)

    assert len(candles) == 120
    assert candles[0]["date"] == index[-120].date().isoformat()
    assert candles[-1] == {
        "date": base_date,
        "open": 288.0,
        "high": 290.0,
        "low": 287.0,
        "close": 289.0,
        "volume": 1188,
    }
    assert candles == sorted(candles, key=lambda candle: candle["date"])
    assert download.call_args.kwargs["end"].isoformat() == (
        index[-1] + pd.Timedelta(days=1)
    ).date().isoformat()


def test_fetch_candles_excludes_rows_after_base_date():
    index = pd.bdate_range("2023-09-01", periods=190)
    prices = pd.DataFrame(
        {
            "Open": range(190),
            "High": range(1, 191),
            "Low": range(190),
            "Close": range(1, 191),
            "Volume": range(2000, 2190),
        },
        index=index,
    )
    base_date = index[-2].date().isoformat()

    with patch("backend.market_data.yf.download", return_value=prices):
        candles = fetch_candles("6758.T", base_date)

    assert len(candles) == 120
    assert candles[-1]["date"] == base_date
    assert all(candle["date"] <= base_date for candle in candles)
    assert candles[-1]["volume"] == 2188


def test_fetch_chart_data_calculates_moving_averages_for_display_dates():
    index = pd.bdate_range("2023-09-01", periods=189)
    prices = pd.DataFrame(
        {
            "Open": range(100, 289),
            "High": range(102, 291),
            "Low": range(99, 288),
            "Close": range(101, 290),
            "Volume": range(1000, 1189),
        },
        index=index,
    )

    with patch("backend.market_data.yf.download", return_value=prices):
        chart_data = fetch_chart_data("7203.T", index[-1].date().isoformat())

    candle_dates = [candle["date"] for candle in chart_data["candles"]]
    for key in ("ma20", "ma40", "ma70"):
        assert len(chart_data[key]) == 120
        assert [point["date"] for point in chart_data[key]] == candle_dates
    assert chart_data["ma20"][-1]["value"] == 279.5
    assert chart_data["ma70"][-1]["value"] == 254.5


def test_fetch_chart_data_backfills_when_first_response_is_partial():
    index = pd.bdate_range("2023-01-02", periods=220)
    prices = pd.DataFrame(
        {
            "Open": range(220),
            "High": range(1, 221),
            "Low": range(220),
            "Close": range(1, 221),
            "Volume": range(1000, 1220),
        },
        index=index,
    )
    partial_prices = prices.tail(93)
    older_prices = prices.loc[prices.index < partial_prices.index.min()]

    with patch(
        "backend.market_data.yf.download",
        side_effect=[partial_prices, older_prices],
    ) as download:
        chart_data = fetch_chart_data("8306.T", index[-1].date().isoformat())

    assert download.call_count == 2
    assert download.call_args_list[1].kwargs["end"] == partial_prices.index.min().date()
    assert len(chart_data["candles"]) == 120
    assert len(chart_data["ma70"]) == 120


def test_fetch_future_candles_excludes_base_date_and_rows_after_evaluation():
    index = pd.bdate_range("2024-05-01", "2024-08-05")
    prices = pd.DataFrame(
        {
            "Open": range(len(index)),
            "High": range(1, len(index) + 1),
            "Low": range(len(index)),
            "Close": range(1, len(index) + 1),
            "Volume": range(1000, 1000 + len(index)),
        },
        index=index,
    )
    with patch("backend.market_data.yf.download", return_value=prices):
        candles = fetch_future_candles("7203.T", "2024-05-01", "2024-08-01")

    assert candles[0]["date"] > "2024-05-01"
    assert candles[-1]["date"] == "2024-08-01"
    assert all(candle["date"] <= "2024-08-01" for candle in candles)
