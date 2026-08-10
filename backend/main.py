

import json
import random
from copy import deepcopy
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

try:
    from .market_data import fetch_chart_data, fetch_future_candles
except ImportError:  # ``cd backend && uvicorn main:app`` での起動に対応する。
    from market_data import fetch_chart_data, fetch_future_candles

app = FastAPI(title="Stock Trainer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_QUESTIONS_PATH = BASE_DIR / "sample_questions.json"
_CHART_LABELS = ("Chart A", "Chart B", "Chart C")
_random = random.SystemRandom()
_chart_orders: dict[int, tuple[int, int, int]] = {}
_active_questions: dict[int, dict] = {}


def _select_question_set(
    question_pool: list[dict], cash_count: int | None = None
) -> list[dict]:
    """現金問題を0〜3問から選び、10問のゲームセットを作る。"""
    normal_questions = [
        question for question in question_pool if question["problemType"] == "normal"
    ]
    cash_questions = [
        question for question in question_pool if question["problemType"] == "cash"
    ]
    if cash_count is None:
        cash_count = _random.randint(0, 3)
    if cash_count not in range(4):
        raise ValueError("現金問題数は0〜3問で指定してください。")
    normal_count = 10 - cash_count
    if len(normal_questions) < normal_count or len(cash_questions) < cash_count:
        raise ValueError("出題比率を満たす問題候補が不足しています。")

    selected = [
        *_random.sample(normal_questions, k=normal_count),
        *_random.sample(cash_questions, k=cash_count),
    ]
    _random.shuffle(selected)
    result = deepcopy(selected)
    for number, question in enumerate(result, start=1):
        question["currentNumber"] = number
        question["totalQuestions"] = 10
    return result


def _apply_chart_order(question: dict) -> dict:
    """銘柄のA/B/C割当をAPIプロセス内で一貫してランダム化する。"""
    stock_choices = [
        choice for choice in question["choices"] if choice["type"] == "stock"
    ]
    cash_choices = [
        choice for choice in question["choices"] if choice["type"] == "cash"
    ]
    if len(stock_choices) != 3 or len(cash_choices) != 1:
        raise ValueError("Chart A/B/Cの3銘柄と現金保有が必要です。")

    question_number = question["currentNumber"]
    order = _chart_orders.setdefault(
        question_number,
        tuple(_random.sample(range(3), k=3)),
    )
    ordered_stocks = [stock_choices[index] for index in order]
    for label, choice in zip(_CHART_LABELS, ordered_stocks, strict=True):
        choice["label"] = label
    question["choices"] = [*ordered_stocks, cash_choices[0]]
    return question


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/questions")
def get_questions():
    with SAMPLE_QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        questions_payload = deepcopy(json.load(file))

    chart_data_cache = {}
    try:
        selected_questions = _select_question_set(questions_payload["questions"])
        active_questions = deepcopy(selected_questions)
        questions_payload["questions"] = selected_questions
        questions_payload["questionCount"] = 10
        _chart_orders.clear()
        for question in questions_payload["questions"]:
            _apply_chart_order(question)
            stock_choices = [
                choice
                for choice in question["choices"]
                if choice["type"] == "stock"
            ]
            if len(stock_choices) != 3:
                raise ValueError("Chart A/B/Cの3銘柄が必要です。")
            tickers = [choice["ticker"] for choice in stock_choices]
            if len(set(tickers)) != len(tickers):
                raise ValueError("同一Question内のtickerが重複しています。")

            for choice in stock_choices:
                cache_key = (choice["ticker"], question["baseDate"])
                if cache_key not in chart_data_cache:
                    chart_data_cache[cache_key] = fetch_chart_data(
                        ticker=choice["ticker"],
                        base_date=question["baseDate"],
                    )
                choice.update(deepcopy(chart_data_cache[cache_key]))
                for hidden_key in (
                    "ticker",
                    "code",
                    "companyName",
                    "baseClose",
                    "evaluationClose",
                    "returnRate",
                    "yahooFinanceUrl",
                ):
                    choice.pop(hidden_key, None)
            question["correctChoiceLabel"] = ""
            question.pop("explanation", None)
            question.pop("problemType", None)
        _active_questions.clear()
        _active_questions.update(
            {
                question["currentNumber"]: question
                for question in active_questions
            }
        )
    except (KeyError, StopIteration, TypeError, ValueError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"株価データを取得できませんでした: {error}",
        ) from error

    return questions_payload


@app.get("/api/results/{question_number}")
def get_result(question_number: int):
    with SAMPLE_QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    try:
        active_question = _active_questions.get(question_number)
        question = deepcopy(
            active_question
            if active_question is not None
            else next(
                item
                for item in payload["questions"]
                if item["currentNumber"] == question_number
            )
        )
        _apply_chart_order(question)
        for choice in question["choices"]:
            if choice["type"] == "cash":
                choice["returnRate"] = 0.0
                continue
            chart_data = fetch_chart_data(choice["ticker"], question["baseDate"])
            future = fetch_future_candles(
                choice["ticker"],
                question["baseDate"],
                question["evaluationDate"],
            )
            choice.update(deepcopy(chart_data))
            choice["resultCandles"] = [*chart_data["candles"], *future]
            choice["baseClose"] = chart_data["candles"][-1]["close"]
            choice["evaluationClose"] = future[-1]["close"]
            choice["yahooFinanceUrl"] = (
                f"https://finance.yahoo.co.jp/quote/{choice['ticker']}/chart"
            )
            choice["returnRate"] = round(
                (choice["evaluationClose"] / choice["baseClose"] - 1) * 100,
                2,
            )

        evaluation_dates = {
            choice["resultCandles"][-1]["date"]
            for choice in question["choices"]
            if choice["type"] == "stock"
        }
        if len(evaluation_dates) != 1:
            raise ValueError("Chart A/B/Cの実評価日が一致しません。")
        question["evaluationDate"] = evaluation_dates.pop()
        stock_returns = [
            choice["returnRate"]
            for choice in question["choices"]
            if choice["type"] == "stock"
        ]
        problem_type = question.pop("problemType")
        positive_count = sum(value > 0 for value in stock_returns)
        negative_count = sum(value < 0 for value in stock_returns)
        if problem_type == "normal" and not (
            positive_count == 1 and negative_count == 2
        ):
            raise ValueError("通常問題の騰落率条件を満たしていません。")
        if problem_type == "cash" and negative_count != 3:
            raise ValueError("現金問題の騰落率条件を満たしていません。")
        if problem_type not in {"normal", "cash"}:
            raise ValueError(f"未知の問題種別です: {problem_type}")
        question["correctChoiceLabel"] = max(
            question["choices"], key=lambda choice: choice["returnRate"]
        )["label"]
        return question
    except (KeyError, StopIteration, TypeError, ValueError) as error:
        raise HTTPException(
            status_code=502,
            detail=f"結果データを取得できませんでした: {error}",
        ) from error
