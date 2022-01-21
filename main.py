import discord
from discord.ext import commands
import os
from BotFun import listaMiast, pogoda, teleAdresat

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print('------')

@bot.command()
async def Witam(ctx):
  await ctx.send("Ahoj!")

@bot.command()
async def BotInfo(ctx):
  with open("README.txt", encoding='utf8') as inf:
    await ctx.send(inf.read().rstrip())
  inf.close()

@bot.command()
async def BotOpcje(ctx):
  with open("BotOptions.txt", encoding='utf8') as opt:
    await ctx.send(opt.read().rstrip())
  opt.close()

@bot.command()
async def Pogoda(ctx, *miasto):
  await ctx.send(pogoda(miasto))

@bot.command()
async def PogodaMiasta(ctx):
  await ctx.send(listaMiast())

@bot.command()
async def Kontakt(ctx, *osoba):
  await ctx.send(teleAdresat(osoba))
  
bot.run(os.environ['TOKEN'])
