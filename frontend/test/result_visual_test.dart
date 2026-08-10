import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/models/answer.dart';
import 'package:stock_trainer_flutter/models/answer_record.dart';
import 'package:stock_trainer_flutter/models/candle.dart';
import 'package:stock_trainer_flutter/models/question.dart';
import 'package:stock_trainer_flutter/screens/answer_review_screen.dart';
import 'package:stock_trainer_flutter/widgets/candlestick_chart.dart';

void main() {
  testWidgets('正解は緑で表示しResultチャートに予測境界を渡す', (tester) async {
    Uri? openedUri;
    await tester.pumpWidget(
      MaterialApp(
        home: AnswerReviewScreen(
          answerRecord: const AnswerRecord(
            questionNumber: 1,
            selectedAnswerLabel: 'Chart A',
          ),
          question: _question,
          correctCount: 1,
          answeredCount: 1,
          totalQuestions: 1,
          isLastQuestion: true,
          onNext: () {},
          externalUrlLauncher: (uri) async {
            openedUri = uri;
            return true;
          },
        ),
      ),
    );

    expect(find.text('○ 正解'), findsNothing);
    expect(find.text('× 不正解'), findsNothing);
    expect(find.text('あなたの回答'), findsNothing);
    expect(find.text('AIひとこと解説'), findsOneWidget);
    expect(find.text('移動平均線と出来高を比較した解説です。'), findsOneWidget);
    expect(find.text('正答'), findsNothing);
    expect(find.text('あなたの選択'), findsOneWidget);
    final chart = tester.widget<CandlestickChart>(
      find.byType(CandlestickChart),
    );
    expect(chart.boundaryDate, '2024-05-01');
    expect(chart.candles, hasLength(2));
    final yahooButton = find.byKey(const ValueKey('yahoo-finance-Chart A'));
    expect(yahooButton, findsOneWidget);
    await tester.tap(yahooButton);
    await tester.pump();
    expect(
      openedUri.toString(),
      'https://finance.yahoo.co.jp/quote/1234.T/chart',
    );
  });

  testWidgets('不正解時は回答を赤、正答を緑で区別する', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: AnswerReviewScreen(
          answerRecord: const AnswerRecord(
            questionNumber: 1,
            selectedAnswerLabel: '現金保有',
          ),
          question: _question,
          correctCount: 0,
          answeredCount: 1,
          totalQuestions: 1,
          isLastQuestion: true,
          onNext: () {},
        ),
      ),
    );

    expect(find.text('あなたの回答'), findsNothing);
    expect(find.text('正答'), findsNothing);
    expect(find.text('あなたの選択'), findsOneWidget);
    expect(find.text('○ 正解'), findsNothing);
    expect(find.text('× 不正解'), findsNothing);
  });
}

const _question = Question(
  currentNumber: 1,
  totalQuestions: 1,
  baseDate: '2024-05-01',
  evaluationDate: '2024-06-03',
  chartLabels: ['Chart A'],
  answers: [
    Answer(
      label: 'Chart A',
      type: AnswerType.stock,
      companyName: 'テスト株式会社',
      ticker: '1234.T',
      returnRate: 10,
      resultCandles: [
        Candle(
          date: '2024-05-01',
          open: 100,
          high: 105,
          low: 95,
          close: 100,
          volume: 1000,
        ),
        Candle(
          date: '2024-06-03',
          open: 100,
          high: 115,
          low: 98,
          close: 110,
          volume: 1200,
        ),
      ],
    ),
    Answer(label: '現金保有', type: AnswerType.cash, returnRate: 0),
  ],
  correctAnswerLabel: 'Chart A',
  explanation: '移動平均線と出来高を比較した解説です。',
);
