class Question {
  final int currentNumber;
  final int totalQuestions;
  final List<String> chartLabels;
  final List<String> answerLabels;
  final String correctAnswerLabel;

  const Question({
    required this.currentNumber,
    required this.totalQuestions,
    required this.chartLabels,
    required this.answerLabels,
    required this.correctAnswerLabel,
  });
}
