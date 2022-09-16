from collections import Counter
from tabnanny import check
import praw
import json
from post import BFpost
from title_check import TitleChecker, check_body_fat
from datetime import datetime
from utils import printProgressBar


class DataAssistant:
    def load_parameters(self, config_path="praw_cred.json", max_posts=10, min_comments=5, sort_method='all', log_path='log.txt'):
        self.config_path = config_path
        self.max_posts = max_posts
        self.min_comments = min_comments
        self.sort_method = sort_method
        self.log_path = log_path

    def load_cred_file(self):
        pc = json.load(open(self.config_path, 'r'))

        self.reddit = praw.Reddit(client_id=pc['client_id'],
                                  client_secret=pc['client_secret'],
                                  username=pc['username'],
                                  password=pc['password'],
                                  user_agent=pc['user_agent'])

        self.subreddit = self.reddit.subreddit('guessmybf')

    def get_posts(self):
        subreddit = self.subreddit
        max_posts = self.max_posts
        min_comments = self.min_comments
        sort_method = self.sort_method
        hot_python = subreddit.top(sort_method, limit=max_posts)
        log_path = self.log_path

        person = {}
        valid_posts = {}

        with open(log_path, 'w') as f:
            f.write(f'LOG CREATION: {datetime.now()}\n\n')
            f.write("Parameters:")
            f.write(f"max_posts: {max_posts}")
            f.write(f"min_comments: {min_comments}")

        for ii, submission in enumerate(hot_python):
            if submission.stickied:
                # ignore stickied posts
                continue
            comments = submission.comments.list()
            title_info = TitleChecker(submission.title)
            # ignore posts with insufficient title data
            if not title_info.is_valid:
                continue
            # ignore posts with insufficient comments
            if len(comments) < min_comments:
                continue

            # find mentions of body fat in each comment
            # this is dumb, should use regex
            bf_votes = []
            for comment in comments:
                if not hasattr(comment, 'body'):
                    continue
                comm_bf = check_body_fat(comment.body)
                if comm_bf != 'empty':
                    bf_votes.append(''.join(filter(str.isdigit, comm_bf)))
                    # bf_votes.append([bf, comment.body]) # to see the vote's source comment

            votes_list = Counter(bf_votes)
            if len(votes_list) == 0:
                continue

            valid_post = BFpost(submission, title_info, votes_list)
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
    query.load_parameters()
    query.load_cred_file()
    query.get_posts()
