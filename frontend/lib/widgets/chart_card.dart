import 'package:flutter/material.dart';

class ChartCard extends StatelessWidget {
  final String label;

  const ChartCard({super.key, required this.label});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: SizedBox(
        height: 160,
        width: double.infinity,
        child: Center(
          child: Text(label, style: Theme.of(context).textTheme.titleLarge),
        ),
      ),
    );
  }
}
