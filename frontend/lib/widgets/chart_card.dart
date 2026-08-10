import 'package:flutter/material.dart';

import '../models/answer.dart';
import 'candlestick_chart.dart';

class ChartCard extends StatelessWidget {
  const ChartCard({
    super.key,
    required this.label,
    this.answer,
    this.showMovingAverages = false,
  });

  final String label;
  final Answer? answer;
  final bool showMovingAverages;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final chartHeight = (constraints.maxWidth * 0.3).clamp(180.0, 220.0);

        return Card(
          child: SizedBox(
            height: chartHeight,
            width: double.infinity,
            child: Center(
              child: answer != null && answer!.candles.isNotEmpty
                  ? Padding(
                      padding: const EdgeInsets.all(8),
                      child: CandlestickChart(
                        candles: answer!.candles,
                        ma20: answer!.ma20,
                        ma40: answer!.ma40,
                        ma70: answer!.ma70,
                        showMa20: showMovingAverages,
                        showMa40: showMovingAverages,
                        showMa70: showMovingAverages,
                      ),
                    )
                  : Text(label, style: Theme.of(context).textTheme.titleLarge),
            ),
          ),
        );
      },
    );
  }
}
