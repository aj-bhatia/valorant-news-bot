import os
import praw

reddit = praw.Reddit(client_id=os.environ['CLIENTID'],      # your client id
                     client_secret=os.environ['CLIENTSECRET'],  #your client secret
                     user_agent='scrape', #user agent name
                     username = os.environ['USERNAME'],     # your reddit username
                     password = os.environ['REDDITPASSWORD'])     # your reddit password

#subreddit = await reddit.subreddit('VALORANTCompetitive')
#async for submission in subreddit.search('VALORANT North America','relevance','lucene','day'):
  #url = submission.url
  #title = submission.title
  #check = True
  #embed.description = '['+title+']('+url+')'
  #await ctx.send(embed=embed)
def scrape():
  for submission in reddit.subreddit("valorant").hot(limit=5):
    print(submission.title)
      