class MovingAveragePoint {
  const MovingAveragePoint({required this.date, required this.value});

  factory MovingAveragePoint.fromJson(Map<String, dynamic> json) {
    return MovingAveragePoint(
      date: json['date'] as String,
      value: (json['value'] as num).toDouble(),
    );
  }

  final String date;
  final double value;
}
