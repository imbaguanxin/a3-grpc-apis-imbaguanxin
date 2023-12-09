# Assignment 3 grpc apis

## repository link

https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin

## protocol buffer definitions:

```
syntax = "proto3";

// Define enumeration for post states
enum PostState {
  POST_STATE_NORMAL = 0;
  POST_STATE_LOCKED = 1;
  POST_STATE_HIDDEN = 2;
}

// Define enumeration for comment states
enum CommentState {
  COMMENT_STATE_NORMAL = 0;
  COMMENT_STATE_HIDDEN = 1;
}

message User {
  optional string user_id = 1;
}

message Post {
  optional int64 post_id = 1;
  optional string title = 2;
  optional string text = 3;
  oneof content_url {
    string video_url = 4;
    string image_url = 5;
  }
  optional User author = 6;
  optional int64 score = 7;
  optional PostState post_state = 8;
  optional string publication_date = 9;
}

message Comment {
  optional int64 comment_id = 1;
  optional int64 parent_post_id = 2;
  optional int64 parent_comment_id = 3;
  optional User author = 4;
  optional string text = 5;
  optional int64 score = 6;
  optional CommentState comment_state = 7;
  optional string publication_date = 8;
}
```

## service definitions:

1. CreatePost

   takes in a CreatePostRequest and returns a CreatePostResponse

   CreatePostRequest contains a Post object

   CreatePostResponse contains a bool success and an int64 post_id

2. VotePost

   takes in a VotePostRequest and returns a VotePostResponse

   VotePostRequest contains an int64 post_id, a User object representing the author and a bool is_upvote

   VotePostResponse contains a bool success and an int64 score

3. GetPostContent

   takes in a GetPostContentRequest and returns a GetPostContentResponse

   GetPostContentRequest contains an int64 post_id

   GetPostContentResponse contains a bool success and a Post object

4. CreateComment

   takes in a CreateCommentRequest and returns a CreateCommentResponse

   CreateCommentRequest contains a User object representing the author and a Comment object

   CreateCommentResponse contains a bool success and an int64 comment_id

5. VoteComment

   takes in a VoteCommentRequest and returns a VoteCommentResponse

   VoteCommentRequest contains an int64 comment_id, a User object representing the author and a bool is_upvote

   VoteCommentResponse contains a bool success and an int64 score

6. GetMostUpvotedComments

   takes in a GetMostUpvotedCommentsRequest and returns a GetMostUpvotedCommentsResponse

   GetMostUpvotedCommentsRequest contains an int64 post_id and an int64 limit

   GetMostUpvotedCommentsResponse contains a list of CommentAndWetherSubcommentsExist objects

   CommentAndWetherSubcommentsExist contains a Comment object and a bool has_subcomment

7. ExpandCommentBranch

   takes in a ExpandCommentBranchRequest and returns a ExpandCommentBranchResponse

   ExpandCommentBranchRequest contains an int64 comment_id and an int64 limit

   ExpandCommentBranchResponse contains a list of CommentAndSubcomments objects

   CommentAndSubcomments contains a Comment object and a list of Comment objects

```
service RedditService {
  rpc CreatePost(CreatePostRequest) returns (CreatePostResponse);

  rpc VotePost(VotePostRequest) returns (VotePostResponse);

  rpc GetPostContent(GetPostContentRequest) returns (GetPostContentResponse);

  rpc CreateComment(CreateCommentRequest) returns (CreateCommentResponse);

  rpc VoteComment(VoteCommentRequest) returns (VoteCommentResponse);

  rpc GetMostUpvotedComments(GetMostUpvotedCommentsRequest)
  returns (GetMostUpvotedCommentsResponse);

  rpc ExpandCommentBranch(ExpandCommentBranchRequest)
  returns (ExpandCommentBranchResponse);
}

message CreatePostRequest {
  optional Post post = 1;
}

message CreatePostResponse {
  optional bool success = 1;
  optional int64 post_id = 2;
}

message VotePostRequest {
  optional int64 post_id = 1;
  optional User user = 2;
  optional bool is_upvote = 3;
}

message VotePostResponse {
  optional bool success = 1;
  optional int64 score = 2;
}

message GetPostContentRequest {
  optional int64 post_id = 1;
}

message GetPostContentResponse {
  optional bool success = 1;
  optional Post post = 2;
}

message CreateCommentRequest {
  optional User author = 1;
  optional Comment comment = 2;
}

message CreateCommentResponse {
  optional bool success = 1;
  optional int64 comment_id = 2;
}

message VoteCommentRequest {
  optional int64 comment_id = 1;
  optional User user = 2;
  optional bool is_upvote = 3;
}

message VoteCommentResponse {
  optional bool success = 1;
  optional int64 score = 2;
}

message GetMostUpvotedCommentsRequest {
  optional int64 post_id = 1;
  optional int64 limit = 2;
}

message CommentAndWetherSubcommentsExist {
  optional Comment comment = 1;
  optional bool has_subcomment = 2;
}

message GetMostUpvotedCommentsResponse {
  repeated CommentAndWetherSubcommentsExist comments = 1;
}

message ExpandCommentBranchRequest {
  optional int64 comment_id = 1;
  optional int64 limit = 2;
}

message CommentAndSubcomments {
  optional Comment comment = 1;
  repeated Comment subcomments = 2;
}

message ExpandCommentBranchResponse {
  repeated CommentAndSubcomments subcomments = 1;
}
```

## storage backend

Just used in memory storage. No persistence.

## Server and Client link

server: https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/server.py

client: https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/client.py

## high level functions and tests

1. retrieve a post

    implementation: 

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L12

    test:

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L45

2. retrieve most upvoted comments

    implementation:

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L16

    test:

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L77

3. expand most upvoted comment
    
    implementation:

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L20

    test:

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L138

4. return the most upvoted reply under the most upvoted comment

    implementation:

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L31

    test:

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L281

    https://github.com/imbaguanxin/a3-grpc-apis-imbaguanxin/blob/main/test.py#L344