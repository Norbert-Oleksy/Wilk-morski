import discord
import os

client = discord.Client()

@client.event
async def on_ready():
  print('Zalogowano jako {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$Witam'):
    await message.channel.send('Ahoj!')


client.run(os.environ['TOKEN'])
