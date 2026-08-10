import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/models/answer.dart';
import 'package:stock_trainer_flutter/models/answer_record.dart';
import 'package:stock_trainer_flutter/models/question.dart';
import 'package:stock_trainer_flutter/screens/result_screen.dart';
import 'package:stock_trainer_flutter/services/result_share_service.dart';

void main() {
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

  testWidgets('最終結果からX・Instagram・LINE・URL共有を実行できる', (tester) async {
    final shareService = _FakeResultShareService();
    await tester.pumpWidget(
      MaterialApp(
        home: ResultScreen(
          answerRecords: _records(selectedLabel: 'Chart A'),
          questions: _questions(),
          shareService: shareService,
        ),
      ),
    );

    for (final key in [
      'share-x',
      'share-instagram',
      'share-line',
      'share-url',
    ]) {
      final button = find.byKey(ValueKey(key));
      expect(button, findsOneWidget);
      await tester.ensureVisible(button);
      await tester.tap(button);
      await tester.pump();
    }

    expect(shareService.xText, contains('10問中10問正解'));
    expect(shareService.xText, contains('正答率100%'));
    expect(shareService.xText, contains(stockTrainerShareUrl));
    expect(shareService.instagramText, shareService.xText);
    expect(shareService.lineText, shareService.xText);
    expect(shareService.didCopyUrl, isTrue);
    expect(find.text('共有URLをコピーしました'), findsOneWidget);
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

class _FakeResultShareService implements ResultShareService {
  String? xText;
  String? instagramText;
  String? lineText;
  bool didCopyUrl = false;

  @override
  Future<void> shareToX(String text) async => xText = text;

  @override
  Future<void> shareToInstagram(String text, Rect? origin) async {
    instagramText = text;
  }

  @override
  Future<void> shareToLine(String text) async => lineText = text;

  @override
  Future<void> copyShareUrl() async => didCopyUrl = true;
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
