'''
THIS SCRIPT NEEDS TO BE CUSTOMIZED FOR USAGE
Downloads the zip from a website and extracts it to a specifed location then create shortcut
RIPPED-FROM: https://github.com/itzCozi/SafeGuard/releases/tag/Installer
'''

try:
  import os, sys
  import requests
  import shutil
  import win32com.client
except:
  print('Error: Missing required modules. Please install the following modules: requests and socket')


class vars:
  log = True
  zip_link = f'https://itzcozi.github.io/SafeGuard/data/safeguard.zip'
  mainFolder = str(f'C:/Users/{os.getlogin()}/Python-SafeGuard')

def install(URL, newpath):
  file_content = requests.get(URL)
  open(newpath, 'wb').write(file_content.content)
  if vars.log:
    print(f'Downloaded file to: {newpath}')


def createStructure():
  if not os.path.exists(vars.mainFolder):
    os.mkdir(vars.mainFolder)
    if vars.log:
      print(f'Created {vars.mainFolder}')
  else:
    if vars.log:
      print('All folders accounted for')


def createShortcut(targetFile):
  if 'coope' in os.getlogin(): desktop = f'C:/Users/coope/OneDrive/Desktop'
  else: os.path.normpath(os.path.expanduser('~/Desktop'))
  path = os.path.join(desktop, 'SafeGuard.lnk')
  shell = win32com.client.Dispatch('WScript.Shell')
  shortcut = shell.CreateShortCut(path)
  shortcut.Targetpath = targetFile
  shortcut.IconLocation = targetFile
  shortcut.save()


if __name__ == '__main__':
  createStructure()
  install(vars.zip_link, f'{vars.mainFolder}/archive.zip')
  shutil.unpack_archive(f'{vars.mainFolder}/archive.zip', vars.mainFolder)
  os.remove(f'{vars.mainFolder}/archive.zip')
  createShortcut(f'{vars.mainFolder}/compiled/safeguard.exe')

  print(f'\nSafeGuard installed at: \
  \n{vars.mainFolder} \
  \nA desktop shortcut has been created though if broken \
  \nor not on your desktop you may need to make your own. \
  \nGithub Link: https://github.com/itzCozi/SafeGuard \
  \nWiki Link: https://github.com/itzCozi/SafeGuard/wiki\n')
  input("Press 'Enter' to continue ")
  sys.exit(0)
