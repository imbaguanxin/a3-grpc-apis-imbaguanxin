from models import Post, Comment, PostState, CommentState, URLType


class RedditController:
    def __init__(self):
        self.posts = {}
        self.post_votes = {}
        self.comments = {}
        self.comments_votes = {}
        self.users = set()
        self.post_count = 0
        self.comment_count = 0

    def create_user(self, user_id):
        """Create a user with user_id, return True if success, False if user_id already exists"""
        if user_id in self.users:
            return False
        else:
            self.users.add(user_id)
            return True

    def create_post(self, title, text,
                    url=None, url_type=None, author=None,
                    score=0, post_state=PostState.NORMAL):
        """Create a post, return the post object"""
        post = Post(self.post_count, title, text, url,
                    url_type, author, score, post_state)
        self.posts[self.post_count] = post
        self.post_count += 1
        self.post_votes[post.post_id] = {
            "upvote": set(), "downvote": set()
        }
        return post

    def create_comment(self, author, text,
                       parent_post_id=None, parrent_comment_id=None,
                       score=0, comment_state=CommentState.NORMAL):
        comment = Comment(self.comment_count, author, text,
                          parent_post_id, parrent_comment_id,
                          score, comment_state)
        """Create a comment, return the comment object"""
        self.comments[self.comment_count] = comment
        self.comment_count += 1
        self.comments_votes[comment.comment_id] = {
            "upvote": set(), "downvote": set()
        }
        return comment

    def get_post(self, post_id):
        """Return the post object if post_id exists, otherwise return None"""
        post = self.posts.get(post_id, None)
        if post is None:
            return None
        if post.post_state == PostState.HIDDEN:
            return None
        return post

    def get_comment(self, comment_id):
        """Return the comment object if comment_id exists, otherwise return None"""
        comment = self.comments.get(comment_id, None)
        if comment is None:
            return None
        if comment.comment_state == CommentState.HIDDEN:
            return None
        return comment

    def vote_post(self, post_id, user_id, is_upvote):
        """
        Vote a post, return True if success, 
        False if user_id already voted or post_id not exists
        """
        post = self.get_post(post_id)
        if post is None:
            return False

        if is_upvote:
            if user_id in self.post_votes[post_id]["upvote"]:
                return False
            if user_id in self.post_votes[post_id]["downvote"]:
                self.post_votes[post_id]["downvote"].remove(user_id)
                post.score += 1
            self.post_votes[post_id]["upvote"].add(user_id)
            post.score += 1
        else:
            if user_id in self.post_votes[post_id]["downvote"]:
                return False
            if user_id in self.post_votes[post_id]["upvote"]:
                self.post_votes[post_id]["upvote"].remove(user_id)
                post.score -= 1
            self.post_votes[post_id]["downvote"].add(user_id)
            post.score -= 1
        return True

    def vote_comment(self, comment_id, user_id, is_upvote):
        """
        Vote a comment, return True if success,
        False if user_id already voted or comment_id not exists
        """
        comment = self.get_comment(comment_id)
        if comment is None:
            return False

        if is_upvote:
            if user_id in self.comments_votes[comment_id]["upvote"]:
                return False
            if user_id in self.comments_votes[comment_id]["downvote"]:
                self.comments_votes[comment_id]["downvote"].remove(user_id)
                comment.score += 1
            self.comments_votes[comment_id]["upvote"].add(user_id)
            comment.score += 1
        else:
            if user_id in self.comments_votes[comment_id]["downvote"]:
                return False
            if user_id in self.comments_votes[comment_id]["upvote"]:
                self.comments_votes[comment_id]["upvote"].remove(user_id)
                comment.score -= 1
            self.comments_votes[comment_id]["downvote"].add(user_id)
            comment.score -= 1
        return True

    def retrieve_n_most_upvoted_comment_under_a_post(self, post_id, n):
        """
        Retrieve n most upvoted comments under a post,
        hidden comments are ignored,
        return a list of (comment, has_sub_comment)
        """
        post = self.get_post(post_id)
        # post not find
        if post is None:
            return []
        # find top n comments
        comments = []
        for comment in self.comments.values():
            if comment.parent_post_id == post_id:
                # comment is hidden, ignore
                if comment.comment_state == CommentState.HIDDEN:
                    continue
                comments.append(comment)
        comments = sorted(comments, key=lambda x: x.score, reverse=True)[:n]
        result = []
        # check if comment has sub comment
        for comment in comments:
            has_sub_comment = False
            for sub_comment in self.comments.values():
                if sub_comment.parrent_comment_id == comment.comment_id:
                    # sub comment is hidden, ignore
                    if sub_comment.comment_state == CommentState.HIDDEN:
                        continue
                    has_sub_comment = True
                    break
            result.append((comment, has_sub_comment))
        return result

    def retrieve_comment_branch(self, comment_id, n):
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
        # comment not find
        if comment is None:
            return []
        # find top n sub comments
        sub_comments = []
        for comment in self.comments.values():
            if comment.parrent_comment_id == comment_id:
                # sub comment is hidden, ignore
                if comment.comment_state == CommentState.HIDDEN:
                    continue
                sub_comments.append(comment)
        sub_comments = sorted(
            sub_comments, key=lambda x: x.score, reverse=True)[:n]

        # find top n sub sub comments
        result = []
        for sub in sub_comments:
            sub_sub_comments = []
            for subsub in self.comments.values():
                if subsub.parrent_comment_id == sub.comment_id:
                    # sub sub comment is hidden, ignore
                    if subsub.comment_state == CommentState.HIDDEN:
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
        self.create_user("user1")
        self.create_user("user2")
        self.create_user("user3")

        p0 = self.create_post("post1", "post1_content", author="user1")
        self.create_post("post2image", "post2_content_image",
                         author="user2", url="img.url.example",
                         url_type=URLType.IMAGE)
        self.create_post("post3video", "post3_content_video",
                         author="user3", url="video.url.example",
                         url_type=URLType.VIDEO)
        self.create_post("post4locked", "post4_content_locked",
                         author="user1", post_state=PostState.LOCKED)
        self.create_post("post5hidden", "post5_content_hidden",
                         author="user2", post_state=PostState.HIDDEN)

        c0 = self.create_comment(
            "user1", "comment0", parent_post_id=p0.post_id)
        c1 = self.create_comment(
            "user2", "comment1", parent_post_id=p0.post_id)
        c2 = self.create_comment(
            "user3", "comment2", parent_post_id=p0.post_id)
        self.vote_comment(c0.comment_id, "user1", True)
        self.vote_comment(c0.comment_id, "user2", True)
        self.vote_comment(c0.comment_id, "user3", True)
        self.vote_comment(c2.comment_id, "user1", True)
        self.vote_comment(c2.comment_id, "user2", True)
        self.vote_comment(c1.comment_id, "user1", False)

        c00 = self.create_comment(
            "user1", "comment00", parrent_comment_id=c0.comment_id)
        c01 = self.create_comment(
            "user2", "comment01", parrent_comment_id=c0.comment_id)
        c02 = self.create_comment(
            "user2", "comment02", parrent_comment_id=c0.comment_id)
        c03 = self.create_comment(
            "user3", "comment03", parrent_comment_id=c0.comment_id)
        self.vote_comment(c00.comment_id, "user1", True)
        self.vote_comment(c00.comment_id, "user2", True)
        self.vote_comment(c00.comment_id, "user3", True)
        self.vote_comment(c02.comment_id, "user1", True)
        self.vote_comment(c02.comment_id, "user2", True)
        self.vote_comment(c03.comment_id, "user1", False)

        c000 = self.create_comment(
            "user1", "comment000", parrent_comment_id=c00.comment_id)
        c001 = self.create_comment(
            "user2", "comment001", parrent_comment_id=c00.comment_id)
        c002 = self.create_comment(
            "user2", "comment002", parrent_comment_id=c00.comment_id)

        self.vote_comment(c000.comment_id, "user1", True)
        self.vote_comment(c000.comment_id, "user2", True)
        self.vote_comment(c000.comment_id, "user3", True)
        self.vote_comment(c002.comment_id, "user1", True)
        self.vote_comment(c002.comment_id, "user2", True)
        self.vote_comment(c001.comment_id, "user1", False)

        # even the hidden comment has high score, it will not be shown
        hidden_comment = self.create_comment(
            "user1", "hidden_comment",
            parent_post_id=p0.post_id,
            comment_state=CommentState.HIDDEN)
        hidden_comment.score = 100

if __name__ == "__main__":
    reddit_controller = RedditController()
    reddit_controller.init()
    print("retrieve_n_most_upvoted_comment; post:0, n:2")
    print(reddit_controller.retrieve_n_most_upvoted_comment_under_a_post(0, 2))
    print("retrieve_comment_branch; comment:0, n:2")
    print(reddit_controller.retrieve_comment_branch(0, 2))