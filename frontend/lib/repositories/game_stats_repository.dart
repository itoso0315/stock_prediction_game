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
  static const _bestCorrectCountKey = 'game_stats.best_correct_count';
  static const _bestCorrectRateKey = 'game_stats.best_correct_rate';
  static const _totalCorrectCountKey = 'game_stats.total_correct_count';
  static const _totalQuestionCountKey = 'game_stats.total_question_count';

  @override
  Future<GameStats> load() async {
    final preferences = SharedPreferencesAsync();
    final values = await Future.wait([
      preferences.getInt(_challengeCountKey),
      preferences.getInt(_bestCorrectCountKey),
      preferences.getInt(_bestCorrectRateKey),
      preferences.getInt(_totalCorrectCountKey),
      preferences.getInt(_totalQuestionCountKey),
    ]);
    return GameStats(
      challengeCount: values[0] ?? 0,
      bestCorrectCount: values[1] ?? 0,
      bestCorrectRate: values[2] ?? 0,
      totalCorrectCount: values[3] ?? 0,
      totalQuestionCount: values[4] ?? 0,
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
    final correctRate = (correctCount / totalQuestions * 100).floor();
    final updated = GameStats(
      challengeCount: previous.challengeCount + 1,
      bestCorrectCount: correctCount > previous.bestCorrectCount
          ? correctCount
          : previous.bestCorrectCount,
      bestCorrectRate: correctRate > previous.bestCorrectRate
          ? correctRate
          : previous.bestCorrectRate,
      totalCorrectCount: previous.totalCorrectCount + correctCount,
      totalQuestionCount: previous.totalQuestionCount + totalQuestions,
    );
    final preferences = SharedPreferencesAsync();
    await Future.wait([
      preferences.setInt(_challengeCountKey, updated.challengeCount),
      preferences.setInt(_bestCorrectCountKey, updated.bestCorrectCount),
      preferences.setInt(_bestCorrectRateKey, updated.bestCorrectRate),
      preferences.setInt(_totalCorrectCountKey, updated.totalCorrectCount),
      preferences.setInt(_totalQuestionCountKey, updated.totalQuestionCount),
    ]);
    return updated;
  }
}
