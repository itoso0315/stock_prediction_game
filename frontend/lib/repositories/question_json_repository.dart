import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/question.dart';

class QuestionJsonRepository {
  const QuestionJsonRepository();

  Future<List<Question>> getQuestions() async {
    final jsonText = await rootBundle.loadString(
      'assets/sample_questions.json',
    );
    final jsonMap = jsonDecode(jsonText) as Map<String, dynamic>;
    final questionJsonList = jsonMap['questions'] as List<dynamic>;

    return questionJsonList
        .map(
          (questionJson) =>
              Question.fromJson(questionJson as Map<String, dynamic>),
        )
        .toList();
  }
}
