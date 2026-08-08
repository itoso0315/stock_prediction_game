from game.question_generator import GameQuestion

def _matches_return_pattern(
    returns: tuple[float, ...],
    target_pattern: str,
) -> bool:
    """騰落率の組み合わせが指定パターンに一致するか返す。"""
    positive_count = sum(value > 0 for value in returns)
    negative_count = sum(value < 0 for value in returns)

    return (
        target_pattern == "one_positive"
        and positive_count == 1
        and negative_count == 2
    ) or (
        target_pattern == "two_positive"
        and positive_count == 2
        and negative_count == 1
    ) or (
        target_pattern == "all_negative"
        and negative_count == 3
    )

def _get_result_judgement(
    question: GameQuestion,
    answer_value: str,
) -> tuple[bool, bool, str, str]:
    """回答結果の判定を返す。"""
    is_correct = answer_value == question.correct_label

    selected_chart = next(
        (
            chart
            for chart in question.charts
            if chart.label == answer_value
        ),
        None,
    )

    is_partial = (
        not is_correct
        and selected_chart is not None
        and selected_chart.future_return_percent >= 0
    )

    if is_correct:
        return True, False, "正解", "○"

    if is_partial:
        return False, True, "おしい", "△"

    return False, False, "不正解", "×"

def calculate_accuracy(correct_count: int, answered_count: int) -> int:
    """回答済み問題に対する整数の正答率を返す。"""
    if answered_count == 0:
        return 0
    return round(correct_count / answered_count * 100)
