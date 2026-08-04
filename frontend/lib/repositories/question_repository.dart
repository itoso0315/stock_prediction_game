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
      ),
      Question(
        currentNumber: 2,
        totalQuestions: 10,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answerLabels: ['Chart A', 'Chart B', 'Chart C', '現金保有'],
      ),
      Question(
        currentNumber: 3,
        totalQuestions: 10,
        chartLabels: ['Chart A', 'Chart B', 'Chart C'],
        answerLabels: ['Chart A', 'Chart B', 'Chart C', '現金保有'],
      ),
    ];
  }

  Question getQuestion(int index) {
    return getQuestions()[index];
  }
}
