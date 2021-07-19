import os
import discord


client = discord.Client()

@client.event
async def on_ready():
  print('It Works! {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$valorant'):
    await message.channel.send('https://playvalorant.com/en-us/news/')

  if message.content.startswith('$reddit'):
    await message.channel.send('https://www.reddit.com/r/ValorantCompetitive/')

  if message.content.startswith('$pbe'):
    await message.channel.send('https://www.reddit.com/r/ValorantPBE/')

  if message.content.startswith('$help'):
    await message.channel.send('Commands:\n$valorant : Link to playVALORANT News page\n$')

client.run(os.environ['TOKEN'])
