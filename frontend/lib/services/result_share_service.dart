import 'package:flutter/services.dart';
import 'package:share_plus/share_plus.dart';
import 'package:url_launcher/url_launcher.dart';

const stockTrainerShareUrl =
    'https://github.com/itoso0315/stock_prediction_game';

String buildResultShareText({
  required int correctCount,
  required int totalQuestions,
  required int correctRate,
}) {
  return 'Stock Trainerで$totalQuestions問中$correctCount問正解！\n'
      '正答率$correctRate%でした📈\n\n'
      '#StockTrainer\n'
      '$stockTrainerShareUrl';
}

abstract interface class ResultShareService {
  Future<void> shareToX(String text);

  Future<void> shareToInstagram(String text, Rect? origin);

  Future<void> shareToLine(String text);

  Future<void> copyShareUrl();
}

class PlatformResultShareService implements ResultShareService {
  const PlatformResultShareService();

  @override
  Future<void> shareToX(String text) async {
    final uri = Uri.https('twitter.com', '/intent/tweet', {'text': text});
    await _launch(uri);
  }

  @override
  Future<void> shareToInstagram(String text, Rect? origin) async {
    await SharePlus.instance.share(
      ShareParams(
        text: text,
        title: 'Stock Trainerの結果',
        sharePositionOrigin: origin,
      ),
    );
  }

  @override
  Future<void> shareToLine(String text) async {
    final uri = Uri.https('social-plugins.line.me', '/lineit/share', {
      'url': stockTrainerShareUrl,
      'text': text,
    });
    await _launch(uri);
  }

  @override
  Future<void> copyShareUrl() {
    return Clipboard.setData(const ClipboardData(text: stockTrainerShareUrl));
  }

  Future<void> _launch(Uri uri) async {
    final launched = await launchUrl(uri, mode: LaunchMode.externalApplication);
    if (!launched) {
      throw StateError('共有先を開けませんでした。');
    }
  }
}
