import discord
import ctypes
import os, sys


# TODO: Add screenshot command


token = 'MTEzODU0OTQwMzc4Nzk5MzEwOA.GFtI4Y.vG5H3YYi2ELg4ZL_8IOwKLT9m2csx3cXdID--w'
bot = discord.Bot()

def getTime():
  time = os.popen('time /t').read()
  return str(time)

def getUptime():
  lib = ctypes.windll.kernel32
  t = lib.GetTickCount64()
  t = int(str(t)[:-3])
  mins, sec = divmod(t, 60)
  hour, mins = divmod(mins, 60)
  days, hour = divmod(hour, 24)
  return(f'{days} days, {hour:02}:{mins:02}')
  

@bot.event
async def on_ready():
  for guild in bot.guilds:
    print('------------------------------------------')
    print(f'- {guild.id} (name: {guild.name})')
  print('Status: READY')

@bot.slash_command(name = 'heartbeat', description = 'Check if PC is still on')
async def heartbeat(ctx):
  await ctx.respond('Response: ' + getTime())
  
@bot.slash_command(name = 'cmd', description = 'Pass a command to PC')
async def passcmd(ctx, command):
  out = os.popen(command).read()
  if out != '':
    await ctx.send(out)
  else:
    await ctx.send('Command returned a blank string')
  
@bot.slash_command(name = 'cmd', description = 'Pass a command to PC')
async def passcmd(ctx, command):
  out = os.popen(command).read()
  await ctx.send(out)

@bot.slash_command(name = 'uptime', description = 'Get computer uptime')
async def uptime(ctx):
  time = getUptime()
  await ctx.send(time)

def start():
  bot.run(token)
  
start()