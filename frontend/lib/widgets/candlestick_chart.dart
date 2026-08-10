import 'package:flutter/material.dart';

import '../models/candle.dart';
import '../models/moving_average_point.dart';

class CandlestickChart extends StatelessWidget {
  const CandlestickChart({
    super.key,
    required this.candles,
    this.ma20 = const [],
    this.ma40 = const [],
    this.ma70 = const [],
    this.showMa20 = false,
    this.showMa40 = false,
    this.showMa70 = false,
    this.boundaryDate,
  });

  final List<Candle> candles;
  final List<MovingAveragePoint> ma20;
  final List<MovingAveragePoint> ma40;
  final List<MovingAveragePoint> ma70;
  final bool showMa20;
  final bool showMa40;
  final bool showMa70;
  final String? boundaryDate;

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: _CandlestickPainter(
        candles: candles,
        ma20: ma20,
        ma40: ma40,
        ma70: ma70,
        showMa20: showMa20,
        showMa40: showMa40,
        showMa70: showMa70,
        boundaryDate: boundaryDate,
      ),
      size: const Size(double.infinity, 180),
    );
  }
}

class _CandlestickPainter extends CustomPainter {
  _CandlestickPainter({
    required this.candles,
    required this.ma20,
    required this.ma40,
    required this.ma70,
    required this.showMa20,
    required this.showMa40,
    required this.showMa70,
    required this.boundaryDate,
  });

  final List<Candle> candles;
  final List<MovingAveragePoint> ma20;
  final List<MovingAveragePoint> ma40;
  final List<MovingAveragePoint> ma70;
  final bool showMa20;
  final bool showMa40;
  final bool showMa70;
  final String? boundaryDate;

  @override
  void paint(Canvas canvas, Size size) {
    if (candles.isEmpty) return;

    const priceAreaRatio = 0.64;
    const volumeAreaTopRatio = 0.69;
    const timeAxisTopRatio = 0.88;
    final priceAreaHeight = size.height * priceAreaRatio;
    final volumeAreaTop = size.height * volumeAreaTopRatio;
    final timeAxisTop = size.height * timeAxisTopRatio;
    final volumeAreaHeight = timeAxisTop - volumeAreaTop;
    final visibleMaValues = <double>[
      if (showMa20) ...ma20.map((point) => point.value),
      if (showMa40) ...ma40.map((point) => point.value),
      if (showMa70) ...ma70.map((point) => point.value),
    ];
    final priceHighs = [...candles.map((c) => c.high), ...visibleMaValues];
    final priceLows = [...candles.map((c) => c.low), ...visibleMaValues];
    final maxPrice = priceHighs.reduce((a, b) => a > b ? a : b);
    final minPrice = priceLows.reduce((a, b) => a < b ? a : b);
    final range = (maxPrice - minPrice).clamp(1.0, double.infinity);
    final maxVolume = candles
        .map((c) => c.volume)
        .reduce((a, b) => a > b ? a : b);

    final bodyWidth = size.width / (candles.length * 2);
    double y(double price) =>
        priceAreaHeight - ((price - minPrice) / range) * priceAreaHeight;

    _paintPastBackground(canvas, size, timeAxisTop);

    for (var i = 0; i < candles.length; i++) {
      final candle = candles[i];
      final x = (i + 0.5) * (size.width / candles.length);

      final candleColor = candle.close >= candle.open
          ? Colors.green
          : Colors.red;
      final paint = Paint()
        ..color = candleColor
        ..strokeWidth = 1.5;

      canvas.drawLine(
        Offset(x, y(candle.high)),
        Offset(x, y(candle.low)),
        paint,
      );

      final top = y(candle.open > candle.close ? candle.open : candle.close);
      final bottom = y(candle.open > candle.close ? candle.close : candle.open);

      canvas.drawRect(
        Rect.fromLTRB(
          x - bodyWidth / 2,
          top,
          x + bodyWidth / 2,
          bottom == top ? bottom + 1 : bottom,
        ),
        paint,
      );

      if (maxVolume > 0 && candle.volume > 0) {
        final volumeHeight = volumeAreaHeight * candle.volume / maxVolume;
        final volumePaint = Paint()
          ..color = Colors.blue.withValues(alpha: 0.55);
        canvas.drawRect(
          Rect.fromLTRB(
            x - bodyWidth / 2,
            timeAxisTop - volumeHeight,
            x + bodyWidth / 2,
            timeAxisTop,
          ),
          volumePaint,
        );
      }
    }

    if (showMa20) {
      _paintMovingAverage(canvas, size, ma20, Colors.amber, y);
    }
    if (showMa40) {
      _paintMovingAverage(canvas, size, ma40, Colors.cyanAccent, y);
    }
    if (showMa70) {
      _paintMovingAverage(canvas, size, ma70, Colors.purpleAccent, y);
    }

    _paintBoundary(canvas, size, priceAreaHeight, timeAxisTop);

    _paintMonthLabels(canvas, size, timeAxisTop);
  }

  void _paintBoundary(
    Canvas canvas,
    Size size,
    double priceAreaHeight,
    double timeAxisTop,
  ) {
    final date = boundaryDate;
    if (date == null) return;
    final index = candles.indexWhere((candle) => candle.date == date);
    if (index < 0) return;
    final x = (index + 0.5) * (size.width / candles.length);
    final paint = Paint()
      ..color = Colors.white70
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;
    const dashLength = 4.0;
    const gapLength = 3.0;
    for (var top = 0.0; top < timeAxisTop; top += dashLength + gapLength) {
      canvas.drawLine(
        Offset(x, top),
        Offset(x, (top + dashLength).clamp(0, timeAxisTop)),
        paint,
      );
    }
    final textPainter = TextPainter(
      text: const TextSpan(
        text: '予測時点',
        style: TextStyle(color: Colors.white70, fontSize: 9),
      ),
      textDirection: TextDirection.ltr,
    )..layout();
    textPainter.paint(
      canvas,
      Offset(
        (x + 3).clamp(0, size.width - textPainter.width),
        priceAreaHeight - textPainter.height,
      ),
    );
  }

  void _paintPastBackground(Canvas canvas, Size size, double timeAxisTop) {
    final date = boundaryDate;
    if (date == null) return;
    final index = candles.indexWhere((candle) => candle.date == date);
    if (index < 0) return;
    final boundaryX = (index + 0.5) * (size.width / candles.length);
    canvas.drawRect(
      Rect.fromLTRB(0, 0, boundaryX, timeAxisTop),
      Paint()..color = Colors.grey.withValues(alpha: 0.10),
    );
  }

  void _paintMovingAverage(
    Canvas canvas,
    Size size,
    List<MovingAveragePoint> points,
    Color color,
    double Function(double) priceToY,
  ) {
    final valuesByDate = {for (final point in points) point.date: point.value};
    final path = Path();
    var hasStarted = false;

    for (var i = 0; i < candles.length; i++) {
      final value = valuesByDate[candles[i].date];
      if (value == null) continue;
      final x = (i + 0.5) * (size.width / candles.length);
      final offset = Offset(x, priceToY(value));
      if (hasStarted) {
        path.lineTo(offset.dx, offset.dy);
      } else {
        path.moveTo(offset.dx, offset.dy);
        hasStarted = true;
      }
    }

    if (hasStarted) {
      canvas.drawPath(
        path,
        Paint()
          ..color = color
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.3
          ..isAntiAlias = true,
      );
    }
  }

  void _paintMonthLabels(Canvas canvas, Size size, double timeAxisTop) {
    const minimumLabelSpacing = 44.0;
    const labelStyle = TextStyle(color: Colors.white54, fontSize: 9);
    String? previousMonth;
    var lastLabelX = double.negativeInfinity;

    for (var i = 0; i < candles.length; i++) {
      final date = DateTime.tryParse(candles[i].date);
      if (date == null) continue;

      final month = '${date.year}${date.month.toString().padLeft(2, '0')}';
      if (month == previousMonth) continue;
      previousMonth = month;

      final x = (i + 0.5) * (size.width / candles.length);
      if (x - lastLabelX < minimumLabelSpacing) continue;

      final textPainter = TextPainter(
        text: TextSpan(text: month, style: labelStyle),
        textDirection: TextDirection.ltr,
      )..layout();
      final left = (x - textPainter.width / 2).clamp(
        0.0,
        size.width - textPainter.width,
      );
      textPainter.paint(canvas, Offset(left, timeAxisTop + 2));
      lastLabelX = x;
    }
  }

  @override
  bool shouldRepaint(covariant _CandlestickPainter oldDelegate) =>
      oldDelegate.candles != candles ||
      oldDelegate.ma20 != ma20 ||
      oldDelegate.ma40 != ma40 ||
      oldDelegate.ma70 != ma70 ||
      oldDelegate.showMa20 != showMa20 ||
      oldDelegate.showMa40 != showMa40 ||
      oldDelegate.showMa70 != showMa70 ||
      oldDelegate.boundaryDate != boundaryDate;
}
