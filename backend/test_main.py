import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from backend.main import (
    _active_questions,
    _chart_orders,
    _select_question_set,
    get_questions,
    get_result,
)


QUESTIONS_PATH = Path(__file__).with_name("sample_questions.json")


@pytest.fixture(autouse=True)
def reset_active_game():
    _active_questions.clear()
    _chart_orders.clear()
    yield
    _active_questions.clear()
    _chart_orders.clear()


def test_question_pool_supports_zero_to_thirty_percent_cash_questions():
    payload = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    questions = payload["questions"]

    assert [question["problemType"] for question in questions].count("normal") >= 10
    assert [question["problemType"] for question in questions].count("cash") >= 3
    signatures = set()
    for question in questions:
        stocks = [choice for choice in question["choices"] if choice["type"] == "stock"]
        tickers = [choice["ticker"] for choice in stocks]
        assert len(tickers) == len(set(tickers)) == 3
        signature = (question["baseDate"], frozenset(tickers))
        assert signature not in signatures
        signatures.add(signature)

    for cash_count in range(4):
        selected = _select_question_set(questions, cash_count=cash_count)
        assert len(selected) == 10
        assert [question["problemType"] for question in selected].count("cash") == cash_count
        assert [question["currentNumber"] for question in selected] == list(range(1, 11))


def test_questions_populates_all_stock_charts():
    candles = [
        {
            "date": "2024-05-01",
            "open": 1.0,
            "high": 2.0,
            "low": 0.5,
            "close": 1.5,
            "volume": 1234567,
        }
    ]

    chart_data = {
        "candles": candles,
        "ma20": [{"date": "2024-05-01", "value": 1.1}],
        "ma40": [{"date": "2024-05-01", "value": 1.2}],
        "ma70": [{"date": "2024-05-01", "value": 1.3}],
    }

    with patch.dict(_chart_orders, {}, clear=True), patch(
        "backend.main.fetch_chart_data", return_value=chart_data
    ) as fetch:
        payload = get_questions()

    expected_requests = {
        (choice["ticker"], question["baseDate"])
        for question in _active_questions.values()
        for choice in question["choices"]
        if choice["type"] == "stock"
    }
    actual_requests = {
        (call.kwargs["ticker"], call.kwargs["base_date"])
        for call in fetch.call_args_list
    }
    assert actual_requests == expected_requests
    for question in payload["questions"]:
        assert question["correctChoiceLabel"] == ""
        assert "problemType" not in question
        assert "explanation" not in question
        chart_a, chart_b, chart_c, cash = question["choices"]
        for chart in (chart_a, chart_b, chart_c):
            assert "ticker" not in chart
            assert "companyName" not in chart
            assert "returnRate" not in chart
            assert chart["candles"] == candles
            assert chart["ma20"] == chart_data["ma20"]
            assert chart["ma40"] == chart_data["ma40"]
            assert chart["ma70"] == chart_data["ma70"]
        assert cash["candles"] == []


def test_result_uses_future_data_and_selects_best_choice():
    past = {
        "candles": [
            {"date": "2024-05-01", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 10}
        ],
        "ma20": [],
        "ma40": [],
        "ma70": [],
    }
    future_closes = iter((110.0, 90.0, 95.0))

    def future(*_args):
        close = next(future_closes)
        return [
            {"date": "2024-06-03", "open": close, "high": close, "low": close, "close": close, "volume": 20}
        ]

    with patch.dict(_chart_orders, {1: (0, 1, 2)}, clear=True), patch(
        "backend.main.fetch_chart_data", return_value=past
    ), patch("backend.main.fetch_future_candles", side_effect=future):
        result = get_result(1, selected_choice_label="Chart B")

    stocks = [choice for choice in result["choices"] if choice["type"] == "stock"]
    assert all(len(choice["resultCandles"]) == 2 for choice in stocks)
    assert [choice["returnRate"] for choice in stocks] == [10.0, -10.0, -5.0]
    assert result["evaluationDate"] == "2024-06-03"
    assert result["correctChoiceLabel"] == "Chart A"
    assert result["choices"][-1]["returnRate"] == 0.0
    assert stocks[0]["yahooFinanceUrl"].endswith("/3099.T/chart")
    assert "problemType" not in result
    assert result["explanation"]


def test_cash_question_selects_cash_when_all_stocks_decline():
    past = {
        "candles": [
            {"date": "2023-12-01", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 10}
        ],
        "ma20": [],
        "ma40": [],
        "ma70": [],
    }
    future_closes = iter((99.0, 90.0, 95.0))

    def future(*_args):
        close = next(future_closes)
        return [
            {"date": "2023-12-29", "open": close, "high": close, "low": close, "close": close, "volume": 20}
        ]

    with patch.dict(_chart_orders, {3: (0, 1, 2)}, clear=True), patch(
        "backend.main.fetch_chart_data", return_value=past
    ), patch("backend.main.fetch_future_candles", side_effect=future):
        result = get_result(3)

    assert result["correctChoiceLabel"] == "現金保有"
    assert [choice["returnRate"] for choice in result["choices"]] == [
        -1.0,
        -10.0,
        -5.0,
        0.0,
    ]


def test_result_rejects_question_that_no_longer_matches_its_pattern():
    past = {
        "candles": [
            {"date": "2023-12-01", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 10}
        ],
        "ma20": [],
        "ma40": [],
        "ma70": [],
    }
    future = [
        {"date": "2023-12-29", "open": 110.0, "high": 110.0, "low": 110.0, "close": 110.0, "volume": 20}
    ]

    with patch.dict(_chart_orders, {3: (0, 1, 2)}, clear=True), patch(
        "backend.main.fetch_chart_data", return_value=past
    ), patch("backend.main.fetch_future_candles", return_value=future):
        with pytest.raises(HTTPException) as error:
            get_result(3)

    assert error.value.status_code == 502
    assert "現金問題の騰落率条件" in error.value.detail


def test_chart_order_is_shared_between_question_and_result_responses():
    chart_data = {"candles": [], "ma20": [], "ma40": [], "ma70": []}
    with patch.dict(_chart_orders, {1: (2, 0, 1)}, clear=True), patch(
        "backend.main.fetch_chart_data", return_value=chart_data
    ):
        payload = get_questions()

    question = payload["questions"][0]
    assert [choice["label"] for choice in question["choices"]] == [
        "Chart A",
        "Chart B",
        "Chart C",
        "現金保有",
    ]
