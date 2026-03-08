import 'package:flutter/material.dart';

/// Typing Indicator Widget
class TypingIndicator extends StatefulWidget {
  final String userName;
  final Color? color;

  const TypingIndicator({
    Key? key,
    required this.userName,
    this.color,
  }) : super(key: key);

  @override
  State<TypingIndicator> createState() => _TypingIndicatorState();
}

class _TypingIndicatorState extends State<TypingIndicator> with TickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 600),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            '${widget.userName} is typing...',
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey[600],
              fontStyle: FontStyle.italic,
            ),
          ),
          SizedBox(height: 4),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: List.generate(3, (index) {
              return Padding(
                padding: EdgeInsets.symmetric(horizontal: 2),
                child: ScaleTransition(
                  scale: Tween<double>(begin: 0.8, end: 1.2).animate(
                    CurvedAnimation(
                      parent: _controller,
                      curve: Interval(
                        index * 0.15,
                        min(0.6, (index + 1) * 0.15),
                        curve: Curves.easeInOut,
                      ),
                    ),
                  ),
                  child: CircleAvatar(
                    radius: 3,
                    backgroundColor: widget.color ?? Color(0xFF42A5F5),
                  ),
                ),
              );
            }),
          ),
        ],
      ),
    );
  }
}

double min(double a, double b) => a < b ? a : b;
