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

    def get_posts(self, max_posts, min_comments, sub_name='guessmybf', sort_method='all', log_path='log.txt'):
        subreddit = self.reddit.subreddit(sub_name)
        hot_python = subreddit.top(sort_method, limit=max_posts)

        valid_posts = {}
        with open(log_path, 'w') as f:
            f.write(f'LOG CREATION: {datetime.now()}\n\n')
            f.write("Parameters:")
            f.write(f"max_posts: {max_posts}")
            f.write(f"min_comments: {min_comments}")

        for ii, submission in enumerate(hot_python):
            # ignore stickied posts
            if submission.stickied:
                continue

            # ignore submissions with insufficient comments
            comments = submission.comments.list()
            if len(comments) < min_comments:
                continue
            
            # ignore posts with insufficient title data
            title_info = TitleChecker(submission.title)
            if not title_info.is_valid:
                continue

            bf_votes = []
            for comment in comments:
                # ignore empty comments
                if not hasattr(comment, 'body'):
                    continue
                comm_bf = check_body_fat(comment.body)
                if comm_bf != 'empty':
                    bf_votes.append(''.join(filter(str.isdigit, comm_bf)))
                    # bf_votes.append([bf, comment.body]) # to see the vote's source comment

            if len(bf_votes) == 0:
                continue

            valid_post = BFpost(submission, title_info, bf_votes)
            # valid_post.print_post_info()
            valid_post.log_post(log_path)
            valid_posts[submission.id] = {
                "title": submission.title,
                "url": submission.url,
                "body_fat": title_info.body_fat,
                "age": title_info.age,
                "sex": title_info.sex,
                "height": title_info.height,
                "weight": title_info.weight,
                "file_name": valid_post.file_name,
                "votes": valid_post.votes
            }
            printProgressBar(ii, max_posts-1)

        with open('valid_posts.json', 'w') as f:
            print(f'Number of json file entries: {len(valid_posts)}')
            json.dump(valid_posts, f, indent=4)


if __name__ == "__main__":
    query = DataAssistant()
    query.get_posts(max_posts=10, min_comments=5)
