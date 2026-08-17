import 'package:flutter_test/flutter_test.dart';
import 'package:stock_trainer_flutter/config/app_config.dart';

void main() {
  test('has the production API URL as its default', () {
    expect(
      AppConfig.defaultApiBaseUrl,
      'https://stock-prediction-game-api.onrender.com',
    );
  });

  test('allows API_BASE_URL to override the production default', () {
    const override = String.fromEnvironment('API_BASE_URL');
    const hasOverride = bool.hasEnvironment('API_BASE_URL');

    expect(
      AppConfig.apiBaseUrl,
      hasOverride ? override : AppConfig.defaultApiBaseUrl,
    );
  });
}
