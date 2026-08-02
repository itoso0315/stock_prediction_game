"""観察期間データからルールベースのテクニカル解説を生成する。"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from game.question_generator import CASH_OPTION_LABEL, GameQuestion


_CHART_LABELS = ("Chart A", "Chart B", "Chart C")
_ALLOWED_LABELS = (*_CHART_LABELS, CASH_OPTION_LABEL)
_REQUIRED_COLUMNS = ("High", "Low", "Close", "Volume")
_MINIMUM_ROWS = 80
_FALLBACK_COMMENT = (
    "今回は移動平均線、直近の高値・安値、出来高の方向がそろわず、"
    "観察時点の指標だけでは優位性を明確に判断できませんでした。"
    "テクニカル指標は将来を保証するものではなく、複数の根拠が同じ方向を示すかを確認することが重要です。"
)
_MAX_COMMENT_LENGTH = 360


def extract_technical_features(prices: pd.DataFrame) -> dict[str, object]:
    """観察期間データから解説用のテクニカル特徴を抽出する。

    Args:
        prices: 昇順かつ一意な日付インデックスを持つ価格・出来高データ。

    Returns:
        移動平均線、価格構造、出来高に関する固定9キーの辞書。

    Raises:
        ValueError: 入力の型、列、件数、日付、数値が仕様を満たさない場合。
    """
    if not isinstance(prices, pd.DataFrame):
        raise ValueError("pricesはpandas.DataFrameである必要があります。")
    if prices.empty:
        raise ValueError("pricesは空にできません。")

    missing_columns = [
        column for column in _REQUIRED_COLUMNS if column not in prices.columns
    ]
    if missing_columns:
        raise ValueError("テクニカル特徴に必要な列がありません。")
    if len(prices) < _MINIMUM_ROWS:
        raise ValueError("テクニカル特徴には80営業日以上必要です。")
    if not isinstance(prices.index, pd.DatetimeIndex):
        raise ValueError("インデックスはDatetimeIndexである必要があります。")
    if prices.index.hasnans:
        raise ValueError("日付インデックスにNaTを使用できません。")
    if not prices.index.is_monotonic_increasing:
        raise ValueError("日付インデックスは昇順である必要があります。")
    if prices.index.has_duplicates:
        raise ValueError("日付インデックスに重複があります。")

    for column in _REQUIRED_COLUMNS:
        if not is_numeric_dtype(prices[column].dtype):
            raise ValueError("価格・出来高列は数値型である必要があります。")

    values = prices.loc[:, _REQUIRED_COLUMNS].to_numpy(dtype=float, copy=True)
    if not np.isfinite(values).all():
        raise ValueError("価格・出来高列には有限値だけを使用できます。")
    if (prices["Volume"].to_numpy(dtype=float, copy=True) < 0).any():
        raise ValueError("Volumeに負の値を使用できません。")

    close = prices["Close"]
    moving_averages = {
        window: close.rolling(window=window, min_periods=window).mean()
        for window in (25, 50, 75)
    }
    current_mas = {
        window: float(moving_average.dropna().iloc[-1])
        for window, moving_average in moving_averages.items()
    }
    slopes = {
        window: _compare_values(
            float(moving_average.dropna().iloc[-1]),
            float(moving_average.dropna().iloc[-6]),
        )
        for window, moving_average in moving_averages.items()
    }

    current_close = float(close.iloc[-1])
    ma25 = current_mas[25]
    ma50 = current_mas[50]
    ma75 = current_mas[75]
    if ma25 > ma50 > ma75:
        alignment = "bullish"
    elif ma25 < ma50 < ma75:
        alignment = "bearish"
    else:
        alignment = "mixed"

    recent = prices.iloc[-20:]
    first_half = recent.iloc[:10]
    second_half = recent.iloc[10:]
    first_high = float(first_half["High"].max())
    second_high = float(second_half["High"].max())
    first_low = float(first_half["Low"].min())
    second_low = float(second_half["Low"].min())
    if second_high > first_high and second_low > first_low:
        price_structure = "higher"
    elif second_high < first_high and second_low < first_low:
        price_structure = "lower"
    else:
        price_structure = "mixed"

    first_volume = float(first_half["Volume"].mean())
    second_volume = float(second_half["Volume"].mean())
    if first_volume == 0:
        volume_trend = "up" if second_volume > 0 else "flat"
    elif second_volume >= first_volume * 1.2:
        volume_trend = "up"
    elif second_volume <= first_volume * 0.8:
        volume_trend = "down"
    else:
        volume_trend = "flat"

    return {
        "close_above_ma25": bool(current_close > ma25),
        "close_above_ma50": bool(current_close > ma50),
        "close_above_ma75": bool(current_close > ma75),
        "ma_alignment": str(alignment),
        "ma25_slope": str(slopes[25]),
        "ma50_slope": str(slopes[50]),
        "ma75_slope": str(slopes[75]),
        "price_structure": str(price_structure),
        "volume_trend": str(volume_trend),
    }


def generate_technical_comment(
    question: GameQuestion,
    selected_label: str,
) -> str:
    """正解と利用者回答から、結果画面用の短い解説を生成する。

    Args:
        question: Chart A/B/Cと正解ラベルを持つゲーム問題。
        selected_label: 利用者が確定した回答ラベル。

    Returns:
        観察期間データだけを根拠にした360文字以内の解説。

    Raises:
        ValueError: 問題構造または回答・正解ラベルが不正な場合。
    """
    _validate_comment_inputs(question, selected_label)

    try:
        features_by_label = {
            chart.label: extract_technical_features(chart.display_data)
            for chart in question.charts
        }
        if question.correct_label == CASH_OPTION_LABEL:
            comment = _cash_comment(features_by_label)
            if selected_label in _CHART_LABELS:
                caution = _caution_comment(
                    selected_label,
                    features_by_label[selected_label],
                )
                if caution is not None:
                    comment = f"{comment}{caution}"
        else:
            correct_features = features_by_label[question.correct_label]
            comment = _strength_comment(question.correct_label, correct_features)
            if (
                selected_label in _CHART_LABELS
                and selected_label != question.correct_label
            ):
                caution = _caution_comment(
                    selected_label,
                    features_by_label[selected_label],
                )
                if caution is not None:
                    comment = f"{comment}{caution}"
            elif selected_label == CASH_OPTION_LABEL:
                comment = (
                    f"{comment}現金を選ぶとこの上昇シグナルを取り逃すため、"
                    "今回は投資する判断が適切でした。"
                )
        if len(comment) > _MAX_COMMENT_LENGTH:
            return _FALLBACK_COMMENT
        return comment
    except Exception:
        return _FALLBACK_COMMENT


def _compare_values(current: float, previous: float) -> str:
    """2つの値を比較してup、down、flatのいずれかを返す。"""
    if current > previous:
        return "up"
    if current < previous:
        return "down"
    return "flat"


def _validate_comment_inputs(
    question: GameQuestion,
    selected_label: str,
) -> None:
    """解説生成に必要な問題構造とラベルを検証する。"""
    if not isinstance(question, GameQuestion):
        raise ValueError("questionはGameQuestionである必要があります。")
    if len(question.charts) != 3:
        raise ValueError("question.chartsは3件である必要があります。")
    labels = tuple(chart.label for chart in question.charts)
    if labels != _CHART_LABELS or len(set(labels)) != 3:
        raise ValueError("Chartラベルの順序または一意性が不正です。")
    if selected_label is None or selected_label not in _ALLOWED_LABELS:
        raise ValueError("selected_labelが許容値ではありません。")
    if question.correct_label not in _ALLOWED_LABELS:
        raise ValueError("correct_labelが許容値ではありません。")


def _strength_comment(label: str, features: dict[str, object]) -> str:
    """正解Chartの複数の強みと、それらが示す意味を返す。"""
    evidence: list[str] = []
    all_slopes_up = all(
        features[key] == "up"
        for key in ("ma25_slope", "ma50_slope", "ma75_slope")
    )
    if features["ma_alignment"] == "bullish" and all_slopes_up:
        evidence.append("MA25＞MA50＞MA75の順行で、3本すべての傾きも上向き")
    elif all_slopes_up:
        evidence.append("MA25・MA50・MA75の傾きがすべて上向き")
    elif features["ma_alignment"] == "bullish":
        evidence.append("MA25＞MA50＞MA75の順行")
    if features["price_structure"] == "higher":
        evidence.append("直近20日における高値・安値の切り上げ")
    if (
        features["close_above_ma75"] is True
        and features["ma75_slope"] == "up"
    ):
        evidence.append("終値が上向きのMA75を上回る中長期の強い位置")
    elif features["close_above_ma25"] is True:
        evidence.append("終値がMA25を上回る短期的に強い位置")
    if features["volume_trend"] == "up":
        evidence.append("直近10日の平均出来高がその前の10日より20%以上増加")

    if not evidence:
        return (
            f"正解の{label}には、観察時点で強い上昇シグナルが十分にはそろっていませんでした。"
            "したがって正解は事前に確実に判別できたものではなく、結果的に3候補で最も高い騰落率となりました。"
        )

    details = "、".join(evidence[:3])
    return (
        f"正解の{label}は、{details}でした。"
        "これらは価格の方向とトレンドの持続性が上向きであることを示し、"
        "観察時点では3候補の中で上昇を期待しやすい形でした。"
    )


def _caution_comment(
    label: str,
    features: dict[str, object],
) -> str | None:
    """不正解Chartの複数の注意点と、それらが示す意味を返す。"""
    evidence: list[str] = []
    if features["ma_alignment"] == "bearish":
        evidence.append("MA25＜MA50＜MA75の逆行で、短期ほど弱い並び")
    if features["ma75_slope"] == "down":
        evidence.append("MA75が下向きで中長期トレンドも弱い状態")
    if features["price_structure"] == "lower":
        evidence.append("直近20日における高値・安値の切り下げ")
    if features["close_above_ma75"] is False:
        evidence.append("終値がMA75を下回る弱い位置")
    if features["volume_trend"] == "down":
        evidence.append("直近10日の平均出来高がその前の10日より20%以上減少")

    if not evidence:
        return (
            f"一方、選択した{label}にも明確な弱気シグナルは少なく、"
            "観察時点の指標だけで不正解を断定できる形ではありませんでした。"
        )

    details = "、".join(evidence[:3])
    return (
        f"一方、選択した{label}は、{details}でした。"
        "これは上昇の継続性に注意が必要なサインであり、投資候補としての優先度を下げる根拠になります。"
    )


def _cash_comment(features_by_label: dict[str, dict[str, object]]) -> str:
    """現金正解時の最優先の見送り理由を固定文で返す。"""
    features = tuple(features_by_label[label] for label in _CHART_LABELS)
    if sum(item["ma_alignment"] == "bearish" for item in features) >= 2:
        return (
            "今回は3つのChartの多くが移動平均線の下降型だったため、"
            "現金で見送る判断が有効でした。"
        )
    if sum(item["ma75_slope"] == "down" for item in features) >= 2:
        return (
            "今回は3つのChartの多くでMA75が下向きだったため、"
            "現金で見送る判断が有効でした。"
        )
    if sum(item["price_structure"] == "lower" for item in features) >= 2:
        return (
            "今回は3つのChartの多くが高値と安値を切り下げていたため、"
            "現金で見送る判断が有効でした。"
        )
    if sum(item["close_above_ma75"] is False for item in features) >= 2:
        return (
            "今回は3つのChartの多くがMA75を上回っておらず、"
            "現金で見送る判断が有効でした。"
        )
    return (
        "今回は3つのChartに明確な上昇優位性が見られず、"
        "現金で見送る判断が最も良い結果でした。"
    )
