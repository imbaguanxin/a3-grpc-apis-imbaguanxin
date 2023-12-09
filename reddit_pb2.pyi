from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    POST_STATE_NORMAL: _ClassVar[PostState]
    POST_STATE_LOCKED: _ClassVar[PostState]
    POST_STATE_HIDDEN: _ClassVar[PostState]

class CommentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    COMMENT_STATE_NORMAL: _ClassVar[CommentState]
    COMMENT_STATE_HIDDEN: _ClassVar[CommentState]
POST_STATE_NORMAL: PostState
POST_STATE_LOCKED: PostState
POST_STATE_HIDDEN: PostState
COMMENT_STATE_NORMAL: CommentState
COMMENT_STATE_HIDDEN: CommentState

class User(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ["post_id", "title", "text", "video_url", "image_url", "author", "score", "post_state", "publication_date"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    POST_STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    title: str
    text: str
    video_url: str
    image_url: str
    author: User
    score: int
    post_state: PostState
    publication_date: str
    def __init__(self, post_id: _Optional[int] = ..., title: _Optional[str] = ..., text: _Optional[str] = ..., video_url: _Optional[str] = ..., image_url: _Optional[str] = ..., author: _Optional[_Union[User, _Mapping]] = ..., score: _Optional[int] = ..., post_state: _Optional[_Union[PostState, str]] = ..., publication_date: _Optional[str] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ["comment_id", "parent_post_id", "parent_comment_id", "author", "text", "score", "comment_state", "publication_date"]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_POST_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    parent_post_id: int
    parent_comment_id: int
    author: User
    text: str
    score: int
    comment_state: CommentState
    publication_date: str
    def __init__(self, comment_id: _Optional[int] = ..., parent_post_id: _Optional[int] = ..., parent_comment_id: _Optional[int] = ..., author: _Optional[_Union[User, _Mapping]] = ..., text: _Optional[str] = ..., score: _Optional[int] = ..., comment_state: _Optional[_Union[CommentState, str]] = ..., publication_date: _Optional[str] = ...) -> None: ...

class CreatePostRequest(_message.Message):
    __slots__ = ["post"]
    POST_FIELD_NUMBER: _ClassVar[int]
    post: Post
    def __init__(self, post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...

class CreatePostResponse(_message.Message):
    __slots__ = ["success", "post_id"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    post_id: int
    def __init__(self, success: bool = ..., post_id: _Optional[int] = ...) -> None: ...

class VotePostRequest(_message.Message):
    __slots__ = ["post_id", "user", "is_upvote"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    IS_UPVOTE_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    user: User
    is_upvote: bool
    def __init__(self, post_id: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ..., is_upvote: bool = ...) -> None: ...

class VotePostResponse(_message.Message):
    __slots__ = ["success", "score"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    score: int
    def __init__(self, success: bool = ..., score: _Optional[int] = ...) -> None: ...

class GetPostContentRequest(_message.Message):
    __slots__ = ["post_id"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    def __init__(self, post_id: _Optional[int] = ...) -> None: ...

class GetPostContentResponse(_message.Message):
    __slots__ = ["success", "post"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    success: bool
    post: Post
    def __init__(self, success: bool = ..., post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...

class CreateCommentRequest(_message.Message):
    __slots__ = ["author", "comment"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    author: User
    comment: Comment
    def __init__(self, author: _Optional[_Union[User, _Mapping]] = ..., comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class CreateCommentResponse(_message.Message):
    __slots__ = ["success", "comment_id"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    comment_id: int
    def __init__(self, success: bool = ..., comment_id: _Optional[int] = ...) -> None: ...

class VoteCommentRequest(_message.Message):
    __slots__ = ["comment_id", "user", "is_upvote"]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    IS_UPVOTE_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    user: User
    is_upvote: bool
    def __init__(self, comment_id: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ..., is_upvote: bool = ...) -> None: ...

class VoteCommentResponse(_message.Message):
    __slots__ = ["success", "score"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    score: int
    def __init__(self, success: bool = ..., score: _Optional[int] = ...) -> None: ...

class GetMostUpvotedCommentsRequest(_message.Message):
    __slots__ = ["post_id", "limit"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    limit: int
    def __init__(self, post_id: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class CommentAndWetherSubcommentsExist(_message.Message):
    __slots__ = ["comment", "has_subcomment"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    HAS_SUBCOMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    has_subcomment: bool
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ..., has_subcomment: bool = ...) -> None: ...

class GetMostUpvotedCommentsResponse(_message.Message):
    __slots__ = ["comments"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[CommentAndWetherSubcommentsExist]
    def __init__(self, comments: _Optional[_Iterable[_Union[CommentAndWetherSubcommentsExist, _Mapping]]] = ...) -> None: ...

class ExpandCommentBranchRequest(_message.Message):
    __slots__ = ["comment_id", "limit"]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    limit: int
    def __init__(self, comment_id: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class CommentAndSubcomments(_message.Message):
    __slots__ = ["comment", "subcomments"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    SUBCOMMENTS_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    subcomments: _containers.RepeatedCompositeFieldContainer[Comment]
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ..., subcomments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ...) -> None: ...

class ExpandCommentBranchResponse(_message.Message):
    __slots__ = ["subcomments"]
    SUBCOMMENTS_FIELD_NUMBER: _ClassVar[int]
    subcomments: _containers.RepeatedCompositeFieldContainer[CommentAndSubcomments]
    def __init__(self, subcomments: _Optional[_Iterable[_Union[CommentAndSubcomments, _Mapping]]] = ...) -> None: ...
