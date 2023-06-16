# A file made for counting hours and minutes spent in a game (used for pirated games🤫)

try:
  import os, sys
  import time
  import win32com.client
except Exception as e:
  print(f'ERROR: {e}')
  time.sleep(5)
  sys.exit(1)


class vars:
  init_time = None
  end_time = None
  log_file = f'<GAME-FOLDER-PATH>/hourlog.txt'
  game = f"{'/'.join(log_file.split('/')[:-1])}/<GAME-EXECUTABLE>.exe"  # Just replaces the last '/' statment
  now = lambda: time.strftime('%Y-%m-%d %H:%M') + '\n'


def createShortcut(targetFile, iconFile):
  if 'coope' in os.getlogin(): desktop = f'C:/Users/coope/OneDrive/Desktop'
  else: os.path.normpath(os.path.expanduser('~/Desktop'))
  path = os.path.join(desktop, 'RainWorld.lnk')
  shell = win32com.client.Dispatch('WScript.Shell')
  shortcut = shell.CreateShortCut(path)
  shortcut.Targetpath = targetFile
  shortcut.IconLocation = iconFile
  shortcut.save()


def prerun():
  if not os.path.exists(vars.log_file):
    open(vars.log_file, 'w')
    print(f'Created log file - {vars.now()}')
  if '<' and '>' in vars.log_file:
    print("ERROR: Log_file variable still has placeholder '<' and '>'")
    time.sleep(5)
    sys.exit(1)
  if '<' and '>' in vars.game:
    print("ERROR: Game variable still has placeholder '<' and '>'")
    time.sleep(5)
    sys.exit(1)
  if os.path.getsize(vars.log_file) == 0:
    with open(vars.log_file, 'w') as f:
      f.writelines('game-time: 0')
      f.close()


def getHours():
  with open(vars.log_file, 'r') as r:
    hours = r.readline()
    r.close()
  return hours.replace('game-time: ', '')


def startGame():
  os.startfile(vars.game)
  print(f'Started Game - {vars.now()}')
  vars.init_time = time.time()


def convertTime():
  inTime = getHours()
  timestr = str(inTime)
  index = timestr.find('.')
  number = timestr[:index]

  hours = float(round(int(number) / 60 / 60, 2))
  return str(hours)


def postGame():
  vars.end_time = time.time()
  elapsed = vars.end_time - vars.init_time
  session_time = float(round(int(elapsed) / 60, 1))
  with open(vars.log_file, 'r') as r:
    logged_time = float(r.readline().replace('game-time: ', ''))
    r.close()
  with open(vars.log_file, 'w') as f:
    f.write(f'game-time: {round(logged_time+elapsed, 2)}')
    f.close()
  print(f'\nMinutes Played: {session_time}')
  print(f'\nOverall Hours: {convertTime()}')
  time.sleep(5)


if __name__ == '__main__':
  try:
    prerun()
    startGame()
    input("Press 'Enter' when the game is closed. ")
    postGame()
    sys.exit(0)
  except Exception as e:
    print(f'ERROR: {e}')
    time.sleep(5)
    sys.exit(1)
