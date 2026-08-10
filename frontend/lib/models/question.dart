import 'answer.dart';

class Question {
  final int currentNumber;
  final int totalQuestions;
  final List<String> chartLabels;
  final List<Answer> answers;
  final String correctAnswerLabel;
  final String baseDate;
  final String evaluationDate;

  const Question({
    required this.currentNumber,
    required this.totalQuestions,
    required this.chartLabels,
    required this.answers,
    required this.correctAnswerLabel,
    this.baseDate = '',
    this.evaluationDate = '',
  });

  factory Question.fromJson(Map<String, dynamic> json) {
    final answers = (json['choices'] as List<dynamic>)
        .map(
          (choiceJson) => Answer.fromJson(choiceJson as Map<String, dynamic>),
        )
        .toList();

    return Question(
      currentNumber: json['currentNumber'] as int,
      totalQuestions: json['totalQuestions'] as int,
      chartLabels: answers
          .where((answer) => answer.isStock)
          .map((answer) => answer.label)
          .toList(),
      answers: answers,
      correctAnswerLabel: json['correctChoiceLabel'] as String,
      baseDate: json['baseDate'] as String? ?? '',
      evaluationDate: json['evaluationDate'] as String? ?? '',
    );
  }

  List<String> get answerLabels =>
      answers.map((answer) => answer.label).toList();

  Answer get correctAnswer =>
      answers.firstWhere((answer) => answer.label == correctAnswerLabel);

  Answer answerByLabel(String label) {
    return answers.firstWhere((answer) => answer.label == label);
  }
}
