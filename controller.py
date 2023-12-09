import reddit_pb2
import reddit_pb2_grpc
from datetime import datetime

class RedditNativeController:

    def __init__(self):
        self.posts = {}
        self.posts_votes = {}
        self.comments = {}
        self.comments_votes = {}
        self.users = set()
        self.post_count = 0
        self.comment_count = 0

    def create_post(self, post: reddit_pb2.Post):
        post.post_id = self.post_count
        post.score = 0
        if not post.HasField('post_state'):
            post.post_state = reddit_pb2.PostState.POST_STATE_NORMAL
        post.publication_date = datetime.now().isoformat()
        self.posts[self.post_count] = post
        self.post_count += 1
        self.posts_votes[post.post_id] = {
            "upvote": set(), "downvote": set()
        }
        return post

    def create_comment(self, comment: reddit_pb2.Comment):
        comment.comment_id = self.comment_count
        if not comment.HasField('comment_state'):
            comment.comment_state = reddit_pb2.CommentState.COMMENT_STATE_NORMAL
        comment.publication_date = datetime.now().isoformat()
        self.comments[self.comment_count] = comment
        self.comment_count += 1
        self.comments_votes[comment.comment_id] = {
            "upvote": set(), "downvote": set()
        }
        return comment

    def get_post(self, post_id: int):
        """Return the post object if post_id exists, otherwise return None"""
        post = self.posts.get(post_id, None)
        if post is None:
            return None
        if post.post_state == reddit_pb2.PostState.POST_STATE_HIDDEN:
            return None
        return post

    def get_comment(self, comment_id: int):
        """Return the comment object if comment_id exists, otherwise return None"""

        comment = self.comments.get(comment_id, None)
        if comment is None:
            return None
        if comment.comment_state == reddit_pb2.CommentState.COMMENT_STATE_HIDDEN:
            return None
        return comment

    def vote_post(self, post_id: int, user_id: str, is_upvote: bool):
        """
        Vote a post, return True if success, 
        False if user_id already voted or post_id not exists
        """
        post = self.get_post(post_id)
        if post is None:
            return False, 0
        if is_upvote:
            if user_id in self.posts_votes[post_id]["upvote"]:
                return False, 0
            if user_id in self.posts_votes[post_id]["downvote"]:
                self.posts_votes[post_id]["downvote"].remove(user_id)
                post.score += 1
            self.posts_votes[post_id]["upvote"].add(user_id)
            post.score += 1
        else:
            if user_id in self.posts_votes[post_id]["downvote"]:
                return False, 0
            if user_id in self.posts_votes[post_id]["upvote"]:
                self.posts_votes[post_id]["upvote"].remove(user_id)
                post.score -= 1
            self.posts_votes[post_id]["downvote"].add(user_id)
            post.score -= 1
        return True, post.score

    def vote_comment(self, comment_id: int, user_id: str, is_upvote: bool):
        """
        Vote a comment, return True if success,
        False if user_id already voted or comment_id not exists
        """
        comment = self.get_comment(comment_id)
        if comment is None:
            return False, 0
        if is_upvote:
            if user_id in self.comments_votes[comment_id]["upvote"]:
                return False, 0
            if user_id in self.comments_votes[comment_id]["downvote"]:
                self.comments_votes[comment_id]["downvote"].remove(user_id)
                comment.score += 1
            self.comments_votes[comment_id]["upvote"].add(user_id)
            comment.score += 1
        else:
            if user_id in self.comments_votes[comment_id]["downvote"]:
                return False, 0
            if user_id in self.comments_votes[comment_id]["upvote"]:
                self.comments_votes[comment_id]["upvote"].remove(user_id)
                comment.score -= 1
            self.comments_votes[comment_id]["downvote"].add(user_id)
            comment.score -= 1
        return True, comment.score

    def retrieve_n_most_upvoted_comment(self, post_id: int, n: int):
        """
        Retrieve n most upvoted comments under a post,
        hidden comments are ignored,
        return a list of (comment, has_sub_comment)
        """
        post = self.get_post(post_id)
        if post is None:
            return []
        comments = []
        for comment in self.comments.values():
            if comment.HasField("parent_post_id") and comment.parent_post_id == post_id:
                if comment.comment_state == reddit_pb2.CommentState.COMMENT_STATE_HIDDEN:
                    continue
                comments.append(comment)
        comments = sorted(comments, key=lambda x: x.score, reverse=True)[:n]
        result = []
        for comment in comments:
            has_sub_comment = False
            for sub_comment in self.comments.values():
                if sub_comment.HasField("parent_post_id") and sub_comment.parent_comment_id == comment.comment_id:
                    if sub_comment.comment_state == reddit_pb2.CommentState.COMMENT_STATE_HIDDEN:
                        continue
                    has_sub_comment = True
                    break
            result.append((comment, has_sub_comment))
        return result

    def retrieve_comment_branch(self, comment_id: int, n: int):
        """
        retrieve comment branch.
        Given a comment_id, return top n sub comments,
        and it's corresponding top n sub sub comments.

        The result is a list of dict, each dict has two keys:
        "sub_comment": the sub comment object
        "sub_sub_comments": a list of sub sub comments.

        The result is a 2-level comment tree.
        """
        comment = self.get_comment(comment_id)
        if comment is None:
            return []
        sub_comments = []
        for comment in self.comments.values():
            if comment.HasField('parent_comment_id') and comment.parent_comment_id == comment_id:
                if comment.comment_state == reddit_pb2.CommentState.COMMENT_STATE_HIDDEN:
                    continue
                sub_comments.append(comment)
        sub_comments = sorted(
            sub_comments, key=lambda x: x.score, reverse=True)[:n]
        result = []
        for sub in sub_comments:
            sub_sub_comments = []
            for subsub in self.comments.values():
                if subsub.HasField('parent_comment_id') and subsub.parent_comment_id == sub.comment_id:
                    if subsub.comment_state == reddit_pb2.CommentState.COMMENT_STATE_HIDDEN:
                        continue
                    sub_sub_comments.append(subsub)
            sub_sub_comments.sort(key=lambda x: x.score, reverse=True)
            sub_sub_comments = sub_sub_comments[:n]
            result.append({
                "sub_comment": sub,
                "sub_sub_comments": sub_sub_comments
            })
        return result

    def init(self):
        """
        Initialize the database with some data
        """
        user1 = reddit_pb2.User(user_id="user1")
        user2 = reddit_pb2.User(user_id="user2")
        user3 = reddit_pb2.User(user_id="user3")

        p0 = reddit_pb2.Post(
            title="post0", text="post0_content")
        self.create_post(p0)
        p1 = reddit_pb2.Post(
            title="post1", text="post1_content")
        self.create_post(p1)
        p2 = reddit_pb2.Post(title="post2image", text="post2_content_image",
                             video_url="img.url.example")
        self.create_post(p2)
        p3 = reddit_pb2.Post(title="post3video", text="post3_content_video",
                             image_url="video.url.example")
        self.create_post(p3)
        p3 = reddit_pb2.Post(title="post4locked", text="post4_content_locked",
                             post_state=reddit_pb2.PostState.POST_STATE_LOCKED)
        self.create_post(p3)
        p4 = reddit_pb2.Post(title="post5hidden", text="post5_content_hidden",
                             post_state=reddit_pb2.PostState.POST_STATE_HIDDEN)
        self.create_post(p4)

        c0 = reddit_pb2.Comment(
            author=user1, text="comment0", parent_post_id=p0.post_id)
        self.create_comment(c0)
        c1 = reddit_pb2.Comment(
            author=user2, text="comment1", parent_post_id=p1.post_id)
        self.create_comment(c1)
        c2 = reddit_pb2.Comment(
            author=user3, text="comment2", parent_post_id=p2.post_id)
        self.create_comment(c2)
        c3 = reddit_pb2.Comment(
            author=user1, text="comment3", parent_post_id=p0.post_id)
        self.create_comment(c3)
        c4 = reddit_pb2.Comment(
            author=user2, text="comment4", parent_post_id=p0.post_id)
        self.create_comment(c4)
        self.vote_comment(c0.comment_id, "user1", True)
        self.vote_comment(c0.comment_id, "user2", True)
        self.vote_comment(c0.comment_id, "user3", True)
        self.vote_comment(c2.comment_id, "user1", True)
        self.vote_comment(c2.comment_id, "user2", True)
        self.vote_comment(c4.comment_id, "user1", True)
        self.vote_comment(c4.comment_id, "user2", True)
        self.vote_comment(c1.comment_id, "user1", False)

        c00 = reddit_pb2.Comment(
            author=user1, text="comment00", parent_comment_id=c0.comment_id)
        self.create_comment(c00)
        c01 = reddit_pb2.Comment(
            author=user2, text="comment01", parent_comment_id=c0.comment_id)
        self.create_comment(c01)
        c02 = reddit_pb2.Comment(
            author=user2, text="comment02", parent_comment_id=c0.comment_id)
        self.create_comment(c02)
        c03 = reddit_pb2.Comment(
            author=user3, text="comment03", parent_comment_id=c0.comment_id)
        self.create_comment(c03)
        self.vote_comment(c00.comment_id, "user1", True)
        self.vote_comment(c00.comment_id, "user2", True)
        self.vote_comment(c00.comment_id, "user3", True)
        self.vote_comment(c02.comment_id, "user1", True)
        self.vote_comment(c02.comment_id, "user2", True)
        self.vote_comment(c03.comment_id, "user1", False)

        c000 = reddit_pb2.Comment(
            author=user1, text="comment000", parent_comment_id=c00.comment_id)
        self.create_comment(c000)
        c001 = reddit_pb2.Comment(
            author=user2, text="comment001", parent_comment_id=c00.comment_id)
        self.create_comment(c001)
        c002 = reddit_pb2.Comment(
            author=user2, text="comment002", parent_comment_id=c00.comment_id)
        self.create_comment(c002)
        self.vote_comment(c000.comment_id, "user1", True)
        self.vote_comment(c000.comment_id, "user2", True)
        self.vote_comment(c000.comment_id, "user3", True)
        self.vote_comment(c002.comment_id, "user1", True)
        self.vote_comment(c002.comment_id, "user2", True)
        self.vote_comment(c001.comment_id, "user1", False)

        # even the hidden comment has high score, it will not be shown
        hidden_comment = reddit_pb2.Comment(
            author=user1, text="hidden_comment",
            parent_post_id=p0.post_id,
            comment_state=reddit_pb2.CommentState.COMMENT_STATE_HIDDEN)
        self.create_comment(hidden_comment)
        hidden_comment.score = 100


if __name__ == "__main__":
    reddit_controller = RedditNativeController()
    reddit_controller.init()
    print("retrieve_n_most_upvoted_comment; post:0, n:2")
    print(reddit_controller.retrieve_n_most_upvoted_comment(0, 2))
    print("=======================================")
    print("retrieve_comment_branch; comment:0, n:2")
    print(reddit_controller.retrieve_comment_branch(0, 2))
