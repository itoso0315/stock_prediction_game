import '../models/question.dart';

class QuestionRepository {
  const QuestionRepository();

  List<Question> getQuestions() {
    return const [
      Question(
        currentNumber: 1,
        totalQuestions: 10,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answerLabels: ['Chart A', 'Chart B', 'Chart C', '現金保有'],
        correctAnswerLabel: 'Chart A',
      ),
      Question(
        currentNumber: 2,
        totalQuestions: 10,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answerLabels: ['Chart A', 'Chart B', 'Chart C', '現金保有'],
        correctAnswerLabel: 'Chart B',
      ),
      Question(
        currentNumber: 3,
        totalQuestions: 10,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answerLabels: ['Chart A', 'Chart B', 'Chart C', '現金保有'],
        correctAnswerLabel: 'Chart C',
      ),
    ];
  }

  Question getQuestion(int index) {
    return getQuestions()[index];
  }
}
