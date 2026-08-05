import 'package:flutter/material.dart';
import '../models/answer_record.dart';

import '../repositories/question_repository.dart';
import 'result_screen.dart';
import '../widgets/chart_card.dart';

class QuestionScreen extends StatefulWidget {
  const QuestionScreen({super.key});

  @override
  State<QuestionScreen> createState() => _QuestionScreenState();
}

class _QuestionScreenState extends State<QuestionScreen> {
  final _questions = const QuestionRepository().getQuestions();
  var _currentIndex = 0;
  final _answerRecords = <AnswerRecord>[];
  String? _selectedAnswerLabel;

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

    _goToNextQuestion(selectedAnswerLabel);
  }

  void _goToNextQuestion(String selectedAnswerLabel) {
    final question = _questions[_currentIndex];
    _answerRecords.add(
      AnswerRecord(
        questionNumber: question.currentNumber,
        selectedAnswerLabel: selectedAnswerLabel,
      ),
    );

    if (_currentIndex >= _questions.length - 1) {
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            answerRecords: _answerRecords,
            questions: _questions,
          ),
        ),
      );
      return;
    }

    setState(() {
      _currentIndex++;
      _selectedAnswerLabel = null;
    });
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
