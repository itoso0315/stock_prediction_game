"""Yahoo Financeから日本株の日足データを取得する。"""

from datetime import date

import pandas as pd
import yfinance as yf


PRICE_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def normalize_japanese_ticker(ticker: str) -> str:
    """銘柄コードをYahoo Financeの日本株ティッカー形式へ変換する。

    Args:
        ticker: 4桁の銘柄コード、または末尾が ``.T`` のティッカー。

    Returns:
        末尾に ``.T`` が付いたYahoo Finance向けティッカー。

    Raises:
        ValueError: 銘柄コードが空、または日本株形式でない場合。
    """
    normalized = ticker.strip().upper()
    if normalized.endswith(".T"):
        code = normalized[:-2]
    else:
        code = normalized

    if len(code) != 4 or not code.isdigit():
        raise ValueError("日本株の4桁銘柄コードを指定してください。")
    return f"{code}.T"


def download_daily_prices(
    ticker: str,
    start: str | date | None = None,
    end: str | date | None = None,
    period: str | None = None,
) -> pd.DataFrame:
    """Yahoo Financeから日本株の日足OHLCVデータを取得する。

    ``start``/``end`` または ``period`` のどちらかで取得期間を指定する。
    どちらも未指定の場合は、利用可能な全期間を取得する。

    Args:
        ticker: 4桁の日本株銘柄コード、または ``.T`` 付きティッカー。
        start: 取得開始日（この日を含む）。
        end: 取得終了日（Yahoo Financeではこの日を含まない）。
        period: ``5y`` など、yfinanceが受け付ける取得期間。

    Returns:
        日付をインデックスとし、Open、High、Low、Close、Volume列を持つ
        日足データ。欠損行は除外される。

    Raises:
        ValueError: 引数の組み合わせが不正、またはデータが取得できない場合。
    """
    if period is not None and (start is not None or end is not None):
        raise ValueError("periodとstart/endは同時に指定できません。")

    symbol = normalize_japanese_ticker(ticker)
    download_options: dict[str, str | date | bool] = {
        "interval": "1d",
        "auto_adjust": False,
        "progress": False,
    }
    if period is not None:
        download_options["period"] = period
    elif start is not None or end is not None:
        if start is not None:
            download_options["start"] = start
        if end is not None:
            download_options["end"] = end
    else:
        download_options["period"] = "max"

    raw_data = yf.download(symbol, **download_options)
    if raw_data.empty:
        raise ValueError(f"{symbol}の株価データを取得できませんでした。")

    if isinstance(raw_data.columns, pd.MultiIndex):
        raw_data.columns = raw_data.columns.get_level_values(0)

    missing_columns = [column for column in PRICE_COLUMNS if column not in raw_data]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"取得データに必要な列がありません: {missing}")

    prices = raw_data.loc[:, PRICE_COLUMNS].copy()
    prices.index = pd.to_datetime(prices.index)
    prices.index.name = "Date"
    return prices.dropna(subset=PRICE_COLUMNS).sort_index()
