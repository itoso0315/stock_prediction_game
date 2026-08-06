import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/models/answer.dart';
import 'package:stock_trainer_flutter/repositories/question_json_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('QuestionJsonRepository', () {
    test('ローカルJSONから3問のQuestionリストを取得できる', () async {
      final questions = await const QuestionJsonRepository().getQuestions();

      expect(questions, hasLength(3));
      expect(questions.first.currentNumber, 1);
      expect(questions.first.totalQuestions, 3);
    });

    test('1問目はChart A/B/Cと現金保有の4つの回答選択肢を持つ', () async {
      final questions = await const QuestionJsonRepository().getQuestions();
      final firstQuestion = questions.first;

      expect(firstQuestion.answers, hasLength(4));
      expect(firstQuestion.answerLabels, [
        'Chart A',
        'Chart B',
        'Chart C',
        '現金保有',
      ]);
    });

    test('chartLabelsには株式チャートだけが入り、現金保有は含まれない', () async {
      final questions = await const QuestionJsonRepository().getQuestions();
      final firstQuestion = questions.first;

      expect(firstQuestion.chartLabels, ['Chart A', 'Chart B', 'Chart C']);
      expect(firstQuestion.chartLabels, isNot(contains('現金保有')));
    });

    test('stockとcashのAnswerTypeをJSONから変換できる', () async {
      final questions = await const QuestionJsonRepository().getQuestions();
      final firstQuestion = questions.first;

      final stockAnswer = firstQuestion.answerByLabel('Chart A');
      final cashAnswer = firstQuestion.answerByLabel('現金保有');

      expect(stockAnswer.type, AnswerType.stock);
      expect(stockAnswer.isStock, isTrue);
      expect(stockAnswer.isCash, isFalse);

      expect(cashAnswer.type, AnswerType.cash);
      expect(cashAnswer.isCash, isTrue);
      expect(cashAnswer.isStock, isFalse);
    });

    test('正解ラベルと正解Answerを取得できる', () async {
      final questions = await const QuestionJsonRepository().getQuestions();
      final firstQuestion = questions.first;

      expect(firstQuestion.correctAnswerLabel, 'Chart B');
      expect(firstQuestion.correctAnswer.label, 'Chart B');
      expect(firstQuestion.correctAnswer.companyName, 'ルネサスエレクトロニクス');
      expect(firstQuestion.correctAnswer.returnRate, 12.54);
    });
  });
}
