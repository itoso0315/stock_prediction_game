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
    this.baseClose,
    this.evaluationClose,
    this.returnRate,
  });

  factory Answer.fromJson(Map<String, dynamic> json) {
    return Answer(
      label: json['label'] as String,
      type: AnswerType.fromJson(json['type'] as String),
      ticker: json['ticker'] as String?,
      companyName: json['companyName'] as String?,
      baseClose: (json['baseClose'] as num?)?.toDouble(),
      evaluationClose: (json['evaluationClose'] as num?)?.toDouble(),
      returnRate: (json['returnRate'] as num?)?.toDouble(),
    );
  }

  final String label;
  final AnswerType type;
  final String? ticker;
  final String? companyName;
  final double? baseClose;
  final double? evaluationClose;
  final double? returnRate;

  bool get isStock => type == AnswerType.stock;
  bool get isCash => type == AnswerType.cash;
}
