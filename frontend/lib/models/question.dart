import 'answer.dart';

class Question {
  final int currentNumber;
  final int totalQuestions;
  final List<String> chartLabels;
  final List<Answer> answers;
  final String correctAnswerLabel;

  const Question({
    required this.currentNumber,
    required this.totalQuestions,
    required this.chartLabels,
    required this.answers,
    required this.correctAnswerLabel,
  });

  List<String> get answerLabels =>
      answers.map((answer) => answer.label).toList();

  Answer get correctAnswer =>
      answers.firstWhere((answer) => answer.label == correctAnswerLabel);

  Answer answerByLabel(String label) {
    return answers.firstWhere((answer) => answer.label == label);
  }
}
