import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/models/answer.dart';
import 'package:stock_trainer_flutter/models/answer_record.dart';
import 'package:stock_trainer_flutter/models/question.dart';
import 'package:stock_trainer_flutter/screens/result_screen.dart';
import 'package:stock_trainer_flutter/widgets/result_share_card.dart';

void main() {
  test('正解数に応じて共有カードの称号を切り替える', () {
    expect(resultAchievementFor(10).label, 'MARKET STRUCTURE');
    expect(resultAchievementFor(10).message, '相場構造を捉えています');
    expect(resultAchievementFor(7).label, 'PRICE ACTION');
    expect(resultAchievementFor(7).message, '値動きの文脈が読めています');
    expect(resultAchievementFor(4).label, 'TREND AWARE');
    expect(resultAchievementFor(4).message, 'トレンドを認識できています');
    expect(resultAchievementFor(0).label, 'CHART OBSERVER');
    expect(resultAchievementFor(0).message, '観察眼を育成中です');
  });

  testWidgets('10問すべて正解なら100%を表示する', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: ResultScreen(
          answerRecords: _records(selectedLabel: 'Chart A'),
          questions: _questions(),
        ),
      ),
    );

    expect(find.text('10問中 10問正解'), findsOneWidget);
    expect(find.text('正答率: 100%'), findsOneWidget);
    expect(find.text('結果を共有しましょう'), findsOneWidget);
    expect(find.text('MARKET STRUCTURE'), findsOneWidget);
    expect(find.text('相場構造を捉えています'), findsOneWidget);
    expect(find.text('もう一度プレイ'), findsOneWidget);
  });

  testWidgets('10問すべて不正解なら0%を表示する', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: ResultScreen(
          answerRecords: _records(selectedLabel: '現金保有'),
          questions: _questions(),
        ),
      ),
    );

    expect(find.text('10問中 0問正解'), findsOneWidget);
    expect(find.text('正答率: 0%'), findsOneWidget);
  });

  testWidgets('最終結果に正方形カードと画像共有ボタンを表示する', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: ResultScreen(
          answerRecords: _records(selectedLabel: 'Chart A'),
          questions: _questions(),
        ),
      ),
    );

    expect(find.byKey(const ValueKey('result-share-card')), findsOneWidget);
    final button = find.byKey(const ValueKey('share-result-image'));
    expect(button, findsOneWidget);
    expect(find.text('結果画像を共有'), findsOneWidget);
  });

  testWidgets('回答詳細から各問題の回答画面を再表示できる', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: ResultScreen(
          answerRecords: _records(selectedLabel: 'Chart A'),
          questions: _questions(),
        ),
      ),
    );

    final firstDetail = find.byKey(const ValueKey('answer-detail-1'));
    await tester.ensureVisible(firstDetail);
    await tester.tap(firstDetail);
    await tester.pumpAndSettle();

    expect(find.text('問題 1 / 10'), findsOneWidget);
    expect(find.text('最終結果へ戻る'), findsOneWidget);

    await tester.ensureVisible(find.text('最終結果へ戻る'));
    await tester.tap(find.text('最終結果へ戻る'));
    await tester.pumpAndSettle();

    expect(find.text('10問中 10問正解'), findsOneWidget);
  });
}

List<Question> _questions() {
  return [
    for (var number = 1; number <= 10; number++)
      Question(
        currentNumber: number,
        totalQuestions: 10,
        chartLabels: const ['Chart A', 'Chart B', 'Chart C'],
        answers: const [
          Answer(label: 'Chart A', type: AnswerType.stock),
          Answer(label: 'Chart B', type: AnswerType.stock),
          Answer(label: 'Chart C', type: AnswerType.stock),
          Answer(label: '現金保有', type: AnswerType.cash),
        ],
        correctAnswerLabel: 'Chart A',
      ),
  ];
}

List<AnswerRecord> _records({required String selectedLabel}) {
  return [
    for (var number = 1; number <= 10; number++)
      AnswerRecord(questionNumber: number, selectedAnswerLabel: selectedLabel),
  ];
}
