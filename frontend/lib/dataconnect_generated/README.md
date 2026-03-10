# dataconnect_generated SDK

## Installation
```sh
flutter pub get firebase_data_connect
flutterfire configure
```
For more information, see [Flutter for Firebase installation documentation](https://firebase.google.com/docs/data-connect/flutter-sdk#use-core).

## Data Connect instance
Each connector creates a static class, with an instance of the `DataConnect` class that can be used to connect to your Data Connect backend and call operations.

### Connecting to the emulator

```dart
String host = 'localhost'; // or your host name
int port = 9399; // or your port number
ExampleConnector.instance.dataConnect.useDataConnectEmulator(host, port);
```

You can also call queries and mutations by using the connector class.
## Queries

### AllMovies
#### Required Arguments
```dart
// No required arguments
ExampleConnector.instance.allMovies().execute();
```



#### Return Type
`execute()` returns a `QueryResult<AllMoviesData, void>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

/// Result of a query request. Created to hold extra variables in the future.
class QueryResult<Data, Variables> extends OperationResult<Data, Variables> {
  QueryResult(super.dataConnect, super.data, super.ref);
}

final result = await ExampleConnector.instance.allMovies();
AllMoviesData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
final ref = ExampleConnector.instance.allMovies().ref();
ref.execute();

ref.subscribe(...);
```


### MyLists
#### Required Arguments
```dart
// No required arguments
ExampleConnector.instance.myLists().execute();
```



#### Return Type
`execute()` returns a `QueryResult<MyListsData, void>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

/// Result of a query request. Created to hold extra variables in the future.
class QueryResult<Data, Variables> extends OperationResult<Data, Variables> {
  QueryResult(super.dataConnect, super.data, super.ref);
}

final result = await ExampleConnector.instance.myLists();
MyListsData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
final ref = ExampleConnector.instance.myLists().ref();
ref.execute();

ref.subscribe(...);
```

## Mutations

### CreateWatch
#### Required Arguments
```dart
String movieId = ...;
DateTime watchDate = ...;
ExampleConnector.instance.createWatch(
  movieId: movieId,
  watchDate: watchDate,
).execute();
```

#### Optional Arguments
We return a builder for each query. For CreateWatch, we created `CreateWatchBuilder`. For queries and mutations with optional parameters, we return a builder class.
The builder pattern allows Data Connect to distinguish between fields that haven't been set and fields that have been set to null. A field can be set by calling its respective setter method like below:
```dart
class CreateWatchVariablesBuilder {
  ...
   CreateWatchVariablesBuilder location(String? t) {
   _location.value = t;
   return this;
  }

  ...
}
ExampleConnector.instance.createWatch(
  movieId: movieId,
  watchDate: watchDate,
)
.location(location)
.execute();
```

#### Return Type
`execute()` returns a `OperationResult<CreateWatchData, CreateWatchVariables>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

final result = await ExampleConnector.instance.createWatch(
  movieId: movieId,
  watchDate: watchDate,
);
CreateWatchData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
String movieId = ...;
DateTime watchDate = ...;

final ref = ExampleConnector.instance.createWatch(
  movieId: movieId,
  watchDate: watchDate,
).ref();
ref.execute();
```


### AddMovieToList
#### Required Arguments
```dart
String listId = ...;
String movieId = ...;
int position = ...;
ExampleConnector.instance.addMovieToList(
  listId: listId,
  movieId: movieId,
  position: position,
).execute();
```



#### Return Type
`execute()` returns a `OperationResult<AddMovieToListData, AddMovieToListVariables>`
```dart
/// Result of an Operation Request (query/mutation).
class OperationResult<Data, Variables> {
  OperationResult(this.dataConnect, this.data, this.ref);
  Data data;
  OperationRef<Data, Variables> ref;
  FirebaseDataConnect dataConnect;
}

final result = await ExampleConnector.instance.addMovieToList(
  listId: listId,
  movieId: movieId,
  position: position,
);
AddMovieToListData data = result.data;
final ref = result.ref;
```

#### Getting the Ref
Each builder returns an `execute` function, which is a helper function that creates a `Ref` object, and executes the underlying operation.
An example of how to use the `Ref` object is shown below:
```dart
String listId = ...;
String movieId = ...;
int position = ...;

final ref = ExampleConnector.instance.addMovieToList(
  listId: listId,
  movieId: movieId,
  position: position,
).ref();
ref.execute();
```

