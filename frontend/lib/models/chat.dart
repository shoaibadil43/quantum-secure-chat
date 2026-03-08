import 'package:json_annotation/json_annotation.dart';

part 'chat.g.dart';

@JsonSerializable()
class ChatSession {
  final String id;
  final String ownerId;
  final String name;
  final String? description;
  final bool isGroup;
  final bool isEncrypted;
  final DateTime createdAt;
  final DateTime updatedAt;

  ChatSession({
    required this.id,
    required this.ownerId,
    required this.name,
    this.description,
    required this.isGroup,
    required this.isEncrypted,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ChatSession.fromJson(Map<String, dynamic> json) => _$ChatSessionFromJson(json);
  Map<String, dynamic> toJson() => _$ChatSessionToJson(this);

  @override
  String toString() => 'ChatSession($id: $name)';
}
