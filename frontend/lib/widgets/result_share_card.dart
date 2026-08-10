import 'package:flutter/material.dart';

class ResultAchievement {
  const ResultAchievement({required this.label, required this.message});

  final String label;
  final String message;
}

ResultAchievement resultAchievementFor(int correctCount) {
  if (correctCount >= 10) {
    return const ResultAchievement(
      label: 'MARKET STRUCTURE',
      message: '相場構造を捉えています',
    );
  }
  if (correctCount >= 7) {
    return const ResultAchievement(
      label: 'PRICE ACTION',
      message: '値動きの文脈が読めています',
    );
  }
  if (correctCount >= 4) {
    return const ResultAchievement(
      label: 'TREND AWARE',
      message: 'トレンドを認識できています',
    );
  }
  return const ResultAchievement(label: 'CHART OBSERVER', message: '観察眼を育成中です');
}

class ResultShareCard extends StatelessWidget {
  const ResultShareCard({
    super.key,
    required this.correctCount,
    required this.totalQuestions,
  });

  final int correctCount;
  final int totalQuestions;

  @override
  Widget build(BuildContext context) {
    final achievement = resultAchievementFor(correctCount);
    final correctRate = totalQuestions == 0
        ? 0
        : (correctCount / totalQuestions * 100).floor();

    return AspectRatio(
      aspectRatio: 1,
      child: Container(
        key: const ValueKey('result-share-card'),
        decoration: BoxDecoration(
          gradient: const RadialGradient(
            center: Alignment.topLeft,
            radius: 1.45,
            colors: [Color(0xFF25282A), Color(0xFF090A0B)],
          ),
          border: Border.all(color: const Color(0xFF3A3325)),
        ),
        child: Stack(
          children: [
            const Positioned.fill(child: CustomPaint(painter: _ChartPainter())),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 24),
              child: FittedBox(
                fit: BoxFit.scaleDown,
                child: SizedBox(
                  width: 420,
                  height: 460,
                  child: Column(
                    children: [
                      Image.asset(
                        'assets/app_icon_master.png',
                        width: 72,
                        height: 72,
                      ),
                      const SizedBox(height: 10),
                      const Text(
                        'S T O C K   T R A I N E R',
                        style: TextStyle(
                          color: Color(0xFFC8A96B),
                          fontSize: 14,
                          letterSpacing: 2.2,
                        ),
                      ),
                      const SizedBox(height: 22),
                      const _GoldDivider(),
                      const Spacer(),
                      Text.rich(
                        TextSpan(
                          children: [
                            TextSpan(
                              text: '$correctCount',
                              style: const TextStyle(color: Color(0xFF42E5AC)),
                            ),
                            TextSpan(text: ' / $totalQuestions'),
                          ],
                        ),
                        style: const TextStyle(
                          color: Color(0xFFF6F3EC),
                          fontSize: 72,
                          fontWeight: FontWeight.w300,
                          height: 1,
                        ),
                      ),
                      const SizedBox(height: 14),
                      Text(
                        '正答率 $correctRate%',
                        style: const TextStyle(
                          color: Color(0xFFE7E1D1),
                          fontSize: 21,
                          letterSpacing: 1,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        achievement.label,
                        style: const TextStyle(
                          color: Color(0xFFC8A96B),
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          letterSpacing: 2.4,
                        ),
                      ),
                      const SizedBox(height: 9),
                      Text(
                        achievement.message,
                        style: const TextStyle(
                          color: Color(0xFFF6F3EC),
                          fontSize: 24,
                          fontWeight: FontWeight.w500,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 22),
                      const _GoldDivider(),
                      const SizedBox(height: 18),
                      const Text(
                        '#StockTrainer',
                        style: TextStyle(
                          color: Color(0xFFB8A47A),
                          fontSize: 14,
                          letterSpacing: 1.2,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _GoldDivider extends StatelessWidget {
  const _GoldDivider();

  @override
  Widget build(BuildContext context) {
    return Container(height: 1, color: const Color(0xFF8D7446));
  }
}

class _ChartPainter extends CustomPainter {
  const _ChartPainter();

  @override
  void paint(Canvas canvas, Size size) {
    final gridPaint = Paint()
      ..color = const Color(0xFF53605B).withAlpha(18)
      ..strokeWidth = 1;
    for (var index = 1; index < 5; index++) {
      final offset = size.width * index / 5;
      canvas.drawLine(
        Offset(offset, 0),
        Offset(offset, size.height),
        gridPaint,
      );
      canvas.drawLine(Offset(0, offset), Offset(size.width, offset), gridPaint);
    }

    final candlePaint = Paint()..color = const Color(0xFF82918A).withAlpha(28);
    const values = [0.72, 0.64, 0.68, 0.52, 0.57, 0.42, 0.34, 0.25];
    final step = size.width / (values.length + 1);
    for (var index = 0; index < values.length; index++) {
      final x = step * (index + 1);
      final centerY = size.height * values[index];
      canvas.drawLine(
        Offset(x, centerY - size.height * 0.07),
        Offset(x, centerY + size.height * 0.07),
        candlePaint,
      );
      canvas.drawRect(
        Rect.fromCenter(
          center: Offset(x, centerY),
          width: size.width * 0.025,
          height: size.height * 0.075,
        ),
        candlePaint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
