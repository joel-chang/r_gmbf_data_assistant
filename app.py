from collections import defaultdict
import praw
import json
from post import BFpost
from title_check import TitleChecker
from data_population import DataPopulation
from datetime import datetime


pc = json.load(open("praw_cred.json", 'r'))

reddit = praw.Reddit(client_id=pc['client_id'],
                     client_secret=pc['client_secret'],
                     username=pc['username'],
                     password=pc['password'],
                     user_agent=pc['user_agent'])

subreddit = reddit.subreddit('guessmybf')

max_posts = 1600
min_comments = 1
hot_python = subreddit.top("all", limit=max_posts)

possible = DataPopulation()

person = {}
valid_posts = {}

log_path = 'log.txt'
with open(log_path, 'w') as f:
    f.write(f'LOG CREATION: {datetime.now()}\n\n')
    f.write("Parameters:")
    f.write(f"max_posts: {max_posts}")
    f.write(f"min_comments: {min_comments}")

for ii, submission in enumerate(hot_python):
    print(f"\nCurrently at submission #{ii}.")
    if submission.stickied:
        continue
    print("Current submission ID: " + str(submission.id))
    comments = submission.comments.list()
    title_info = TitleChecker(submission.title)
    if not title_info.is_valid:
        print("Title info is not valid.")
        continue
    if len(comments) < min_comments:
        print(f"Submission #{ii} ID: {submission.id} has less than {min_comments}.")
        continue
    bf_votes = []
    for comment in comments:
        for bf in possible.bfs:
            if hasattr(comment, 'body') and comment.body.find(bf) != -1:
                bf_votes.append(''.join(filter(str.isdigit, bf)))
                # bf_votes.append([bf, comment.body]) # to see the vote's source comment
    votes_list = defaultdict(int)
    for vote in bf_votes:
        votes_list[vote] += 1
    if len(votes_list) == 0:
        continue

    valid_post = BFpost(submission.id, title_info,
                        votes_list, submission.url)
    valid_post.print_post_info()
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
    # printProgressBar(ii, max_posts)

with open('valid_posts.json', 'w') as f:
    print(f'Number of json file entries: {len(valid_posts)}')
    json.dump(valid_posts, f, indent=4)
