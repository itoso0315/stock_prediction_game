

import streamlit as st

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

        .result-status-partial {
            background: var(--warning-soft);
            border: 2px solid #F59E0B;
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

        .status-partial {
            color: var(--warning);
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
            margin-top: 12px;
        }

        .cash-explanation {
            background: var(--warning-soft);
            border: 1px solid #F5D48B;
            border-radius: 12px;
            padding: 14px 18px;
            color: #475569;
            font-weight: 650;
            margin-top: 12px;
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

        .recommended-book-card {
            background: #FFFFFF;
            border: 1px solid #F3D08A;
            border-radius: 16px;
            padding: 20px 22px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
            margin: 16px 0;
            text-align: center;
        }

        .recommended-book-title {
            color: var(--text);
            font-size: 1.2rem;
            font-weight: 850;
            margin-bottom: 6px;
        }

        .recommended-book-subtitle {
            color: #334155;
            font-size: 0.98rem;
            font-weight: 700;
            margin-bottom: 14px;
        }

        

        .recommended-book-details {
            text-align: left;
            padding: 6px 4px;
        }

        .recommended-book-name {
            color: var(--text);
            font-size: 1.1rem;
            font-weight: 900;
            line-height: 1.5;
            margin-bottom: 8px;
        }

        .recommended-book-author {
            color: var(--muted);
            font-size: 0.92rem;
            margin-bottom: 14px;
        }

        .recommended-book-description {
            color: #334155;
            font-size: 0.95rem;
            line-height: 1.65;
            margin-bottom: 12px;
        }

        .recommended-book-rating {
            color: #F59E0B;
            font-size: 1.05rem;
            letter-spacing: 0.08rem;
            margin-bottom: 12px;
        }

        .affiliate-disclosure {
            color: var(--muted);
            font-size: 0.75rem;
            margin-top: 10px;
        }

        .st-key-amazon_book_link a {
            background: #FF9900;
            color: #111827;
            border: none;
            border-radius: 10px;
            min-height: 46px;
            font-weight: 850;
            justify-content: center;
        }

        .st-key-amazon_book_link a:hover {
            background: #F59E0B;
            color: #111827;
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