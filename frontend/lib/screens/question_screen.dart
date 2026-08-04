import 'package:flutter/material.dart';
import '../models/answer_record.dart';

import '../repositories/question_repository.dart';
import 'result_screen.dart';
import '../widgets/answer_button.dart';
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
        child: SingleChildScrollView(
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 800),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Column(
                  children: [
                    for (
                      var index = 0;
                      index < question.chartLabels.length;
                      index++
                    ) ...[
                      ChartCard(label: question.chartLabels[index]),
                      if (index < question.chartLabels.length - 1)
                        const SizedBox(height: 16),
                    ],
                    for (
                      var index = 0;
                      index < question.answerLabels.length;
                      index++
                    ) ...[
                      AnswerButton(
                        label: question.answerLabels[index],
                        onPressed: () =>
                            _goToNextQuestion(question.answerLabels[index]),
                      ),
                      if (index < question.answerLabels.length - 1)
                        const SizedBox(height: 12),
                    ],
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
