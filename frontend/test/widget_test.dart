import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/main.dart';
import 'package:stock_trainer_flutter/repositories/question_repository.dart';
import 'package:stock_trainer_flutter/widgets/chart_card.dart';

void main() {
  test('Task025でQuestionの正解ラベルが選択肢に含まれている', () {
    final questions = const QuestionRepository().getQuestions();

    for (final question in questions) {
      expect(question.correctAnswerLabel, isNotEmpty);
      expect(question.answerLabels, contains(question.correctAnswerLabel));
    }
  });

  testWidgets('Task031で説明文つきQuestionScreenから回答できる', (tester) async {
    await tester.pumpWidget(const StockTrainerApp());

    expect(find.text('ゲーム開始'), findsOneWidget);

    await tester.tap(find.text('ゲーム開始'));
    await tester.pumpAndSettle();

    expect(find.text('Question 1 / 10'), findsOneWidget);
    expect(
      find.text('6か月分のチャートを見て、1か月後の評価日に最も騰落率が高い選択肢を選んでください。'),
      findsOneWidget,
    );
    expect(find.text('銘柄名は隠されています。チャートの形だけで判断しましょう。'), findsOneWidget);
    expect(find.byType(ChartCard), findsNWidgets(3));
    expect(find.text('Chart A'), findsNWidgets(2));
    expect(find.text('Chart B'), findsNWidgets(2));
    expect(find.text('Chart C'), findsNWidgets(2));
    expect(find.text('現金保有'), findsOneWidget);
    expect(find.text('回答する'), findsOneWidget);
    expect(find.byType(SingleChildScrollView), findsOneWidget);
    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNull,
    );

    await tester.ensureVisible(find.text('Chart A').last);
    await tester.tap(find.text('Chart A').last);
    await tester.pumpAndSettle();

    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNotNull,
    );

    await tester.ensureVisible(find.text('回答する'));
    await tester.tap(find.text('回答する'));
    await tester.pumpAndSettle();

    expect(find.text('Question 2 / 10'), findsOneWidget);
    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNull,
    );

    await tester.ensureVisible(find.text('現金保有'));
    await tester.tap(find.text('現金保有'));
    await tester.pumpAndSettle();

    await tester.ensureVisible(find.text('回答する'));
    await tester.tap(find.text('回答する'));
    await tester.pumpAndSettle();

    expect(find.text('Question 3 / 10'), findsOneWidget);
    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNull,
    );

    await tester.ensureVisible(find.text('現金保有'));
    await tester.tap(find.text('現金保有'));
    await tester.pumpAndSettle();

    await tester.ensureVisible(find.text('回答する'));
    await tester.tap(find.text('回答する'));
    await tester.pumpAndSettle();

    expect(find.text('結果発表'), findsOneWidget);
    expect(find.text('ゲーム終了です'), findsOneWidget);
    expect(find.text('回答数: 3件'), findsOneWidget);
    expect(find.text('正解数: 1問'), findsOneWidget);
    expect(find.text('正答率: 33%'), findsOneWidget);
    expect(find.text('ランク: C'), findsOneWidget);
    expect(find.text('Q1'), findsOneWidget);
    expect(find.text('選択: Chart A'), findsOneWidget);
    expect(find.text('正解: Chart A'), findsOneWidget);
    expect(find.text('結果: 正解'), findsOneWidget);
    expect(find.text('Q2'), findsOneWidget);
    expect(find.text('選択: 現金保有'), findsNWidgets(2));
    expect(find.text('正解: Chart B'), findsOneWidget);
    expect(find.text('結果: 不正解'), findsNWidgets(2));
    expect(find.text('Q3'), findsOneWidget);
    expect(find.text('正解: Chart C'), findsOneWidget);
    expect(find.text('ホームへ戻る'), findsOneWidget);
    expect(find.text('ゲーム開始'), findsNothing);

    await tester.ensureVisible(find.text('ホームへ戻る'));
    await tester.tap(find.text('ホームへ戻る'));
    await tester.pumpAndSettle();

    expect(find.text('ゲーム開始'), findsOneWidget);
    expect(find.byType(ChartCard), findsNothing);
  });
}
