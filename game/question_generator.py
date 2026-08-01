"""過去の株価データから出題用データを生成する。"""

from dataclasses import dataclass
import math
from numbers import Real
import random

import pandas as pd


DISPLAY_TRADING_DAYS = 120
FORECAST_TRADING_DAYS = 20
_CHART_LABELS = ("Chart A", "Chart B", "Chart C")
_REQUIRED_PRICE_COLUMNS = ("Open", "High", "Low", "Close", "Volume")


@dataclass(frozen=True)
class ChartQuestion:
    """1銘柄分の表示データと将来評価結果を保持する。"""

    label: str
    ticker: str
    display_data: pd.DataFrame
    base_date: pd.Timestamp
    evaluation_date: pd.Timestamp
    base_close: float
    future_close: float
    future_return_percent: float
    future_data: pd.DataFrame


@dataclass(frozen=True)
class GameQuestion:
    """Chart A、Chart B、Chart Cからなるゲーム1問分を保持する。"""

    charts: tuple[ChartQuestion, ChartQuestion, ChartQuestion]
    correct_label: str


def _normalize_price_frame(prices: pd.DataFrame) -> pd.DataFrame:
    """株価データのコピーを日付単位の一意なインデックスへ正規化する。"""
    if prices.empty:
        raise ValueError("空の株価データは使用できません。")

    normalized = prices.copy(deep=True)
    try:
        dates = pd.DatetimeIndex(pd.to_datetime(normalized.index, errors="raise"))
    except (TypeError, ValueError) as error:
        raise ValueError("日付へ変換できないインデックスが含まれています。") from error

    if dates.isna().any():
        raise ValueError("日付インデックスにNaTが含まれています。")
    if dates.tz is not None:
        dates = dates.tz_localize(None)

    normalized.index = dates.normalize()
    normalized = normalized.loc[
        ~normalized.index.duplicated(keep="last")
    ].sort_index()
    return normalized


def select_common_window(
    price_frames: tuple[pd.DataFrame, ...],
    window_size: int = DISPLAY_TRADING_DAYS,
    rng: random.Random | None = None,
) -> tuple[pd.DataFrame, ...]:
    """3銘柄の共通取引日から同一期間の株価データを抽出する。

    Args:
        price_frames: 入力順を維持する3銘柄分の株価データ。
        window_size: 抽出する共通取引日の件数。
        rng: 結果を再現するときに使用する乱数生成器。

    Returns:
        同一の日付インデックスを持つ株価データのタプル。

    Raises:
        ValueError: 入力数、期間、日付インデックスが要件を満たさない場合。
    """
    if window_size <= 0:
        raise ValueError("表示期間は1日以上である必要があります。")
    if len(price_frames) != 3:
        raise ValueError("3銘柄分の株価データが必要です。")

    normalized_frames = tuple(
        _normalize_price_frame(prices) for prices in price_frames
    )
    common_dates = normalized_frames[0].index
    for prices in normalized_frames[1:]:
        common_dates = common_dates.intersection(prices.index)
    common_dates = pd.DatetimeIndex(common_dates).sort_values()

    if len(common_dates) < window_size:
        raise ValueError("共通取引日が表示期間に足りません。")

    max_start_index = len(common_dates) - window_size
    random_source = rng if rng is not None else random
    start_index = random_source.randint(0, max_start_index) if max_start_index else 0
    selected_dates = common_dates[start_index : start_index + window_size]

    selected_frames: list[pd.DataFrame] = []
    for prices in normalized_frames:
        selected = prices.loc[selected_dates].copy()
        selected.index = selected_dates.copy()
        selected_frames.append(selected)
    return tuple(selected_frames)


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


def _validated_close(value: object) -> float:
    """終値が数値、有限、正値であることを検証して返す。"""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("終値は数値である必要があります。")
    close = float(value)
    if not math.isfinite(close) or close <= 0:
        raise ValueError("終値は有限かつ0より大きい必要があります。")
    return close


def generate_game_question(
    tickers: tuple[str, str, str],
    price_frames: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    rng: random.Random | None = None,
) -> GameQuestion:
    """3銘柄の共通取引日からゲーム1問分のデータを生成する。

    Args:
        tickers: Chart A、Chart B、Chart Cに対応する証券コード。
        price_frames: 証券コードと同じ順番の3銘柄分のOHLCVデータ。
        rng: 結果を再現するときに使用する乱数生成器。

    Returns:
        表示データ、将来評価結果、正解ラベルを持つゲーム問題。

    Raises:
        ValueError: 入力値、共通取引日、価格が要件を満たさない場合。
    """
    if len(tickers) != 3 or len(price_frames) != 3:
        raise ValueError("3銘柄分の証券コードと株価データが必要です。")
    if any(not isinstance(ticker, str) or not ticker for ticker in tickers):
        raise ValueError("証券コードは空でない文字列である必要があります。")
    if len(set(tickers)) != 3:
        raise ValueError("証券コードに重複があります。")

    for prices in price_frames:
        if prices.empty:
            raise ValueError("空の株価データは使用できません。")
        missing_columns = [
            column for column in _REQUIRED_PRICE_COLUMNS if column not in prices
        ]
        if missing_columns:
            missing = ", ".join(missing_columns)
            raise ValueError(f"株価データに必要な列がありません: {missing}")

    normalized_frames = tuple(
        _normalize_price_frame(prices) for prices in price_frames
    )
    common_dates = normalized_frames[0].index
    for prices in normalized_frames[1:]:
        common_dates = common_dates.intersection(prices.index)
    common_dates = pd.DatetimeIndex(common_dates).sort_values()

    required_days = DISPLAY_TRADING_DAYS + FORECAST_TRADING_DAYS
    if len(common_dates) < required_days:
        raise ValueError("問題生成に必要な共通取引日が足りません。")

    max_start_index = len(common_dates) - required_days
    random_source = rng if rng is not None else random
    start_index = random_source.randint(0, max_start_index) if max_start_index else 0
    display_end_index = start_index + DISPLAY_TRADING_DAYS - 1
    evaluation_index = display_end_index + FORECAST_TRADING_DAYS
    display_dates = common_dates[start_index : display_end_index + 1]
    future_dates = common_dates[display_end_index + 1 : evaluation_index + 1]
    base_date = pd.Timestamp(common_dates[display_end_index])
    evaluation_date = pd.Timestamp(common_dates[evaluation_index])

    charts: list[ChartQuestion] = []
    for label, ticker, prices in zip(
        _CHART_LABELS,
        tickers,
        normalized_frames,
        strict=True,
    ):
        base_close = _validated_close(prices.at[base_date, "Close"])
        future_close = _validated_close(prices.at[evaluation_date, "Close"])
        display_data = prices.loc[display_dates].copy(deep=True)
        display_data.index = display_dates.copy()
        future_data = prices.loc[future_dates].copy(deep=True)
        future_data.index = future_dates.copy()
        charts.append(
            ChartQuestion(
                label=label,
                ticker=ticker,
                display_data=display_data,
                base_date=base_date,
                evaluation_date=evaluation_date,
                base_close=base_close,
                future_close=future_close,
                future_return_percent=calculate_return_percent(
                    base_close,
                    future_close,
                ),
                future_data=future_data,
            )
        )

    chart_tuple = (charts[0], charts[1], charts[2])
    correct_chart = max(chart_tuple, key=lambda chart: chart.future_return_percent)
    return GameQuestion(charts=chart_tuple, correct_label=correct_chart.label)


@dataclass(frozen=True)
class Question:
    """1銘柄分の約6か月のチャートと、その後約1か月の結果を保持する。"""

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

    連続する120営業日をチャート表示用に切り出し、その最終日の終値と、
    さらに20営業日後（約1か月後）の終値から騰落率を計算する。

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
