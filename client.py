import reddit_pb2
import reddit_pb2_grpc
import argparse
import grpc


class RedditClient:

    def __init__(self, stub=None, host=None, port=None):
        if stub is None:
            channel = grpc.insecure_channel(f'{host}:{port}')
            stub = reddit_pb2_grpc.RedditServiceStub(channel)
        self.stub = stub

    def post_to_dict(self, post: reddit_pb2.Post):
        result = {}
        if post.HasField('post_id'):
            result['post_id'] = post.post_id
        if post.HasField('title'):
            result['title'] = post.title
        if post.HasField('text'):
            result['text'] = post.text
        if post.HasField('video_url'):
            result['video_url'] = post.video_url
        if post.HasField('image_url'):
            result['image_url'] = post.image_url
        if post.HasField('author'):
            result['author'] = post.author.user_id
        if post.HasField('score'):
            result['score'] = post.score
        if post.HasField('post_state'):
            if post.post_state == reddit_pb2.PostState.POST_STATE_NORMAL:
                result['post_state'] = 'normal'
            elif post.post_state == reddit_pb2.PostState.POST_STATE_LOCKED:
                result['post_state'] = 'locked'
            elif post.post_state == reddit_pb2.PostState.POST_STATE_HIDDEN:
                result['post_state'] = 'hidden'
        if post.HasField('publication_date'):
            result['publication_date'] = post.publication_date
        return result

    def comment_to_dict(self, comment: reddit_pb2.Comment):
        result = {}
        if comment.HasField('comment_id'):
            result['comment_id'] = comment.comment_id
        if comment.HasField('parent_post_id'):
            result['parent_post_id'] = comment.parent_post_id
        if comment.HasField('parent_comment_id'):
            result['parent_comment_id'] = comment.parent_comment_id
        if comment.HasField('text'):
            result['text'] = comment.text
        if comment.HasField('author'):
            result['author'] = comment.author.user_id
        if comment.HasField('score'):
            result['score'] = comment.score
        if comment.HasField('comment_state'):
            if comment.comment_state == reddit_pb2.CommentState.COMMENT_STATE_NORMAL:
                result['comment_state'] = 'normal'
            elif comment.comment_state == reddit_pb2.CommentState.COMMENT_STATE_LOCKED:
                result['comment_state'] = 'locked'
            elif comment.comment_state == reddit_pb2.CommentState.COMMENT_STATE_HIDDEN:
                result['comment_state'] = 'hidden'
        if comment.HasField('publication_date'):
            result['publication_date'] = comment.publication_date
        return result

    def create_post(self, title, text, video_url=None, image_url=None, author=None, post_state=None):
        post_dict = {}
        post_dict['title'] = title
        post_dict['text'] = text
        if video_url is not None:
            post_dict['video_url'] = video_url
        elif image_url is not None:
            post_dict['image_url'] = image_url
        if author is not None:
            post_dict['author'] = reddit_pb2.User(user_id=author)
        if post_state is not None:
            if post_state.lower() == 'normal':
                post_dict['post_state'] = reddit_pb2.PostState.POST_STATE_NORMAL
            elif post_state.lower() == 'locked':
                post_dict['post_state'] = reddit_pb2.PostState.POST_STATE_LOCKED
            elif post_state.lower() == 'hidden':
                post_dict['post_state'] = reddit_pb2.PostState.POST_STATE_HIDDEN
        post = reddit_pb2.Post(**post_dict)
        request = reddit_pb2.CreatePostRequest(post=post)
        response = self.stub.CreatePost(request)
        if response.success:
            return response.post_id
        else:
            return None

    def vote_post(self, post_id, user_id, is_upvote):
        request = reddit_pb2.VotePostRequest(
            post_id=post_id,
            user=reddit_pb2.User(user_id=user_id),
            is_upvote=is_upvote,
        )
        response = self.stub.VotePost(request)
        if response.success:
            return response.score
        else:
            return None

    def get_post_content(self, post_id):
        request = reddit_pb2.GetPostContentRequest(post_id=post_id)
        response = self.stub.GetPostContent(request)
        if response.success:
            post = response.post
            result = self.post_to_dict(post)
            return result
        else:
            return None

    def create_comment(self, author_id, parent_post_id=None,
                       parent_comment_id=None, text=None,
                       comment_state=None):
        comment_dict = {}
        author = reddit_pb2.User(user_id=author_id)
        comment_dict['author'] = author
        if parent_post_id is not None:
            comment_dict['parent_post_id'] = parent_post_id
        if parent_comment_id is not None:
            comment_dict['parent_comment_id'] = parent_comment_id
        if text is not None:
            comment_dict['text'] = text
        if comment_state is not None:
            if comment_state.lower() == 'normal':
                comment_dict['comment_state'] = reddit_pb2.CommentState.COMMENT_STATE_NORMAL
            elif comment_state.lower() == 'locked':
                comment_dict['comment_state'] = reddit_pb2.CommentState.COMMENT_STATE_LOCKED
            elif comment_state.lower() == 'hidden':
                comment_dict['comment_state'] = reddit_pb2.CommentState.COMMENT_STATE_HIDDEN
        comment = reddit_pb2.Comment(**comment_dict)
        request = reddit_pb2.CreateCommentRequest(
            author=author,
            comment=comment,
        )
        response = self.stub.CreateComment(request)
        if response.success:
            return response.comment_id
        else:
            return None

    def vote_comment(self, comment_id, user_id, is_upvote):
        request = reddit_pb2.VoteCommentRequest(
            comment_id=comment_id,
            user=reddit_pb2.User(user_id=user_id),
            is_upvote=is_upvote,
        )
        response = self.stub.VoteComment(request)
        if response.success:
            return response.score
        else:
            return None

    def get_most_upvoted_comments(self, post_id, n):
        request = reddit_pb2.GetMostUpvotedCommentsRequest(
            post_id=post_id,
            limit=n,
        )
        response = self.stub.GetMostUpvotedComments(request)
        result = []
        for comment in response.comments:
            has_subcomment = comment.HasField(
                'has_subcomment') and comment.has_subcomment
            comment_dict = self.comment_to_dict(comment.comment)
            comment_dict['has_subcomment'] = has_subcomment
            result.append(comment_dict)
        return result

    def expand_comment_branch(self, comment_id, n):
        request = reddit_pb2.ExpandCommentBranchRequest(
            comment_id=comment_id,
            limit=n,
        )
        response = self.stub.ExpandCommentBranch(request)
        result = []
        for sub_subsub in response.subcomments:
            sub = self.comment_to_dict(sub_subsub.comment)
            subsub = []
            for subsub_comment in sub_subsub.subcomments:
                subsub.append(self.comment_to_dict(subsub_comment))
            result.append({'sub_comment': sub, 'sub_sub_comments': subsub})
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='reddit client')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Host address of the client')
    parser.add_argument('--port', type=int, default=50051,
                        help='Port number of the client')
    args = parser.parse_args()
    client = RedditClient(host=args.host, port=args.port)
    result = client.create_post(
        'title', 'text', 'url', None, 'author', 'normal')
    print(result)
    result = client.get_most_upvoted_comments(0, 2)
    for e in result:
        print(e)
    result = client.expand_comment_branch(0, 2)
    for e in result:
        print(e)
