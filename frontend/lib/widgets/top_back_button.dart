import 'package:flutter/material.dart';

class TopBackButton extends StatelessWidget {
  const TopBackButton({super.key, this.onPressed});

  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return TextButton.icon(
      key: const ValueKey('top-back-button'),
      onPressed:
          onPressed ??
          () => Navigator.of(context).popUntil((route) => route.isFirst),
      icon: const Icon(Icons.chevron_left, size: 22),
      label: const Text('Topに戻る'),
      style: TextButton.styleFrom(
        padding: const EdgeInsets.only(left: 4, right: 4),
      ),
    );
  }
}
