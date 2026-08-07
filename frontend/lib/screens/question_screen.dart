import 'package:flutter/material.dart';

import '../models/answer_record.dart';
import '../models/answer.dart';
import '../models/question.dart';
import '../repositories/question_api_repository.dart';
import '../widgets/chart_card.dart';
import 'answer_review_screen.dart';
import 'result_screen.dart';

class QuestionScreen extends StatefulWidget {
  const QuestionScreen({
    super.key,
    this.initialIndex = 0,
    this.initialAnswerRecords = const [],
    this.initialQuestions,
    this.questionRepository,
  });

  final int initialIndex;
  final List<AnswerRecord> initialAnswerRecords;
  final List<Question>? initialQuestions;
  final QuestionApiRepository? questionRepository;

  @override
  State<QuestionScreen> createState() => _QuestionScreenState();
}

class _QuestionScreenState extends State<QuestionScreen> {
  List<Question>? _questions;
  late int _currentIndex;
  late final List<AnswerRecord> _answerRecords;
  var _isLoading = true;
  String? _errorMessage;
  String? _selectedAnswerLabel;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialIndex;
    _answerRecords = List<AnswerRecord>.from(widget.initialAnswerRecords);

    final initialQuestions = widget.initialQuestions;

    if (initialQuestions != null) {
      _questions = initialQuestions;
      _isLoading = false;
      return;
    }

    _loadQuestions();
  }

  Future<void> _loadQuestions() async {
    try {
      final repository =
          widget.questionRepository ??
          QuestionApiRepository(baseUrl: 'http://127.0.0.1:8000');
      final questions = await repository.getQuestions();

      if (!mounted) {
        return;
      }

      setState(() {
        _questions = questions;
        _isLoading = false;
      });
    } catch (_) {
      if (!mounted) {
        return;
      }

      setState(() {
        _errorMessage = '問題データを読み込めませんでした';
        _isLoading = false;
      });
    }
  }

  void _selectAnswer(String answerLabel) {
    setState(() {
      _selectedAnswerLabel = answerLabel;
    });
  }

  void _confirmAnswer() {
    final selectedAnswerLabel = _selectedAnswerLabel;
    final questions = _questions;

    if (selectedAnswerLabel == null || questions == null) {
      return;
    }

    final question = questions[_currentIndex];
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
          totalQuestions: questions.length,
          isLastQuestion: _currentIndex >= questions.length - 1,
          onNext: _goToNextFromReview,
        ),
      ),
    );
  }

  int _calculateCorrectCount() {
    final questions = _questions;

    if (questions == null) {
      return 0;
    }

    var correctCount = 0;

    for (final answerRecord in _answerRecords) {
      final question = questions.firstWhere(
        (question) => question.currentNumber == answerRecord.questionNumber,
      );

      if (answerRecord.selectedAnswerLabel == question.correctAnswerLabel) {
        correctCount++;
      }
    }

    return correctCount;
  }

  void _goToNextFromReview() {
    final questions = _questions;

    if (questions == null) {
      return;
    }

    if (_currentIndex >= questions.length - 1) {
      Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(
          builder: (context) =>
              ResultScreen(answerRecords: _answerRecords, questions: questions),
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
          initialQuestions: questions,
        ),
      ),
      (route) => route.isFirst,
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    final errorMessage = _errorMessage;

    if (errorMessage != null) {
      return Scaffold(body: Center(child: Text(errorMessage)));
    }

    final questions = _questions!;
    final question = questions[_currentIndex];

    return Scaffold(
      appBar: AppBar(
        title: Text('Question ${_currentIndex + 1} / ${questions.length}'),
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
                            label: question.answers[index].label,
                            answer: question.answers[index],
                            isSelected: _selectedAnswerLabel == question.answers[index].label,
                            onTap: () => _selectAnswer(question.answers[index].label),
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
    required this.answer,
    required this.isSelected,
    required this.onTap,
  });

  final String label;
  final Answer? answer;
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
                ChartCard(
                  label: label,
                  answer: answer,
                ),
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
