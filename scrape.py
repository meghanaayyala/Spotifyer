import praw
reddit = praw.Reddit(client_id='cvj6G2C8Z4LVOplMPbIKAQ', client_secret='tQpEboGfFwKIZwpwRo81EuqTkMWLhA', user_agent='kpopscraper')




import pandas as pd
posts = []
ml_subreddit = reddit.subreddit('kpop')

for post in ml_subreddit.top(time_filter="year",limit=1000):
    if post.link_flair_text=='[MV]' or post.link_flair_text=='[Audio]' :
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created,post.link_flair_text])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created','link_flair_text'])
#print(posts)

# saving the dataframe
posts.to_csv('tomvdata.csv')
