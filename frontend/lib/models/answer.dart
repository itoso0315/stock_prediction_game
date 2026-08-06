enum AnswerType { stock, cash }

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
