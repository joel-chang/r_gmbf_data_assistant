import praw, requests, re
import urllib.request as ur
import time
import json
from datetime import datetime


download_dir = "img/"

def download_reddit(_url, _file_name):
    r = requests.get(_url)
    with open(download_dir + _file_name,"wb") as f:
        f.write(r.content)


def download_imgur(_url, _fpath):
    contents = ur.urlopen(_url)
    f = open(download_dir + _fpath, 'wb')
    f.write(contents.read())
    f.close()

def download_gallery_reddit(_id):
    from app import reddit
    post = reddit.submission(_id)
    gallery = []
    for i in post.media_metadata.items():
        url = i[1]['p'][0]['u']
        url = url.split("?")[0].replace("preview", "i")
        gallery.append(url)
        header = {'user-agent': 'python:img-downloader:0.1'}

    for i, img in enumerate(gallery):
        req = requests.get(img, headers=header)
        with open(download_dir + _id + '_' + str(i) + '.jpg', 'wb') as f:
            f.write(req.content)
            time.sleep(0.5)


class BFpost:
    
    def __init__(self, _id, _title_info, _votes,  _url) -> None:
        self.id = _id
        self.info = _title_info
        self.votes = _votes
        self.url = _url
        self.file_name = self.id + ".jpg"
        if "imgur" in self.url:
            download_imgur(self.url, self.file_name)
        elif "gallery" in self.url:
            download_gallery_reddit(self.id)
        else:
            download_reddit(self.url, self.file_name)        
    
    def print_post_info(self):
        print(50*"==")
        print(f"Post ID: {self.id}")
        print(" ")
        print("Post INFO:")
        self.info.print_info()
        print("Post VOTES: ")
        print(self.votes)
        print(" ")
        print("Post URL (for the images):")
        print(self.url)
        print(50*"==")
        print(" ")



    def log_post(self, dest):
        log_entry = '\n'
        log_entry += str(datetime.now().time())
        log_entry += "\n"+20*"=="+'\n' #r/badcode
        log_entry += f"Post ID: {self.id}\n"
        log_entry += "Post INFO:\n"
        log_entry += self.info.get_info()
        log_entry += "Post VOTES: \n"
        log_entry += json.dumps(self.votes, indent=4, sort_keys=True)
        log_entry += "\n"
        log_entry += "Post URL (for the images):\n"
        log_entry += self.url
        log_entry += "\n"+20*"=="+"\n"
        log_entry += "\n"

        with open(dest, 'a') as f:
            f.write(log_entry)

