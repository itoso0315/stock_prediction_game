import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/answer_record.dart';
import '../models/question.dart';
import '../models/answer.dart';
import '../widgets/candlestick_chart.dart';
import '../widgets/top_back_button.dart';

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
    this.isHistoryReview = false,
    this.externalUrlLauncher,
  });

  final AnswerRecord answerRecord;
  final Question question;
  final int correctCount;
  final int answeredCount;
  final int totalQuestions;
  final bool isLastQuestion;
  final VoidCallback onNext;
  final bool isHistoryReview;
  final Future<bool> Function(Uri uri)? externalUrlLauncher;

  bool get isCorrect =>
      answerRecord.selectedAnswerLabel == question.correctAnswerLabel;

  int get correctRate {
    if (answeredCount == 0) {
      return 0;
    }

    return (correctCount / answeredCount * 100).floor();
  }

  Future<void> _openYahooFinance(BuildContext context, Answer answer) async {
    final uri = answer.yahooFinanceUri;
    if (uri == null) return;

    try {
      final launched = await (externalUrlLauncher != null
          ? externalUrlLauncher!(uri)
          : launchUrl(uri, mode: LaunchMode.platformDefault));
      if (launched || !context.mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Yahoo!ファイナンスを開けませんでした')));
    } catch (_) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Yahoo!ファイナンスを開けませんでした')));
    }
  }

  @override
  Widget build(BuildContext context) {
    final buttonText = isHistoryReview
        ? '最終結果へ戻る'
        : isLastQuestion
        ? '最終結果を見る'
        : '次の問題へ';

    return Scaffold(
      appBar: AppBar(
        leadingWidth: 112,
        leading: const TopBackButton(),
        title: const Text('結果発表'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isWideScreen = constraints.maxWidth >= 700;
            final horizontalPadding = isWideScreen ? 32.0 : 16.0;
            final contentMaxWidth = isWideScreen
                ? 1000.0
                : constraints.maxWidth;
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
                        Text(
                          '基準日：${_formatDate(question.baseDate)}　'
                          '評価日：${_formatDate(question.evaluationDate)}',
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 12),
                        for (final answer in question.answers) ...[
                          _ResultAnswerCard(
                            answer: answer,
                            baseDate: question.baseDate,
                            evaluationDate: question.evaluationDate,
                            isSelected:
                                answer.label ==
                                answerRecord.selectedAnswerLabel,
                            isCorrect:
                                answer.label == question.correctAnswerLabel,
                            onOpenYahooFinance: answer.yahooFinanceUri == null
                                ? null
                                : () => _openYahooFinance(context, answer),
                          ),
                          const SizedBox(height: 12),
                        ],
                        if (question.explanation.isNotEmpty) ...[
                          const SizedBox(height: 4),
                          Card(
                            key: const ValueKey('ai-commentary'),
                            child: Padding(
                              padding: const EdgeInsets.all(18),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Icon(
                                        Icons.auto_awesome,
                                        size: 18,
                                        color: Theme.of(
                                          context,
                                        ).colorScheme.primary,
                                      ),
                                      const SizedBox(width: 8),
                                      Text(
                                        'AIひとこと解説',
                                        style: Theme.of(
                                          context,
                                        ).textTheme.titleMedium,
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 10),
                                  Text(
                                    question.explanation,
                                    style: Theme.of(
                                      context,
                                    ).textTheme.bodyLarge,
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ],
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

String _formatDate(String value) => value.replaceAll('-', '/');

class _ResultAnswerCard extends StatelessWidget {
  const _ResultAnswerCard({
    required this.answer,
    required this.baseDate,
    required this.evaluationDate,
    required this.isSelected,
    required this.isCorrect,
    this.onOpenYahooFinance,
  });

  final Answer answer;
  final String baseDate;
  final String evaluationDate;
  final bool isSelected;
  final bool isCorrect;
  final VoidCallback? onOpenYahooFinance;

  @override
  Widget build(BuildContext context) {
    final rate = answer.returnRate ?? 0;
    final rateText = '${rate > 0 ? '+' : ''}${rate.toStringAsFixed(2)}%';
    final colorScheme = Theme.of(context).colorScheme;

    final statusColor = isCorrect
        ? Colors.greenAccent
        : isSelected
        ? Colors.redAccent
        : colorScheme.outlineVariant;

    return Card(
      color: (isCorrect || isSelected)
          ? statusColor.withAlpha(10)
          : colorScheme.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: statusColor,
          width: isCorrect || isSelected ? 2 : 1,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Wrap(
              spacing: 8,
              runSpacing: 4,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                Text(
                  answer.label,
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                if (answer.companyName != null) Text(answer.companyName!),
                if (answer.ticker != null) Text(answer.ticker!),
                if (isSelected)
                  Chip(
                    backgroundColor:
                        (isCorrect ? Colors.greenAccent : Colors.redAccent)
                            .withAlpha(28),
                    side: BorderSide(
                      color: isCorrect ? Colors.greenAccent : Colors.redAccent,
                    ),
                    label: const Text('あなたの選択'),
                  ),
                if (isCorrect)
                  const Chip(
                    backgroundColor: Color(0x1C69F0AE),
                    side: BorderSide(color: Colors.greenAccent),
                    label: Text('正解'),
                  ),
                if (onOpenYahooFinance != null)
                  OutlinedButton.icon(
                    key: ValueKey('yahoo-finance-${answer.label}'),
                    onPressed: onOpenYahooFinance,
                    icon: const Icon(Icons.open_in_new, size: 16),
                    label: const Text('Yahoo!ファイナンス'),
                  ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              rateText,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                color: rate >= 0 ? Colors.greenAccent : Colors.redAccent,
              ),
            ),
            if (answer.isStock && answer.resultCandles.isNotEmpty) ...[
              const SizedBox(height: 10),
              SizedBox(
                height: 240,
                child: CandlestickChart(
                  candles: answer.resultCandles,
                  boundaryDate: baseDate,
                ),
              ),
            ],
          ],
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
