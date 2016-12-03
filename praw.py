import praw
import time

r = praw.Reddit(user_agent = "Created by Nicholas Moore")
print("Logging in...")

infile = open('pass.txt', 'r')
password = infile.readline()
infile.close()
r.login('HighResolutionBot', password)

keyWord = ['!hiresbot', 'hiresbot']
cache = []

def run_bot():
    print("Grabbing subreddit...")
    subreddit = r.get_subreddit("test")
    print("Grabbing comments...")
    comments = subreddit.get_comments(limit = 200)
    for comment in comments:
        comment_text = comment.body.lower()
        isMatch = any(string in comment_text for string in keyWord)
        if comment.id not in cache and isMatch:
            print("Match found! Comment ID: " + comment.id)
            print("Finding submission URL...")
            # Grab the submission's image URL linked to the comment
            submissionURL = comment.submission.url


            # comment.reply("Highest resolution image goes here")
            print("Reply successful!")
            cache.append(comment.id)
    print("Comments loop finished, time to sleep")

while True:
    run_bot()
    time.sleep(10)
