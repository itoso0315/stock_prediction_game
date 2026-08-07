import 'package:flutter/material.dart';
import '../models/answer.dart';
import 'candlestick_chart.dart';

class ChartCard extends StatelessWidget {
  final String label;
  final Answer? answer;

  const ChartCard({
    super.key,
    required this.label,
    this.answer,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: SizedBox(
        height: 160,
        width: double.infinity,
        child: Center(
          child: answer != null && answer!.candles.isNotEmpty
              ? Padding(
                  padding: const EdgeInsets.all(8),
                  child: CandlestickChart(candles: answer!.candles),
                )
              : Text(
                  label,
                  style: Theme.of(context).textTheme.titleLarge,
                ),
        ),
      ),
    );
  }
}
