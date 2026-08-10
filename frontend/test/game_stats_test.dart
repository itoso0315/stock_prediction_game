import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences_platform_interface/in_memory_shared_preferences_async.dart';
import 'package:shared_preferences_platform_interface/shared_preferences_async_platform_interface.dart';
import 'package:stock_trainer_flutter/main.dart';
import 'package:stock_trainer_flutter/models/answer.dart';
import 'package:stock_trainer_flutter/models/answer_record.dart';
import 'package:stock_trainer_flutter/models/game_stats.dart';
import 'package:stock_trainer_flutter/models/question.dart';
import 'package:stock_trainer_flutter/repositories/game_stats_repository.dart';
import 'package:stock_trainer_flutter/screens/result_screen.dart';

void main() {
  test('完了したゲームから挑戦回数・平均正答率を保存する', () async {
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
    const repository = LocalGameStatsRepository();

    await repository.recordGame(correctCount: 4, totalQuestions: 10);
    final stats = await repository.recordGame(
      correctCount: 7,
      totalQuestions: 10,
    );

    expect(stats.challengeCount, 2);
    expect(stats.averageCorrectRate, 55);
  });

  testWidgets('トップ画面に過去の成績指標を表示する', (tester) async {
    final repository = _FakeStatsRepository(
      const GameStats(
        challengeCount: 8,
        totalCorrectCount: 42,
        totalQuestionCount: 80,
      ),
    );
    await tester.pumpWidget(StockTrainerApp(gameStatsRepository: repository));
    await tester.pumpAndSettle();

    expect(find.text('これまでの記録'), findsOneWidget);
    expect(find.text('最高正答率'), findsNothing);
    expect(find.text('最高正解数'), findsNothing);
    expect(find.text('挑戦回数'), findsOneWidget);
    expect(find.text('8回'), findsOneWidget);
    expect(find.text('平均正答率'), findsOneWidget);
    expect(find.text('52%'), findsOneWidget);
  });

  testWidgets('最終Result表示時にゲーム結果を一度記録する', (tester) async {
    final repository = _FakeStatsRepository(const GameStats());
    await tester.pumpWidget(
      MaterialApp(
        home: ResultScreen(
          answerRecords: const [
            AnswerRecord(questionNumber: 1, selectedAnswerLabel: 'Chart A'),
          ],
          questions: const [
            Question(
              currentNumber: 1,
              totalQuestions: 1,
              chartLabels: ['Chart A'],
              answers: [Answer(label: 'Chart A', type: AnswerType.stock)],
              correctAnswerLabel: 'Chart A',
            ),
          ],
          gameStatsRepository: repository,
        ),
      ),
    );
    await tester.pump();

    expect(repository.recordCalls, 1);
    expect(repository.lastCorrectCount, 1);
    expect(repository.lastTotalQuestions, 1);
  });
}

class _FakeStatsRepository implements GameStatsRepository {
  _FakeStatsRepository(this.stats);

  GameStats stats;
  int recordCalls = 0;
  int? lastCorrectCount;
  int? lastTotalQuestions;

  @override
  Future<GameStats> load() async => stats;

  @override
  Future<GameStats> recordGame({
    required int correctCount,
    required int totalQuestions,
  }) async {
    recordCalls++;
    lastCorrectCount = correctCount;
    lastTotalQuestions = totalQuestions;
    return stats;
  }
}
