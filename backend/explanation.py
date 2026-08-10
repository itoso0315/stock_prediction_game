"""観察期間のチャートから短いテクニカル解説を生成する。"""

from __future__ import annotations


_CHART_LABELS = ("Chart A", "Chart B", "Chart C")
_CASH_LABEL = "現金保有"
_FALLBACK_COMMENT = (
    "移動平均線、高値・安値、出来高の方向がそろわず、"
    "観察時点では優位性を明確に判断しにくい形でした。"
)


def generate_technical_comment(
    choices: list[dict],
    correct_label: str,
    selected_label: str | None,
) -> str:
    """正解と利用者回答を、観察期間だけを根拠に約100文字で説明する。"""
    try:
        stocks = {
            choice["label"]: choice
            for choice in choices
            if choice.get("type") == "stock"
        }
        if set(stocks) != set(_CHART_LABELS):
            return _FALLBACK_COMMENT
        features = {
            label: _extract_features(choice) for label, choice in stocks.items()
        }
        selected = selected_label if selected_label in (*_CHART_LABELS, _CASH_LABEL) else correct_label

        if correct_label == _CASH_LABEL:
            return _cash_comment(features, selected)

        correct_reason = _best_reason(features[correct_label], positive=True)
        if selected == correct_label:
            return (
                f"{correct_label}は{correct_reason}ため、上昇の根拠が最もそろっていました。"
                "移動平均線・値動き・出来高を合わせて見るのがポイントです。"
            )
        if selected == _CASH_LABEL:
            return (
                f"{correct_label}は{correct_reason}ため、現金で見送るより上昇を期待できる形でした。"
                "複数の根拠が同じ方向を示す場面です。"
            )

        selected_reason = _best_reason(features[selected], positive=False)
        return (
            f"{correct_label}は{correct_reason}一方、{selected}は{selected_reason}ため、"
            f"{correct_label}の優位性が高いと判断できます。"
        )
    except (KeyError, TypeError, ValueError, IndexError):
        return _FALLBACK_COMMENT


def _extract_features(choice: dict) -> dict[str, str | bool]:
    candles = choice["candles"]
    if len(candles) < 20:
        raise ValueError("ローソク足が不足しています。")

    moving_averages = {
        window: choice[f"ma{window}"] for window in (20, 40, 70)
    }
    if any(len(points) < 6 for points in moving_averages.values()):
        raise ValueError("移動平均線が不足しています。")

    current_mas = {
        window: float(points[-1]["value"])
        for window, points in moving_averages.items()
    }
    slopes = {
        window: _compare(float(points[-1]["value"]), float(points[-6]["value"]))
        for window, points in moving_averages.items()
    }
    if current_mas[20] > current_mas[40] > current_mas[70]:
        alignment = "bullish"
    elif current_mas[20] < current_mas[40] < current_mas[70]:
        alignment = "bearish"
    else:
        alignment = "mixed"

    recent = candles[-20:]
    first_half = recent[:10]
    second_half = recent[10:]
    first_high = max(float(item["high"]) for item in first_half)
    second_high = max(float(item["high"]) for item in second_half)
    first_low = min(float(item["low"]) for item in first_half)
    second_low = min(float(item["low"]) for item in second_half)
    if second_high > first_high and second_low > first_low:
        price_structure = "higher"
    elif second_high < first_high and second_low < first_low:
        price_structure = "lower"
    else:
        price_structure = "mixed"

    first_volume = sum(float(item["volume"]) for item in first_half) / 10
    second_volume = sum(float(item["volume"]) for item in second_half) / 10
    if second_volume >= first_volume * 1.2:
        volume_trend = "up"
    elif first_volume > 0 and second_volume <= first_volume * 0.8:
        volume_trend = "down"
    else:
        volume_trend = "flat"

    return {
        "close_above_ma20": float(candles[-1]["close"]) > current_mas[20],
        "alignment": alignment,
        "ma20_slope": slopes[20],
        "ma40_slope": slopes[40],
        "ma70_slope": slopes[70],
        "price_structure": price_structure,
        "volume_trend": volume_trend,
    }


def _best_reason(features: dict[str, str | bool], *, positive: bool) -> str:
    if positive:
        if features["alignment"] == "bullish" and all(
            features[f"ma{window}_slope"] == "up" for window in (20, 40, 70)
        ):
            return "MA20・40・70が順行し、3本とも上向いている"
        if features["price_structure"] == "higher":
            return "直近で高値・安値を切り上げている"
        if features["volume_trend"] == "up":
            return "直近の出来高が増え、買いの勢いが確認できる"
        if features["close_above_ma20"] is True and features["ma20_slope"] == "up":
            return "終値が上向きのMA20を上回っている"
        return "他候補より下落を示す材料が少ない"

    if features["alignment"] == "bearish":
        return "MA20・40・70が下降型に並んでいる"
    if features["price_structure"] == "lower":
        return "直近で高値・安値を切り下げている"
    if features["volume_trend"] == "down":
        return "直近の出来高が減少している"
    if features["ma70_slope"] == "down":
        return "MA70が下向きで中期の勢いが弱い"
    return "上昇を裏付ける材料が相対的に少ない"


def _cash_comment(
    features: dict[str, dict[str, str | bool]],
    selected_label: str,
) -> str:
    bearish_count = sum(
        item["alignment"] == "bearish" or item["price_structure"] == "lower"
        for item in features.values()
    )
    base = (
        "3つのChartの多くで下降型の移動平均線や高値・安値の切り下げが見られ、"
        "現金で見送る判断が有効でした。"
        if bearish_count >= 2
        else "3つのChartに明確な上昇根拠がそろわず、現金で見送る判断が有効でした。"
    )
    if selected_label in _CHART_LABELS:
        return f"{base}{selected_label}は{_best_reason(features[selected_label], positive=False)}状態です。"
    return base


def _compare(current: float, previous: float) -> str:
    if current > previous:
        return "up"
    if current < previous:
        return "down"
    return "flat"
