"""過去の株価データから出題用データを生成する。"""

from dataclasses import dataclass
import math
from numbers import Real
import random
import re

import pandas as pd


DISPLAY_TRADING_DAYS = 200
FORECAST_TRADING_DAYS = 20
CASH_OPTION_LABEL = "どれにも投資しない（現金で保有）"
_CHART_LABELS = ("Chart A", "Chart B", "Chart C")
_REQUIRED_PRICE_COLUMNS = ("Open", "High", "Low", "Close", "Volume")
_SECURITY_CODE_PATTERN = re.compile(r"(?:[0-9]{4}|[0-9]{3}[A-Z])\Z", re.ASCII)

# 日経平均プロフィル「構成銘柄一覧」（更新日付: 2026-07-31）の社名。
# 証券コードと企業名を同じマッピングで管理し、対応のずれを防ぐ。
_COMPANY_NAMES_BY_SECURITY_CODE: dict[str, str] = {
    "4151": "協和キリン（株）", "4502": "武田薬品工業（株）", "4503": "アステラス製薬（株）",
    "4506": "住友ファーマ（株）", "4507": "塩野義製薬（株）", "4519": "中外製薬（株）",
    "4523": "エーザイ（株）", "4568": "第一三共（株）", "4578": "大塚ホールディングス（株）",
    "285A": "キオクシアホールディングス（株）", "4062": "イビデン（株）", "6479": "ミネベアミツミ（株）",
    "6501": "（株）日立製作所", "6503": "三菱電機（株）", "6504": "富士電機（株）",
    "6506": "（株）安川電機", "6526": "（株）ソシオネクスト", "6645": "オムロン（株）",
    "6701": "日本電気（株）", "6702": "富士通（株）", "6723": "ルネサスエレクトロニクス（株）",
    "6724": "セイコーエプソン（株）", "6752": "パナソニック ホールディングス（株）", "6753": "シャープ（株）",
    "6758": "ソニーグループ（株）", "6762": "ＴＤＫ（株）", "6770": "アルプスアルパイン（株）",
    "6841": "横河電機（株）", "6857": "（株）アドバンテスト", "6861": "（株）キーエンス",
    "6902": "（株）デンソー", "6920": "レーザーテック（株）", "6954": "ファナック（株）",
    "6963": "ローム（株）", "6971": "京セラ（株）", "6976": "太陽誘電（株）",
    "6981": "（株）村田製作所", "7735": "（株）ＳＣＲＥＥＮホールディングス", "7751": "キヤノン（株）",
    "7752": "（株）リコー", "8035": "東京エレクトロン（株）", "543A": "ＡＲＣＨＩＯＮ（株）",
    "7201": "日産自動車（株）", "7202": "いすゞ自動車（株）", "7203": "トヨタ自動車（株）",
    "7211": "三菱自動車工業（株）", "7261": "マツダ（株）", "7267": "本田技研工業（株）",
    "7269": "スズキ（株）", "7270": "（株）ＳＵＢＡＲＵ", "7272": "ヤマハ発動機（株）",
    "4543": "テルモ（株）", "4902": "コニカミノルタ（株）", "6146": "（株）ディスコ",
    "7731": "（株）ニコン", "7733": "オリンパス（株）", "7741": "ＨＯＹＡ（株）",
    "9432": "ＮＴＴ（株）", "9433": "ＫＤＤＩ（株）", "9434": "ソフトバンク（株）",
    "9984": "ソフトバンクグループ（株）", "5831": "（株）しずおかフィナンシャルグループ", "7186": "（株）横浜フィナンシャルグループ",
    "8304": "（株）あおぞら銀行", "8306": "（株）三菱ＵＦＪフィナンシャル・グループ", "8308": "（株）りそなホールディングス",
    "8309": "三井住友トラストグループ（株）", "8316": "（株）三井住友フィナンシャルグループ", "8331": "（株）千葉銀行",
    "8354": "（株）ふくおかフィナンシャルグループ", "8411": "（株）みずほフィナンシャルグループ", "8253": "（株）クレディセゾン",
    "8591": "オリックス（株）", "8697": "（株）日本取引所グループ", "8601": "（株）大和証券グループ本社",
    "8604": "野村ホールディングス（株）", "8630": "ＳＯＭＰＯホールディングス（株）", "8725": "ＭＳ＆ＡＤインシュアランスグループホールディングス（株）",
    "8750": "（株）第一ライフグループ", "8766": "東京海上ホールディングス（株）", "8795": "（株）Ｔ＆Ｄホールディングス",
    "1332": "（株）ニッスイ", "2002": "（株）日清製粉グループ本社", "2269": "明治ホールディングス（株）",
    "2282": "日本ハム（株）", "2501": "サッポロビール（株）", "2502": "アサヒグループホールディングス（株）",
    "2503": "キリンホールディングス（株）", "2801": "キッコーマン（株）", "2802": "味の素（株）",
    "2871": "（株）ニチレイ", "2914": "日本たばこ産業（株）", "3086": "Ｊ．フロント リテイリング（株）",
    "3092": "（株）ＺＯＺＯ", "3099": "（株）三越伊勢丹ホールディングス", "3382": "（株）セブン＆アイ・ホールディングス",
    "7453": "（株）良品計画", "7532": "（株）パン・パシフィック・インターナショナルホールディングス", "8233": "（株）高島屋",
    "8252": "（株）丸井グループ", "8267": "イオン（株）", "9843": "（株）ニトリホールディングス",
    "9983": "（株）ファーストリテイリング", "2413": "エムスリー（株）", "2432": "（株）ディー・エヌ・エー",
    "3659": "（株）ネクソン", "3697": "（株）ＳＨＩＦＴ", "4307": "（株）野村総合研究所",
    "4324": "（株）電通グループ", "4385": "（株）メルカリ", "4661": "（株）オリエンタルランド",
    "4689": "ＬＩＮＥヤフー（株）", "4704": "トレンドマイクロ（株）", "4751": "（株）サイバーエージェント",
    "4755": "楽天グループ（株）", "6098": "（株）リクルートホールディングス", "6178": "日本郵政（株）",
    "6532": "（株）ベイカレント", "7974": "任天堂（株）", "9602": "東宝（株）",
    "9735": "セコム（株）", "9766": "コナミグループ（株）", "1605": "（株）ＩＮＰＥＸ",
    "3401": "帝人（株）", "3402": "東レ（株）", "3861": "王子ホールディングス（株）",
    "3405": "（株）クラレ", "3407": "旭化成（株）", "4004": "（株）レゾナック・ホールディングス",
    "4005": "住友化学（株）", "4021": "日産化学（株）", "4042": "東ソー（株）",
    "4043": "（株）トクヤマ", "4061": "デンカ（株）", "4063": "信越化学工業（株）",
    "4183": "三井化学（株）", "4188": "三菱ケミカルグループ（株）", "4208": "ＵＢＥ（株）",
    "4452": "花王（株）", "4901": "富士フイルムホールディングス（株）", "4911": "（株）資生堂",
    "6988": "日東電工（株）", "5019": "出光興産（株）", "5020": "ＥＮＥＯＳホールディングス（株）",
    "5101": "横浜ゴム（株）", "5108": "（株）ブリヂストン", "5201": "ＡＧＣ（株）",
    "5214": "日本電気硝子（株）", "5233": "太平洋セメント（株）", "5301": "東海カーボン（株）",
    "5332": "ＴＯＴＯ（株）", "5333": "ＮＧＫ（株）", "5401": "日本製鉄（株）",
    "5406": "（株）神戸製鋼所", "5411": "ＪＦＥホールディングス（株）", "3436": "（株）ＳＵＭＣＯ",
    "5706": "三井金属（株）", "5711": "三菱マテリアル（株）", "5713": "住友金属鉱山（株）",
    "5714": "ＤＯＷＡホールディングス（株）", "5801": "古河電気工業（株）", "5802": "住友電気工業（株）",
    "5803": "（株）フジクラ", "2768": "双日（株）", "8001": "伊藤忠商事（株）",
    "8002": "丸紅（株）", "8015": "豊田通商（株）", "8031": "三井物産（株）",
    "8053": "住友商事（株）", "8058": "三菱商事（株）", "1721": "コムシスホールディングス（株）",
    "1801": "大成建設（株）", "1802": "（株）大林組", "1803": "清水建設（株）",
    "1808": "（株）長谷工コーポレーション", "1812": "鹿島建設（株）", "1925": "大和ハウス工業（株）",
    "1928": "積水ハウス（株）", "1963": "日揮ホールディングス（株）", "5631": "（株）日本製鋼所",
    "6103": "オークマ（株）", "6113": "（株）アマダ", "6273": "ＳＭＣ（株）",
    "6301": "（株）小松製作所", "6302": "住友重機械工業（株）", "6305": "日立建機（株）",
    "6326": "（株）クボタ", "6361": "（株）荏原製作所", "6367": "ダイキン工業（株）",
    "6471": "日本精工（株）", "6472": "ＮＴＮ（株）", "6473": "（株）ジェイテクト",
    "7004": "カナデビア（株）", "7011": "三菱重工業（株）", "7013": "（株）ＩＨＩ",
    "7012": "川崎重工業（株）", "7832": "（株）バンダイナムコホールディングス", "7911": "ＴＯＰＰＡＮホールディングス（株）",
    "7912": "大日本印刷（株）", "7951": "ヤマハ（株）", "3289": "東急不動産ホールディングス（株）",
    "8801": "三井不動産（株）", "8802": "三菱地所（株）", "8804": "東京建物（株）",
    "8830": "住友不動産（株）", "9001": "東武鉄道（株）", "9005": "東急（株）",
    "9007": "小田急電鉄（株）", "9008": "京王電鉄（株）", "9009": "京成電鉄（株）",
    "9020": "東日本旅客鉄道（株）", "9021": "西日本旅客鉄道（株）", "9022": "東海旅客鉄道（株）",
    "9064": "ヤマトホールディングス（株）", "9147": "ＮＩＰＰＯＮ ＥＸＰＲＥＳＳホールディングス（株）", "9101": "日本郵船（株）",
    "9104": "（株）商船三井", "9107": "川崎汽船（株）", "9201": "日本航空（株）",
    "9202": "ＡＮＡホールディングス（株）", "9501": "東京電力ホールディングス（株）", "9502": "中部電力（株）",
    "9503": "関西電力（株）", "9531": "東京瓦斯（株）", "9532": "大阪瓦斯（株）",
}


@dataclass(frozen=True)
class ChartQuestion:
    """1銘柄分の表示データと将来評価結果を保持する。"""

    label: str
    ticker: str
    company_name: str
    security_code: str
    display_data: pd.DataFrame
    base_date: pd.Timestamp
    evaluation_date: pd.Timestamp
    base_close: float
    future_close: float
    future_return_percent: float
    future_data: pd.DataFrame


def _resolve_security(
    ticker: str,
) -> tuple[str, str, str]:
    """tickerを検証し、証券コード・企業名・Yahoo用tickerを返す。"""
    if not isinstance(ticker, str) or not ticker or ticker != ticker.strip():
        raise ValueError("tickerは空白を含まない文字列である必要があります。")
    security_code = ticker[:-2] if ticker.endswith(".T") else ticker
    if not _SECURITY_CODE_PATTERN.fullmatch(security_code):
        raise ValueError("証券コードの形式が正しくありません。")
    official_company_name = _COMPANY_NAMES_BY_SECURITY_CODE.get(security_code)
    if (
        not isinstance(official_company_name, str)
        or not official_company_name.strip()
    ):
        raise ValueError("証券コードに対応する企業名がありません。")
    company_name = official_company_name.strip()
    if company_name.startswith("（株）"):
        company_name = company_name.removeprefix("（株）").strip()
    if company_name.endswith("（株）"):
        company_name = company_name.removesuffix("（株）").strip()
    if not company_name:
        raise ValueError("企業名が空です。")
    yahoo_ticker = f"{security_code}.T"
    return security_code, company_name, yahoo_ticker


def create_yahoo_chart_url(ticker: str) -> str:
    """検証済みtickerからYahoo!ファイナンスのチャートURLを返す。"""
    _, _, yahoo_ticker = _resolve_security(ticker)
    return f"https://finance.yahoo.co.jp/quote/{yahoo_ticker}/chart"


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

    securities = tuple(_resolve_security(ticker) for ticker in tickers)

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
    for label, ticker, prices, security in zip(
        _CHART_LABELS,
        tickers,
        normalized_frames,
        securities,
        strict=True,
    ):
        security_code, company_name, _ = security
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
                company_name=company_name,
                security_code=security_code,
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
    best_chart = max(chart_tuple, key=lambda chart: chart.future_return_percent)
    correct_label = (
        CASH_OPTION_LABEL
        if best_chart.future_return_percent <= 0
        else best_chart.label
    )
    return GameQuestion(charts=chart_tuple, correct_label=correct_label)


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

    連続する200営業日をチャート表示用に切り出し、その最終日の終値と、
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
