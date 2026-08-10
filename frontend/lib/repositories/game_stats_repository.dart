import 'package:shared_preferences/shared_preferences.dart';

import '../models/game_stats.dart';

abstract interface class GameStatsRepository {
  Future<GameStats> load();

  Future<GameStats> recordGame({
    required int correctCount,
    required int totalQuestions,
  });
}

class LocalGameStatsRepository implements GameStatsRepository {
  const LocalGameStatsRepository();

  static const _challengeCountKey = 'game_stats.challenge_count';
  static const _totalCorrectCountKey = 'game_stats.total_correct_count';
  static const _totalQuestionCountKey = 'game_stats.total_question_count';

  @override
  Future<GameStats> load() async {
    final preferences = SharedPreferencesAsync();
    final values = await Future.wait([
      preferences.getInt(_challengeCountKey),
      preferences.getInt(_totalCorrectCountKey),
      preferences.getInt(_totalQuestionCountKey),
    ]);
    return GameStats(
      challengeCount: values[0] ?? 0,
      totalCorrectCount: values[1] ?? 0,
      totalQuestionCount: values[2] ?? 0,
    );
  }

  @override
  Future<GameStats> recordGame({
    required int correctCount,
    required int totalQuestions,
  }) async {
    if (totalQuestions <= 0 ||
        correctCount < 0 ||
        correctCount > totalQuestions) {
      throw ArgumentError('ゲーム結果が不正です。');
    }

    final previous = await load();
    final updated = GameStats(
      challengeCount: previous.challengeCount + 1,
      totalCorrectCount: previous.totalCorrectCount + correctCount,
      totalQuestionCount: previous.totalQuestionCount + totalQuestions,
    );
    final preferences = SharedPreferencesAsync();
    await Future.wait([
      preferences.setInt(_challengeCountKey, updated.challengeCount),
      preferences.setInt(_totalCorrectCountKey, updated.totalCorrectCount),
      preferences.setInt(_totalQuestionCountKey, updated.totalQuestionCount),
    ]);
    return updated;
  }
}
