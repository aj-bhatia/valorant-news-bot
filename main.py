import os
import discord
import asyncpraw
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
#from reddit import scrape

reddit = asyncpraw.Reddit(client_id=os.environ['CLIENTID'],      # your client id
                     client_secret=os.environ['CLIENTSECRET'],  #your client secret
                     user_agent='scrape', #user agent name
                     username = os.environ['USERNAME'],     # your reddit username
                     password = os.environ['REDDITPASSWORD'])     # your reddit password
                  
client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('For Help: $commands'))
  print('Bot is now active! {0.user}'.format(client))

@client.command()
async def commands(ctx):
  embed = discord.Embed(title='Commands',descrption='Lists all commands that are currently implemented in the bot!')
  embed.description = ('Prefix:$\nCommands:\n$valorant : Link to [playVALORANT News page](https://playvalorant.com/en-us/news/)\n$mainreddit : Link to [r/VALORANT](https://www.reddit.com/r/VALORANT/)\n$compreddit : Link to [r/ValorantCompetitive](https://www.reddit.com/r/ValorantCompetitive)\n$pbe : Link to [r/ValorantPBE](https://www.reddit.com/r/ValorantPBE/)\n$search : Search a subreddit for the top post. Use format: $search Subreddit SearchQuery Time NumberOfPosts. Time should be: hour, day, week, month, year, or all\n$hot : Search a subreddit for most recent hot posts. Use format: $hot Subreddit NumberOfPosts \n$matches : Sends most recent Post-Match-Discussions from the past 24 hours.')
  await ctx.send(embed=embed)

@client.command()
async def valorant(ctx):
  embed = discord.Embed()
  embed.description = ('[Valorant News Page](https://playvalorant.com/en-us/news/)')
  await ctx.send(embed=embed)

@client.command()
async def mainreddit(ctx):
  embed = discord.Embed()
  embed.description = ('[r/VALORANT](https://www.reddit.com/r/VALORANT/)')
  await ctx.send(embed=embed)

@client.command()
async def compreddit(ctx):
  embed = discord.Embed()
  embed.description = ('[r/ValorantCompetitive](https://www.reddit.com/r/ValorantCompetitive)')
  await ctx.send(embed=embed) 

@client.command()
async def pbe(ctx):
  embed = discord.Embed()
  embed.description = ('[r/ValorantPBE](https://www.reddit.com/r/ValorantPBE/)')
  await ctx.send(embed=embed) 

@client.command()
async def search(ctx, *args):
  if len(args) != 4:
    await ctx.send('Please re-try your search with the proper number of arguments.')
  else:
    subreddit = await reddit.subreddit(args[0])
    embed = discord.Embed(title='Your Reddit Search:', description="These are the top results for your search", color=0x0000ff)
    async for submission in subreddit.search(args[1], time_filter=args[2], limit=int(args[3])):
      title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
      embed.add_field(name=title, value='['+str(submission.author)+']('+submission.url+')')
    await ctx.send(embed=embed)

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
      embed.add_field(name=title, value='['+str(submission.author)+']('+submission.url+')')
      count += 1
  await ctx.send(embed=embed)

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

async def digest():
    while True:
      await client.wait_until_ready()
      channel = client.get_channel(866418599300038721)
      await asyncio.sleep(1800)
      subreddit = await reddit.subreddit('VALORANT')
      check = False
      embed = discord.Embed(title='Valorant News Digest:', description="Sends all of the most recent playVALORANT news!", color=0x00ff00)
      async for submission in subreddit.search(query='flair:"News"',syntax='lucene',time_filter='hour',limit=6):
        check = True
        title = submission.title[:60]+'...' if len(submission.title) > 60 else submission.title
        embed.add_field(name=title, value='['+str(submission.author)+']('+submission.url+')')
      if check == True:
        await channel.send(embed=embed)
      await asyncio.sleep(1800)

async def esports():
    while True:
      await client.wait_until_ready()
      channel = client.get_channel(866418599300038721)
      subreddit = await reddit.subreddit('VALORANTCompetitive')
      check = False
      embed = discord.Embed(title='Valorant E-Sports Digest:', description="Sends all of the most recent Post-Match Discussions!", color=0xff0000)
      async for submission in subreddit.search(query='Post-Match Discussion', time_filter='hour',limit=6):
        check = True
        teams = submission.title.split('/')
        game = teams[1]
        teams = teams[0][:-1]
        embed.add_field(name=teams, value='['+game+']('+submission.url+')')
      if check == True:
        await channel.send(embed=embed)
      await asyncio.sleep(3600)

client.loop.create_task(digest())
client.loop.create_task(esports())

keep_alive()

client.run(os.environ['TOKEN'])


