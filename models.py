from enum import Enum
from datetime import datetime
import reddit_pb2
import reddit_pb2_grpc


class PostState(Enum):
    NORMAL = 0
    LOCKED = 1
    HIDDEN = 2


class CommentState(Enum):
    NORMAL = 0
    HIDDEN = 2


class URLType(Enum):
    VIDEO = 0
    IMAGE = 1


class Post:
    def __init__(self, post_id, title, text,
                 url=None, url_type=None, author=None,
                 score=0, post_state=PostState.NORMAL):
        self.post_id = post_id
        self.title = title
        self.text = text
        self.url = url
        self.url_type = url_type
        self.author = author

        self.score = score
        self.post_state = post_state
        self.publication_date = datetime.now()

    def to_proto(self):
        post_dict = {}
        post_dict['post_id'] = self.post_id
        post_dict['title'] = self.title
        post_dict['text'] = self.text
        if self.url and self.url_type is not None:
            if self.url_type == URLType.video:
                post_dict['video_url'] = self.url
            elif self.url_type == URLType.image:
                post_dict['image_url'] = self.url
        if self.author:
            post_dict['author'] = reddit_pb2.User(user_id=self.author)
        post_dict['score'] = self.score
        if self.post_state == PostState.NORMAL:
            post_dict['post_state'] = reddit_pb2.PostState.POST_STATE_NORMAL
        elif self.post_state == PostState.LOCKED:
            post_dict['post_state'] = reddit_pb2.PostState.POST_STATE_LOCKED
        elif self.post_state == PostState.HIDDEN:
            post_dict['post_state'] = reddit_pb2.PostState.POST_STATE_HIDDEN
        post_dict['publication_date'] = self.publication_date.isoformat()
        return reddit_pb2.Post(**post_dict)

    def __repr__(self):
        return f"Post(post_id={self.post_id}, title={self.title}, text={self.text}, post_state={self.post_state})"


class Comment:
    def __init__(self, comment_id, author, text,
                 parent_post_id=None, parrent_comment_id=None,
                 score=0, comment_state=CommentState.NORMAL):
        self.comment_id = comment_id
        self.author = author
        self.text = text
        self.parent_post_id = parent_post_id
        self.parrent_comment_id = parrent_comment_id
        self.score = score
        self.comment_state = comment_state
        self.publication_date = datetime.now()

    def to_proto(self):
        comment_dict = {}
        comment_dict['comment_id'] = self.comment_id
        comment_dict['author'] = reddit_pb2.User(user_id=self.author)
        comment_dict['text'] = self.text
        if parent_post_id:
            comment_dict['parent_post_id'] = self.parent_post_id
        if parrent_comment_id:
            comment_dict['parrent_comment_id'] = self.parrent_comment_id
        comment_dict['score'] = self.score
        if self.comment_state == CommentState.NORMAL:
            comment_dict['comment_state'] = reddit_pb2.CommentState.COMMENT_STATE_NORMAL
        elif self.comment_state == CommentState.HIDDEN:
            comment_dict['comment_state'] = reddit_pb2.CommentState.COMMENT_STATE_HIDDEN
        comment_dict['publication_date'] = self.publication_date.isoformat()
        return reddit_pb2.Comment(**comment_dict)

    def __repr__(self):
        return f"Comment(comment_id={self.comment_id}, author={self.author}, text={self.text}, parent_post_id={self.parent_post_id}, parrent_comment_id={self.parrent_comment_id}, comment_state={self.comment_state})"
