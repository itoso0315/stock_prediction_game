from backend.explanation import generate_technical_comment


def _stock_choice(label: str, *, rising: bool) -> dict:
    candles = []
    for index in range(20):
        close = 100 + index if rising else 140 - index
        candles.append(
            {
                "date": f"2024-01-{index + 1:02d}",
                "open": close - 1,
                "high": close + 2,
                "low": close - 2,
                "close": close,
                "volume": 200 if rising and index >= 10 else 100,
            }
        )
    if rising:
        ma20 = [100 + index for index in range(6)]
        ma40 = [90 + index for index in range(6)]
        ma70 = [80 + index for index in range(6)]
    else:
        ma20 = [100 - index for index in range(6)]
        ma40 = [110 - index for index in range(6)]
        ma70 = [120 - index for index in range(6)]
    return {
        "label": label,
        "type": "stock",
        "candles": candles,
        "ma20": _points(ma20),
        "ma40": _points(ma40),
        "ma70": _points(ma70),
    }


def _points(values: list[int]) -> list[dict]:
    return [
        {"date": f"2024-01-{index + 1:02d}", "value": value}
        for index, value in enumerate(values)
    ]


def test_comment_compares_correct_and_selected_charts_in_about_100_characters():
    choices = [
        _stock_choice("Chart A", rising=True),
        _stock_choice("Chart B", rising=False),
        _stock_choice("Chart C", rising=False),
        {"label": "現金保有", "type": "cash"},
    ]

    comment = generate_technical_comment(choices, "Chart A", "Chart B")

    assert "Chart A" in comment
    assert "Chart B" in comment
    assert "MA20・40・70" in comment
    assert 60 <= len(comment) <= 150


def test_comment_explains_why_cash_is_correct():
    choices = [
        _stock_choice("Chart A", rising=False),
        _stock_choice("Chart B", rising=False),
        _stock_choice("Chart C", rising=False),
        {"label": "現金保有", "type": "cash"},
    ]

    comment = generate_technical_comment(choices, "現金保有", "Chart A")

    assert "現金で見送る判断" in comment
    assert "Chart A" in comment
