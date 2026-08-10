import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';

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
  Future<void> shareResultImage(
    Uint8List imageBytes,
    String text,
    Rect? origin,
  );
}

class PlatformResultShareService implements ResultShareService {
  const PlatformResultShareService();

  @override
  Future<void> shareResultImage(
    Uint8List imageBytes,
    String text,
    Rect? origin,
  ) async {
    await SharePlus.instance.share(
      ShareParams(
        files: [
          XFile.fromData(
            imageBytes,
            mimeType: 'image/png',
            name: 'stock-trainer-result.png',
          ),
        ],
        text: text,
        title: 'Stock Trainerの結果',
        sharePositionOrigin: origin,
      ),
    );
  }
}
