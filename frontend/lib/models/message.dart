import 'package:json_annotation/json_annotation.dart';

part 'message.g.dart';

@JsonSerializable()
class Message {
  final String id;
  final String senderId;
  final String sessionId;
  final String content;
  final String? encryptedContent;
  final bool isDelivered;
  final bool isRead;
  final DateTime createdAt;
  final String? senderUsername;

  Message({
    required this.id,
    required this.senderId,
    required this.sessionId,
    required this.content,
    this.encryptedContent,
    required this.isDelivered,
    required this.isRead,
    required this.createdAt,
    this.senderUsername,
  });

  factory Message.fromJson(Map<String, dynamic> json) => _$MessageFromJson(json);
  Map<String, dynamic> toJson() => _$MessageToJson(this);

  @override
  String toString() => 'Message($id from $senderId)';
}
