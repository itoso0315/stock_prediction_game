import 'package:flutter/material.dart';

import '../config/app_config.dart';
import '../models/answer_record.dart';
import '../models/answer.dart';
import '../models/question.dart';
import '../repositories/question_api_repository.dart';
import '../repositories/game_stats_repository.dart';
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
    this.initialShowMovingAverages = false,
    this.gameStatsRepository,
  });

  final int initialIndex;
  final List<AnswerRecord> initialAnswerRecords;
  final List<Question>? initialQuestions;
  final QuestionApiRepository? questionRepository;
  final bool initialShowMovingAverages;
  final GameStatsRepository? gameStatsRepository;

  @override
  State<QuestionScreen> createState() => _QuestionScreenState();
}

class _QuestionScreenState extends State<QuestionScreen> {
  final _scrollController = ScrollController();
  List<Question>? _questions;
  late int _currentIndex;
  late final List<AnswerRecord> _answerRecords;
  var _isLoading = true;
  String? _errorMessage;
  String? _selectedAnswerLabel;
  late bool _showMovingAverages;
  var _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialIndex;
    _answerRecords = List<AnswerRecord>.from(widget.initialAnswerRecords);
    _showMovingAverages = widget.initialShowMovingAverages;

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
          QuestionApiRepository(baseUrl: AppConfig.apiBaseUrl);
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

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _selectAnswer(String answerLabel) {
    setState(() {
      _selectedAnswerLabel = answerLabel;
    });
  }

  Future<void> _confirmAnswer() async {
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

    setState(() {
      _isSubmitting = true;
    });

    try {
      final repository =
          widget.questionRepository ??
          QuestionApiRepository(baseUrl: AppConfig.apiBaseUrl);
      final resultQuestion = await repository.getResultQuestion(
        question.currentNumber,
      );
      if (!mounted) return;
      questions[_currentIndex] = resultQuestion;
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _isSubmitting = false;
        _errorMessage = '結果データを読み込めませんでした';
      });
      return;
    }

    _answerRecords.add(answerRecord);

    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => AnswerReviewScreen(
          answerRecord: answerRecord,
          question: questions[_currentIndex],
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
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            answerRecords: _answerRecords,
            questions: questions,
            gameStatsRepository: widget.gameStatsRepository,
          ),
        ),
      );
      return;
    }

    Navigator.of(context).pop();
    setState(() {
      _currentIndex++;
      _selectedAnswerLabel = null;
      _isSubmitting = false;
      _errorMessage = null;
    });
    if (_scrollController.hasClients) {
      _scrollController.jumpTo(0);
    }
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
            final chartAnswers = question.answers
                .where((answer) => answer.isStock)
                .toList(growable: false);
            final cashAnswer = question.answers.firstWhere(
              (answer) => answer.isCash,
            );

            return SingleChildScrollView(
              controller: _scrollController,
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
                          '過去約半年のチャートを見て、評価日までに最も騰落率が高い選択肢を選んでください。',
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        if (question.baseDate.isNotEmpty &&
                            question.evaluationDate.isNotEmpty) ...[
                          const SizedBox(height: 8),
                          Text(
                            '基準日：${_formatDate(question.baseDate)}　'
                            '評価日：${_formatDate(question.evaluationDate)}',
                            textAlign: TextAlign.center,
                          ),
                        ],
                        const SizedBox(height: 8),
                        Text(
                          '銘柄名は隠されています。チャートの形だけで判断しましょう。',
                          style: Theme.of(context).textTheme.bodyMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 12),
                        FilterChip(
                          key: const ValueKey('toggle-moving-averages'),
                          label: const Wrap(
                            alignment: WrapAlignment.center,
                            crossAxisAlignment: WrapCrossAlignment.center,
                            spacing: 6,
                            runSpacing: 2,
                            children: [
                              Text('移動平均線 ON／OFF'),
                              _MovingAverageLegend(
                                color: Colors.amber,
                                label: '20',
                              ),
                              _MovingAverageLegend(
                                color: Colors.cyanAccent,
                                label: '40',
                              ),
                              _MovingAverageLegend(
                                color: Colors.purpleAccent,
                                label: '70',
                              ),
                            ],
                          ),
                          selected: _showMovingAverages,
                          onSelected: (value) {
                            setState(() {
                              _showMovingAverages = value;
                            });
                          },
                        ),
                        const SizedBox(height: 24),
                        Column(
                          children: [
                            for (
                              var index = 0;
                              index < chartAnswers.length;
                              index++
                            ) ...[
                              _AnswerSelectionCard(
                                label: chartAnswers[index].label,
                                answer: chartAnswers[index],
                                isSelected:
                                    _selectedAnswerLabel ==
                                    chartAnswers[index].label,
                                onTap: () =>
                                    _selectAnswer(chartAnswers[index].label),
                                showMovingAverages: _showMovingAverages,
                              ),
                              if (index < chartAnswers.length - 1)
                                const SizedBox(height: 12),
                            ],
                          ],
                        ),
                        const SizedBox(height: 12),
                        ConstrainedBox(
                          constraints: BoxConstraints(
                            maxWidth: answerButtonMaxWidth,
                          ),
                          child: _AnswerSelectionCard(
                            label: cashAnswer.label,
                            answer: cashAnswer,
                            isSelected:
                                _selectedAnswerLabel == cashAnswer.label,
                            onTap: () => _selectAnswer(cashAnswer.label),
                            showMovingAverages: _showMovingAverages,
                          ),
                        ),
                        const SizedBox(height: 24),
                        ConstrainedBox(
                          constraints: BoxConstraints(
                            maxWidth: answerButtonMaxWidth,
                          ),
                          child: SizedBox(
                            width: double.infinity,
                            child: FilledButton(
                              onPressed:
                                  _selectedAnswerLabel == null || _isSubmitting
                                  ? null
                                  : _confirmAnswer,
                              child: _isSubmitting
                                  ? const SizedBox.square(
                                      dimension: 20,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2,
                                      ),
                                    )
                                  : const Text('回答する'),
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

class _MovingAverageLegend extends StatelessWidget {
  const _MovingAverageLegend({required this.color, required this.label});

  final Color color;
  final String label;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 10,
          height: 3,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(2),
          ),
        ),
        const SizedBox(width: 2),
        Text(label),
      ],
    );
  }
}

class _AnswerSelectionCard extends StatelessWidget {
  const _AnswerSelectionCard({
    required this.label,
    required this.answer,
    required this.isSelected,
    required this.onTap,
    required this.showMovingAverages,
  });

  final String label;
  final Answer? answer;
  final bool isSelected;
  final VoidCallback onTap;
  final bool showMovingAverages;

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
                  showMovingAverages: showMovingAverages,
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
