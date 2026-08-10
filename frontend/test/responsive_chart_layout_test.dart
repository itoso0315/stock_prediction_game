import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/models/answer.dart';
import 'package:stock_trainer_flutter/models/candle.dart';
import 'package:stock_trainer_flutter/models/moving_average_point.dart';
import 'package:stock_trainer_flutter/models/question.dart';
import 'package:stock_trainer_flutter/screens/question_screen.dart';
import 'package:stock_trainer_flutter/widgets/candlestick_chart.dart';
import 'package:stock_trainer_flutter/widgets/chart_card.dart';

void main() {
  testWidgets('すべての画面幅でチャートを縦3段に配置する', (tester) async {
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    tester.view.devicePixelRatio = 1;

    await _pumpAtSize(tester, const Size(1200, 900));
    _expectRows(tester, [1, 1, 1]);
    expect(find.byType(CandlestickChart), findsNWidgets(3));
    await tester.tap(find.byKey(const ValueKey('toggle-moving-averages')));
    await tester.pump();
    for (final chart in tester.widgetList<CandlestickChart>(
      find.byType(CandlestickChart),
    )) {
      expect(chart.showMa20, isTrue);
      expect(chart.showMa40, isTrue);
      expect(chart.showMa70, isTrue);
    }

    await _pumpAtSize(tester, const Size(800, 900));
    _expectRows(tester, [1, 1, 1]);

    await _pumpAtSize(tester, const Size(390, 844));
    _expectRows(tester, [1, 1, 1]);
  });
}

Future<void> _pumpAtSize(WidgetTester tester, Size size) async {
  tester.view.physicalSize = size;
  await tester.pumpWidget(
    const MaterialApp(home: QuestionScreen(initialQuestions: [_question])),
  );
  await tester.pumpAndSettle();
}

void _expectRows(WidgetTester tester, List<int> expectedCounts) {
  final cards = find.byType(ChartCard);
  final yPositions = [
    for (var index = 0; index < 3; index++)
      tester.getTopLeft(cards.at(index)).dy.round(),
  ];
  final countsByRow = <int, int>{};
  for (final y in yPositions) {
    countsByRow[y] = (countsByRow[y] ?? 0) + 1;
  }
  expect(countsByRow.values.toList(), expectedCounts);
}

const _question = Question(
  currentNumber: 1,
  totalQuestions: 1,
  chartLabels: ['Chart A', 'Chart B', 'Chart C'],
  answers: [
    Answer(
      label: 'Chart A',
      type: AnswerType.stock,
      candles: [_candle],
      ma20: [_ma],
      ma40: [_ma],
      ma70: [_ma],
    ),
    Answer(
      label: 'Chart B',
      type: AnswerType.stock,
      candles: [_candle],
      ma20: [_ma],
      ma40: [_ma],
      ma70: [_ma],
    ),
    Answer(
      label: 'Chart C',
      type: AnswerType.stock,
      candles: [_candle],
      ma20: [_ma],
      ma40: [_ma],
      ma70: [_ma],
    ),
    Answer(label: '現金保有', type: AnswerType.cash),
  ],
  correctAnswerLabel: 'Chart A',
);

const _candle = Candle(
  date: '2024-01-01',
  open: 100,
  high: 110,
  low: 90,
  close: 105,
  volume: 1000,
);

const _ma = MovingAveragePoint(date: '2024-01-01', value: 102);
