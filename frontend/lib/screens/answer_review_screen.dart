import 'package:flutter/material.dart';

import '../models/answer_record.dart';
import '../models/question.dart';

class AnswerReviewScreen extends StatelessWidget {
  const AnswerReviewScreen({
    super.key,
    required this.answerRecord,
    required this.question,
    required this.correctCount,
    required this.answeredCount,
    required this.totalQuestions,
    required this.isLastQuestion,
    required this.onNext,
  });

  final AnswerRecord answerRecord;
  final Question question;
  final int correctCount;
  final int answeredCount;
  final int totalQuestions;
  final bool isLastQuestion;
  final VoidCallback onNext;

  bool get isCorrect =>
      answerRecord.selectedAnswerLabel == question.correctAnswerLabel;

  int get correctRate {
    if (answeredCount == 0) {
      return 0;
    }

    return (correctCount / answeredCount * 100).floor();
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final resultText = isCorrect ? '○ 正解' : '× 不正解';
    final buttonText = isLastQuestion ? '最終結果を見る' : '次の問題へ';

    final selectedAnswer = question.answerByLabel(
      answerRecord.selectedAnswerLabel,
    );
    final correctAnswer = question.correctAnswer;

    return Scaffold(
      appBar: AppBar(title: const Text('結果発表'), centerTitle: true),
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
                          '問題 ${question.currentNumber} / $totalQuestions',
                          style: Theme.of(context).textTheme.bodyLarge,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 28),
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    Expanded(
                                      child: _ReviewMetric(
                                        label: '現在の成績',
                                        value:
                                            '$correctCount問正解 / $answeredCount問回答',
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 12),
                                Row(
                                  children: [
                                    Expanded(
                                      child: _ReviewMetric(
                                        label: '現在の正答率',
                                        value: '$correctRate%',
                                      ),
                                    ),
                                    const SizedBox(width: 12),
                                    const Expanded(
                                      child: _ReviewMetric(
                                        label: '目標',
                                        value: '70%',
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                Text(
                                  '結果',
                                  style: Theme.of(context).textTheme.bodyMedium,
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  resultText,
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineMedium
                                      ?.copyWith(color: colorScheme.primary),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 20),
                                _AnswerDetail(
                                  label: 'あなたの回答',
                                  answerLabel: selectedAnswer.label,
                                  companyName: selectedAnswer.companyName,
                                  returnRate: selectedAnswer.returnRate,
                                ),
                                const SizedBox(height: 16),
                                _AnswerDetail(
                                  label: '正解',
                                  answerLabel: correctAnswer.label,
                                  companyName: correctAnswer.companyName,
                                  returnRate: correctAnswer.returnRate,
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          '正答率70%を目指しましょう',
                          style: Theme.of(context).textTheme.bodyMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 28),
                        Center(
                          child: ConstrainedBox(
                            constraints: BoxConstraints(
                              maxWidth: buttonMaxWidth,
                            ),
                            child: SizedBox(
                              width: double.infinity,
                              child: FilledButton(
                                onPressed: onNext,
                                child: Text(buttonText),
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

class _ReviewMetric extends StatelessWidget {
  const _ReviewMetric({required this.label, required this.value});

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

class _AnswerDetail extends StatelessWidget {
  const _AnswerDetail({
    required this.label,
    required this.answerLabel,
    required this.companyName,
    required this.returnRate,
  });

  final String label;
  final String answerLabel;
  final String? companyName;
  final double? returnRate;

  String get _returnRateText {
    final rate = returnRate;

    if (rate == null) {
      return '騰落率 --';
    }

    final prefix = rate > 0 ? '+' : '';
    return '騰落率 $prefix${rate.toStringAsFixed(2)}%';
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: colorScheme.surface,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: colorScheme.outlineVariant),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 8),
          Text(answerLabel, style: Theme.of(context).textTheme.titleMedium),
          if (companyName != null) ...[
            const SizedBox(height: 6),
            Text(companyName!, style: Theme.of(context).textTheme.bodyMedium),
          ],
          const SizedBox(height: 6),
          Text(_returnRateText, style: Theme.of(context).textTheme.bodyMedium),
        ],
      ),
    );
  }
}
