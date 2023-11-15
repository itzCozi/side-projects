"""
THIS SCRIPT NEEDS TO BE CUSTOMIZED FOR USAGE
-----------------------------------------------
Downloads the zip from a website and extracts it to a specified location then create shortcut
RIPPED-FROM: https://github.com/itzCozi/SafeGuard/releases/tag/Installer
"""

try:
  import os
  import sys
  import requests
  import shutil
  import win32com.client
except ModuleNotFoundError as e:  # If you don't have a package installed
  e: str = str(e)
  idx: int = e.find('named')
  missing_package: str = e[idx:].replace('named ', '').replace('\'', '')
  print('-----------------------------------------------------------------------')
  print(f'Package \'{missing_package}\' failed to import if you have Python installed \
  \nyou can install the package by typing the below command into \'cmd\':')
  print(f'pip install {missing_package}')
  print('-----------------------------------------------------------------------')

# Define global variable
global Any


class Setup:
  Any: object = object()  # Any type

  class _Vars:
    # To customize this script for a use case all you have to do is
    # edit the __init__ function and change the variables below

    log: bool = True
    program_name: str = 'SafeGuard'
    github_link: str = 'https://github.com/itzCozi/SafeGuard'
    wiki_link: str = 'https://github.com/itzCozi/SafeGuard/wiki'
    zip_link: str | None = 'https://itzcozi.github.io/SafeGuard/data/safeguard.zip'  # Set to 'None' if N/A
    mainFolder: str | None = f'C:/Users/{os.getlogin()}/Python-SafeGuard'  # Set to 'None' if N/A

  def __init__(*self: Any) -> None:
    print('----------------------------------------')
    Setup.create_structure()                                                                 # Create main folder
    Setup.download(Setup._Vars.zip_link, f'{Setup._Vars.mainFolder}/archive.zip')             # Download the .zip file to the main folder
    shutil.unpack_archive(f'{Setup._Vars.mainFolder}/archive.zip', Setup._Vars.mainFolder)     # Unpack the archive
    os.remove(f'{Setup._Vars.mainFolder}/archive.zip')                                          # Remove the .zip file
    Setup.create_shortcut(f'{Setup._Vars.mainFolder}/compiled/safeguard.exe')                    # Create a shortcut for the binary

    def _exit() -> None:
      print('----------------------------------------')
      input("Press 'Enter' to continue... ")
      sys.exit(0)

    # Prints a different end text depending on 
    # if github_link and wiki_link is None

    if Setup._Vars.github_link is not None and Setup._Vars.wiki_link is not None:
      print(f'\n{Setup._Vars.program_name} installed at: {Setup._Vars.mainFolder} \
      \nA desktop shortcut has been created for {Setup._Vars.program_name}, \
      \nthough if broken you may need to make your own. \
      \nGithub Link: {Setup._Vars.github_link} \
      \nWiki Link: {Setup._Vars.wiki_link}')
      _exit()

    elif Setup._Vars.github_link is not None:
      print(f'\n{Setup._Vars.program_name} installed at: {Setup._Vars.mainFolder} \
      \nA desktop shortcut has been created for {Setup._Vars.program_name}, \
      \nthough if broken you may need to make your own. \
      \nGithub Link: {Setup._Vars.github_link}')
      _exit()

    elif Setup._Vars.wiki_link is not None:
      print(f'\n{Setup._Vars.program_name} installed at: {Setup._Vars.mainFolder} \
      \nA desktop shortcut has been created for {Setup._Vars.program_name}, \
      \nthough if broken you may need to make your own. \
      \nWiki Link: {Setup._Vars.wiki_link}')
      _exit()

    else:
      print(f'\n{Setup._Vars.program_name} installed at: {Setup._Vars.mainFolder} \
      \nA desktop shortcut has been created for {Setup._Vars.program_name}, \
      \nthough if broken you may need to make your own.')
      _exit()

  @staticmethod
  def download(url: str, newpath: str) -> None:
    file_content: requests.models.Response = requests.get(url)
    open(newpath, 'wb').write(file_content.content)
    if Setup._Vars.log:
      print(f'Downloaded file to: {newpath}')

  @staticmethod
  def create_structure() -> None:
    if not os.path.exists(Setup._Vars.mainFolder):
      os.mkdir(Setup._Vars.mainFolder)
      if Setup._Vars.log:
        print(f'Created {Setup._Vars.mainFolder}')
    else:
      if Setup._Vars.log:
        print('Main folder accounted for...')

  @staticmethod
  def create_shortcut(target_file: str) -> None:
    if 'Desktop' in os.listdir(f'C:/Users/{os.getlogin()}/OneDrive'):
      desktop: str = f'C:/Users/{os.getlogin()}/OneDrive/Desktop'
    else:
      os.path.normpath(os.path.expanduser('~/Desktop'))

    path: str = os.path.join(desktop, 'SafeGuard.lnk')
    shell: win32com.client.CDispatch = win32com.client.Dispatch('WScript.Shell')
    shortcut: win32com.client.CDispatch = shell.CreateShortCut(path)
    shortcut.Targetpath: str = target_file
    shortcut.IconLocation: str = target_file
    shortcut.save()


if __name__ == '__main__':
  Setup()
