import os
import discord
import asyncpraw
import asyncio
from discord.ext import commands
from discord.utils import find
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
  print('I\'m in ' + str(len(client.guilds)) + ' servers! {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello! Thanks for adding me to your server! If you would like to recieve automatic Valorant News please use $addchannel to add a channel for the bot to send the news to. If you would like to access other commands, please browse the current features with $help.')

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Error! Command not found. Please look at the $help menu for viable commands.")
    pass
  else:
    raise error

@client.event
async def on_guild_channel_delete(channel):
  if str(channel.id) in db.keys():
    del db[str(channel.id)]
    print('A Channel has been deleted. It has been removed from the database.')

@client.event
async def on_guild_remove(guild):
  for i in guild.channels:
    if str(i.id) in db.keys():
      del db[str(i.id)]
      print ('Server has been deleted. Channel has been removed from the database.')

# Sets $commands as the help command. Displays different commands and their functions
@client.command()
async def help(ctx):
  embed = discord.Embed(title='Help Menu',description='Lists all commands that are currently implemented in the bot!\nNOTE: Without setting a channel using this command, the bot will NOT send automatic messages.\nPrefix: $\nIf you like this bot please consider giving it an upvote or review on top.gg\n(link in bot description)', color=0x0fe0e0)
  embed.add_field(name='$valorant', value='Link to [playVALORANT News page](https://playvalorant.com/en-us/news/)', inline=False)
  embed.add_field(name='$mainreddit', value='Link to [r/VALORANT](https://www.reddit.com/r/VALORANT/)', inline=False)
  embed.add_field(name='$compreddit', value='Link to [r/ValorantCompetitive](https://www.reddit.com/r/ValorantCompetitive)', inline=False)
  embed.add_field(name='$pbereddit', value='Link to [r/ValorantPBE](https://www.reddit.com/r/ValorantPBE/)', inline=False)
  embed.add_field(name='$feedback', value='Link to the [Feedback Form](https://forms.gle/FhKvyZV4aamjw8bGA)', inline=False)
  embed.add_field(name='$search', value='Search r/VALORANTCompetitivefor the top post with a specific search query.', inline=False)
  embed.add_field(name='$hot', value='Search r/VALORANTCompetitive for most recent hot posts.', inline=False)
  embed.add_field(name='$matches', value='Sends most recent Post-Match-Discussions from the past 24 hours.', inline=False)
  embed.add_field(name='$digest', value='Sends most recent VALORANT news from the past 24 hours.', inline=False)
  embed.add_field(name='$addchannel',value='Sets the channel where all automatic messages will be sent. Use this command in whichever channel you would like to recieve the notifications.', inline=False)
  embed.add_field(name='$removechannel',value='Removes the channel where all automatic messages will be sent. Use this command in whichever channel you would like to remove.', inline=False)
  embed.add_field(name='$sub', value='Subscribes to specific automatic news updates: gamenews, esportsnews, discussions, or all.', inline=False)
  embed.add_field(name='$unsub', value='Unsubscribes from specific automatic news updates: gamenews, esportsnews, discussions, or all.', inline=False)
  await ctx.send(embed=embed)

@help.error
async def help_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

# Creates $valorant command that sends a link to the Valorant News Page
@client.command()
async def valorant(ctx):
  await ctx.send(embed=discord.Embed(title='Valorant News Page', url='https://playvalorant.com/en-us/news/', color=0x301934))

@valorant.error
async def valorant_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

# Creates $mainreddit command that sends a link to the playVALORANT Reddit page
@client.command()
async def mainreddit(ctx):
  await ctx.send(embed=discord.Embed(title='r/VALORANT', url='https://www.reddit.com/r/VALORANT/', color=0x301934))

@mainreddit.error
async def mainreddit_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

# Creates $compreddit command that sends a link to the VALORANTCompetitive Reddit page
@client.command()
async def compreddit(ctx):
  await ctx.send(embed=discord.Embed(title='r/ValorantCompetitive', url='https://www.reddit.com/r/ValorantCompetitive', color=0x301934))

@compreddit.error
async def compreddit_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

# Creates $pbereddit command that sends a link to the VALORANT PBE Reddit page
@client.command()
async def pbereddit(ctx):
  await ctx.send(embed=discord.Embed(title='r/ValorantPBE', url='https://www.reddit.com/r/ValorantPBE/', color=0x301934))

@pbereddit.error
async def pbereddit_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

@client.command()
async def feedback(ctx):
  await ctx.send(embed=discord.Embed(title='Feedback Form', url='https://forms.gle/FhKvyZV4aamjw8bGA', color=0xFF5733))

@feedback.error
async def feedback_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

@client.command()
async def addchannel(ctx):
  check = False
  for i in db.keys():
    if int(ctx.channel.id) == int(i):
      check = True
      await ctx.send('This channel is already added.')
  if check == False:
    db[ctx.channel.id] = str(111)
    await ctx.send('This channel has been added!')

@addchannel.error
async def addchannel_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

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

@removechannel.error
async def removechannel_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

@client.command()
async def unsub(ctx, arg):
  cid = ctx.channel.id
  cid = str(cid)
  check1 = False
  check2 = False
  if cid in db.keys():
    check2 = True
  if str(arg) == 'gamenews' or str(arg) == 'esportsnews' or str(arg) == 'discussions' or str(arg) == 'all':
    check1 = True
  if check1 == True and check2 == True:
    if arg == 'all':
      db[cid] = '000'
      await ctx.send('This channel has been unsubscribed from all news updates.')
    if arg == 'gamenews':
      value = db[cid]
      if value[0] == '1':
        value = '0'+value[1:]
      db[cid] = value
      await ctx.send('This channel has been unsubscribed from game news updates.')
    if arg == 'esportsnews':
      value = db[cid]
      if value[1] == '1':
        value = value[0]+'0'+value[2]
      db[cid] = value
      await ctx.send('This channel has been unsubscribed from esports news updates.')
    if arg == 'discussions':
      value = db[cid]
      if value[2] == '1':
        value = value[:2]+'0'
      db[cid] = value
      await ctx.send('This channel has been unsubscribed from post-match discussions threads.')
  elif check1 == False and check2 == True:
    await ctx.send('Please enter the category of post you would like to unsubscribe from: gamenews, esportsnews, discussions, or all.')
  else:
    await ctx.send('This channel is not being sent auto-messages, please add the channel and then unsubscribe from specific post types.')

@unsub.error
async def unsub_error(ctx, error: commands.CommandError):
  if isinstance(error, commands.MissingRequiredArgument):
    message = 'Please re-try the command with a category to be unsubscribed from: gamenews, esportsnews, discussions, or all.'
  else:
    message = 'Oh no! Something went wrong while running the command! Please re-try the command.'
  await ctx.send(message)

@client.command()
async def sub(ctx, arg):
  cid = ctx.channel.id
  cid = str(cid)
  check1 = False
  check2 = False
  if cid in db.keys():
    check2 = True
  if str(arg) == 'gamenews' or str(arg) == 'esportsnews' or str(arg) == 'discussions' or str(arg) == 'all':
    check1 = True
  if check1 == True and check2 == True:
    if arg == 'all':
      db[cid] = '111'
      await ctx.send('This channel has been subscribed to all news updates.')
    if arg == 'gamenews':
      value = db[cid]
      if value[0] == '0':
        value = '1'+value[1:]
      db[cid] = value
      await ctx.send('This channel has been subscribed to game news updates.')
    if arg == 'esportsnews':
      value = db[cid]
      if value[1] == '0':
        value = value[0]+'1'+value[2]
      db[cid] = value
      await ctx.send('This channel has been subscribed to esports news updates.')
    if arg == 'discussions':
      value = db[cid]
      if value[2] == '0':
        value = value[:2]+'1'
      db[cid] = value
      await ctx.send('This channel has been subscribed to post-match discussions threads.')
  elif check1 == False and check2 == True:
    await ctx.send('Please enter the category of post you would like to subscribe to: gamenews, esportsnews, discussions, or all.')
  else:
    await ctx.send('This channel is not being sent auto-messages, please add the channel and then subscribe to specific post types.')

@sub.error
async def sub_error(ctx, error: commands.CommandError):
  if isinstance(error, commands.MissingRequiredArgument):
    message = 'Please re-try the command with a category to be subscribed to: gamenews, esportsnews, discussions, or all.'
  else:
    message = 'Oh no! Something went wrong while running the command! Please re-try the command.'
  await ctx.send(message)

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

@search.error
async def search_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

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

@hot.error
async def hot_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

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

@matches.error
async def matches_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

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

@digest.error
async def digest_error(ctx, error: commands.CommandError):
  await ctx.send('Oh no! Something went wrong while running the command! Please re-try the command. If this continues to not work, please submit a bug report to the feedback form.')

async def gamenews():
    while True:
      await client.wait_until_ready()
      posts = []
      for cid, val in db.items():
        check = False
        channel = client.get_channel(int(cid))
        subreddit = await reddit.subreddit('VALORANT')
        embed = discord.Embed(title='Latest VALORANT News:', color=0x00ff00)
        async for submission in subreddit.search(query='flair:"News"',syntax='lucene',time_filter='hour',limit=10):
          if submission.id not in sentposts:
            if submission.id not in posts:
              posts.append(submission.id)
            check = True 
            embed.add_field(name=submission.title, value='[Source]('+submission.url+')')
        if check == True and val[0] == '1':
          try:
            await channel.send(embed=embed)
          except:
            continue
      for i in posts:
        sentposts.append(i)
      await asyncio.sleep(120)

# Automatically sends the latest VALORANTCompetitive subreddit posts that are flaired with News & Events
async def esportsnews():
    while True:
      await asyncio.sleep(60)
      await client.wait_until_ready()
      posts = []
      live = []
      for cid, val in db.items():
        check = False
        channel = client.get_channel(int(cid))
        subreddit = await reddit.subreddit('VALORANTCompetitive')
        embed = discord.Embed(title='New Esports News!', color=0xff0ff0)
        async for submission in subreddit.search(query='Live Discussion Thread',sort='new',time_filter='day', limit=50):
          live.append(submission.id)
        async for submission in subreddit.search(query='flair:"News & Events | Esports"', syntax='lucene', time_filter='hour',limit=12):
          if submission.id not in sentposts and submission.id not in live:
            if submission.id not in posts:
              posts.append(submission.id)
            check = True
            embed.add_field(name=submission.title, value='[Source]('+submission.url+')')
        if check == True and val[1] == '1':
          try:
            await channel.send(embed=embed)
          except:
            continue
      for i in posts:
        sentposts.append(i)
      await asyncio.sleep(60)

# Automatically sends the latest VALORANTCompetitive subreddit posts that are post match discussions
async def esportsdiscussions():
    while True:
      await asyncio.sleep(30)
      await client.wait_until_ready()
      posts = []
      for cid, val in db.items():
        check = False
        channel = client.get_channel(int(cid))
        subreddit = await reddit.subreddit('VALORANTCompetitive')
        embed = discord.Embed(title='New Post-Match Discussion!', color=0xff0000)
        async for submission in subreddit.search(query='Post-Match Discussion',sort='new',time_filter='day',limit=9):
          if submission.id not in sentposts:
            if submission.id not in posts:
              posts.append(submission.id)
            check = True
            teams = submission.title.split('/')
            game = teams[1]
            teams = teams[0][:-1] if teams[0][-1] == ' ' else teams[0]
            embed.add_field(name=teams, value='['+game+']('+submission.url+')')
        if check == True and val[2] == '1':
          try:
            await channel.send(embed=embed)
          except:
            continue
      for i in posts:
        sentposts.append(i)
      await asyncio.sleep(90)

# Loops all tasks constantly
client.loop.create_task(gamenews())
client.loop.create_task(esportsnews())
client.loop.create_task(esportsdiscussions())

#"""Test Commands"""
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