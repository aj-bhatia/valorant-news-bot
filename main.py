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
client.remove_command('help')

sentposts = []

# Sets notification when the bot is ready and sets the activity of the bot
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('For Help: $help'))
  print('Bot is now active! {0.user}'.format(client))

# Sets $commands as the help command. Displays different commands and their functions
@client.command()
async def help(ctx):
  embed = discord.Embed(title='Help',description='Lists all commands that are currently implemented in the bot!\nNOTE: Without setting a channel using this command, the bot will NOT send automatic messages.\nPrefix: $', color=0x0fe0e0)
  embed.add_field(name='$valorant', value='Link to [playVALORANT News page](https://playvalorant.com/en-us/news/)')
  embed.add_field(name='$mainreddit', value='Link to [r/VALORANT](https://www.reddit.com/r/VALORANT/)')
  embed.add_field(name='$compreddit', value='Link to [r/ValorantCompetitive](https://www.reddit.com/r/ValorantCompetitive)')
  embed.add_field(name='$pbereddit', value='Link to [r/ValorantPBE](https://www.reddit.com/r/ValorantPBE/)')
  embed.add_field(name='$search', value='Search r/VALORANTCompetitivefor the top post with a specific search query.')
  embed.add_field(name='$hot', value='Search r/VALORANTCompetitive for most recent hot posts.')
  embed.add_field(name='$matches', value='Sends most recent Post-Match-Discussions from the past 24 hours.')
  embed.add_field(name='$digest', value='Sends most recent VALORANT news from the past 24 hours.')
  embed.add_field(name='$addchannel',value='Sets the channel where all automatic messages will be sent. Use this command in whichever channel you would like to recieve the notifications.')
  embed.add_field(name='$removechannel',value='Removes the channel where all automatic messages will be sent. Use this command in whichever channel you would like to remove.')
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

# Creates $compreddit command that sends a link to the VALORANTCompetitive Reddit page
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
async def addchannel(ctx):
  check = False
  for i in db.keys():
    if int(ctx.channel.id) == int(i):
      check = True
      await ctx.send('This channel is already added.')
  if check == False:
    db[ctx.channel.id] = ctx.guild.id
    await ctx.send('This channel has been added!')

@client.command()
async def removechannel(ctx):
  check = False
  for i in db.keys():
    if int(ctx.channel.id) == int(i):
      check = True
      del db[i]
      await ctx.send('This channel has been removed!')
  if check == False:
    await ctx.send('No channel is currently added.')

# Creates $search command that scrapes Reddit for a specific type of post
@client.command()
async def search(ctx, *args):
  if len(args) == 0:
    await ctx.send('Please re-try your search with a search query.')
  else:
    subreddit = await reddit.subreddit('VALORANTCompetitive')
    embed = discord.Embed(title='Your r/VALORANTCompetitive Search:', color=0x0000ff)
    async for submission in subreddit.search(args, time_filter='week', limit=9):
      embed.add_field(name=submission.title, value='[Source]('+submission.url+')')
    await ctx.send(embed=embed)

# Creates $hot command that scrapes Reddit for the top posts from a specific subreddit
@client.command()
async def hot(ctx):
  subreddit = await reddit.subreddit('VALORANTCompetitive')
  count = 0
  embed = discord.Embed(title='HOT posts r/VALORANTCompetitive:', color=0x0000ff)
  async for submission in subreddit.hot():
    if count != 12:
      embed.add_field(name=submission.title, value='[Source]('+submission.url+')')
      count += 1
  await ctx.send(embed=embed)

# Creates $matches command that scrapes Reddit for th emost recent Post-Match Discussions
@client.command()
async def matches(ctx):
  check = False
  discussions = []
  subreddit = await reddit.subreddit('VALORANTCompetitive')
  embed = discord.Embed(title='Most Recent Valorant Matches:', color=0xf0f0f0)
  async for submission in subreddit.search(query='flair:"Discussion | Esports"',sort='new',time_filter='day', limit=50):
          discussions.append(submission.id)
  async for submission in subreddit.search(query='Post-Match Discussion',sort='new',time_filter='day',limit=9):
    if submission.id in discussions:
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
    embed.add_field(name=submission.title, value='[Source]('+submission.url+')')
  if check == True:
    await ctx.send(embed=embed)

async def gamenews():
    while True:
      await client.wait_until_ready()
      counter = 1
      for cid in db.keys():
        channel = client.get_channel(int(cid))
        subreddit = await reddit.subreddit('VALORANT')
        check = False
        embed = discord.Embed(title='Latest VALORANT News:', color=0x00ff00)
        async for submission in subreddit.search(query='flair:"News"',syntax='lucene',time_filter='hour',limit=10):
          if submission.id not in sentposts:
            check = True 
            embed.add_field(name=submission.title, value='[Source]('+submission.url+')')
            if counter == len(db.keys()):
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
      for cid in db.keys():
        check = False
        channel = client.get_channel(int(cid))
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
      live = []
      for cid in db.keys():
        channel = client.get_channel(int(cid))
        subreddit = await reddit.subreddit('VALORANTCompetitive')
        check = False
        embed = discord.Embed(title='New Esports News!', color=0xff0ff0)
        async for submission in subreddit.search(query='Live Discussion Thread',sort='new',time_filter='day', limit=50):
          live.append(submission.id)
        async for submission in subreddit.search(query='flair:"News & Events | Esports"', syntax='lucene', time_filter='hour',limit=12):
          if submission.id not in sentposts and submission.id not in live:
            check = True
            embed.add_field(name=submission.title, value='[Source]('+submission.url+')')
            if counter == len(db.keys()):
              sentposts.append(submission.id)
        if check == True:
          await channel.send(embed=embed)
        counter += 1
      await asyncio.sleep(60)

# Loops all tasks constantly
client.loop.create_task(gamenews())
client.loop.create_task(esportsdiscussions())
client.loop.create_task(esportsnews())

"""Test Commands"""
#@client.command()
#async def get_database(ctx):
#  counter = 1
#  for i in db.keys():
#    await ctx.send('{}. {}: {}'.format(counter, i, db[i]))
#    counter += 1
#  if len(db.keys()) == 0:
#    await ctx.send("The database is empty")

#@client.command()
#async def get_posts(ctx):
#  counter = 1
#  for i in sentposts:
#    await ctx.send('{}. {}'.format(counter, i))
#    counter += 1

#@client.command()
#async def clear_database(ctx):
#  for i in db.keys():
#    del db[i]
#  await ctx.send("Done!")

#@client.command()
#async def clear_chat(ctx):
#

# Function to keep the webserver up
keep_alive()

# Runs the bot with a specific token
client.run(os.environ['TOKEN'])