
"""Stock TrainerのStreamlitエントリーポイント。"""

from html import escape

import streamlit as st
import streamlit.components.v1 as components

from analytics.explanation import generate_technical_comment
from data.downloader import download_daily_prices
from data.nikkei225 import NIKKEI_225_TICKERS

from game.question_generator import (
    CASH_OPTION_LABEL,
    GameQuestion,
    create_yahoo_chart_url,
    generate_game_question,
    select_random_tickers,
)
from ui.charts import create_candlestick_chart, create_review_chart


CHART_TITLES = ("Chart A", "Chart B", "Chart C")
CHART_CARD_KEYS = ("chart_card_a", "chart_card_b", "chart_card_c")
CHART_BUTTON_KEYS = ("select_chart_a", "select_chart_b", "select_chart_c")
ANSWER_LABELS = (*CHART_TITLES, CASH_OPTION_LABEL)
RESULT_CHART_CARD_KEYS = (
    "result_chart_card_a",
    "result_chart_card_b",
    "result_chart_card_c",
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
CHALLENGE_STATE_KEYS = (
    "challenge_question_number",
    "challenge_correct_count",
    "challenge_answered_count",
)


class _ChallengeStartError(RuntimeError):
    """旧Session Stateからのチャレンジ開始失敗を表す。"""


class _ChallengeInitializationError(RuntimeError):
    """不正なチャレンジ状態の初期化失敗を表す。"""


def _generate_question_with_figures(
    show_ma25: bool,
    show_ma50: bool,
    show_ma75: bool,
) -> GameQuestion:
    """株価取得に失敗した場合は、別の銘柄で再試行する。"""
    last_error: Exception | None = None

    for _ in range(5):
        selected_tickers = select_random_tickers(NIKKEI_225_TICKERS)

        try:
            price_frames = tuple(
                download_daily_prices(ticker, period="5y")
                for ticker in selected_tickers
            )
            question = generate_game_question(selected_tickers, price_frames)
            tuple(
                create_candlestick_chart(
                    chart.display_data,
                    title=chart.label,
                    show_ma25=show_ma25,
                    show_ma50=show_ma50,
                    show_ma75=show_ma75,
                )
                for chart in question.charts
            )
            return question
        except Exception as error:
            last_error = error

    raise ValueError(
        "株価データの取得に複数回失敗しました。"
    ) from last_error


def _initial_challenge_state(question: GameQuestion) -> dict[str, object]:
    """新しい10問チャレンジの初期状態を返す。"""
    return {
        "game_question": question,
        "answer_choice": None,
        "selected_label": None,
        "submitted": False,
        "current_view": "question",
        "challenge_question_number": 1,
        "challenge_correct_count": 0,
        "challenge_answered_count": 0,
        "scroll_to_page_top": True,
    }


def _is_plain_int(value: object) -> bool:
    """boolを除くintかどうかを返す。"""
    return isinstance(value, int) and not isinstance(value, bool)


def _scroll_page_to_top() -> None:
    """Scroll Streamlit's main page container to the top after a view change."""
    components.html(
        """
        <script>
        const scrollToTop = () => {
            const parentDocument = window.parent.document;
            const selectors = [
                '[data-testid="stMain"]',
                'section.main',
                '.main',
                '[data-testid="stAppViewContainer"]'
            ];
            for (const selector of selectors) {
                for (const element of parentDocument.querySelectorAll(selector)) {
                    element.scrollTo(0, 0);
                    element.scrollTop = 0;
                    element.scrollLeft = 0;
                }
            }
            if (parentDocument.scrollingElement) {
                parentDocument.scrollingElement.scrollTo(0, 0);
                parentDocument.scrollingElement.scrollTop = 0;
            }
            window.parent.scrollTo(0, 0);
        };
        scrollToTop();
        window.parent.requestAnimationFrame(scrollToTop);
        for (const delay of [50, 150, 350, 700, 1200]) {
            window.parent.setTimeout(scrollToTop, delay);
        }
        </script>
        """,
        height=1,
    )


def _is_valid_session_state() -> bool:
    """チャレンジ状態が画面ごとの不変条件を満たすか検証する。"""
    required_keys = {
        "game_question",
        "answer_choice",
        "selected_label",
        "submitted",
        "current_view",
        *CHALLENGE_STATE_KEYS,
    }
    if not required_keys.issubset(st.session_state):
        return False

    question_number = st.session_state.challenge_question_number
    correct_count = st.session_state.challenge_correct_count
    answered_count = st.session_state.challenge_answered_count
    if not all(
        _is_plain_int(value)
        for value in (question_number, correct_count, answered_count)
    ):
        return False
    if not 1 <= question_number <= CHALLENGE_TOTAL_QUESTIONS:
        return False
    if not 0 <= correct_count <= answered_count <= CHALLENGE_TOTAL_QUESTIONS:
        return False
    if not isinstance(st.session_state.submitted, bool):
        return False

    current_view = st.session_state.current_view
    if current_view == "question":
        return (
            not st.session_state.submitted
            and st.session_state.selected_label is None
            and st.session_state.answer_choice in (None, *ANSWER_LABELS)
            and answered_count == question_number - 1
        )
    if current_view == "result":
        return (
            st.session_state.submitted
            and st.session_state.selected_label in ANSWER_LABELS
            and st.session_state.answer_choice
            == st.session_state.selected_label
            and answered_count == question_number
        )
    if current_view == "challenge_result":
        return (
            st.session_state.submitted
            and st.session_state.selected_label in ANSWER_LABELS
            and st.session_state.answer_choice
            == st.session_state.selected_label
            and question_number == CHALLENGE_TOTAL_QUESTIONS
            and answered_count == CHALLENGE_TOTAL_QUESTIONS
        )
    return False


def initialize_session_state(
    show_ma25: bool,
    show_ma50: bool,
    show_ma75: bool,
) -> None:
    """旧状態を安全に移行し、チャレンジ状態を初期化する。"""
    if any(key not in st.session_state for key in CHALLENGE_STATE_KEYS):
        try:
            question = _generate_question_with_figures(
                show_ma25,
                show_ma50,
                show_ma75,
            )
        except Exception as error:
            raise _ChallengeStartError from error
        st.session_state.update(_initial_challenge_state(question))
        return

    normalize_session_state(show_ma25, show_ma50, show_ma75)


def normalize_session_state(
    show_ma25: bool,
    show_ma50: bool,
    show_ma75: bool,
) -> None:
    """不正な状態を新しいチャレンジの初期状態へ原子的に戻す。"""
    if _is_valid_session_state():
        return

    try:
        question = _generate_question_with_figures(
            show_ma25,
            show_ma50,
            show_ma75,
        )
    except Exception as error:
        raise _ChallengeInitializationError from error
    st.session_state.update(_initial_challenge_state(question))


def select_answer(label: str) -> None:
    """回答確定前の選択中ラベルを保存する。"""
    if not st.session_state.submitted:
        st.session_state.answer_choice = label


def toggle_moving_averages() -> None:
    """MA25・MA50・MA75の表示状態を一括で切り替える。"""
    show_all = not all(
        bool(st.session_state.get(key, False))
        for key in ("show_ma25", "show_ma50", "show_ma75")
    )
    st.session_state.update(
        {
            "show_ma25": show_all,
            "show_ma50": show_all,
            "show_ma75": show_all,
        }
    )


def format_return_percent(value: float) -> str:
    """騰落率を符号付き小数第2位の表示文字列へ変換する。"""
    rounded = round(value, 2)
    if rounded == 0:
        return "0.00%"
    return f"{rounded:+.2f}%"


def format_price(value: float) -> str:
    """価格を3桁区切り、小数第2位、円表記へ変換する。"""
    return f"{value:,.2f}円"


def render_global_styles() -> None:
    """問題・結果画面で共通利用するスタイルを定義する。"""
    st.markdown(
        """
        <style>
        :root {
            --page-bg: #F6F8FB;
            --card-bg: #FFFFFF;
            --border: #D9E2EC;
            --text: #0F172A;
            --muted: #64748B;
            --primary: #2563EB;
            --primary-soft: #EFF6FF;
            --success: #16A34A;
            --success-soft: #ECFDF3;
            --danger: #DC2626;
            --danger-soft: #FEF2F2;
            --warning: #F59E0B;
            --warning-soft: #FFF8E8;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 15% 0%, rgba(37, 99, 235, 0.05), transparent 25%),
                var(--page-bg);
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1500px;
            padding-top: 1.4rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: var(--text);
        }

        .app-subtitle {
            color: var(--muted);
            font-size: 1.05rem;
            margin-top: -0.65rem;
            margin-bottom: 1.25rem;
        }

        .section-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
            margin-bottom: 16px;
        }

        .date-grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 24px;
            align-items: center;
        }

        .date-item {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .date-icon {
            font-size: 1.45rem;
        }

        .date-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
        }

        .date-value {
            color: var(--text);
            font-size: 1rem;
            font-weight: 700;
            margin-top: 2px;
        }

        .question-panel {
            background: linear-gradient(135deg, #F8FBFF, #EEF5FF);
            border: 1px solid #9EC5FE;
            border-radius: 16px;
            padding: 18px 20px;
            margin-bottom: 16px;
        }

        .question-title {
            color: var(--text);
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .question-main {
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 650;
        }

        .question-note {
            color: var(--muted);
            font-size: 0.92rem;
            margin-top: 5px;
        }

        .selection-heading {
            text-align: center;
            color: var(--text);
            font-size: 1.2rem;
            font-weight: 800;
            margin: 6px 0 14px;
        }

        .result-summary-card {
            border-radius: 16px;
            padding: 20px 22px;
            min-height: 220px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        }

        .result-status-correct {
            background: var(--success-soft);
            border: 2px solid #22C55E;
        }

        .result-status-incorrect {
            background: var(--danger-soft);
            border: 2px solid #EF4444;
        }

        .answer-summary {
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
        }

        .correct-summary {
            background: var(--success-soft);
            border: 1px solid #86EFAC;
        }

        .summary-label {
            color: var(--text);
            font-size: 0.95rem;
            font-weight: 800;
            margin-bottom: 18px;
        }

        .status-main {
            text-align: center;
            font-size: 2.15rem;
            font-weight: 900;
            margin-top: 12px;
        }

        .status-correct {
            color: var(--success);
        }

        .status-incorrect {
            color: var(--danger);
        }

        .summary-main {
            text-align: center;
            color: var(--text);
            font-size: 1.55rem;
            line-height: 1.35;
            font-weight: 900;
            margin-top: 38px;
        }

        .answer-wrong {
            color: var(--danger);
        }

        .answer-right {
            color: var(--success);
        }

        .status-detail {
            text-align: center;
            color: #334155;
            font-size: 0.95rem;
            font-weight: 650;
            margin-top: 10px;
        }

        .cash-strip {
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 12px;
            padding: 14px 18px;
            font-weight: 750;
            color: var(--text);
        }

        .cash-explanation {
            background: var(--warning-soft);
            border: 1px solid #F5D48B;
            border-radius: 12px;
            padding: 14px 18px;
            color: #475569;
            font-weight: 650;
        }

        .technical-comment-card {
            background: #FFFFFF;
            border: 1px solid #BFDBFE;
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
            margin: 16px 0;
            text-align: left;
        }

        .technical-comment-title {
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 850;
        }

        .technical-comment-note {
            color: var(--muted);
            font-size: 0.8rem;
            margin-top: 3px;
        }

        .technical-comment-body {
            color: #334155;
            font-size: 0.98rem;
            line-height: 1.7;
            margin-top: 12px;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 8px;
            background: #F8FAFC;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0 8px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.74rem;
            font-weight: 700;
        }

        .metric-value {
            color: var(--text);
            font-size: 0.95rem;
            font-weight: 850;
            margin-top: 3px;
        }

        .metric-positive {
            color: var(--success);
        }

        .metric-negative {
            color: var(--danger);
        }

        .chart-company {
            color: var(--text);
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .challenge-progress-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 14px 16px;
            box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
            text-align: center;
            margin-bottom: 16px;
        }

        .challenge-progress-label {
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 750;
        }

        .challenge-progress-value {
            color: var(--text);
            font-size: 1.15rem;
            font-weight: 900;
            margin-top: 3px;
        }

        .challenge-final-card {
            border-radius: 18px;
            padding: 24px;
            text-align: center;
            margin: 18px 0;
            box-shadow: 0 5px 18px rgba(15, 23, 42, 0.07);
        }

        .challenge-final-achieved {
            background: var(--success-soft);
            border: 2px solid #22C55E;
        }

        .challenge-final-pending {
            background: var(--warning-soft);
            border: 2px solid #F59E0B;
        }

        .challenge-final-title {
            color: var(--text);
            font-size: 1.7rem;
            font-weight: 900;
        }

        .challenge-final-message {
            color: #334155;
            font-size: 1rem;
            font-weight: 700;
            margin-top: 8px;
        }

        .st-key-chart_card_a,
        .st-key-chart_card_b,
        .st-key-chart_card_c,
        .st-key-cash_option_card,
        .st-key-result_chart_card_a,
        .st-key-result_chart_card_b,
        .st-key-result_chart_card_c {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 12px;
            box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
        }

        .st-key-chart_card_a,
        .st-key-chart_card_b,
        .st-key-chart_card_c {
            margin-bottom: 12px;
        }

        .st-key-toggle_moving_averages button {
            min-height: 64px;
            border-radius: 14px;
            background: #EFF6FF;
            border: 1px solid #BFDBFE;
            color: #334155;
            font-size: 1.1rem;
            font-weight: 850;
            justify-content: flex-start;
            text-align: left;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
        }

        .st-key-toggle_moving_averages button:hover {
            background: #E0EDFF;
            border-color: #93C5FD;
            color: #1E3A5F;
        }

        .st-key-cash_option_card {
            background: var(--warning-soft);
            border-color: #F5D48B;
        }

        .st-key-submit_answer button,
        .st-key-next_question button,
        .st-key-show_challenge_result button,
        .st-key-restart_challenge button {
            background: linear-gradient(135deg, #2563EB, #0F6CE5);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            font-weight: 800;
            min-height: 48px;
        }

        .st-key-submit_answer button:hover,
        .st-key-next_question button:hover,
        .st-key-show_challenge_result button:hover,
        .st-key-restart_challenge button:hover {
            background: linear-gradient(135deg, #1D4ED8, #075BC4);
            color: #FFFFFF;
        }

        @media (max-width: 900px) {
            .date-grid,
            .metric-grid {
                grid-template-columns: 1fr;
            }

            .result-summary-card {
                min-height: 180px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_date_card(base_date_text: str, evaluation_date_text: str) -> None:
    """基準日と評価日を1つのカードに表示する。"""
    st.markdown(
        f"""
        <div class="section-card">
            <div class="date-grid">
                <div class="date-item">
                    <div class="date-icon">🗓️</div>
                    <div>
                        <div class="date-label">基準日</div>
                        <div class="date-value">{escape(base_date_text)}</div>
                    </div>
                </div>
                <div class="date-item">
                    <div class="date-icon">🗓️</div>
                    <div>
                        <div class="date-label">評価日</div>
                        <div class="date-value">
                            {escape(evaluation_date_text)}
                            （20共通取引日後・おおむね約1か月後）
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_cards(items: tuple[tuple[str, str], ...]) -> None:
    """チャレンジ進捗を横並びのカードで表示する。"""
    columns = st.columns(len(items), gap="small")
    for column, (label, value) in zip(columns, items, strict=True):
        with column:
            st.markdown(
                f"""
                <div class="challenge-progress-card">
                    <div class="challenge-progress-label">{escape(label)}</div>
                    <div class="challenge-progress-value">{escape(value)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def calculate_accuracy(correct_count: int, answered_count: int) -> int:
    """回答済み問題に対する整数の正答率を返す。"""
    if answered_count == 0:
        return 0
    return round(correct_count / answered_count * 100)


def main() -> None:
    """10問チャレンジの3画面と回答UIを表示する。"""
    st.set_page_config(page_title="Stock Trainer", page_icon="📈", layout="wide")
    render_global_styles()

    st.title("📈 Stock Trainer")
    st.markdown(
        '<div class="app-subtitle">チャートで未来を予測して、投資判断力を鍛えよう！</div>',
        unsafe_allow_html=True,
    )

    show_ma25 = bool(st.session_state.get("show_ma25", False))
    show_ma50 = bool(st.session_state.get("show_ma50", False))
    show_ma75 = bool(st.session_state.get("show_ma75", False))

    try:
        initialize_session_state(show_ma25, show_ma50, show_ma75)
    except _ChallengeStartError as e:
        st.exception(e.__cause__)
        return
    except Exception as e:
        st.exception(e)
        return

    if st.session_state.pop("scroll_to_page_top", False):
        _scroll_page_to_top()

    question = st.session_state.game_question
    question_number = st.session_state.challenge_question_number
    correct_count = st.session_state.challenge_correct_count
    answered_count = st.session_state.challenge_answered_count

    if st.session_state.current_view == "challenge_result":
        try:
            if not _is_valid_session_state():
                raise ValueError("Invalid challenge result state.")
            incorrect_count = CHALLENGE_TOTAL_QUESTIONS - correct_count
            final_accuracy = round(
                correct_count / CHALLENGE_TOTAL_QUESTIONS * 100
            )
            target_achieved = correct_count >= CHALLENGE_TARGET_CORRECT
            remaining_count = max(0, CHALLENGE_TARGET_CORRECT - correct_count)
            final_items = (
                ("正解数", f"{correct_count} / {CHALLENGE_TOTAL_QUESTIONS}"),
                ("不正解数", f"{incorrect_count} / {CHALLENGE_TOTAL_QUESTIONS}"),
                ("正答率", f"{final_accuracy}%"),
                ("目標", "70%"),
            )
            final_title = "🎉 目標達成！" if target_achieved else "あと少し！"
            final_message = (
                "チャート判断の正答率70%以上を達成しました。"
                if target_achieved
                else f"目標70%まで、あと{remaining_count}問です。"
            )
            final_class = (
                "challenge-final-achieved"
                if target_achieved
                else "challenge-final-pending"
            )
        except Exception as e:
            st.exception(e)
            return

        st.header("10問チャレンジ結果")
        render_progress_cards(final_items)
        st.markdown(
            f"""
            <div class="challenge-final-card {final_class}">
                <div class="challenge-final-title">{escape(final_title)}</div>
                <div class="challenge-final-message">{escape(final_message)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _, restart_column, _ = st.columns([1, 0.9, 1])
        with restart_column:
            if st.button(
                "もう一度10問に挑戦する",
                key="restart_challenge",
                width="stretch",
            ):
                try:
                    next_question = _generate_question_with_figures(
                        show_ma25,
                        show_ma50,
                        show_ma75,
                    )
                except Exception:
                    st.error(ERROR_MESSAGE)
                else:
                    st.session_state.update(
                        _initial_challenge_state(next_question)
                    )
                    st.rerun()
        return

    if st.session_state.current_view == "result":
        try:
            if not _is_valid_session_state():
                raise ValueError("Invalid result state.")
            review_figures = tuple(
                create_review_chart(
                    chart.display_data,
                    chart.future_data,
                    chart.base_date,
                    title=f"{chart.label} - Review",
                    show_ma25=show_ma25,
                    show_ma50=show_ma50,
                    show_ma75=show_ma75,
                )
                for chart in question.charts
            )
            common_chart = question.charts[0]
            base_date_text = common_chart.base_date.strftime("%Y-%m-%d")
            evaluation_date_text = common_chart.evaluation_date.strftime("%Y-%m-%d")
            comparison_values = tuple(
                (
                    format_price(chart.base_close),
                    format_price(chart.future_close),
                    format_return_percent(chart.future_return_percent),
                )
                for chart in question.charts
            )
            company_texts = tuple(
                f"{chart.company_name}（{chart.security_code}）"
                for chart in question.charts
            )
            yahoo_chart_urls = tuple(
                create_yahoo_chart_url(chart.ticker) for chart in question.charts
            )
            answer_value = st.session_state.selected_label
            correct_value = question.correct_label
            is_correct = answer_value == correct_value
            result_text = "正解" if is_correct else "不正解"
            result_icon = "🎉" if is_correct else "☹"
            cash_result_text = (
                "3つのChartがすべて0%以下だったため、現金保有が最も良い結果でした。"
                if question.correct_label == CASH_OPTION_LABEL
                else None
            )
            current_accuracy = calculate_accuracy(correct_count, answered_count)
            result_progress_items = (
                ("問題", f"{question_number} / {CHALLENGE_TOTAL_QUESTIONS}"),
                ("現在の成績", f"{correct_count}問正解 / {answered_count}問回答"),
                ("現在の正答率", f"{current_accuracy}%"),
                ("目標", "70%"),
            )
            is_last_question = question_number == CHALLENGE_TOTAL_QUESTIONS
            action_label = (
                "10問の結果を見る" if is_last_question else "次の問題へ"
            )
            action_key = (
                "show_challenge_result" if is_last_question else "next_question"
            )
            technical_comment = generate_technical_comment(
                question,
                answer_value,
            )
        except Exception:
            st.error(RESULT_ERROR_MESSAGE)
            return

        st.header("🏆 結果発表")
        render_progress_cards(result_progress_items)
        render_date_card(base_date_text, evaluation_date_text)

        result_column, answer_column, correct_column = st.columns(
            [1.05, 0.95, 1.05], gap="medium"
        )
        status_class = (
            "result-status-correct" if is_correct else "result-status-incorrect"
        )
        status_text_class = "status-correct" if is_correct else "status-incorrect"
        answer_text_class = "answer-right" if is_correct else "answer-wrong"
        detail_text = (
            "素晴らしい判断でした！"
            if is_correct
            else (
                "現金で保有が最も良い結果でした。"
                if question.correct_label == CASH_OPTION_LABEL
                else f"{question.correct_label}が最も良い結果でした。"
            )
        )
        with result_column:
            st.markdown(
                f"""
                <div class="result-summary-card {status_class}">
                    <div class="summary-label">結果</div>
                    <div class="status-main {status_text_class}">{result_icon} {escape(result_text)}</div>
                    <div class="status-detail">{escape(detail_text)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with answer_column:
            st.markdown(
                f"""
                <div class="result-summary-card answer-summary">
                    <div class="summary-label">あなたの回答</div>
                    <div class="summary-main {answer_text_class}">{escape(str(answer_value))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with correct_column:
            st.markdown(
                f"""
                <div class="result-summary-card correct-summary">
                    <div class="summary-label">正解</div>
                    <div class="summary-main answer-right">{escape(str(correct_value))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        cash_column, explanation_column = st.columns([1, 2], gap="small")
        with cash_column:
            st.markdown(
                '<div class="cash-strip">💵 現金で保有：0.00%</div>',
                unsafe_allow_html=True,
            )
        with explanation_column:
            if cash_result_text is not None:
                st.markdown(
                    f'<div class="cash-explanation">💡 {escape(cash_result_text)}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            f"""
            <div class="technical-comment-card">
                <div class="technical-comment-title">🤖 AIひとこと解説</div>
                <div class="technical-comment-note">
                    価格・出来高・移動平均線から自動生成したルールベース解説です。
                </div>
                <div class="technical-comment-body">
                    {escape(technical_comment)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        moving_averages_visible = show_ma25 and show_ma50 and show_ma75
        st.button(
            "📈 移動平均線表示（ON）"
            if moving_averages_visible
            else "📈 移動平均線表示",
            key="toggle_moving_averages",
            type="secondary",
            on_click=toggle_moving_averages,
            width="stretch",
        )

        result_columns = st.columns(3, gap="small")
        for column, card_key, chart, figure, comparison, company_text, yahoo_url in zip(
            result_columns,
            RESULT_CHART_CARD_KEYS,
            question.charts,
            review_figures,
            comparison_values,
            company_texts,
            yahoo_chart_urls,
            strict=True,
        ):
            base_price, future_price, return_percent = comparison
            return_class = (
                "metric-positive"
                if chart.future_return_percent > 0
                else "metric-negative"
                if chart.future_return_percent < 0
                else ""
            )
            with column:
                with st.container(key=card_key):
                    st.subheader(chart.label)
                    st.markdown(
                        f'<div class="chart-company">{escape(company_text)}</div>',
                        unsafe_allow_html=True,
                    )
                    st.link_button("↗ Yahoo!ファイナンスでチャートを見る", yahoo_url)
                    st.markdown(
                        f"""
                        <div class="metric-grid">
                            <div><div class="metric-label">基準日終値</div><div class="metric-value">{escape(base_price)}</div></div>
                            <div><div class="metric-label">評価日終値</div><div class="metric-value">{escape(future_price)}</div></div>
                            <div><div class="metric-label">騰落率</div><div class="metric-value {return_class}">{escape(return_percent)}</div></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.plotly_chart(figure, use_container_width=True)

        _, next_button_column, _ = st.columns([1, 0.7, 1])
        with next_button_column:
            if st.button(action_label, key=action_key, width="stretch"):
                if is_last_question:
                    if _is_valid_session_state():
                        st.session_state.update(
                            {
                                "current_view": "challenge_result",
                                "scroll_to_page_top": True,
                            }
                        )
                        st.rerun()
                    else:
                        try:
                            normalize_session_state(show_ma25, show_ma50, show_ma75)
                        except _ChallengeInitializationError:
                            st.error(CHALLENGE_INITIALIZATION_ERROR_MESSAGE)
                else:
                    try:
                        next_question = _generate_question_with_figures(
                            show_ma25,
                            show_ma50,
                            show_ma75,
                        )
                    except Exception:
                        st.error(ERROR_MESSAGE)
                    else:
                        st.session_state.update(
                            {
                                "game_question": next_question,
                                "answer_choice": None,
                                "selected_label": None,
                                "submitted": False,
                                "current_view": "question",
                                "challenge_question_number": question_number + 1,
                                "challenge_correct_count": correct_count,
                                "challenge_answered_count": answered_count,
                                "scroll_to_page_top": True,
                            }
                        )
                        st.rerun()
        return

    try:
        figures = tuple(
            create_candlestick_chart(
                chart.display_data,
                title="",
                show_ma25=show_ma25,
                show_ma50=show_ma50,
                show_ma75=show_ma75,
            )
            for chart in question.charts
        )
        common_chart = question.charts[0]
        base_date_text = common_chart.base_date.strftime("%Y-%m-%d")
        evaluation_date_text = common_chart.evaluation_date.strftime("%Y-%m-%d")
        question_progress_items = (
            ("問題", f"{question_number} / {CHALLENGE_TOTAL_QUESTIONS}"),
            ("正解数", f"{correct_count}問"),
            ("目標", "70%"),
        )
    except Exception as e:
        st.exception(e)
        return

    render_progress_cards(question_progress_items)
    render_date_card(base_date_text, evaluation_date_text)

    st.markdown(
        """
        <div class="question-panel">
            <div class="question-title">🎯 問題</div>
            <div class="question-main">
                3つのチャートの中で、評価日に最も騰落率が高くなるものを選んでください。
            </div>
            <div class="question-note">
                ※ 現金で保有（値動き0%）という選択肢もあります。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    moving_averages_visible = show_ma25 and show_ma50 and show_ma75
    st.button(
        "📈 移動平均線表示（ON）"
        if moving_averages_visible
        else "📈 移動平均線表示",
        key="toggle_moving_averages",
        type="secondary",
        on_click=toggle_moving_averages,
        width="stretch",
    )

    chart_columns = st.columns(3, gap="small")

    for column, chart, figure, card_key in zip(
        chart_columns,
        question.charts,
        figures,
        CHART_CARD_KEYS,
        strict=True,
    ):
        with column:
            with st.container(key=card_key):
                st.subheader(chart.label)
                st.plotly_chart(figure, use_container_width=True)

    st.markdown(
        '<div class="section-card"><div class="selection-heading">'
        "どれに投資しますか？"
        "</div></div>",
        unsafe_allow_html=True,
    )

    selected_card_key = None
    if st.session_state.answer_choice in CHART_TITLES:
        selected_index = CHART_TITLES.index(st.session_state.answer_choice)
        selected_card_key = CHART_BUTTON_KEYS[selected_index]
    elif st.session_state.answer_choice == CASH_OPTION_LABEL:
        selected_card_key = "select_cash_option"

    selected_button_css = ""
    if selected_card_key is not None:
        selected_button_css = f"""
        .st-key-{selected_card_key} button {{
            background: #E8F1FF;
            border: 2px solid #2563EB;
            color: #174EA6;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.14);
        }}
        """

    st.markdown(
        f"""
        <style>
        {selected_button_css}
        .st-key-select_chart_a button,
        .st-key-select_chart_b button,
        .st-key-select_chart_c button,
        .st-key-select_cash_option button {{
            min-height: 96px;
            border-radius: 12px;
            font-weight: 800;
            white-space: normal;
        }}
        .st-key-select_cash_option button {{
            background: #FFF8E8;
            border-color: #F5D48B;
            color: #92400E;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    option_columns = st.columns(4, gap="small")
    for column, chart, button_key in zip(
        option_columns[:3],
        question.charts,
        CHART_BUTTON_KEYS,
        strict=True,
    ):
        with column:
            selection_mark = (
                "●" if st.session_state.answer_choice == chart.label else "○"
            )
            st.button(
                f"{selection_mark}  {chart.label}\nに投資する",
                key=button_key,
                on_click=select_answer,
                args=(chart.label,),
                width="stretch",
            )

    with option_columns[3]:
        cash_selection_mark = (
            "●" if st.session_state.answer_choice == CASH_OPTION_LABEL else "○"
        )
        st.button(
            f"{cash_selection_mark}  💵 現金で保有\n（値動き 0%）",
            key="select_cash_option",
            on_click=select_answer,
            args=(CASH_OPTION_LABEL,),
            width="stretch",
        )

    _, submit_column, _ = st.columns([1, 0.75, 1])
    with submit_column:
        if st.button(
            "▶ 回答を確定する",
            key="submit_answer",
            width="stretch",
        ):
            if st.session_state.answer_choice is None:
                st.warning("1つ選択してください。")
            elif (
                not st.session_state.submitted
                and st.session_state.current_view == "question"
                and st.session_state.challenge_answered_count
                == st.session_state.challenge_question_number - 1
            ):
                selected_label = st.session_state.answer_choice
                next_answered_count = answered_count + 1
                next_correct_count = correct_count + int(
                    selected_label == question.correct_label
                )
                st.session_state.update(
                    {
                        "selected_label": selected_label,
                        "submitted": True,
                        "current_view": "result",
                        "challenge_answered_count": next_answered_count,
                        "challenge_correct_count": next_correct_count,
                        "scroll_to_page_top": True,
                    }
                )
                st.rerun()

        st.caption("一度回答したら変更できません。")


if __name__ == "__main__":
    main()
