from collections import Counter
from tabnanny import check
import praw
import json
from post import BFpost
from title_check import TitleChecker, check_body_fat
from datetime import datetime
from utils import printProgressBar


class DataAssistant:
    def __init__(self, config_path="praw_cred.json"):
        """Initialize a DataAssistant object.

        Args:
            log_path (str, optional): Path to store log of retrieved posts. Defaults to 'log.txt'.
        """
        self.load_cred_file(config_path)

    def load_cred_file(self, config_path):
        """Function to load credentials file for Reddit application.
        """
        pc = json.load(open(config_path, 'r'))
        self.reddit = praw.Reddit(client_id=pc['client_id'],
                                  client_secret=pc['client_secret'],
                                  username=pc['username'],
                                  password=pc['password'],
                                  user_agent=pc['user_agent'])

    def parse_post(self, submission, min_comments):
        # ignore stickied posts
        if submission.stickied:
            return None

        # ignore posts with insufficient title data
        title_info = TitleChecker(submission.title)
        if title_info.is_useful() is False:
            return None

        # ignore submissions with insufficient comments
        comments = submission.comments.list()
        if len(comments) < min_comments:
            return None

        # collect mentions of body fat from post's comments
        bf_votes = []
        for comment in comments:
            # ignore empty comments
            if not hasattr(comment, 'body'):
                continue

            # ignore comments with no mention of body fat percentage
            bf_mention_in_comment = check_body_fat(comment.body)
            if bf_mention_in_comment == 'empty':
                continue

            bf_votes.append(''.join(filter(str.isdigit, bf_mention_in_comment)))
            # bf_votes.append([bf, comment.body]) # to see the vote's source comment

        # ignore posts/submissions with no mentions of body fat percentage in the comments
        if len(bf_votes) == 0:
            return None

        return BFpost(submission, title_info, bf_votes)

    def get_posts(self, max_posts, min_comments, sub_name='guessmybf', log_path='log.txt', time_range='all'):
        print('Now running scraper with the following values:')
        print(f'Max # of posts: {max_posts}')
        print(f'Min number of comments a post should have: {min_comments}')
        print(f'Name of target subreddit: {sub_name}')
        print(f'Time_range: {time_range}')
        print(f'Outputting logs to the following destination: {log_path}')

        target_subreddit = self.reddit.subreddit(sub_name)
        top_posts = target_subreddit.top(limit=max_posts, time_filter=time_range)

        valid_posts = {}
        for submission_index, submission in enumerate(top_posts):
            valid_post = self.parse_post(submission, min_comments)
            if not valid_post:
                continue
            # valid_post.print_post_info()
            # valid_post.log_post(log_path)
            valid_posts[submission.id] = {
                "title": valid_post.title,
                "url": valid_post.url,
                "body_fat": valid_post.body_fat,
                "age": valid_post.age,
                "sex": valid_post.sex,
                "height": valid_post.height,
                "weight": valid_post.weight,
                "file_name": valid_post.file_name,
                "votes": valid_post.votes
            }
            printProgressBar(submission_index, max_posts-1)

        with open('valid_posts.json', 'w') as f:
            print(f'Number of json file entries: {len(valid_posts)}')
            json.dump(valid_posts, f, indent=4)


if __name__ == "__main__":
    query = DataAssistant()
    query.get_posts(max_posts=10, min_comments=5)
