import 'dart:convert';

import 'package:flutter/services.dart';

import '../models/question.dart';

class QuestionJsonRepository {
  const QuestionJsonRepository();

  Future<List<Question>> getQuestions() async {
    final jsonString = await rootBundle.loadString(
      'assets/sample_questions.json',
    );

    final decoded = jsonDecode(jsonString) as Map<String, dynamic>;
    final questionsJson = decoded['questions'] as List<dynamic>;

    return questionsJson
        .map(
          (item) => Question.fromJson(item as Map<String, dynamic>),
        )
        .toList();
  }
}
