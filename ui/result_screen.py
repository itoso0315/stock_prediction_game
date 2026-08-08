"""結果画面で使用するヘルパー関数。"""

from html import escape

import streamlit as st


def get_chart_judgement(
    chart_label: str,
    future_return_percent: float,
    correct_label: str,
) -> tuple[str, str]:
    """結果画面の各チャートの判定表示を返す。"""
    if chart_label == correct_label:
        return "○ 正解", "metric-positive"

    if future_return_percent >= 0:
        return "△ プラス", "status-partial"

    return "× マイナス", "metric-negative"


def get_result_summary(
    is_correct: bool,
    is_partial: bool,
    correct_label: str,
    cash_option_label: str,
) -> tuple[str, str, str, str]:
    """結果サマリー表示に必要な情報を返す。"""
    if is_correct:
        return (
            "result-status-correct",
            "status-correct",
            "answer-right",
            "最も騰落率が高い選択肢を選べました！",
        )

    if is_partial:
        return (
            "result-status-partial",
            "status-partial",
            "status-partial",
            f"プラスの騰落率でしたが、{correct_label}の方が高い結果でした。",
        )

    detail_text = (
        "現金で保有が最も良い結果でした。"
        if correct_label == cash_option_label
        else f"{correct_label}が最も良い結果でした。"
    )

    return (
        "result-status-incorrect",
        "status-incorrect",
        "answer-wrong",
        detail_text,
    )


def render_result_summary_cards(
    *,
    is_correct: bool,
    is_partial: bool,
    correct_label: str,
    cash_option_label: str,
    result_icon: str,
    result_text: str,
    answer_value: str,
) -> None:
    """結果サマリー3枚を表示する。"""
    (
        status_class,
        status_text_class,
        answer_text_class,
        detail_text,
    ) = get_result_summary(
        is_correct,
        is_partial,
        correct_label,
        cash_option_label,
    )

    result_column, answer_column, correct_column = st.columns(
        [1.05, 0.95, 1.05], gap="medium"
    )

    with result_column:
        st.markdown(
            f"""
            <div class="result-summary-card {status_class}">
                <div class="summary-label">結果</div>
                <div class="status-main {status_text_class}">{escape(result_icon)} {escape(result_text)}</div>
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
                <div class="summary-main answer-right">{escape(str(correct_label))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_cash_result(cash_result_text: str | None) -> None:
    """現金保有の結果を表示する。"""
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


def render_ai_comment(technical_comment: str) -> None:
    """AI解説を、正解・不正解・学びの3ポイントに分けて表示する。"""
    selected_marker = "一方、選択した"
    lesson_marker = "今回のポイントは、"

    correct_text = technical_comment
    selected_text = ""
    lesson_text = ""

    if lesson_marker in correct_text:
        before_lesson, lesson_body = correct_text.split(lesson_marker, 1)
        correct_text = before_lesson.strip()
        lesson_text = f"{lesson_marker}{lesson_body.strip()}"

    if selected_marker in correct_text:
        correct_part, selected_part = correct_text.split(selected_marker, 1)
        correct_text = correct_part.strip()
        selected_text = f"{selected_marker}{selected_part.strip()}"

    st.markdown(
        """
        <div class="technical-comment-card">
            <div class="technical-comment-title">🤖 AIひとこと解説</div>
            <div class="technical-comment-note">
                価格・出来高・移動平均線から自動生成したルールベース解説です。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if correct_text:
        st.markdown(
            f"""
            <div style="
                background:#ECFDF3;
                border:1px solid #86EFAC;
                border-radius:14px;
                padding:16px 18px;
                margin:10px 0;
            ">
                <div style="font-weight:850; color:#166534; margin-bottom:8px;">
                    ✅ 正解Chartのポイント
                </div>
                <div style="color:#334155; line-height:1.7;">
                    {escape(correct_text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if selected_text:
        st.markdown(
            f"""
            <div style="
                background:#FEF2F2;
                border:1px solid #FCA5A5;
                border-radius:14px;
                padding:16px 18px;
                margin:10px 0;
            ">
                <div style="font-weight:850; color:#991B1B; margin-bottom:8px;">
                    ⚠️ 選んだChartの注意点
                </div>
                <div style="color:#334155; line-height:1.7;">
                    {escape(selected_text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if lesson_text:
        st.markdown(
            f"""
            <div style="
                background:#FFF8E8;
                border:1px solid #F5D48B;
                border-radius:14px;
                padding:16px 18px;
                margin:10px 0 16px;
            ">
                <div style="font-weight:850; color:#92400E; margin-bottom:8px;">
                    💡 今回のポイント
                </div>
                <div style="color:#334155; line-height:1.7;">
                    {escape(lesson_text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_recommended_book(
    recommended_book: dict[str, str],
) -> None:
    """おすすめ本を表示する。"""
    st.markdown(
        """
        <div class="recommended-book-card">
            <div class="recommended-book-title">📚 この考え方が学べる本</div>
            <div class="recommended-book-subtitle">
                今日のチャート判断を、もう少し深く学びたい人へ
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    book_image_column, book_detail_column = st.columns(
        [0.8, 1.7],
        gap="medium",
        vertical_alignment="center",
    )

    with book_image_column:
        st.image(
            recommended_book["image"],
            width="stretch",
        )

    with book_detail_column:
        st.markdown(
            f"""
            <div class="recommended-book-details">
                <div class="recommended-book-name">
                    {escape(str(recommended_book["title"]))}
                </div>
                <div class="recommended-book-author">
                    著者：{escape(str(recommended_book["author"]))}
                </div>
                <div class="recommended-book-rating">
                    おすすめ度：★★★★★
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button(
            "Amazonで見る",
            recommended_book["url"],
            key="amazon_book_link",
            width="stretch",
        )

    st.markdown(
        '<div class="affiliate-disclosure">'
        "※Amazonのアソシエイトとして、適格販売により収入を得ています。"
        "</div>",
        unsafe_allow_html=True,
    )


def render_result_charts(
    *,
    charts,
    review_figures,
    comparison_values,
    company_texts,
    yahoo_chart_urls,
    result_chart_card_keys,
    correct_label,
) -> None:
    """結果チャート3枚を表示する。"""
    result_columns = st.columns(3, gap="small")

    for (
        column,
        card_key,
        chart,
        figure,
        comparison,
        company_text,
        yahoo_url,
    ) in zip(
        result_columns,
        result_chart_card_keys,
        charts,
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

        chart_judgement, chart_judgement_class = get_chart_judgement(
            chart.label,
            chart.future_return_percent,
            correct_label,
        )

        with column:
            with st.container(key=card_key):
                st.subheader(chart.label)

                st.markdown(
                    f'<div class="{chart_judgement_class}" '
                    f'style="font-weight: 850; margin-bottom: 6px;">'
                    f'{escape(chart_judgement)}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="chart-company">'
                    f'{escape(company_text)}</div>',
                    unsafe_allow_html=True,
                )

                st.link_button(
                    "↗ Yahoo!ファイナンスでチャートを見る",
                    yahoo_url,
                )

                st.markdown(
                    f"""
                    <div class="metric-grid">
                        <div>
                            <div class="metric-label">基準日終値</div>
                            <div class="metric-value">
                                {escape(base_price)}
                            </div>
                        </div>
                        <div>
                            <div class="metric-label">評価日終値</div>
                            <div class="metric-value">
                                {escape(future_price)}
                            </div>
                        </div>
                        <div>
                            <div class="metric-label">騰落率</div>
                            <div class="metric-value {return_class}">
                                {escape(return_percent)}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

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
