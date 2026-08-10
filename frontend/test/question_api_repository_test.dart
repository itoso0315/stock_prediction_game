import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

import 'package:stock_trainer_flutter/repositories/question_api_repository.dart';

void main() {
  test('returns questions when API responds with 200', () async {
    final client = MockClient((request) async {
      expect(request.url.path, '/api/questions');
      return http.Response(
        '''{"questions": [
          {
            "currentNumber": 1,
            "totalQuestions": 3,
            "choices": [
              {
                "label": "Chart A",
                "type": "stock"
              },
              {
                "label": "現金保有",
                "type": "cash"
              }
            ],
            "correctChoiceLabel": "Chart A"
          }
        ]}''',
        200,
        headers: {'content-type': 'application/json'},
      );
    });

    final repository = QuestionApiRepository(
      baseUrl: 'http://127.0.0.1:8000',
      client: client,
    );

    final questions = await repository.getQuestions();
    expect(questions.length, 1);
  });

  test('throws on non-200 response', () async {
    final client = MockClient((_) async => http.Response('error', 500));

    final repository = QuestionApiRepository(
      baseUrl: 'http://127.0.0.1:8000',
      client: client,
    );

    expect(repository.getQuestions(), throwsException);
  });

  test('throws on invalid json', () async {
    final client = MockClient((_) async => http.Response('not json', 200));

    final repository = QuestionApiRepository(
      baseUrl: 'http://127.0.0.1:8000',
      client: client,
    );

    expect(repository.getQuestions(), throwsException);
  });

  test('returns result question from result endpoint', () async {
    final client = MockClient((request) async {
      expect(request.url.path, '/api/results/1');
      return http.Response(
        '''{
          "currentNumber": 1,
          "totalQuestions": 1,
          "baseDate": "2024-05-01",
          "evaluationDate": "2024-06-03",
          "choices": [
            {"label": "Chart A", "type": "stock", "resultCandles": []},
            {"label": "現金保有", "type": "cash", "returnRate": 0}
          ],
          "correctChoiceLabel": "現金保有"
        }''',
        200,
        headers: {'content-type': 'application/json; charset=utf-8'},
      );
    });
    final repository = QuestionApiRepository(
      baseUrl: 'http://127.0.0.1:8000',
      client: client,
    );

    final question = await repository.getResultQuestion(1);
    expect(question.baseDate, '2024-05-01');
    expect(question.evaluationDate, '2024-06-03');
    expect(question.correctAnswerLabel, '現金保有');
  });
}
