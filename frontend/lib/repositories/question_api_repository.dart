import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/question.dart';

class QuestionApiRepository {
  QuestionApiRepository({
    required String baseUrl,
    http.Client? client,
  })  : _baseUrl = baseUrl.replaceAll(RegExp(r'/$'), ''),
        _client = client ?? http.Client();

  final String _baseUrl;
  final http.Client _client;

  Future<List<Question>> getQuestions() async {
    final uri = Uri.parse('$_baseUrl/api/questions');
    final response = await _client.get(uri);

    if (response.statusCode != 200) {
      throw QuestionApiException(
        'Failed to load questions: HTTP ${response.statusCode}',
      );
    }

    try {
      final decoded = jsonDecode(utf8.decode(response.bodyBytes));

      if (decoded is! Map<String, dynamic>) {
        throw const FormatException('Expected a JSON object.');
      }

      final questionsJson = decoded['questions'];

      if (questionsJson is! List) {
        throw const FormatException('Expected "questions" to be a JSON array.');
      }

      return questionsJson
          .map(
            (item) => Question.fromJson(
              Map<String, dynamic>.from(item as Map),
            ),
          )
          .toList(growable: false);
    } on FormatException catch (error) {
      throw QuestionApiException(
        'Invalid questions response: ${error.message}',
      );
    } on TypeError catch (error) {
      throw QuestionApiException(
        'Invalid questions response: $error',
      );
    }
  }
}

class QuestionApiException implements Exception {
  const QuestionApiException(this.message);

  final String message;

  @override
  String toString() => 'QuestionApiException: $message';
}
