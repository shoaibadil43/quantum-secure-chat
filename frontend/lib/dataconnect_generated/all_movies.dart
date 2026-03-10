part of 'generated.dart';

class AllMoviesVariablesBuilder {
  
  final FirebaseDataConnect _dataConnect;
  AllMoviesVariablesBuilder(this._dataConnect, );
  Deserializer<AllMoviesData> dataDeserializer = (dynamic json)  => AllMoviesData.fromJson(jsonDecode(json));
  
  Future<QueryResult<AllMoviesData, void>> execute() {
    return ref().execute();
  }

  QueryRef<AllMoviesData, void> ref() {
    
    return _dataConnect.query("AllMovies", dataDeserializer, emptySerializer, null);
  }
}

@immutable
class AllMoviesMovies {
  final String id;
  final String title;
  final int year;
  final List<String>? genres;
  final int? runtime;
  final String? summary;
  AllMoviesMovies.fromJson(dynamic json):
  
  id = nativeFromJson<String>(json['id']),
  title = nativeFromJson<String>(json['title']),
  year = nativeFromJson<int>(json['year']),
  genres = json['genres'] == null ? null : (json['genres'] as List<dynamic>)
        .map((e) => nativeFromJson<String>(e))
        .toList(),
  runtime = json['runtime'] == null ? null : nativeFromJson<int>(json['runtime']),
  summary = json['summary'] == null ? null : nativeFromJson<String>(json['summary']);
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final AllMoviesMovies otherTyped = other as AllMoviesMovies;
    return id == otherTyped.id && 
    title == otherTyped.title && 
    year == otherTyped.year && 
    genres == otherTyped.genres && 
    runtime == otherTyped.runtime && 
    summary == otherTyped.summary;
    
  }
  @override
  int get hashCode => Object.hashAll([id.hashCode, title.hashCode, year.hashCode, genres.hashCode, runtime.hashCode, summary.hashCode]);
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['id'] = nativeToJson<String>(id);
    json['title'] = nativeToJson<String>(title);
    json['year'] = nativeToJson<int>(year);
    if (genres != null) {
      json['genres'] = genres?.map((e) => nativeToJson<String>(e)).toList();
    }
    if (runtime != null) {
      json['runtime'] = nativeToJson<int?>(runtime);
    }
    if (summary != null) {
      json['summary'] = nativeToJson<String?>(summary);
    }
    return json;
  }

  AllMoviesMovies({
    required this.id,
    required this.title,
    required this.year,
    this.genres,
    this.runtime,
    this.summary,
  });
}

@immutable
class AllMoviesData {
  final List<AllMoviesMovies> movies;
  AllMoviesData.fromJson(dynamic json):
  
  movies = (json['movies'] as List<dynamic>)
        .map((e) => AllMoviesMovies.fromJson(e))
        .toList();
  @override
  bool operator ==(Object other) {
    if(identical(this, other)) {
      return true;
    }
    if(other.runtimeType != runtimeType) {
      return false;
    }

    final AllMoviesData otherTyped = other as AllMoviesData;
    return movies == otherTyped.movies;
    
  }
  @override
  int get hashCode => movies.hashCode;
  

  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    json['movies'] = movies.map((e) => e.toJson()).toList();
    return json;
  }

  AllMoviesData({
    required this.movies,
  });
}

