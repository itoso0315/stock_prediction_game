import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../models/answer_record.dart';
import '../models/question.dart';
import '../repositories/game_stats_repository.dart';
import '../services/result_share_service.dart';
import '../widgets/result_share_card.dart';
import 'answer_review_screen.dart';

class ResultScreen extends StatefulWidget {
  const ResultScreen({
    super.key,
    required this.answerRecords,
    required this.questions,
    this.shareService = const PlatformResultShareService(),
    this.gameStatsRepository,
  });

  final List<AnswerRecord> answerRecords;
  final List<Question> questions;
  final ResultShareService shareService;
  final GameStatsRepository? gameStatsRepository;

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  late final Future<void> _recordResultFuture;
  final _shareCardKey = GlobalKey();

  List<AnswerRecord> get answerRecords => widget.answerRecords;
  List<Question> get questions => widget.questions;
  ResultShareService get shareService => widget.shareService;

  @override
  void initState() {
    super.initState();
    _recordResultFuture = _recordResult();
  }

  Future<void> _recordResult() async {
    if (answerRecords.isEmpty) return;
    try {
      await (widget.gameStatsRepository ?? const LocalGameStatsRepository())
          .recordGame(
            correctCount: _calculateCorrectCount(),
            totalQuestions: answerRecords.length,
          );
    } catch (_) {
      // 記録保存の失敗で最終Result画面を壊さない。
    }
  }

  Future<void> _goBackHome(BuildContext context) async {
    await _recordResultFuture;
    if (!context.mounted) return;
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

  Rect? _shareOrigin(BuildContext context) {
    final renderObject = context.findRenderObject();
    if (renderObject is! RenderBox) return null;
    return renderObject.localToGlobal(Offset.zero) & renderObject.size;
  }

  Future<void> _shareResultCard(BuildContext context, String text) async {
    final shareOrigin = _shareOrigin(context);
    final boundary = _shareCardKey.currentContext?.findRenderObject();
    if (boundary is! RenderRepaintBoundary) {
      throw StateError('共有画像を生成できませんでした。');
    }
    final image = await boundary.toImage(pixelRatio: 3);
    try {
      final byteData = await image.toByteData(format: ui.ImageByteFormat.png);
      if (byteData == null) {
        throw StateError('共有画像を生成できませんでした。');
      }
      await shareService.shareResultImage(
        byteData.buffer.asUint8List(),
        text,
        shareOrigin,
      );
    } finally {
      image.dispose();
    }
  }

  Future<void> _performShare(
    BuildContext context,
    Future<void> Function() action, {
    String? successMessage,
  }) async {
    try {
      await action();
      if (!context.mounted || successMessage == null) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(successMessage)));
    } catch (_) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('共有できませんでした。もう一度お試しください。')));
    }
  }

  List<Widget> _buildAnswerResultItems(BuildContext context) {
    return [
      for (final answerRecord in answerRecords) ...[
        _AnswerResultItem(
          answerRecord: answerRecord,
          question: questions.firstWhere(
            (question) => question.currentNumber == answerRecord.questionNumber,
          ),
          onTap: () => _openAnswerReview(context, answerRecord),
        ),
        const SizedBox(height: 12),
      ],
    ];
  }

  void _openAnswerReview(BuildContext context, AnswerRecord selectedRecord) {
    final answeredRecords = answerRecords
        .where(
          (record) => record.questionNumber <= selectedRecord.questionNumber,
        )
        .toList(growable: false);
    final correctCount = answeredRecords.where((record) {
      final question = questions.firstWhere(
        (item) => item.currentNumber == record.questionNumber,
      );
      return record.selectedAnswerLabel == question.correctAnswerLabel;
    }).length;
    final question = questions.firstWhere(
      (item) => item.currentNumber == selectedRecord.questionNumber,
    );

    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (reviewContext) => AnswerReviewScreen(
          answerRecord: selectedRecord,
          question: question,
          correctCount: correctCount,
          answeredCount: answeredRecords.length,
          totalQuestions: questions.length,
          isLastQuestion: selectedRecord.questionNumber == questions.length,
          isHistoryReview: true,
          onNext: () => Navigator.of(reviewContext).pop(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final correctCount = _calculateCorrectCount();
    final correctRate = answerRecords.isEmpty
        ? 0
        : (correctCount / answerRecords.length * 100).floor();
    final colorScheme = Theme.of(context).colorScheme;
    final shareText = buildResultShareText(
      correctCount: correctCount,
      totalQuestions: answerRecords.length,
      correctRate: correctRate,
    );

    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: const Text('Result'),
        centerTitle: true,
      ),
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
                                  '${answerRecords.length}問中 $correctCount問正解',
                                  style: Theme.of(context).textTheme.titleLarge,
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
                        Text(
                          '結果を共有しましょう',
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 12),
                        Center(
                          child: ConstrainedBox(
                            constraints: const BoxConstraints(maxWidth: 520),
                            child: RepaintBoundary(
                              key: _shareCardKey,
                              child: ResultShareCard(
                                correctCount: correctCount,
                                totalQuestions: answerRecords.length,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),
                        Center(
                          child: ConstrainedBox(
                            constraints: BoxConstraints(
                              maxWidth: buttonMaxWidth,
                            ),
                            child: SizedBox(
                              width: double.infinity,
                              child: OutlinedButton.icon(
                                key: const ValueKey('share-result-image'),
                                onPressed: () => _performShare(
                                  context,
                                  () => _shareResultCard(context, shareText),
                                ),
                                icon: const Icon(Icons.ios_share),
                                label: const Text('結果画像を共有'),
                              ),
                            ),
                          ),
                        ),
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
                                child: const Text('もう一度プレイ'),
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
  const _AnswerResultItem({
    required this.answerRecord,
    required this.question,
    required this.onTap,
  });

  final AnswerRecord answerRecord;
  final Question question;
  final VoidCallback onTap;

  bool get _isCorrect =>
      answerRecord.selectedAnswerLabel == question.correctAnswerLabel;

  @override
  Widget build(BuildContext context) {
    final resultLabel = _isCorrect ? '正解' : '不正解';
    final colorScheme = Theme.of(context).colorScheme;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        key: ValueKey('answer-detail-${question.currentNumber}'),
        onTap: onTap,
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
                  const SizedBox(width: 8),
                  const Icon(Icons.chevron_right),
                ],
              ),
              const SizedBox(height: 12),
              Text('選択: ${answerRecord.selectedAnswerLabel}'),
              const SizedBox(height: 4),
              Text('正解: ${question.correctAnswerLabel}'),
            ],
          ),
        ),
      ),
    );
  }
}
