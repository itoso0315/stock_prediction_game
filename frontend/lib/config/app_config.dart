class AppConfig {
  const AppConfig._();

  static const defaultApiBaseUrl =
      'https://stock-prediction-game-api.onrender.com';

  static const apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: defaultApiBaseUrl,
  );
}
