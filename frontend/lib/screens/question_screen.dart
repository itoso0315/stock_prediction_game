import 'package:flutter/material.dart';

import '../models/answer_record.dart';
import '../repositories/question_repository.dart';
import '../widgets/chart_card.dart';
import 'answer_review_screen.dart';
import 'result_screen.dart';

class QuestionScreen extends StatefulWidget {
  const QuestionScreen({
    super.key,
    this.initialIndex = 0,
    this.initialAnswerRecords = const [],
  });

  final int initialIndex;
  final List<AnswerRecord> initialAnswerRecords;

  @override
  State<QuestionScreen> createState() => _QuestionScreenState();
}

class _QuestionScreenState extends State<QuestionScreen> {
  final _questions = const QuestionRepository().getQuestions();
  late int _currentIndex;
  late final List<AnswerRecord> _answerRecords;
  String? _selectedAnswerLabel;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialIndex;
    _answerRecords = List<AnswerRecord>.from(widget.initialAnswerRecords);
  }

  void _selectAnswer(String answerLabel) {
    setState(() {
      _selectedAnswerLabel = answerLabel;
    });
  }

  void _confirmAnswer() {
    final selectedAnswerLabel = _selectedAnswerLabel;

    if (selectedAnswerLabel == null) {
      return;
    }

    final question = _questions[_currentIndex];
    final answerRecord = AnswerRecord(
      questionNumber: question.currentNumber,
      selectedAnswerLabel: selectedAnswerLabel,
    );

    _answerRecords.add(answerRecord);

    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => AnswerReviewScreen(
          answerRecord: answerRecord,
          question: question,
          correctCount: _calculateCorrectCount(),
          answeredCount: _answerRecords.length,
          totalQuestions: _questions.length,
          isLastQuestion: _currentIndex >= _questions.length - 1,
          onNext: _goToNextFromReview,
        ),
      ),
    );
  }

  int _calculateCorrectCount() {
    var correctCount = 0;

    for (final answerRecord in _answerRecords) {
      final question = _questions.firstWhere(
        (question) => question.currentNumber == answerRecord.questionNumber,
      );

      if (answerRecord.selectedAnswerLabel == question.correctAnswerLabel) {
        correctCount++;
      }
    }

    return correctCount;
  }

  void _goToNextFromReview() {
    if (_currentIndex >= _questions.length - 1) {
      Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            answerRecords: _answerRecords,
            questions: _questions,
          ),
        ),
        (route) => route.isFirst,
      );
      return;
    }

    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(
        builder: (context) => QuestionScreen(
          initialIndex: _currentIndex + 1,
          initialAnswerRecords: _answerRecords,
        ),
      ),
      (route) => route.isFirst,
    );
  }

  @override
  Widget build(BuildContext context) {
    final question = _questions[_currentIndex];

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Question ${question.currentNumber} / ${question.totalQuestions}',
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isWideScreen = constraints.maxWidth >= 700;
            final horizontalPadding = isWideScreen ? 32.0 : 16.0;
            final contentMaxWidth = isWideScreen ? 720.0 : constraints.maxWidth;
            final answerButtonMaxWidth = isWideScreen
                ? 520.0
                : constraints.maxWidth;

            return SingleChildScrollView(
              child: Center(
                child: ConstrainedBox(
                  constraints: BoxConstraints(maxWidth: contentMaxWidth),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: horizontalPadding,
                      vertical: 16,
                    ),
                    child: Column(
                      children: [
                        const SizedBox(height: 24),
                        Text(
                          '6か月分のチャートを見て、1か月後の評価日に最も騰落率が高い選択肢を選んでください。',
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          '銘柄名は隠されています。チャートの形だけで判断しましょう。',
                          style: Theme.of(context).textTheme.bodyMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 24),
                        for (
                          var index = 0;
                          index < question.answerLabels.length;
                          index++
                        ) ...[
                          _AnswerSelectionCard(
                            label: question.answerLabels[index],
                            isSelected:
                                _selectedAnswerLabel ==
                                question.answerLabels[index],
                            onTap: () =>
                                _selectAnswer(question.answerLabels[index]),
                          ),
                          if (index < question.answerLabels.length - 1)
                            const SizedBox(height: 12),
                        ],
                        const SizedBox(height: 24),
                        ConstrainedBox(
                          constraints: BoxConstraints(
                            maxWidth: answerButtonMaxWidth,
                          ),
                          child: SizedBox(
                            width: double.infinity,
                            child: FilledButton(
                              onPressed: _selectedAnswerLabel == null
                                  ? null
                                  : _confirmAnswer,
                              child: const Text('回答する'),
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

class _AnswerSelectionCard extends StatelessWidget {
  const _AnswerSelectionCard({
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: isSelected ? colorScheme.primary : colorScheme.outlineVariant,
          width: isSelected ? 2 : 1,
        ),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (label.startsWith('Chart')) ...[
                ChartCard(label: label),
                const SizedBox(height: 12),
              ],
              Text(
                label,
                style: Theme.of(context).textTheme.titleMedium,
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
