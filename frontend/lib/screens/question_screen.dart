import 'package:flutter/material.dart';
import '../models/answer_record.dart';
import '../repositories/question_repository.dart';

class ResultScreen extends StatelessWidget {
  final List<AnswerRecord> answerRecords;
  final List<Question> questions;

  const ResultScreen({
    super.key,
    required this.answerRecords,
    required this.questions,
  });

  int get correctCount {
    var count = 0;
    for (var i = 0; i < answerRecords.length; i++) {
      if (answerRecords[i].selectedAnswerLabel ==
          questions[i].correctAnswerLabel) {
        count++;
      }
    }
    return count;
  }

  double get accuracy {
    if (answerRecords.isEmpty) {
      return 0;
    }
    return correctCount / answerRecords.length;
  }

  String get rank {
    final acc = accuracy;
    if (acc == 1) {
      return 'S';
    } else if (acc >= 0.8) {
      return 'A';
    } else if (acc >= 0.6) {
      return 'B';
    } else if (acc >= 0.4) {
      return 'C';
    } else {
      return 'D';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('結果発表'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final isWideScreen = constraints.maxWidth >= 700;
            final horizontalPadding = isWideScreen ? 32.0 : 16.0;
            final contentMaxWidth = isWideScreen ? 720.0 : constraints.maxWidth;

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
                        const SizedBox(height: 24),
                        Text(
                          'ゲーム終了です',
                          style: Theme.of(context).textTheme.headlineSmall,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 24),
                        Text(
                          '回答数: ${answerRecords.length}',
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        Text(
                          '正解数: $correctCount',
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        Text(
                          '正答率: ${(accuracy * 100).toStringAsFixed(1)}%',
                          style: Theme.of(context).textTheme.titleMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 24),
                        Text(
                          'ランク: $rank',
                          style: Theme.of(context).textTheme.headlineMedium,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 32),
                        FilledButton(
                          onPressed: () {
                            Navigator.of(context).popUntil((route) => route.isFirst);
                          },
                          child: const Text('トップに戻る'),
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
