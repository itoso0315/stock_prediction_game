"""過去の株価データから出題用データを生成する。"""

from dataclasses import dataclass
import random

import pandas as pd


DISPLAY_TRADING_DAYS = 60
FORECAST_TRADING_DAYS = 60


def select_random_tickers(
    tickers: tuple[str, ...],
    count: int = 3,
    rng: random.Random | None = None,
) -> tuple[str, ...]:
    """銘柄一覧から重複しない銘柄をランダムに選択する。

    Args:
        tickers: 選択元の銘柄コード一覧。
        count: 選択する銘柄数。
        rng: 結果を再現するときに使用する乱数生成器。

    Returns:
        選択された銘柄コードのタプル。

    Raises:
        ValueError: 選択数が0以下、または一覧の件数を超える場合。
    """
    if count <= 0:
        raise ValueError("選択数は1以上である必要があります。")
    if count > len(tickers):
        raise ValueError("選択数が銘柄一覧の件数を超えています。")

    random_source = rng if rng is not None else random
    return tuple(random_source.sample(tickers, count))


@dataclass(frozen=True)
class Question:
    """1銘柄分のチャートと、その後約3か月の結果を保持する。"""

    display_data: pd.DataFrame
    future_return_percent: float
    base_date: pd.Timestamp
    evaluation_date: pd.Timestamp


def calculate_return_percent(start_price: float, end_price: float) -> float:
    """開始価格から終了価格までの騰落率を百分率で計算する。

    Args:
        start_price: 判定開始時点の終値。
        end_price: 判定終了時点の終値。

    Returns:
        騰落率（%）。

    Raises:
        ValueError: 開始価格が0以下の場合。
    """
    if start_price <= 0:
        raise ValueError("開始価格は0より大きい必要があります。")
    return (end_price / start_price - 1) * 100


def generate_question(
    prices: pd.DataFrame,
    rng: random.Random | None = None,
) -> Question:
    """ランダムな開始位置から出題用データを生成する。

    連続する60営業日をチャート表示用に切り出し、その最終日の終値と、
    さらに60営業日後（約3か月後）の終値から騰落率を計算する。

    Args:
        prices: 日付順のOHLCVデータ。少なくともClose列が必要。
        rng: 乱数生成器。テストなどで出題を再現するときに指定する。

    Returns:
        表示データと将来の騰落率を含む問題。

    Raises:
        ValueError: 必要な列・行数・終値が揃っていない場合。
    """
    if "Close" not in prices.columns:
        raise ValueError("株価データにClose列が必要です。")

    required_rows = DISPLAY_TRADING_DAYS + FORECAST_TRADING_DAYS
    ordered_prices = prices.sort_index()
    if len(ordered_prices) < required_rows:
        raise ValueError(f"問題生成には少なくとも{required_rows}営業日分のデータが必要です。")

    random_source = rng if rng is not None else random.Random()
    max_start_index = len(ordered_prices) - required_rows
    start_index = random_source.randint(0, max_start_index)
    display_end_index = start_index + DISPLAY_TRADING_DAYS - 1
    evaluation_index = display_end_index + FORECAST_TRADING_DAYS

    display_data = ordered_prices.iloc[
        start_index : display_end_index + 1
    ].copy()
    base_price = float(ordered_prices["Close"].iloc[display_end_index])
    evaluation_price = float(ordered_prices["Close"].iloc[evaluation_index])

    if pd.isna(base_price) or pd.isna(evaluation_price):
        raise ValueError("騰落率の計算に必要な終値が欠損しています。")

    return Question(
        display_data=display_data,
        future_return_percent=calculate_return_percent(base_price, evaluation_price),
        base_date=pd.Timestamp(ordered_prices.index[display_end_index]),
        evaluation_date=pd.Timestamp(ordered_prices.index[evaluation_index]),
    )
