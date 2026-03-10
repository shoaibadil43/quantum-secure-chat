library dataconnect_generated;
import 'package:firebase_data_connect/firebase_data_connect.dart';
import 'package:flutter/foundation.dart';
import 'dart:convert';

part 'all_movies.dart';

part 'my_lists.dart';

part 'create_watch.dart';

part 'add_movie_to_list.dart';







class ExampleConnector {
  
  
  AllMoviesVariablesBuilder allMovies () {
    return AllMoviesVariablesBuilder(dataConnect, );
  }
  
  
  MyListsVariablesBuilder myLists () {
    return MyListsVariablesBuilder(dataConnect, );
  }
  
  
  CreateWatchVariablesBuilder createWatch ({required String movieId, required DateTime watchDate, }) {
    return CreateWatchVariablesBuilder(dataConnect, movieId: movieId,watchDate: watchDate,);
  }
  
  
  AddMovieToListVariablesBuilder addMovieToList ({required String listId, required String movieId, required int position, }) {
    return AddMovieToListVariablesBuilder(dataConnect, listId: listId,movieId: movieId,position: position,);
  }
  

  static ConnectorConfig connectorConfig = ConnectorConfig(
    'us-east4',
    'example',
    'quantum-secure-chat',
  );

  ExampleConnector({required this.dataConnect});
  static ExampleConnector get instance {
    return ExampleConnector(
        dataConnect: FirebaseDataConnect.instanceFor(
            connectorConfig: connectorConfig,
            sdkType: CallerSDKType.generated));
  }

  FirebaseDataConnect dataConnect;
}
