from html import escape

import streamlit as st

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