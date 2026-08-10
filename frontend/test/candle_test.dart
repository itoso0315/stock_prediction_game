import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/models/candle.dart';
import 'package:stock_trainer_flutter/models/answer.dart';

void main() {
  test('CandleがOHLCと出来高をJSONから読み込める', () {
    final candle = Candle.fromJson({
      'date': '2024-05-01',
      'open': 1000,
      'high': 1050.5,
      'low': 980,
      'close': 1030,
      'volume': 1234567,
    });

    expect(candle.date, '2024-05-01');
    expect(candle.open, 1000.0);
    expect(candle.high, 1050.5);
    expect(candle.low, 980.0);
    expect(candle.close, 1030.0);
    expect(candle.volume, 1234567);
  });

  test('volumeがない既存JSONは0として読み込める', () {
    final candle = Candle.fromJson({
      'date': '2024-05-01',
      'open': 1000,
      'high': 1050,
      'low': 980,
      'close': 1030,
    });

    expect(candle.volume, 0);
  });

  test('AnswerがMA20・MA40・MA70をJSONから読み込める', () {
    final answer = Answer.fromJson({
      'label': 'Chart A',
      'type': 'stock',
      'candles': <dynamic>[],
      'ma20': [
        {'date': '2024-05-01', 'value': 101.5},
      ],
      'ma40': [
        {'date': '2024-05-01', 'value': 99},
      ],
      'ma70': [
        {'date': '2024-05-01', 'value': 95.25},
      ],
    });

    expect(answer.ma20.single.value, 101.5);
    expect(answer.ma40.single.value, 99.0);
    expect(answer.ma70.single.value, 95.25);
  });
}
