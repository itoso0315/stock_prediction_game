import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/models/answer.dart';
import 'package:stock_trainer_flutter/models/candle.dart';
import 'package:stock_trainer_flutter/models/moving_average_point.dart';
import 'package:stock_trainer_flutter/widgets/candlestick_chart.dart';
import 'package:stock_trainer_flutter/widgets/chart_card.dart';

void main() {
  testWidgets('画面幅に応じてチャートの高さを180〜220に調整する', (tester) async {
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(width: 720, child: ChartCard(label: 'A')),
        ),
      ),
    );

    // Cardの上下マージン各2pxを含む表示高。
    expect(tester.getSize(find.byType(Card)).height, 224);
  });

  testWidgets('共通設定がONのときMA20・MA40・MA70をすべて表示する', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ChartCard(
            label: 'Chart A',
            answer: _answer(),
            showMovingAverages: true,
          ),
        ),
      ),
    );

    final chart = tester.widget<CandlestickChart>(
      find.byType(CandlestickChart),
    );
    expect(chart.showMa20, isTrue);
    expect(chart.showMa40, isTrue);
    expect(chart.showMa70, isTrue);
    expect(find.text('移動平均線表示'), findsNothing);
  });
}

Answer _answer() {
  const date = '2024-01-01';
  const point = MovingAveragePoint(date: date, value: 102);
  return const Answer(
    label: 'Chart A',
    type: AnswerType.stock,
    candles: [
      Candle(
        date: date,
        open: 100,
        high: 110,
        low: 90,
        close: 105,
        volume: 1000,
      ),
    ],
    ma20: [point],
    ma40: [point],
    ma70: [point],
  );
}
