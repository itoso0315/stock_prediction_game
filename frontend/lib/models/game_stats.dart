class GameStats {
  const GameStats({
    this.challengeCount = 0,
    this.bestCorrectCount = 0,
    this.bestCorrectRate = 0,
    this.totalCorrectCount = 0,
    this.totalQuestionCount = 0,
  });

  final int challengeCount;
  final int bestCorrectCount;
  final int bestCorrectRate;
  final int totalCorrectCount;
  final int totalQuestionCount;

  int get averageCorrectRate => totalQuestionCount == 0
      ? 0
      : (totalCorrectCount / totalQuestionCount * 100).floor();
}
