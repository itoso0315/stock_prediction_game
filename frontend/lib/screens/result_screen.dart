import 'package:flutter/material.dart';

import '../models/answer_record.dart';
import '../models/question.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({
    super.key,
    required this.answerRecords,
    required this.questions,
  });

  final List<AnswerRecord> answerRecords;
  final List<Question> questions;

  void _goBackHome(BuildContext context) {
    Navigator.of(context).popUntil((route) => route.isFirst);
  }

  int _calculateCorrectCount() {
    var correctCount = 0;

    for (final answerRecord in answerRecords) {
      final question = questions.firstWhere(
        (question) => question.currentNumber == answerRecord.questionNumber,
      );

      if (answerRecord.selectedAnswerLabel == question.correctAnswerLabel) {
        correctCount++;
      }
    }

    return correctCount;
  }

  String _calculateRank(int correctRate) {
    if (correctRate >= 80) {
      return 'A';
    }

    if (correctRate >= 50) {
      return 'B';
    }

    return 'C';
  }

  List<Widget> _buildAnswerResultItems(BuildContext context) {
    return [
      for (final answerRecord in answerRecords) ...[
        _AnswerResultItem(
          answerRecord: answerRecord,
          question: questions.firstWhere(
            (question) => question.currentNumber == answerRecord.questionNumber,
          ),
        ),
        const SizedBox(height: 12),
      ],
    ];
  }

  @override
  Widget build(BuildContext context) {
    final correctCount = _calculateCorrectCount();
    final correctRate = answerRecords.isEmpty
        ? 0
        : (correctCount / answerRecords.length * 100).floor();
    final rank = _calculateRank(correctRate);
    return Scaffold(
      appBar: AppBar(title: const Text('Result'), centerTitle: true),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 24),
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
                  const SizedBox(height: 16),
                  Text(
                    '正解数: $correctCount問',
                    style: Theme.of(context).textTheme.bodyLarge,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    '正答率: $correctRate%',
                    style: Theme.of(context).textTheme.bodyLarge,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'ランク: $rank',
                    style: Theme.of(context).textTheme.bodyLarge,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  ..._buildAnswerResultItems(context),
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
      ),
    );
  }
}

class _AnswerResultItem extends StatelessWidget {
  const _AnswerResultItem({required this.answerRecord, required this.question});

  final AnswerRecord answerRecord;
  final Question question;

  bool get _isCorrect =>
      answerRecord.selectedAnswerLabel == question.correctAnswerLabel;

  @override
  Widget build(BuildContext context) {
    final resultLabel = _isCorrect ? '正解' : '不正解';

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Q${question.currentNumber}',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text('選択: ${answerRecord.selectedAnswerLabel}'),
            const SizedBox(height: 4),
            Text('正解: ${question.correctAnswerLabel}'),
            const SizedBox(height: 4),
            Text('結果: $resultLabel'),
          ],
        ),
      ),
    );
  }
}
