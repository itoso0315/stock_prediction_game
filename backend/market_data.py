"""Yahoo Financeの株価をFlutter向けローソク足へ変換する。"""

from datetime import date, timedelta
from functools import lru_cache

import pandas as pd
import yfinance as yf


DEFAULT_CANDLE_COUNT = 120
_CALENDAR_LOOKBACK_DAYS = 320
_MOVING_AVERAGE_WINDOWS = (20, 40, 70)


def fetch_candles(
    ticker: str,
    base_date: str | date,
    count: int = DEFAULT_CANDLE_COUNT,
) -> list[dict[str, str | float | int]]:
    """基準日以前の日足OHLCを日付昇順で返す。

    yfinanceの ``end`` は排他的なため、基準日の翌日を指定する。
    休場日を含む暦日で広めに取得した後、末尾の営業日だけを採用する。
    """
    return fetch_chart_data(ticker, base_date, count)["candles"]


@lru_cache(maxsize=128)
def fetch_chart_data(
    ticker: str,
    base_date: str | date,
    count: int = DEFAULT_CANDLE_COUNT,
) -> dict[str, list[dict[str, str | float | int]]]:
    """基準日以前のローソク足と移動平均線を返す。"""
    if count <= 0:
        raise ValueError("ローソク足の本数は1以上である必要があります。")

    normalized_ticker = ticker.strip().upper()
    if not normalized_ticker.endswith(".T"):
        raise ValueError("日本株のYahoo Finance ticker（.T）を指定してください。")

    cutoff = pd.Timestamp(base_date).normalize()
    start = (cutoff - timedelta(days=_CALENDAR_LOOKBACK_DAYS)).date()
    end = (cutoff + timedelta(days=1)).date()
    prices = yf.download(
        normalized_ticker,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if prices.empty:
        raise ValueError(f"{normalized_ticker}の株価データを取得できませんでした。")
    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = prices.columns.get_level_values(0)

    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    missing = [column for column in required_columns if column not in prices]
    if missing:
        raise ValueError(f"取得データに必要な列がありません: {', '.join(missing)}")

    prices = prices.loc[:, required_columns].dropna().sort_index()
    prices.index = pd.to_datetime(prices.index).tz_localize(None).normalize()
    prices = prices.loc[prices.index <= cutoff]
    required_count = count + max(_MOVING_AVERAGE_WINDOWS) - 1
    if len(prices) < required_count:
        raise ValueError(
            f"{normalized_ticker}の株価データが不足しています: "
            f"{len(prices)}/{required_count}営業日"
        )

    for window in _MOVING_AVERAGE_WINDOWS:
        prices[f"MA{window}"] = prices["Close"].rolling(window=window).mean()

    display_prices = prices.tail(count)
    candles = [
        {
            "date": timestamp.date().isoformat(),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        }
        for timestamp, row in display_prices.iterrows()
    ]
    result: dict[str, list[dict[str, str | float | int]]] = {
        "candles": candles
    }
    for window in _MOVING_AVERAGE_WINDOWS:
        column = f"MA{window}"
        result[f"ma{window}"] = [
            {
                "date": timestamp.date().isoformat(),
                "value": float(row[column]),
            }
            for timestamp, row in display_prices.iterrows()
            if pd.notna(row[column])
        ]
    return result


def fetch_future_candles(
    ticker: str,
    base_date: str | date,
    evaluation_date: str | date,
) -> list[dict[str, str | float | int]]:
    """基準日より後から評価日までのResult用日足を返す。"""
    normalized_ticker = ticker.strip().upper()
    if not normalized_ticker.endswith(".T"):
        raise ValueError("日本株のYahoo Finance ticker（.T）を指定してください。")

    base = pd.Timestamp(base_date).normalize()
    evaluation = pd.Timestamp(evaluation_date).normalize()
    if evaluation <= base:
        raise ValueError("評価日は基準日より後である必要があります。")

    prices = yf.download(
        normalized_ticker,
        start=(base + timedelta(days=1)).date(),
        end=(evaluation + timedelta(days=8)).date(),
        interval="1d",
        auto_adjust=False,
        progress=False,
    )
    if prices.empty:
        raise ValueError(f"{normalized_ticker}の将来株価を取得できませんでした。")
    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = prices.columns.get_level_values(0)

    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    missing = [column for column in required_columns if column not in prices]
    if missing:
        raise ValueError(f"取得データに必要な列がありません: {', '.join(missing)}")

    prices = prices.loc[:, required_columns].dropna().sort_index()
    prices.index = pd.to_datetime(prices.index).tz_localize(None).normalize()
    prices = prices.loc[(prices.index > base) & (prices.index <= evaluation)]
    if prices.empty:
        raise ValueError(f"{normalized_ticker}の評価期間データがありません。")

    return [
        {
            "date": timestamp.date().isoformat(),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        }
        for timestamp, row in prices.iterrows()
    ]
