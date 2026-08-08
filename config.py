

"""Stock Trainer 全体で使う定数・設定値。"""

from game.question_generator import CASH_OPTION_LABEL


CHART_TITLES = ("Chart A", "Chart B", "Chart C")
CHART_CARD_KEYS = ("chart_card_a", "chart_card_b", "chart_card_c")
CHART_BUTTON_KEYS = ("select_chart_a", "select_chart_b", "select_chart_c")
ANSWER_LABELS = (*CHART_TITLES, CASH_OPTION_LABEL)
RESULT_CHART_CARD_KEYS = (
    "result_chart_card_a",
    "result_chart_card_b",
    "result_chart_card_c",
)

RECOMMENDED_BOOKS = (
    {
        "title": (
            "2000億円超を運用した伝説のファンドマネジャーの "
            "株トレ 世界一楽しい「一問一答」株の教科書"
        ),
        "author": "窪田 真之",
        "image": "assets/kabutore.jpg",
        "url": "https://link.amazon/B04Md0kbt",
    },
    {
        "title": (
            "2000億円超を運用した伝説のファンドマネジャーの "
            "株トレ ファンダメンタルズ編"
        ),
        "author": "窪田 真之",
        "image": "assets/kabutore2.jpg",
        "url": "https://link.amazon/B0ihXx6zR",
    },
    {
        "title": (
            "メガ盛「株ドリル」億を儲けた"
            "“鬼神プロトレーダーの技術”全部のせ"
        ),
        "author": "元機関投資家トレーダー堀江",
        "image": "assets/megamori.jpg",
        "url": "https://link.amazon/B06EKbeWT",
    },
)

ERROR_MESSAGE = "問題データを生成できませんでした。時間をおいて再度お試しください。"
RESULT_ERROR_MESSAGE = "結果を表示できませんでした。時間をおいて再度お試しください。"
CHALLENGE_START_ERROR_MESSAGE = (
    "チャレンジを開始できませんでした。時間をおいて再度お試しください。"
)
CHALLENGE_INITIALIZATION_ERROR_MESSAGE = (
    "チャレンジを初期化できませんでした。時間をおいて再度お試しください。"
)
CHALLENGE_RESULT_ERROR_MESSAGE = (
    "チャレンジ結果を表示できませんでした。時間をおいて再度お試しください。"
)

CHALLENGE_TOTAL_QUESTIONS = 10
CHALLENGE_TARGET_CORRECT = 7
QUESTION_RETURN_PATTERNS = (
    "one_positive",
    "two_positive",
    "all_negative",
    "one_positive",
    "two_positive",
    "one_positive",
    "all_negative",
    "two_positive",
    "one_positive",
    "all_negative",
)
CHALLENGE_STATE_KEYS = (
    "challenge_question_number",
    "challenge_correct_count",
    "challenge_answered_count",
)