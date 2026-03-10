part of 'generated.dart';

class MyListsVariablesBuilder {
  
  final FirebaseDataConnect _dataConnect;
  MyListsVariablesBuilder(this._dataConnect, );
  Deserializer<MyListsData> dataDeserializer = (dynamic json)  => MyListsData.fromJson(jsonDecode(json));
  
  Future<QueryResult<MyListsData, void>> execute() {
    return ref().execute();
  }

  QueryRef<MyListsData, void> ref() {
    
    return _dataConnect.query("MyLists", dataDeserializer, emptySerializer, null);
  }
}

@immutable
class MyListsLists {
  final String id;
  final String name;
  final bool public;
  final Timestamp createdAt;
  final Timestamp updatedAt;
  final String? description;
  MyListsLists.fromJson(dynamic json):
  
  id = nativeFromJson<String>(json['id']),
  name = nativeFromJson<String>(json['name']),
  public = nativeFromJson<bool>(json['public']),
  createdAt = Timestamp.fromJson(json['createdAt']),
  updatedAt = Timestamp.fromJson(json['updatedAt']),
  description = json['description'] == null ? null : nativeFromJson<String>(json['description']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final MyListsLists otherTyped = other as MyListsLists;
    return id == otherTyped.id && 
    name == otherTyped.name && 
    public == otherTyped.public && 
    createdAt == otherTyped.createdAt && 
    updatedAt == otherTyped.updatedAt && 
    description == otherTyped.description;
    
  }
  @override
  int get hashCode => Object.hashAll([id.hashCode, name.hashCode, public.hashCode, createdAt.hashCode, updatedAt.hashCode, description.hashCode]);
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['id'] = nativeToJson<String>(id);
    json['name'] = nativeToJson<String>(name);
    json['public'] = nativeToJson<bool>(public);
    json['createdAt'] = createdAt.toJson();
    json['updatedAt'] = updatedAt.toJson();
    if (description != null) {
      json['description'] = nativeToJson<String?>(description);
    }
    return json;
  }

  MyListsLists({
    required this.id,
    required this.name,
    required this.public,
    required this.createdAt,
    required this.updatedAt,
    this.description,
  });
}

@immutable
class MyListsData {
  final List<MyListsLists> lists;
  MyListsData.fromJson(dynamic json):
  
  lists = (json['lists'] as List<dynamic>)
        .map((e) => MyListsLists.fromJson(e))
        .toList();
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final MyListsData otherTyped = other as MyListsData;
    return lists == otherTyped.lists;
    
  }
  @override
  int get hashCode => lists.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['lists'] = lists.map((e) => e.toJson()).toList();
    return json;
  }

  MyListsData({
    required this.lists,
  });
}

