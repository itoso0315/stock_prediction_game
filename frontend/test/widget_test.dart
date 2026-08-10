import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:stock_trainer_flutter/main.dart';
import 'package:stock_trainer_flutter/repositories/question_api_repository.dart';
import 'package:stock_trainer_flutter/repositories/question_repository.dart';
import 'package:stock_trainer_flutter/widgets/chart_card.dart';
import 'package:stock_trainer_flutter/widgets/candlestick_chart.dart';

void main() {
  test('Task025でQuestionの正解ラベルが選択肢に含まれている', () {
    final questions = const QuestionRepository().getQuestions();

    for (final question in questions) {
      expect(question.correctAnswerLabel, isNotEmpty);
      expect(question.answerLabels, contains(question.correctAnswerLabel));
    }
  });

  testWidgets('Task035で回答後に1問ごとの結果発表画面を表示できる', (tester) async {
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final client = MockClient((request) async {
      if (request.url.path.startsWith('/api/results/')) {
        return _resultResponse(int.parse(request.url.pathSegments.last));
      }
      expect(request.url.path, '/api/questions');

      return http.Response(
        '''{"questions": [
          {
            "currentNumber": 1, "baseDate": "2024-05-01", "evaluationDate": "2024-06-03",
            "totalQuestions": 3,
            "choices": [
              {"label": "Chart A", "type": "stock"},
              {"label": "Chart B", "type": "stock"},
              {"label": "Chart C", "type": "stock"},
              {"label": "現金保有", "type": "cash"}
            ],
            "correctChoiceLabel": "Chart B"
          },
          {
            "currentNumber": 2, "baseDate": "2024-06-03", "evaluationDate": "2024-07-01",
            "totalQuestions": 3,
            "choices": [
              {"label": "Chart A", "type": "stock"},
              {"label": "Chart B", "type": "stock"},
              {"label": "Chart C", "type": "stock"},
              {"label": "現金保有", "type": "cash"}
            ],
            "correctChoiceLabel": "Chart B"
          },
          {
            "currentNumber": 3, "baseDate": "2024-07-01", "evaluationDate": "2024-08-01",
            "totalQuestions": 3,
            "choices": [
              {"label": "Chart A", "type": "stock"},
              {"label": "Chart B", "type": "stock"},
              {"label": "Chart C", "type": "stock"},
              {"label": "現金保有", "type": "cash"}
            ],
            "correctChoiceLabel": "Chart C"
          }
        ]}''',
        200,
        headers: {'content-type': 'application/json; charset=utf-8'},
      );
    });

    final repository = QuestionApiRepository(
      baseUrl: 'http://127.0.0.1:8000',
      client: client,
    );

    await tester.pumpWidget(StockTrainerApp(questionRepository: repository));

    expect(find.text('ゲーム開始'), findsOneWidget);
    expect(find.text('10問チャレンジ'), findsOneWidget);

    await tester.tap(find.text('ゲーム開始'));
    await tester.pumpAndSettle();

    expect(find.text('Question 1 / 3'), findsOneWidget);
    expect(
      find.text('過去約半年のチャートを見て、評価日までに最も騰落率が高い選択肢を選んでください。'),
      findsOneWidget,
    );
    expect(find.text('基準日：2024/05/01　評価日：2024/06/03'), findsOneWidget);
    expect(find.text('銘柄名は隠されています。チャートの形だけで判断しましょう。'), findsOneWidget);
    expect(find.byType(ChartCard), findsNWidgets(3));
    final chartCards = find.byType(ChartCard);
    final firstChartTopLeft = tester.getTopLeft(chartCards.at(0));
    final secondChartTopLeft = tester.getTopLeft(chartCards.at(1));
    final thirdChartTopLeft = tester.getTopLeft(chartCards.at(2));
    expect(secondChartTopLeft.dy, greaterThan(firstChartTopLeft.dy));
    expect(thirdChartTopLeft.dy, greaterThan(secondChartTopLeft.dy));
    expect(secondChartTopLeft.dx, firstChartTopLeft.dx);
    expect(thirdChartTopLeft.dx, firstChartTopLeft.dx);
    expect(find.text('Chart A'), findsNWidgets(2));
    expect(find.text('Chart B'), findsNWidgets(2));
    expect(find.text('Chart C'), findsNWidgets(2));
    expect(find.text('現金保有'), findsOneWidget);
    expect(find.text('回答する'), findsOneWidget);
    expect(find.text('20'), findsOneWidget);
    expect(find.text('40'), findsOneWidget);
    expect(find.text('70'), findsOneWidget);
    expect(find.byType(SingleChildScrollView), findsOneWidget);
    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNull,
    );

    await tester.tap(find.byKey(const ValueKey('toggle-moving-averages')));
    await tester.pumpAndSettle();
    expect(
      tester
          .widget<FilterChip>(
            find.byKey(const ValueKey('toggle-moving-averages')),
          )
          .selected,
      isTrue,
    );
    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNull,
    );

    await tester.ensureVisible(find.text('Chart A').last);
    await tester.tap(find.text('Chart A').last);
    await tester.pumpAndSettle();

    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNotNull,
    );

    await tester.ensureVisible(find.text('回答する'));
    await tester.tap(find.text('回答する'));
    await tester.pumpAndSettle();

    expect(find.text('結果発表'), findsWidgets);
    expect(find.text('問題 1 / 3'), findsOneWidget);
    expect(find.text('現在の成績'), findsOneWidget);
    expect(find.text('現在の正答率'), findsOneWidget);
    expect(find.text('目標'), findsOneWidget);
    expect(find.text('70%'), findsOneWidget);
    expect(find.text('あなたの回答'), findsNothing);
    expect(find.text('正解'), findsWidgets);
    expect(find.text('正答率70%を目指しましょう'), findsOneWidget);
    expect(find.text('次の問題へ'), findsOneWidget);
    expect(find.text('× 不正解'), findsNothing);
    expect(find.byType(CandlestickChart), findsNWidgets(3));
    expect(find.text('3099.T'), findsOneWidget);
    expect(find.text('現金保有'), findsWidgets);
    expect(find.text('0.00%'), findsWidgets);

    await tester.ensureVisible(find.text('次の問題へ'));
    await tester.tap(find.text('次の問題へ'));
    await tester.pumpAndSettle();

    expect(find.text('Question 2 / 3'), findsOneWidget);
    expect(
      tester
          .widget<FilterChip>(
            find.byKey(const ValueKey('toggle-moving-averages')),
          )
          .selected,
      isTrue,
    );
    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNull,
    );

    await tester.ensureVisible(find.text('現金保有'));
    await tester.tap(find.text('現金保有'));
    await tester.pumpAndSettle();

    await tester.ensureVisible(find.text('回答する'));
    await tester.tap(find.text('回答する'));
    await tester.pumpAndSettle();

    expect(find.text('結果発表'), findsWidgets);
    expect(find.text('問題 2 / 3'), findsOneWidget);
    expect(find.text('あなたの回答'), findsNothing);
    expect(find.text('正解'), findsWidgets);
    expect(find.text('正答率70%を目指しましょう'), findsOneWidget);
    expect(find.text('次の問題へ'), findsOneWidget);

    await tester.ensureVisible(find.text('次の問題へ'));
    await tester.tap(find.text('次の問題へ'));
    await tester.pumpAndSettle();

    expect(find.text('Question 3 / 3'), findsOneWidget);
    expect(
      tester
          .widget<FilledButton>(find.widgetWithText(FilledButton, '回答する'))
          .onPressed,
      isNull,
    );

    await tester.ensureVisible(find.text('現金保有'));
    await tester.tap(find.text('現金保有'));
    await tester.pumpAndSettle();

    await tester.ensureVisible(find.text('回答する'));
    await tester.tap(find.text('回答する'));
    await tester.pumpAndSettle();

    expect(find.text('結果発表'), findsWidgets);
    expect(find.text('問題 3 / 3'), findsOneWidget);
    expect(find.text('あなたの回答'), findsNothing);
    expect(find.text('正解'), findsWidgets);
    expect(find.text('正答率70%を目指しましょう'), findsOneWidget);
    expect(find.text('最終結果を見る'), findsOneWidget);

    await tester.ensureVisible(find.text('最終結果を見る'));
    await tester.tap(find.text('最終結果を見る'));
    await tester.pumpAndSettle();

    expect(find.text('結果発表'), findsOneWidget);
    expect(find.text('ゲーム終了です'), findsOneWidget);
    expect(find.text('回答数'), findsOneWidget);
    expect(find.text('3件'), findsOneWidget);
    expect(find.text('正解数'), findsOneWidget);
    expect(find.text('正答率70%を目指しましょう'), findsOneWidget);
    expect(find.text('Q1'), findsOneWidget);
    expect(find.text('選択: Chart A'), findsOneWidget);
    expect(find.text('正解: Chart B'), findsNWidgets(2));
    expect(find.text('Q2'), findsOneWidget);
    expect(find.text('選択: 現金保有'), findsNWidgets(2));
    expect(find.text('結果: 不正解'), findsNWidgets(3));
    expect(find.text('Q3'), findsOneWidget);
    expect(find.text('正解: Chart C'), findsOneWidget);
    expect(find.text('3問中 0問正解'), findsOneWidget);
    expect(find.text('もう一度プレイ'), findsOneWidget);
    expect(find.text('ゲーム開始'), findsNothing);

    await tester.ensureVisible(find.text('もう一度プレイ'));
    await tester.tap(find.text('もう一度プレイ'));
    await tester.pumpAndSettle();

    expect(find.text('ゲーム開始'), findsOneWidget);
    expect(find.byType(ChartCard), findsNothing);
  });
}

http.Response _resultResponse(int questionNumber) {
  final baseDates = ['2024-05-01', '2024-06-03', '2024-07-01'];
  final evaluationDates = ['2024-06-03', '2024-07-01', '2024-08-01'];
  final correctLabels = ['Chart B', 'Chart B', 'Chart C'];
  final baseDate = baseDates[questionNumber - 1];
  final evaluationDate = evaluationDates[questionNumber - 1];
  final labels = ['Chart A', 'Chart B', 'Chart C'];
  final choices = <Map<String, dynamic>>[
    for (var index = 0; index < labels.length; index++)
      {
        'label': labels[index],
        'type': 'stock',
        'ticker': questionNumber == 1 && index == 0
            ? '3099.T'
            : '${1000 + questionNumber * 10 + index}.T',
        'companyName': 'テスト銘柄${index + 1}',
        'returnRate': index == 1 ? 10.0 : index.toDouble(),
        'candles': <dynamic>[],
        'resultCandles': [
          {
            'date': baseDate,
            'open': 100,
            'high': 110,
            'low': 90,
            'close': 100,
            'volume': 1000,
          },
          {
            'date': evaluationDate,
            'open': 100,
            'high': 120,
            'low': 95,
            'close': 110,
            'volume': 1200,
          },
        ],
      },
    {
      'label': '現金保有',
      'type': 'cash',
      'returnRate': 0.0,
      'candles': <dynamic>[],
    },
  ];
  return http.Response(
    jsonEncode({
      'currentNumber': questionNumber,
      'totalQuestions': 3,
      'baseDate': baseDate,
      'evaluationDate': evaluationDate,
      'choices': choices,
      'correctChoiceLabel': correctLabels[questionNumber - 1],
    }),
    200,
    headers: {'content-type': 'application/json; charset=utf-8'},
  );
}
