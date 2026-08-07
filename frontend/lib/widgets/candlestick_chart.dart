

import 'package:flutter/material.dart';

import '../models/candle.dart';

class CandlestickChart extends StatelessWidget {
  const CandlestickChart({
    super.key,
    required this.candles,
  });

  final List<Candle> candles;

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: _CandlestickPainter(candles),
      size: const Size(double.infinity, 180),
    );
  }
}

class _CandlestickPainter extends CustomPainter {
  _CandlestickPainter(this.candles);

  final List<Candle> candles;

  @override
  void paint(Canvas canvas, Size size) {
    if (candles.isEmpty) return;

    final maxPrice = candles.map((c) => c.high).reduce((a, b) => a > b ? a : b);
    final minPrice = candles.map((c) => c.low).reduce((a, b) => a < b ? a : b);
    final range = (maxPrice - minPrice).clamp(1.0, double.infinity);

    final bodyWidth = size.width / (candles.length * 2);

    for (var i = 0; i < candles.length; i++) {
      final candle = candles[i];
      final x = (i + 0.5) * (size.width / candles.length);

      double y(double price) => size.height - ((price - minPrice) / range) * size.height;

      final paint = Paint()
        ..color = candle.close >= candle.open ? Colors.green : Colors.red
        ..strokeWidth = 1.5;

      canvas.drawLine(Offset(x, y(candle.high)), Offset(x, y(candle.low)), paint);

      final top = y(candle.open > candle.close ? candle.open : candle.close);
      final bottom = y(candle.open > candle.close ? candle.close : candle.open);

      canvas.drawRect(
        Rect.fromLTRB(x - bodyWidth / 2, top, x + bodyWidth / 2, bottom == top ? bottom + 1 : bottom),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant _CandlestickPainter oldDelegate) =>
      oldDelegate.candles != candles;
}