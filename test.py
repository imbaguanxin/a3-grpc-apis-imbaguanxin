import unittest
from unittest.mock import patch, MagicMock
import grpc

from reddit_pb2_grpc import RedditServiceStub
import reddit_pb2
from client import RedditClient


# high level fuctions:

def retrieve_a_post(client, post_id):
    return client.get_post_content(post_id)


def retrieve_most_upvoted_comments(client, post_id, limit):
    return client.get_most_upvoted_comments(post_id, limit)


def expand_most_upvoted_comment(client, post_id):
    # get the most upvoted comment
    comment = client.get_most_upvoted_comments(post_id, 1)[0]
    # expand the comment
    sub_comments = client.expand_comment_branch(comment['comment_id'], 10)
    return {
        'comment': comment,
        'sub_comments': sub_comments,
    }


def most_upvoted_sub_comment(client, post_id):
    # get the most upvoted comment
    comment = client.get_most_upvoted_comments(post_id, 1)[0]
    if comment['has_subcomment']:
        # find the most upvoted sub comment
        sub_comment = client.expand_comment_branch(comment['comment_id'], 1)[0]
        return sub_comment['sub_comment']
    else:
        return None


class TestClient(unittest.TestCase):

    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_client_retrieve_a_post(self, mock_stub):
        mock_stub = MagicMock()
        mock_stub.GetPostContent.return_value = reddit_pb2.GetPostContentResponse(
            success=True,
            post=reddit_pb2.Post(
                post_id=1,
                title='title',
                text='text',
                video_url='url',
                author=reddit_pb2.User(user_id='author'),
                score=1,
                post_state=reddit_pb2.PostState.POST_STATE_NORMAL,
                publication_date="now",
            )
        )
        client = RedditClient(stub=mock_stub)
        post = retrieve_a_post(client, 1)
        self.assertEqual(post, {
            'post_id': 1,
            'title': 'title',
            'text': 'text',
            'video_url': 'url',
            'author': 'author',
            'score': 1,
            'post_state': 'normal',
            'publication_date': 'now',
        })
        mock_stub.GetPostContent.assert_called_once_with(
            reddit_pb2.GetPostContentRequest(post_id=1)
        )

    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_client_retrieve_most_upvoted_comments(self, mock_stub):
        mock_stub = MagicMock()
        mock_stub.GetMostUpvotedComments.return_value = reddit_pb2.GetMostUpvotedCommentsResponse(
            comments=[
                reddit_pb2.CommentAndWetherSubcommentsExist(
                    comment=reddit_pb2.Comment(
                        comment_id=1,
                        parent_post_id=0,
                        author=reddit_pb2.User(user_id='author'),
                        text='text',
                        score=5,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                    has_subcomment=True,
                ),
                reddit_pb2.CommentAndWetherSubcommentsExist(
                    comment=reddit_pb2.Comment(
                        comment_id=2,
                        parent_post_id=0,
                        author=reddit_pb2.User(user_id='author'),
                        text='text',
                        score=3,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                    has_subcomment=False,
                ),
            ]
        )
        client = RedditClient(stub=mock_stub)
        result = retrieve_most_upvoted_comments(client, 0, 2)
        mock_stub.GetMostUpvotedComments.assert_called_once_with(
            reddit_pb2.GetMostUpvotedCommentsRequest(
                post_id=0,
                limit=2,
            )
        )
        self.assertEqual(result, [
            {
                'comment_id': 1,
                'parent_post_id': 0,
                'author': 'author',
                'text': 'text',
                'score': 5,
                'comment_state': 'normal',
                'publication_date': 'now',
                'has_subcomment': True,
            }, {
                'comment_id': 2,
                'parent_post_id': 0,
                'author': 'author',
                'text': 'text',
                'score': 3,
                'comment_state': 'normal',
                'publication_date': 'now',
                'has_subcomment': False,
            }
        ])

    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_client_expand_most_upvoted_comment(self, mock_stub):
        """
        expand the most upvoted comment
        """
        mock_stub = MagicMock()
        mock_stub.GetMostUpvotedComments.return_value = reddit_pb2.GetMostUpvotedCommentsResponse(
            comments=[
                reddit_pb2.CommentAndWetherSubcommentsExist(
                    comment=reddit_pb2.Comment(
                        comment_id=1,
                        parent_post_id=0,
                        author=reddit_pb2.User(user_id='author'),
                        text='text',
                        score=5,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                    has_subcomment=True,
                ),
            ]
        )
        mock_stub.ExpandCommentBranch.return_value = reddit_pb2.ExpandCommentBranchResponse(
            subcomments=[
                reddit_pb2.CommentAndSubcomments(
                    comment=reddit_pb2.Comment(
                        comment_id=10,
                        parent_comment_id=1,
                        author=reddit_pb2.User(user_id='author1'),
                        text='sub text 10',
                        score=10,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                ),
                reddit_pb2.CommentAndSubcomments(
                    comment=reddit_pb2.Comment(
                        comment_id=11,
                        parent_comment_id=1,
                        author=reddit_pb2.User(user_id='author2'),
                        text='sub text 11',
                        score=5,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                    subcomments=[
                        reddit_pb2.Comment(
                            comment_id=20,
                            parent_comment_id=11,
                            author=reddit_pb2.User(user_id='author3'),
                            text='sub text 20',
                            score=20,
                            comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                            publication_date='now',
                        ),
                        reddit_pb2.Comment(
                            comment_id=21,
                            parent_comment_id=11,
                            author=reddit_pb2.User(user_id='author4'),
                            text='sub text 21',
                            score=15,
                            comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                            publication_date='now',
                        ),
                    ]
                ),
            ]
        )
        client = RedditClient(stub=mock_stub)
        result = expand_most_upvoted_comment(client, 0)
        mock_stub.GetMostUpvotedComments.assert_called_once_with(
            reddit_pb2.GetMostUpvotedCommentsRequest(
                post_id=0,
                limit=1,
            )
        )
        mock_stub.ExpandCommentBranch.assert_called_once_with(
            reddit_pb2.ExpandCommentBranchRequest(
                comment_id=1,
                limit=10,
            )
        )
        self.assertEqual(
            result,
            {
                "comment": {
                    "comment_id": 1,
                    "parent_post_id": 0,
                    "text": "text",
                    "author": "author",
                    "score": 5,
                    "comment_state": "normal",
                    "publication_date": "now",
                    "has_subcomment": True,
                },
                "sub_comments": [
                    {
                        "sub_comment": {
                            "comment_id": 10,
                            "parent_comment_id": 1,
                            "text": "sub text 10",
                            "author": "author1",
                            "score": 10,
                            "comment_state": "normal",
                            "publication_date": "now",
                        },
                        "sub_sub_comments": [],
                    },
                    {
                        "sub_comment": {
                            "comment_id": 11,
                            "parent_comment_id": 1,
                            "text": "sub text 11",
                            "author": "author2",
                            "score": 5,
                            "comment_state": "normal",
                            "publication_date": "now",
                        },
                        "sub_sub_comments": [
                            {
                                "comment_id": 20,
                                "parent_comment_id": 11,
                                "text": "sub text 20",
                                "author": "author3",
                                "score": 20,
                                "comment_state": "normal",
                                "publication_date": "now",
                            },
                            {
                                "comment_id": 21,
                                "parent_comment_id": 11,
                                "text": "sub text 21",
                                "author": "author4",
                                "score": 15,
                                "comment_state": "normal",
                                "publication_date": "now",
                            },
                        ],
                    },
                ],
            }
        )

    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_client_most_upvoted_sub_comment(self, mock_stub):
        """
        sub_comment exists under the most upvoted comment
        """
        mock_stub = MagicMock()
        mock_stub.GetMostUpvotedComments.return_value = reddit_pb2.GetMostUpvotedCommentsResponse(
            comments=[
                reddit_pb2.CommentAndWetherSubcommentsExist(
                    comment=reddit_pb2.Comment(
                        comment_id=1,
                        parent_post_id=0,
                        author=reddit_pb2.User(user_id='author'),
                        text='text',
                        score=5,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                    has_subcomment=True,
                ),
            ]
        )
        mock_stub.ExpandCommentBranch.return_value = reddit_pb2.ExpandCommentBranchResponse(
            subcomments=[
                reddit_pb2.CommentAndSubcomments(
                    comment=reddit_pb2.Comment(
                        comment_id=10,
                        parent_comment_id=1,
                        author=reddit_pb2.User(user_id='author1'),
                        text='sub text 10',
                        score=10,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                ),
            ]
        )
        client = RedditClient(stub=mock_stub)
        result = most_upvoted_sub_comment(client, 0)
        mock_stub.GetMostUpvotedComments.assert_called_once_with(
            reddit_pb2.GetMostUpvotedCommentsRequest(
                post_id=0,
                limit=1,
            )
        )
        mock_stub.ExpandCommentBranch.assert_called_once_with(
            reddit_pb2.ExpandCommentBranchRequest(
                comment_id=1,
                limit=1,
            )
        )
        self.assertEqual(
            result,
            {
                "comment_id": 10,
                "parent_comment_id": 1,
                "text": "sub text 10",
                "author": "author1",
                "score": 10,
                "comment_state": "normal",
                "publication_date": "now",
            }
        )

    @patch('reddit_pb2_grpc.RedditServiceStub')
    def test_client_most_upvoted_sub_comment_no_subcomment(self, mock_stub):
        """
        there is no sub commnet under the most upvoted comment
        """
        mock_stub = MagicMock()
        mock_stub.GetMostUpvotedComments.return_value = reddit_pb2.GetMostUpvotedCommentsResponse(
            comments=[
                reddit_pb2.CommentAndWetherSubcommentsExist(
                    comment=reddit_pb2.Comment(
                        comment_id=1,
                        parent_post_id=0,
                        author=reddit_pb2.User(user_id='author'),
                        text='text',
                        score=5,
                        comment_state=reddit_pb2.CommentState.COMMENT_STATE_NORMAL,
                        publication_date='now',
                    ),
                    has_subcomment=False,
                ),
            ]
        )
        client = RedditClient(stub=mock_stub)
        result = most_upvoted_sub_comment(client, 0)
        mock_stub.GetMostUpvotedComments.assert_called_once_with(
            reddit_pb2.GetMostUpvotedCommentsRequest(
                post_id=0,
                limit=1,
            )
        )
        mock_stub.ExpandCommentBranch.assert_not_called()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
