
"""Stock TrainerのStreamlitエントリーポイント。"""
import random
from html import escape
from typing import Any

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
from ui.common import render_date_card, render_progress_cards
from ui.styles import render_global_styles

from game.rules import (
    _get_result_judgement,
    _matches_return_pattern,
    calculate_accuracy,
)

from ui.result_screen import (
    render_result_summary_cards,
    render_ai_comment,
    render_recommended_book,
    render_result_charts,
)

# Import constants from config.py
from config import (
    ANSWER_LABELS,
    CHALLENGE_STATE_KEYS,
    CHALLENGE_TARGET_CORRECT,
    CHALLENGE_TOTAL_QUESTIONS,
    CHART_BUTTON_KEYS,
    CHART_CARD_KEYS,
    CHART_TITLES,
    ERROR_MESSAGE,
    QUESTION_RETURN_PATTERNS,
    RECOMMENDED_BOOKS,
    RESULT_CHART_CARD_KEYS,
    RESULT_ERROR_MESSAGE,
    CHALLENGE_START_ERROR_MESSAGE,
    CHALLENGE_INITIALIZATION_ERROR_MESSAGE,
    CHALLENGE_RESULT_ERROR_MESSAGE,
)


class _ChallengeStartError(RuntimeError):
    """旧Session Stateからのチャレンジ開始失敗を表す。"""


class _ChallengeInitializationError(RuntimeError):
    """不正なチャレンジ状態の初期化失敗を表す。"""


def _generate_question_with_figures(
    show_ma25: bool,
    show_ma50: bool,
    show_ma75: bool,
    question_number: int = 1,
) -> GameQuestion:
    """株価取得に失敗した場合は、別の銘柄で再試行する。"""
    last_error: Exception | None = None
    pattern_order = st.session_state.get(
        "challenge_pattern_order",
        list(QUESTION_RETURN_PATTERNS),
    )
    target_pattern = pattern_order[question_number - 1]

    for _ in range(20):
        selected_tickers = select_random_tickers(NIKKEI_225_TICKERS)

        try:
            price_frames = tuple(
                download_daily_prices(ticker, period="5y")
                for ticker in selected_tickers
            )
            question = generate_game_question(selected_tickers, price_frames)
            returns = tuple(
                chart.future_return_percent for chart in question.charts
            )
            if not _matches_return_pattern(returns, target_pattern):
                continue
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
        "指定した騰落率パターンの問題を生成できませんでした。"
    ) from last_error


def _initial_challenge_state(question: GameQuestion) -> dict[str, object]:
    """新しい10問チャレンジの初期状態を返す。"""
    return {
        "challenge_pattern_order": random.sample(
            list(QUESTION_RETURN_PATTERNS),
            len(QUESTION_RETURN_PATTERNS),
        ),
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



def _get_recommended_book(question_number: int) -> dict[str, str]:
    """問題番号に応じたおすすめ本を返す。"""
    return RECOMMENDED_BOOKS[
        (question_number - 1) % len(RECOMMENDED_BOOKS)
    ]




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
                question_number=1,
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
            question_number=1,
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

def render_challenge_result_view(
    show_ma25: bool,
    show_ma50: bool,
    show_ma75: bool,
    correct_count: int,
) -> None:
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
                    question_number=1,
                )
            except Exception:
                st.error(ERROR_MESSAGE)
            else:
                st.session_state.update(
                    _initial_challenge_state(next_question)
                )
                st.rerun()
    return

def render_result_view(
    question: GameQuestion,
    show_ma25: bool,
    show_ma50: bool,
    show_ma75: bool,
    question_number: int,
    correct_count: int,
    answered_count: int,
) -> None:
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

        (
            is_correct,
            is_partial,
            result_text,
            result_icon,
        ) = _get_result_judgement(
            question,
            answer_value,
        )
        
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
        recommended_book = _get_recommended_book(question_number)

    except Exception:
        st.error(RESULT_ERROR_MESSAGE)
        return

    st.header("🏆 結果発表")
    render_progress_cards(result_progress_items)
    render_date_card(base_date_text, evaluation_date_text)

    render_result_summary_cards(
        is_correct=is_correct,
        is_partial=is_partial,
        correct_label=question.correct_label,
        cash_option_label=CASH_OPTION_LABEL,
        result_icon=result_icon,
        result_text=result_text,
        answer_value=answer_value,
    )

    render_ai_comment(technical_comment)

    render_recommended_book(recommended_book)

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

    render_result_charts(
        charts=question.charts,
        review_figures=review_figures,
        comparison_values=comparison_values,
        company_texts=company_texts,
        yahoo_chart_urls=yahoo_chart_urls,
        result_chart_card_keys=RESULT_CHART_CARD_KEYS,
        correct_label=question.correct_label,
    )

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
                        question_number=question_number + 1,
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

def render_question_view(
    question: GameQuestion,
    show_ma25: bool,
    show_ma50: bool,
    show_ma75: bool,
    question_number: int,
    correct_count: int,
    answered_count: int,
) -> None:
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

    st.markdown(
        '<div class="section-card"><div class="selection-heading">'
        "どれに投資しますか？"
        "</div></div>",
        unsafe_allow_html=True,
    )

    selected_card_key = None
    if st.session_state.answer_choice in CHART_TITLES:
        selected_index = CHART_TITLES.index(st.session_state.answer_choice)
        selected_card_key = CHART_CARD_KEYS[selected_index]
    elif st.session_state.answer_choice == CASH_OPTION_LABEL:
        selected_card_key = "cash_option_card"

    selected_card_css = ""
    if selected_card_key is not None:
        selected_card_css = f"""
        .st-key-{selected_card_key} {{
            background: #EEF5FF !important;
            border: 2px solid #2563EB !important;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.16) !important;
        }}
        """

    st.markdown(
        f"""
        <style>
        {selected_card_css}
        .st-key-select_chart_a button,
        .st-key-select_chart_b button,
        .st-key-select_chart_c button {{
            min-height: 46px;
            border-radius: 10px;
            font-weight: 800;
            margin-top: 6px;
        }}
        .st-key-select_cash_option button {{
            min-height: 54px;
            border-radius: 10px;
            font-weight: 850;
            background: #FFF8E8;
            border-color: #F5D48B;
            color: #92400E;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    chart_columns = st.columns(3, gap="small")

    for column, chart, figure, card_key, button_key in zip(
        chart_columns,
        question.charts,
        figures,
        CHART_CARD_KEYS,
        CHART_BUTTON_KEYS,
        strict=True,
    ):
        with column:
            with st.container(key=card_key):
            
                st.subheader(chart.label)
                st.plotly_chart(
                    figure,
                    use_container_width=True,
                    config={
                        "displaylogo": False,
                        "modeBarButtonsToRemove": [
                            "toImage",
                            "zoom2d",
                            "zoomIn2d",
                            "zoomOut2d",
                            "select2d",
                            "lasso2d",
                            "autoScale2d",
                            "toggleSpikelines",
                            "hoverClosestCartesian",
                            "hoverCompareCartesian",
                        ],
                    },
                )
                st.button(
                    f"{chart.label}を選択",
                    key=button_key,
                    on_click=select_answer,
                    args=(chart.label,),
                    width="stretch",
                )

    with st.container(key="cash_option_card"):
        st.markdown(
            """
            <div style="font-weight:850; font-size:1.05rem; margin-bottom:4px;">
                💵 現金で保有する
            </div>
            <div style="color:#64748B; font-size:0.9rem; margin-bottom:8px;">
                3つのChartより投資妙味が低いと判断した場合はこちらを選択
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            f"現金で保有を選択（値動き 0%）",
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
        render_challenge_result_view(
            show_ma25,
            show_ma50,
            show_ma75,
            correct_count,
        )
        return

    if st.session_state.current_view == "result":
        render_result_view(
            question,
            show_ma25,
            show_ma50,
            show_ma75,
            question_number,
            correct_count,
            answered_count,
        )
        return

    render_question_view(
        question,
        show_ma25,
        show_ma50,
        show_ma75,
        question_number,
        correct_count,
        answered_count,
)


if __name__ == "__main__":
    main()
