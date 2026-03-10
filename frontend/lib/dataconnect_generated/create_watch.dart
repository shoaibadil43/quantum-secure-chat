part of 'generated.dart';

class CreateWatchVariablesBuilder {
  String movieId;
  DateTime watchDate;
  Optional<String> _location = Optional.optional(nativeFromJson, nativeToJson);

  final FirebaseDataConnect _dataConnect;  CreateWatchVariablesBuilder location(String? t) {
   _location.value = t;
   return this;
  }

  CreateWatchVariablesBuilder(this._dataConnect, {required  this.movieId,required  this.watchDate,});
  Deserializer<CreateWatchData> dataDeserializer = (dynamic json)  => CreateWatchData.fromJson(jsonDecode(json));
  Serializer<CreateWatchVariables> varsSerializer = (CreateWatchVariables vars) => jsonEncode(vars.toJson());
  Future<OperationResult<CreateWatchData, CreateWatchVariables>> execute() {
    return ref().execute();
  }

  MutationRef<CreateWatchData, CreateWatchVariables> ref() {
    CreateWatchVariables vars= CreateWatchVariables(movieId: movieId,watchDate: watchDate,location: _location,);
    return _dataConnect.mutation("CreateWatch", dataDeserializer, varsSerializer, vars);
  }
}

@immutable
class CreateWatchWatchInsert {
  final String id;
  CreateWatchWatchInsert.fromJson(dynamic json):
  
  id = nativeFromJson<String>(json['id']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final CreateWatchWatchInsert otherTyped = other as CreateWatchWatchInsert;
    return id == otherTyped.id;
    
  }
  @override
  int get hashCode => id.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['id'] = nativeToJson<String>(id);
    return json;
  }

  CreateWatchWatchInsert({
    required this.id,
  });
}

@immutable
class CreateWatchData {
  final CreateWatchWatchInsert watch_insert;
  CreateWatchData.fromJson(dynamic json):
  
  watch_insert = CreateWatchWatchInsert.fromJson(json['watch_insert']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final CreateWatchData otherTyped = other as CreateWatchData;
    return watch_insert == otherTyped.watch_insert;
    
  }
  @override
  int get hashCode => watch_insert.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['watch_insert'] = watch_insert.toJson();
    return json;
  }

  CreateWatchData({
    required this.watch_insert,
  });
}

@immutable
class CreateWatchVariables {
  final String movieId;
  final DateTime watchDate;
  late final Optional<String>location;
  @Deprecated('fromJson is deprecated for Variable classes as they are no longer required for deserialization.')
  CreateWatchVariables.fromJson(Map<String, dynamic> json):
  
  movieId = nativeFromJson<String>(json['movieId']),
  watchDate = nativeFromJson<DateTime>(json['watchDate']) {
  
  
  
  
    location = Optional.optional(nativeFromJson, nativeToJson);
    location.value = json['location'] == null ? null : nativeFromJson<String>(json['location']);
  
  }
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final CreateWatchVariables otherTyped = other as CreateWatchVariables;
    return movieId == otherTyped.movieId && 
    watchDate == otherTyped.watchDate && 
    location == otherTyped.location;
    
  }
  @override
  int get hashCode => Object.hashAll([movieId.hashCode, watchDate.hashCode, location.hashCode]);
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['movieId'] = nativeToJson<String>(movieId);
    json['watchDate'] = nativeToJson<DateTime>(watchDate);
    if(location.state == OptionalState.set) {
      json['location'] = location.toJson();
    }
    return json;
  }

  CreateWatchVariables({
    required this.movieId,
    required this.watchDate,
    required this.location,
  });
}

