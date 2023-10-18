# Emulates the windows terminal and cmd
import os
import sys
from colorama import Fore, Back, Style

# CODE
'''
* All variable declarations must be type hinted EX: num: int = 0
* All paths use '/' to separate dies instead of '\' like windows
* If a function has parameters each variable must have specified types
* All functions and classes use camelCase and variables use snake_case
* Functions without 'self' parameter in a class must have the @staticmethod tag
* If a variable or function uses more than one type use EX: num: int | float = 0.1
'''

# TODO
'''
* Add doc-strings
* COMPILE TO .EXE
'''


class Globals:
  platform = sys.platform
  current_working_dir: str = os.getcwd()
  command_map: dict = {
    "cd": 1,
    "ls": 2,
    "pwd": 3,
    "echo": 4,
    "clear": 5,
    "touch": 6,  # Creates a file
    "rm": 7  # Removes a file
  }


class Interface:

  def command_loop() -> str:
    # Handles calling the right command and sending arguments
    commands: list = list(Globals.command_map.keys())
    loop: bool = True

    while loop is True:
      cmd: str = input('> ')

      if cmd.split(' ')[0].lower() == 'cd':
        Commands.cd(cmd.split(' ')[1])
      elif cmd.split(' ')[0].lower() == 'ls':
        Commands.ls()
      elif cmd.split(' ')[0].lower() == 'pwd':
        Commands.pwd()
      elif cmd.split(' ')[0].lower() == 'echo':
        Commands.echo(cmd.split(' ')[1:])
      else:
        print(f'Given command {cmd} is invalid.')


class Commands:

  def cd(path: str) -> None:
    path: str = path.replace('\\', '/')

    if 'linux' in Globals.platform:
      if path == '~':
        os.chdir(os.path.expanduser('~'))
      if '..' in path:
        path_list: list = list(path.split('/'))
        if len(path_list) > 1:
          path_list.pop()
        path: str = '/'.join(path_list)
        os.chdir(path)
      else:
        os.chdir(path)
      Globals.current_working_dir: str = os.getcwd()

    else:
      if path == 'C:':
        os.chdir(os.path.expanduser('C:'))
      if '..' in path:
        path_list: list = list(path.split('/'))
        path_list.pop()
        path: str = '/'.join(path_list)
        os.chdir(path)
      else:
        os.chdir(path)
      Globals.current_working_dir: str = os.getcwd()

  def ls() -> None:
    dir = os.getcwd().replace('\\', '/')
    dir_items = os.listdir(dir)
    ticker = 0
    print('---------------------------------------------')
    for file in dir_items:
      ticker += 1
      if os.path.isdir(file):
        color = Fore.BLUE
      elif os.path.isfile(file):
        color = Fore.YELLOW

      if 4 > ticker:
        print(f'{color}{file}{Style.RESET_ALL}', end=', ')
      if ticker == 4 or dir_items.index(file) + 1 == len(dir_items):
        print(f'{color}{file}{Style.RESET_ALL}')
        ticker = 0
    print('---------------------------------------------')

  def pwd() -> None:
    current_dir = os.getcwd()
    print(current_dir)

  def echo(message: list) -> None:
    formatted_out: str = ' '.join(message)
    print(formatted_out)

Interface.command_loop()
