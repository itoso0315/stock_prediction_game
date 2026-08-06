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
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(title: const Text('Result'), centerTitle: true),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isWideScreen = constraints.maxWidth >= 700;
            final horizontalPadding = isWideScreen ? 32.0 : 16.0;
            final contentMaxWidth = isWideScreen ? 720.0 : constraints.maxWidth;
            final buttonMaxWidth = isWideScreen ? 520.0 : constraints.maxWidth;

            return SingleChildScrollView(
              child: Center(
                child: ConstrainedBox(
                  constraints: BoxConstraints(maxWidth: contentMaxWidth),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: horizontalPadding,
                      vertical: 24,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(
                          '結果発表',
                          style: Theme.of(context).textTheme.headlineMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 12),
                        Text(
                          'ゲーム終了です',
                          style: Theme.of(context).textTheme.bodyLarge,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 28),
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(24),
                            child: Column(
                              children: [
                                Text(
                                  '正答率: $correctRate%',
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineMedium
                                      ?.copyWith(color: colorScheme.primary),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 12),
                                Text(
                                  '正答率70%を目指しましょう',
                                  style: Theme.of(context).textTheme.bodyMedium,
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 20),
                                Row(
                                  children: [
                                    Expanded(
                                      child: _SummaryMetric(
                                        label: '回答数',
                                        value: '${answerRecords.length}件',
                                      ),
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: _SummaryMetric(
                                        label: '正解数',
                                        value: '$correctCount問',
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 28),
                        Text(
                          '回答詳細',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        const SizedBox(height: 12),
                        ..._buildAnswerResultItems(context),
                        const SizedBox(height: 24),
                        Center(
                          child: ConstrainedBox(
                            constraints: BoxConstraints(
                              maxWidth: buttonMaxWidth,
                            ),
                            child: SizedBox(
                              width: double.infinity,
                              child: FilledButton(
                                onPressed: () => _goBackHome(context),
                                child: const Text('ホームへ戻る'),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _SummaryMetric extends StatelessWidget {
  const _SummaryMetric({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
      decoration: BoxDecoration(
        color: colorScheme.surface,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: colorScheme.outlineVariant),
      ),
      child: Column(
        children: [
          Text(
            label,
            style: Theme.of(context).textTheme.bodyMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 6),
          Text(
            value,
            style: Theme.of(context).textTheme.titleMedium,
            textAlign: TextAlign.center,
          ),
        ],
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
    final colorScheme = Theme.of(context).colorScheme;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    'Q${question.currentNumber}',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: _isCorrect
                        ? colorScheme.primary.withAlpha(30)
                        : colorScheme.surface,
                    borderRadius: BorderRadius.circular(999),
                    border: Border.all(
                      color: _isCorrect
                          ? colorScheme.primary.withAlpha(120)
                          : colorScheme.outlineVariant,
                    ),
                  ),
                  child: Text(
                    '結果: $resultLabel',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text('選択: ${answerRecord.selectedAnswerLabel}'),
            const SizedBox(height: 4),
            Text('正解: ${question.correctAnswerLabel}'),
          ],
        ),
      ),
    );
  }
}
