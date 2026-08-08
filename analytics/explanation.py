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
_MAX_COMMENT_LENGTH = 520


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
            if (
                selected_label in _CHART_LABELS
                and selected_label != question.correct_label
            ):
                comment = _comparison_comment(
                    question.correct_label,
                    correct_features,
                    selected_label,
                    features_by_label[selected_label],
                )
            else:
                comment = _strength_comment(
                    question.correct_label,
                    correct_features,
                )
                if selected_label == CASH_OPTION_LABEL:
                    comment = (
                        f"{comment}今回は現金で見送るより、"
                        f"{question.correct_label}に見られた上昇根拠を優先する場面でした。"
                    )
        if "今回のポイントは、" not in comment:
            if question.correct_label == CASH_OPTION_LABEL:
                comment = (
                    f"{comment}今回のポイントは、明確な上昇根拠が乏しいときは無理に投資せず、"
                    "移動平均線の方向、高値・安値の推移、出来高を候補同士で比較して見送る判断も持つことです。"
                )
            else:
                comment = (
                    f"{comment}今回のポイントは、1つの指標だけで決めず、"
                    "移動平均線の並びと傾き、高値・安値の方向、出来高の変化を組み合わせて判断することです。"
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


def _collect_strengths(features: dict[str, object]) -> list[str]:
    """上昇を支持する特徴を、説明用の日本語で返す。"""
    evidence: list[str] = []
    all_slopes_up = all(
        features[key] == "up"
        for key in ("ma25_slope", "ma50_slope", "ma75_slope")
    )
    if features["ma_alignment"] == "bullish" and all_slopes_up:
        evidence.append("MA25＞MA50＞MA75の順行で3本とも上向き")
    elif all_slopes_up:
        evidence.append("MA25・MA50・MA75がそろって上向き")
    elif features["ma_alignment"] == "bullish":
        evidence.append("MA25＞MA50＞MA75の順行")
    if features["price_structure"] == "higher":
        evidence.append("直近20日で高値・安値を切り上げている")
    if features["close_above_ma75"] is True and features["ma75_slope"] == "up":
        evidence.append("終値が上向きのMA75を上回っている")
    elif features["close_above_ma25"] is True and features["ma25_slope"] == "up":
        evidence.append("終値が上向きのMA25を上回っている")
    if features["volume_trend"] == "up":
        evidence.append("直近10日の平均出来高が前の10日より20%以上増えている")
    return evidence


def _collect_weaknesses(features: dict[str, object]) -> list[str]:
    """上昇を妨げる特徴を、説明用の日本語で返す。"""
    evidence: list[str] = []
    if features["ma_alignment"] == "bearish":
        evidence.append("MA25＜MA50＜MA75の逆行になっている")
    if features["ma75_slope"] == "down":
        evidence.append("MA75が下向きで中長期トレンドが弱い")
    if features["price_structure"] == "lower":
        evidence.append("直近20日で高値・安値を切り下げている")
    if features["close_above_ma75"] is False:
        evidence.append("終値がMA75を下回っている")
    if features["volume_trend"] == "down":
        evidence.append("直近10日の平均出来高が前の10日より20%以上減っている")
    return evidence


def _comparison_comment(
    correct_label: str,
    correct_features: dict[str, object],
    selected_label: str,
    selected_features: dict[str, object],
) -> str:
    """正解Chartと選択Chartを比較し、正解・不正解の根拠を説明する。"""
    correct_strengths = _collect_strengths(correct_features)
    correct_weaknesses = _collect_weaknesses(correct_features)
    selected_strengths = _collect_strengths(selected_features)
    selected_weaknesses = _collect_weaknesses(selected_features)

    if correct_strengths:
        correct_reason = "、".join(correct_strengths[:3])
        first = (
            f"正解の{correct_label}は、{correct_reason}ため、"
            "3候補の中では上昇を期待する根拠が比較的そろっていました。"
        )
    else:
        relative_advantages: list[str] = []
        if correct_features["price_structure"] != "lower":
            relative_advantages.append("高値・安値が明確な切り下げではない")
        if correct_features["ma75_slope"] != "down":
            relative_advantages.append("MA75が下向きではない")
        if correct_features["volume_trend"] != "down":
            relative_advantages.append("出来高が明確な減少ではない")
        if correct_features["close_above_ma25"] is True:
            relative_advantages.append("終値がMA25を上回っている")

        if relative_advantages:
            correct_reason = "、".join(relative_advantages[:3])
            first = (
                f"正解の{correct_label}に強烈な買いシグナルはありませんでしたが、"
                f"{correct_reason}ため、弱気材料が相対的に少ない候補でした。"
            )
        else:
            first = (
                f"正解の{correct_label}も明確な上昇形ではなく、"
                "観察時点だけで高い確信を持てる問題ではありませんでした。"
            )

    if selected_weaknesses:
        selected_reason = "、".join(selected_weaknesses[:3])
        second = (
            f"一方、選択した{selected_label}は、{selected_reason}ため、"
            f"{correct_label}より上昇継続への不安材料が多い状態でした。"
        )
    elif selected_strengths:
        selected_reason = "、".join(selected_strengths[:2])
        second = (
            f"選択した{selected_label}にも{selected_reason}という良い材料はありました。"
            f"ただし、{correct_label}と比べるとトレンド・価格構造・出来高の裏付けが弱く、"
            "買い候補としての優先度で一歩劣りました。"
        )
    else:
        second = (
            f"選択した{selected_label}には大きな弱気サインこそありませんでしたが、"
            "上昇を積極的に支持する材料も少なく、他候補より優先する根拠が不足していました。"
        )

    lesson = (
        "今回のポイントは、1つの指標だけで決めず、"
        "移動平均線の並びと傾き、高値・安値の方向、出来高の変化を候補同士で比較することです。"
    )
    comment = f"{first}{second}{lesson}"

    if correct_weaknesses and not correct_strengths:
        comment = (
            f"{comment}なお、正解Chartにも弱気材料は残っており、"
            "『絶対に上がる形』ではなく、あくまで3候補の比較で判断する問題でした。"
        )
    return comment


def _strength_comment(label: str, features: dict[str, object]) -> str:
    """正解Chartを選ぶ根拠を、観察時点の特徴から具体的に説明する。"""
    strengths = _collect_strengths(features)
    weaknesses = _collect_weaknesses(features)

    if strengths:
        details = "、".join(strengths[:3])
        comment = (
            f"正解の{label}を選ぶ根拠は、{details}が確認できたことです。"
            "これらは短期の勢いだけでなく、トレンドの方向や継続性を裏付ける材料になります。"
        )
    else:
        neutral_points: list[str] = []
        if features["close_above_ma25"] is True:
            neutral_points.append("終値がMA25を上回っていた")
        if features["ma25_slope"] == "up":
            neutral_points.append("MA25が上向いていた")
        if features["price_structure"] != "lower":
            neutral_points.append("高値・安値が明確な切り下げではなかった")
        if features["volume_trend"] != "down":
            neutral_points.append("出来高が明確に減少していなかった")

        if neutral_points:
            details = "、".join(neutral_points[:3])
            comment = (
                f"正解の{label}には強烈な上昇シグナルこそありませんでしたが、"
                f"{details}ため、少なくとも下落継続を強く示す形ではありませんでした。"
                "候補を比較するときは、強い買いシグナルだけでなく、弱気材料の少なさも判断材料になります。"
            )
        else:
            comment = (
                f"正解の{label}にも観察時点で明確な上昇優位性は乏しく、"
                "テクニカルだけで高い確信を持てる問題ではありませんでした。"
                "この場合は無理に単一指標で決めず、複数Chartの弱気材料の数と強さを比較することが重要です。"
            )

    if weaknesses:
        comment = (
            f"{comment}ただし、{label}にも{weaknesses[0]}という注意点はあり、"
            "完全な上昇形ではなかった点には注意が必要です。"
        )
    return comment


def _caution_comment(
    label: str,
    features: dict[str, object],
) -> str | None:
    """不正解Chartの優先度を下げる根拠を具体的に説明する。"""
    weaknesses = _collect_weaknesses(features)
    strengths = _collect_strengths(features)

    if weaknesses:
        details = "、".join(weaknesses[:3])
        return (
            f"一方、選択した{label}は、{details}ため、"
            "上昇継続への確信を持ちにくい形でした。"
            "こうした弱気材料が複数重なるChartは、他候補より優先度を下げる判断ができます。"
        )

    if strengths:
        details = "、".join(strengths[:2])
        return (
            f"一方、選択した{label}にも{details}という良い材料はありました。"
            "ただし、その材料だけでは他候補より強いとは言い切れず、"
            "移動平均線・価格構造・出来高まで含めて比較する必要がありました。"
        )

    return (
        f"一方、選択した{label}は強い弱気形ではありませんでしたが、"
        "上昇を積極的に裏付ける材料も乏しい状態でした。"
        "『悪くない』だけでは買いの根拠として弱く、他候補により明確な上昇材料があればそちらを優先します。"
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
