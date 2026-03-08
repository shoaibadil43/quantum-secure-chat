import 'package:flutter/material.dart';
import '../widgets/message_bubble.dart';
import '../widgets/typing_indicator.dart';
import '../widgets/message_input.dart';

/// Conversation Screen - WhatsApp Style
class ConversationScreen extends StatefulWidget {
  final String roomId;

  const ConversationScreen({
    Key? key,
    required this.roomId,
  }) : super(key: key);

  @override
  State<ConversationScreen> createState() => _ConversationScreenState();
}

class _ConversationScreenState extends State<ConversationScreen> {
  final messageController = TextEditingController();
  final List<_MessageItem> messages = [];
  bool _isTypingVisible = false;
  String _typingUser = '';
  bool _isLoading = false;
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _loadMessages();
  }

  @override
  void dispose() {
    messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _loadMessages() {
    setState(() {
      messages.addAll([
        _MessageItem(
          id: '1',
          content: 'Hey! Welcome to Quantum Secure Chat',
          isCurrentUser: false,
          timestamp: DateTime.now().subtract(const Duration(minutes: 5)),
          isRead: true,
        ),
        _MessageItem(
          id: '2',
          content: 'Thanks! Excited to test out the end-to-end encryption',
          isCurrentUser: true,
          timestamp: DateTime.now().subtract(const Duration(minutes: 4)),
          isRead: true,
        ),
        _MessageItem(
          id: '3',
          content: 'Your messages are completely secure and private 🔐',
          isCurrentUser: false,
          timestamp: DateTime.now().subtract(const Duration(minutes: 3)),
          isRead: true,
        ),
      ]);
    });
    _scrollDown();
  }

  void _sendMessage() {
    if (messageController.text.isEmpty) return;

    setState(() {
      messages.add(
        _MessageItem(
          id: DateTime.now().toString(),
          content: messageController.text,
          isCurrentUser: true,
          timestamp: DateTime.now(),
          isRead: false,
        ),
      );
    });

    messageController.clear();
    _scrollDown();
  }

  void _scrollDown() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('John Doe'),
            Text(
              'Active now',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Colors.white70,
                fontSize: 12,
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.call),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Call feature coming soon!')),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.videocam),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Video call feature coming soon!')),
              );
            },
          ),
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'key') {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Generating quantum key...')),
                );
              }
            },
            itemBuilder: (BuildContext context) => [
              const PopupMenuItem(
                value: 'key',
                child: Row(
                  children: [
                    Icon(Icons.vpn_key, size: 20),
                    SizedBox(width: 12),
                    Text('Generate Quantum Key'),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'info',
                child: Row(
                  children: [
                    Icon(Icons.info, size: 20),
                    SizedBox(width: 12),
                    Text('Chat Info'),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: messages.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.lock_outline,
                          size: 64,
                          color: Colors.grey.withOpacity(0.5),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Secured with End-to-End Encryption',
                          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    controller: _scrollController,
                    reverse: false,
                    itemCount: messages.length + (_isTypingVisible ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == messages.length && _isTypingVisible) {
                        return TypingIndicator(
                          userName: _typingUser,
                          color: Theme.of(context).primaryColor,
                        );
                      }

                      final message = messages[index];

                      return MessageBubble(
                        content: message.content,
                        isCurrentUser: message.isCurrentUser,
                        timestamp: message.timestamp,
                        isRead: message.isRead,
                      );
                    },
                  ),
          ),
          MessageInput(
            controller: messageController,
            onSend: _sendMessage,
            onTyping: () {
              // TODO: Send typing indicator to server
            },
            onStopTyping: () {
              // TODO: Send stop typing to server
            },
            isLoading: _isLoading,
          ),
        ],
      ),
    );
  }
}

/// Internal message item class
class _MessageItem {
  final String id;
  final String content;
  final bool isCurrentUser;
  final DateTime timestamp;
  final bool isRead;

  _MessageItem({
    required this.id,
    required this.content,
    required this.isCurrentUser,
    required this.timestamp,
    required this.isRead,
  });
}
