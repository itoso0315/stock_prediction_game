import 'package:flutter/material.dart';

import '../models/question.dart';
import '../widgets/answer_button.dart';
import '../widgets/chart_card.dart';

class QuestionScreen extends StatelessWidget {
  const QuestionScreen({super.key});

  static const Question _question = Question(
    currentNumber: 1,
    totalQuestions: 10,
    chartLabels: ['Chart A', 'Chart B', 'Chart C'],
    answerLabels: ['Chart A', 'Chart B', 'Chart C', '現金保有'],
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Question ${_question.currentNumber} / ${_question.totalQuestions}',
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
                      index < _question.chartLabels.length;
                      index++
                    ) ...[
                      ChartCard(label: _question.chartLabels[index]),
                      if (index < _question.chartLabels.length - 1)
                        const SizedBox(height: 16),
                    ],
                    for (
                      var index = 0;
                      index < _question.answerLabels.length;
                      index++
                    ) ...[
                      AnswerButton(
                        label: _question.answerLabels[index],
                        onPressed: () {},
                      ),
                      if (index < _question.answerLabels.length - 1)
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
