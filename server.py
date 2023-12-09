import grpc
from concurrent import futures
import argparse
import reddit_pb2_grpc
import controller


class RedditServicer(reddit_pb2_grpc.RedditServiceServicer):

    def __init__(self):
        self.controller = controller.RedditNativeController()
        self.controller.init()

    def CreatePost(self, request, context):
        if not request.HasField('post'):
            return reddit_pb2.CreatePostResponse(success=False)
        post = self.controller.create_post(request.post)
        return reddit_pb2.CreatePostResponse(success=True, post_id=post.post_id)

    def VotePost(self, request, context):
        if not request.HasField('post_id') or \
                not request.HasField('user') or \
                not request.HasField('is_upvote'):
            return reddit_pb2.VotePostResponse(
                success=False,
            )
        post_id = request.post_id
        user_id = request.user.user_id
        is_upvote = request.is_upvote
        suceess, score = self.controller.vote_post(post_id, user_id, is_upvote)
        if suceess:
            return reddit_pb2.VotePostResponse(
                success=True,
                score=score,
            )
        else:
            return reddit_pb2.VotePostResponse(
                success=False,
            )

    def GetPostContent(self, request, context):
        if not request.HasField('post_id'):
            return reddit_pb2.GetPostContentResponse(success=False)

        post_id = request.post_id
        post = self.controller.get_post_content(post_id)
        if post is None:
            return reddit_pb2.GetPostContentResponse(success=False)
        else:
            return reddit_pb2.GetPostContentResponse(success=True, post=post)

    def CreateComment(self, request, context):
        if not request.HasField('comment'):
            return reddit_pb2.CreateCommentResponse(success=False)
        comment = self.controller.create_comment(request.comment)
        if request.HasField('author'):
            author = request.author
            comment.author = author

        self.controller.create_comment(request.comment)
        return reddit_pb2.CreateCommentResponse(success=True, comment_id=comment.comment_id)

    def VoteComment(self, request, context):
        if not request.HasField('comment_id') or \
                not request.HasField('user') or \
                not request.HasField('is_upvote'):
            return reddit_pb2.VoteCommentResponse(
                success=False,
            )
        comment_id = request.comment_id
        user_id = request.user.user_id
        is_upvote = request.is_upvote
        suceess, score = self.controller.vote_comment(
            comment_id, user_id, is_upvote)
        if suceess:
            return reddit_pb2.VoteCommentResponse(
                success=True,
                score=score,
            )
        else:
            return reddit_pb2.VoteCommentResponse(
                success=False,
            )

    def GetMostUpvotedComments(self, request, context):
        limit = request.limit
        result = self.controller.retrieve_n_most_upvoted_comment(
            request.post_id, limit)
        comment_pair_list = []
        for comment, has_sub in result:
            comment_pair_list.append(
                reddit_pb2.CommentAndWetherSubcommentsExist(
                    comment=comment,
                    has_subcomment=has_sub,
                )
            )
        return reddit_pb2.GetMostUpvotedCommentsResponse(
            comments=comment_pair_list,
        )

    def ExpandCommentBranch(self, request, context):
        limit = request.limit
        result = self.controller.retrieve_comment_branch(
            request.comment_id, limit)
        comment_subcomments_list = []
        for sub_comment_dict in result:
            sub = sub_comment_dict['sub_comment']
            subsub = sub_comment_dict['sub_sub_comments']
            comment_subcomments_list.append(
                reddit_pb2.CommentAndSubcomments(
                    comment=sub,
                    subcomments=subsub,
                )
            )
        return reddit_pb2.ExpandCommentBranchResponse(
            subcomments=comment_subcomments_list,
        )


class AuthInterceptor(grpc.ServerInterceptor):

    def intercept_service(self, continuation, handler_call_details):
        """This is a dummy auth implementation"""
        return continuation(handler_call_details)


def serve(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=(AuthInterceptor(),))
    reddit_pb2_grpc.add_RedditServiceServicer_to_server(
        RedditServicer(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=50051)
    parser.add_argument('--host', type=str, default='localhost')
    args = parser.parse_args()

    serve(args.host, args.port)
