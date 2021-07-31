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

sentposts = []

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
  embed.add_field(name='$setchannel',value='Sets the channel where all automatic messages will be sent. NOTE: Without setting a channel using this command, the bot will NOT send automatic messages. Format: $setchannel ChannelName')
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

@client.command()
async def setchannel(ctx, channel: discord.TextChannel):
    if channel.id in db.values():  # check if the guild already exists in the db
      await ctx.send('You have already set a channel')
    #if channel in ctx.guild.text_channels:
      #await ctx.send('This channel does not exist, please try the command again.')
    else:  # add the guild and channel to the db
      db[ctx.guild.id] = channel.id
      await ctx.send('Channel has been added!')

# Creates $search command that scrapes Reddit for a specific type of post
@client.command()
async def search(ctx, *args):
  if len(args) != 4:
    await ctx.send('Please re-try your search with the proper number of arguments.')
  else:
    subreddit = await reddit.subreddit(args[0])
    embed = discord.Embed(title='Your Reddit Search:', description='These are the top results for your search', color=0x0000ff)
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
  embed = discord.Embed(title='HOT posts from your subreddit:', description='These are the HOT posts from ' + args[0], color=0x0000ff)
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
  embed = discord.Embed(title='Most Recent Valorant Matches:', color=0xf0f0f0)
  async for submission in subreddit.search(query='Post-Match Discussion',sort='new',time_filter='day',limit=9):
    check = True
    teams = submission.title.split('/')
    game = teams[1]
    teams = teams[0][:-1] if teams[0][-1] == ' ' else teams[0]
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
  embed = discord.Embed(title='Valorant News Digest:', description='All of the most recent playVALORANT news!', color=0x00ff00)
  async for submission in subreddit.search(query='flair:"News"',syntax='lucene',time_filter='month',limit=9):
    check = True
    title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
    embed.add_field(name=title, value='[Source]('+submission.url+')')
  if check == True:
    await ctx.send(embed=embed)

async def gamenews():
    while True:
      await client.wait_until_ready()
      counter = 1
      for cid in db.values():
        channel = client.get_channel(cid)
        subreddit = await reddit.subreddit('VALORANT')
        check = False
        embed = discord.Embed(title='Latest VALORANT News:', color=0x00ff00)
        async for submission in subreddit.search(query='flair:"News"',syntax='lucene',time_filter='hour',limit=10):
          if submission.id not in sentposts:
            check = True
            title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
            embed.add_field(name=title, value='[Source]('+submission.url+')')
            if counter == len(db.values()):
              sentposts.append(submission.id)
        if check == True:
          await channel.send(embed=embed)
        counter += 1
      await asyncio.sleep(60)

# Automatically sends the latest VALORANTCompetitive subreddit posts that are post match discussions
async def esportsdiscussions():
    while True:
      await client.wait_until_ready()
      counter = 1
      for cid in db.values():
        check = False
        channel = client.get_channel(cid)
        subreddit = await reddit.subreddit('VALORANTCompetitive')
        embed = discord.Embed(title='New Post-Match Discussion!', color=0xff0000)
        async for submission in subreddit.search(query='Post-Match Discussion',sort='new',time_filter='hour',limit=12):
          if submission.id not in sentposts:
            check = True
            teams = submission.title.split('/')
            game = teams[1]
            teams = teams[0][:-1] if teams[0][-1] == ' ' else teams[0]
            embed.add_field(name=teams, value='['+game+']('+submission.url+')')
            if counter == len(db):
              sentposts.append(submission.id)
        if check == True:
          await channel.send(embed=embed)
        counter += 1
      await asyncio.sleep(60)

# Automatically sends the latest VALORANTCompetitive subreddit posts that are flaired with News & Events
async def esportsnews():
    while True:
      await client.wait_until_ready()
      counter = 1
      for cid in db.values():
        channel = client.get_channel(cid)
        subreddit = await reddit.subreddit('VALORANTCompetitive')
        check = False
        embed = discord.Embed(title='New Esports News!', color=0xff0ff0)
        async for submission in subreddit.search(query='flair:"News & Events | Esports"', syntax='lucene', time_filter='hour',limit=10):
          if submission.id not in sentposts:
            check = True
            title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
            embed.add_field(name=title, value='[Source]('+submission.url+')')
            if counter == len(db.values()):
              sentposts.append(submission.id)
        if check == True:
          await channel.send(embed=embed)
        counter += 1
      await asyncio.sleep(60)

# Loops both tasks constantly
client.loop.create_task(gamenews())
client.loop.create_task(esportsdiscussions())
client.loop.create_task(esportsnews())

"""Test Commands"""
@client.command()
async def get_database(ctx):
  counter = 1
  for i in db.keys():
    await ctx.send('{}. {}: {}'.format(counter, i, db[i]))
    counter += 1

@client.command()
async def get_posts(ctx):
  counter = 1
  for i in sentposts:
    await ctx.send('{}. {}'.format(counter, i))
    counter += 1

# Function to keep the webserver up
keep_alive()

# Runs the bot with a specific token
client.run(os.environ['TOKEN'])