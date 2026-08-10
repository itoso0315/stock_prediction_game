import 'candle.dart';
import 'moving_average_point.dart';

enum AnswerType {
  stock,
  cash;

  factory AnswerType.fromJson(String value) {
    switch (value) {
      case 'stock':
        return AnswerType.stock;
      case 'cash':
        return AnswerType.cash;
      default:
        throw ArgumentError('Unknown answer type: $value');
    }
  }
}

class Answer {
  const Answer({
    required this.label,
    required this.type,
    this.ticker,
    this.companyName,
    this.yahooFinanceUrl,
    this.baseClose,
    this.evaluationClose,
    this.returnRate,
    this.candles = const [],
    this.ma20 = const [],
    this.ma40 = const [],
    this.ma70 = const [],
    this.resultCandles = const [],
  });

  factory Answer.fromJson(Map<String, dynamic> json) {
    return Answer(
      label: json['label'] as String,
      type: AnswerType.fromJson(json['type'] as String),
      ticker: json['ticker'] as String?,
      companyName: json['companyName'] as String?,
      yahooFinanceUrl: json['yahooFinanceUrl'] as String?,
      baseClose: (json['baseClose'] as num?)?.toDouble(),
      evaluationClose: (json['evaluationClose'] as num?)?.toDouble(),
      returnRate: (json['returnRate'] as num?)?.toDouble(),
      candles:
          (json['candles'] as List<dynamic>?)
              ?.map((e) => Candle.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      ma20: _movingAverageFromJson(json['ma20']),
      ma40: _movingAverageFromJson(json['ma40']),
      ma70: _movingAverageFromJson(json['ma70']),
      resultCandles:
          (json['resultCandles'] as List<dynamic>?)
              ?.map((item) => Candle.fromJson(item as Map<String, dynamic>))
              .toList(growable: false) ??
          const [],
    );
  }

  final String label;
  final AnswerType type;
  final String? ticker;
  final String? companyName;
  final String? yahooFinanceUrl;
  final double? baseClose;
  final double? evaluationClose;
  final double? returnRate;
  final List<Candle> candles;
  final List<MovingAveragePoint> ma20;
  final List<MovingAveragePoint> ma40;
  final List<MovingAveragePoint> ma70;
  final List<Candle> resultCandles;

  bool get isStock => type == AnswerType.stock;
  bool get isCash => type == AnswerType.cash;

  Uri? get yahooFinanceUri {
    final configuredUrl = yahooFinanceUrl;
    if (configuredUrl != null && configuredUrl.isNotEmpty) {
      return Uri.tryParse(configuredUrl);
    }
    final stockTicker = ticker;
    if (!isStock || stockTicker == null || stockTicker.isEmpty) return null;
    return Uri.https(
      'finance.yahoo.co.jp',
      '/quote/${Uri.encodeComponent(stockTicker)}/chart',
    );
  }
}

List<MovingAveragePoint> _movingAverageFromJson(dynamic value) {
  if (value is! List) return const [];
  return value
      .map(
        (point) => MovingAveragePoint.fromJson(
          Map<String, dynamic>.from(point as Map),
        ),
      )
      .toList(growable: false);
}
