import 'package:flutter/material.dart';

import '../models/answer_record.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({super.key, required this.answerRecords});

  final List<AnswerRecord> answerRecords;

  void _goBackHome(BuildContext context) {
    Navigator.of(context).popUntil((route) => route.isFirst);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Result'), centerTitle: true),
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  '結果発表',
                  style: Theme.of(context).textTheme.headlineMedium,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 16),
                Text(
                  'ゲーム終了です',
                  style: Theme.of(context).textTheme.bodyLarge,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 16),
                Text(
                  '回答数: ${answerRecords.length}件',
                  style: Theme.of(context).textTheme.bodyLarge,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 32),
                FilledButton(
                  onPressed: () => _goBackHome(context),
                  child: const Text('ホームへ戻る'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
