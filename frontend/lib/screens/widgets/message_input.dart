import 'package:flutter/material.dart';

/// Message Input Widget - WhatsApp Style
class MessageInput extends StatefulWidget {
  final TextEditingController controller;
  final VoidCallback onSend;
  final VoidCallback onTyping;
  final VoidCallback onStopTyping;
  final bool isLoading;

  const MessageInput({
    Key? key,
    required this.controller,
    required this.onSend,
    required this.onTyping,
    required this.onStopTyping,
    this.isLoading = false,
  }) : super(key: key);

  @override
  State<MessageInput> createState() => _MessageInputState();
}

class _MessageInputState extends State<MessageInput> {
  bool _isTyping = false;

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      decoration: BoxDecoration(
        border: Border(
          top: BorderSide(
            color: isDarkMode ? Colors.grey[800]! : Colors.grey[300]!,
            width: 0.5,
          ),
        ),
      ),
      child: Row(
        children: [
          // Emoji Button
          IconButton(
            onPressed: () {
              // TODO: Show emoji picker
            },
            icon: const Icon(Icons.emoji_emotions_outlined),
            color: Theme.of(context).primaryColor,
          ),
          // Message Input Field
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                color: isDarkMode ? const Color(0xFF1E272C) : Colors.grey[100],
                borderRadius: BorderRadius.circular(24),
              ),
              child: TextField(
                controller: widget.controller,
                maxLines: null,
                minLines: 1,
                maxLength: 4096,
                onChanged: (value) {
                  if (value.isNotEmpty && !_isTyping) {
                    setState(() => _isTyping = true);
                    widget.onTyping();
                  } else if (value.isEmpty && _isTyping) {
                    setState(() => _isTyping = false);
                    widget.onStopTyping();
                  }
                },
                decoration: InputDecoration(
                  hintText: 'Message',
                  hintStyle: TextStyle(
                    color: isDarkMode ? Colors.grey[500] : Colors.grey[600],
                  ),
                  border: InputBorder.none,
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                  counterText: '',
                ),
                style: TextStyle(
                  color: isDarkMode ? Colors.white : Colors.black87,
                ),
              ),
            ),
          ),
          const SizedBox(width: 4),
          // Attachment Button (if message is empty)
          if (widget.controller.text.isEmpty)
            IconButton(
              onPressed: () {
                // TODO: Show attachment options
              },
              icon: const Icon(Icons.attachment),
              color: Theme.of(context).primaryColor,
            ),
          // Send Button
          IconButton(
            onPressed: widget.isLoading
                ? null
                : () {
                    if (widget.controller.text.isNotEmpty) {
                      widget.onSend();
                      setState(() => _isTyping = false);
                    }
                  },
            icon: Icon(
              widget.controller.text.isEmpty ? Icons.mic : Icons.send,
              color: Theme.of(context).primaryColor,
            ),
            iconSize: 22,
          ),
        ],
      ),
    );
  }
}
