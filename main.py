import os
import discord
import asyncpraw
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
from replit import db

# intializes reddit with necessary information
reddit = asyncpraw.Reddit(client_id=os.environ['CLIENTID'],
                     client_secret=os.environ['CLIENTSECRET'],
                     user_agent=os.environ['USERAGENT'],
                     username = os.environ['REDDITUSERNAME'],
                     password = os.environ['REDDITPASSWORD'])
                  
client = commands.Bot(command_prefix='$') # Set command prefix

# Sets notification when the bot is ready and sets the activity of the bot
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('For Help: $commands'))
  print('Bot is now active! {0.user}'.format(client))

# Sets $commands as the help command. Displays different commands and their functions
@client.command()
async def commands(ctx):
  embed = discord.Embed(title='Commands',descrption='Lists all commands that are currently implemented in the bot! Prefix: $', color=0x0fe0e0)
  embed.add_field(name='$valorant', value='Link to [playVALORANT News page](https://playvalorant.com/en-us/news/)')
  embed.add_field(name='$mainreddit', value='Link to [r/VALORANT](https://www.reddit.com/r/VALORANT/)')
  embed.add_field(name='$compreddit', value='Link to [r/ValorantCompetitive](https://www.reddit.com/r/ValorantCompetitive)')
  embed.add_field(name='$pbereddit', value='Link to [r/ValorantPBE](https://www.reddit.com/r/ValorantPBE/)')
  embed.add_field(name='$search', value='Search a subreddit for the top post. Use format: $search Subreddit SearchQuery Time NumberOfPosts. Time should be: hour, day, week, month, year, or all')
  embed.add_field(name='$hot', value='Search a subreddit for most recent hot posts. Use format: $hot Subreddit NumberOfPosts')
  embed.add_field(name='$matches', value='Sends most recent Post-Match-Discussions from the past 24 hours.')
  embed.add_field(name='$digest', value='Sends most recent VALORANT news from the past 24 hours.')
  await ctx.send(embed=embed)

# Creates $valorant command that sends a link to the Valorant News Page
@client.command()
async def valorant(ctx):
  embed = discord.Embed()
  embed.description = ('[Valorant News Page](https://playvalorant.com/en-us/news/)')
  await ctx.send(embed=embed)

# Creates $mainreddit command that sends a link to the playVALORANT Reddit page
@client.command()
async def mainreddit(ctx):
  embed = discord.Embed()
  embed.description = ('[r/VALORANT](https://www.reddit.com/r/VALORANT/)')
  await ctx.send(embed=embed)

# Creates $compreddit command that sends a link to the VALORANTCompetitve Reddit page
@client.command()
async def compreddit(ctx):
  embed = discord.Embed()
  embed.description = ('[r/ValorantCompetitive](https://www.reddit.com/r/ValorantCompetitive)')
  await ctx.send(embed=embed) 

# Creates $pbereddit command that sends a link to the VALORANT PBE Reddit page
@client.command()
async def pbereddit(ctx):
  embed = discord.Embed()
  embed.description = ('[r/ValorantPBE](https://www.reddit.com/r/ValorantPBE/)')
  await ctx.send(embed=embed) 

# Creates $search command that scrapes Reddit for a specific type of post
@client.command()
async def search(ctx, *args):
  if len(args) != 4:
    await ctx.send('Please re-try your search with the proper number of arguments.')
  else:
    subreddit = await reddit.subreddit(args[0])
    embed = discord.Embed(title='Your Reddit Search:', description="These are the top results for your search", color=0x0000ff)
    async for submission in subreddit.search(args[1], time_filter=args[2], limit=int(args[3])):
      title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
      embed.add_field(name=title, value='[Source]('+submission.url+')')
    await ctx.send(embed=embed)

# Creates $hot command that scrapes Reddit for the top posts from a specific subreddit
@client.command()
async def hot(ctx, *args):
  if len(args) != 2:
    await ctx.send('Please re-try your search with the proper number of arguments.')
  subreddit = await reddit.subreddit(args[0])
  count = 0
  embed = discord.Embed(title='HOT posts from your subreddit:', description="These are the HOT posts from " + args[0], color=0x0000ff)
  async for submission in subreddit.hot():
    if int(args[1]) != count:
      title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
      embed.add_field(name=title, value='[Source]('+submission.url+')')
      count += 1
  await ctx.send(embed=embed)

# Creates $matches command that scrapes Reddit for th emost recent Post-Match Discussions
@client.command()
async def matches(ctx):
  check = False
  subreddit = await reddit.subreddit('VALORANTCompetitive')
  embed = discord.Embed(title='Most Recent Valorant Matches:', description="Sends all of the most recent Valorant Esport Post-Match Discussions!", color=0xf0f0f0)
  async for submission in subreddit.search(query='Post-Match Discussion',sort='new',time_filter='day',limit=6):
    check = True
    teams = submission.title.split('/')
    game = teams[1]
    teams = teams[0][:-1]
    embed.add_field(name=teams, value='['+game+']('+submission.url+')')
  if check == True:
    await ctx.send(embed=embed)
  else:
    await ctx.send('No new Post-Match Discussions')

# Creates $digest that sends the latest playVALORANT subreddit posts that are flaired as News
@client.command()
async def digest(ctx):
      subreddit = await reddit.subreddit('VALORANT')
      check = False
      embed = discord.Embed(title='Valorant News Digest:', description="All of the most recent playVALORANT news!", color=0x00ff00)
      async for submission in subreddit.search(query='flair:"News"',syntax='lucene',time_filter='month',limit=9):
        check = True
        title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
        embed.add_field(name=title, value='[Source]('+submission.url+')')
      if check == True:
        await ctx.send(embed=embed)

async def gamenews():
    while True:
      await client.wait_until_ready()
      channel = client.get_channel(866418599300038721)
      subreddit = await reddit.subreddit('VALORANT')
      check = False
      embed = discord.Embed(title='Latest VALORANT News:', color=0x00ff00)
      async for submission in subreddit.search(query='flair:"News"',syntax='lucene',time_filter='hour',limit=6):
        if submission.id not in db.keys():
          check = True
          title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
          embed.add_field(name=title, value='[Source]('+submission.url+')')
          db[submission.id] = submission.title
      if check == True:
        await channel.send(embed=embed)
      await asyncio.sleep(60)

# Automatically sends the latest VALORANT subreddit with the flair "Esports"
async def valorantesports():
    while True:
      await client.wait_until_ready()
      channel = client.get_channel(866418599300038721)
      subreddit = await reddit.subreddit('VALORANT')
      check = False
      embed = discord.Embed(title='New Esports News!', color=0xf0ff0f)
      async for submission in subreddit.search(query='flair:"Esports"',syntax='lucene',time_filter='hour',limit=3):
        if submission.id not in db.keys():
          check = True
          title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
          embed.add_field(name=title, value='[Source]('+submission.url+')')
          db[submission.id] = submission.title
      if check == True:
        await channel.send(embed=embed)
      await asyncio.sleep(60)

# Automatically sends the latest VALORANTCompetitive subreddit posts that are post match discussions
async def esportsdiscussions():
    while True:
      await client.wait_until_ready()
      channel = client.get_channel(866418599300038721)
      subreddit = await reddit.subreddit('VALORANTCompetitive')
      check = False
      embed = discord.Embed(title='New Post-Match Discussion!', color=0xff0000)
      async for submission in subreddit.search(query='Post-Match Discussion', time_filter='hour',limit=3):
        if submission.id not in db.keys():
          check = True
          teams = submission.title.split('/')
          game = teams[1]
          teams = teams[0][:-1]
          embed.add_field(name=teams, value='['+game+']('+submission.url+')')
          db[submission.id] = submission.title
      if check == True:
        await channel.send(embed=embed)
      await asyncio.sleep(60)

# Automatically sends the latest VALORANTCompetitive subreddit posts that are flaired with News & Events
async def esportsnews():
    while True:
      await client.wait_until_ready()
      channel = client.get_channel(866418599300038721)
      subreddit = await reddit.subreddit('VALORANTCompetitive')
      check = False
      embed = discord.Embed(title='New Esports News!', color=0xff0ff0)
      async for submission in subreddit.search(query='flair:"News & Events | Esports"', syntax='lucene', time_filter='hour',limit=3):
        if submission.id not in db.keys():
          check = True
          teams = submission.title.split('/')
          game = teams[1]
          teams = teams[0][:-1]
          embed.add_field(name=teams, value='['+game+']('+submission.url+')')
          db[submission.id] = submission.title
      if check == True:
        await channel.send(embed=embed)
      await asyncio.sleep(60)

async def clear_database():
  while True:
    await client.wait_until_ready()
    if len(db) >= 250:
      for i in db.keys():
        del db[i]
    await asyncio.sleep(86400)

# Loops both tasks constantly
client.loop.create_task(gamenews())
client.loop.create_task(esportsdiscussions())
client.loop.create_task(esportsnews())
client.loop.create_task(clear_database())

# Function to keep the webserver up
keep_alive()

# Runs the bot with a specific token
client.run(os.environ['TOKEN'])