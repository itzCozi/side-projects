# Emulates the windows terminal and cmd
import os
import sys
import shutil
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
* Add size function and make it scale to the files
size so if its like 4 KB we print 4 KB instead of a
fixed mesurement we use KB MB and GB
* Add doc-strings
* COMPILE TO .EXE
'''


class Globals:
  exit_code: None = None
  platform: str = sys.platform
  current_working_dir: str = os.getcwd()
  invaild_char_list: list = list('/\\:*?"<>|')
  command_map: dict = {
    "cd": 0,
    "ls": 1,
    "pwd": 2,
    "echo": 3,
    "clear": 4,
    "touch": 5,
    "rm": 6,
    "mkdir": 7,
    "size": 8  # Prints the size of a file or dir
  }


class Interface:

  def command_loop() -> str:
    # Handles calling the right command and sending arguments
    commands: list = list(Globals.command_map.keys())
    loop: bool = True

    while loop is True:
      cmd: str = input('> ')
      cmd_list: list = cmd.split(' ')
      keyword: str = cmd.split(' ')[0].lower()

      if keyword == '<sys>':  # Passes cmd directly to system
        cmd_dupe: list = cmd_list.copy() 
        if 'ps' in cmd_dupe:
          idx = cmd_dupe.index('ps')
          cmd_dupe[idx] = 'powershell'
        os.system(' '.join(cmd_dupe[1:]))

      elif keyword == commands[0]:
        Commands.cd(cmd.split(' ')[1])

      elif keyword == commands[1]:
        Commands.ls()

      elif keyword == commands[2]:
        Commands.pwd()

      elif keyword == commands[3]:
        Commands.echo(cmd.split(' ')[1:])

      elif keyword == commands[4] or keyword == 'cls':
        Commands.clear()

      elif keyword == commands[5]:
        Commands.touch(cmd.split(' ')[1])

      elif keyword == commands[6]:
        Commands.rm(cmd.split(' ')[1:])

      elif keyword == commands[7]:
        Commands.mkdir(cmd.split(' ')[1:])

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
        if len(path_list) > 1:
          path_list.pop()
        path: str = '/'.join(path_list)
        os.chdir(path)
      else:
        os.chdir(path)
      Globals.current_working_dir: str = os.getcwd()

  def ls() -> None:
    dir: str = os.getcwd().replace('\\', '/')
    dir_items: list = os.listdir(dir)
    ticker: int = 0
    print('---------------------------------------------')
    for file in dir_items:
      ticker += 1
      if os.path.isdir(file):
        color: str = Fore.BLUE
      elif os.path.isfile(file):
        color: str = Fore.YELLOW

      if 4 > ticker:
        print(f'{color}{file}{Style.RESET_ALL}', end=', ')
      if ticker == 4 or dir_items.index(file) + 1 == len(dir_items):
        print(f'{color}{file}{Style.RESET_ALL}')
        ticker: int = 0
    print('---------------------------------------------')

  def touch(file_name: str) -> None:
    current_dir: str = os.getcwd().replace('\\', '/')
    with open(f'{current_dir}/{file_name}', 'x') as file:
      file.close()

  def rm(file_list: list) -> None:
    for file in file_list:
      del_question: str = f'Are you sure you want to delete {file}? (y/n): '

      if os.path.isfile(file):
        if os.path.getsize(file) < 375:  # Less than 3 kilobytes
          os.remove(file)
        else:
          usr_input: str = input(del_question).lower()
          if usr_input == 'yes' or usr_input == 'y':
            os.remove(file)
          else:
            return Globals.exit_code

      elif os.path.isdir(file):
        if os.path.getsize(file) < 375:  # Less than 3 kilobytes
          shutil.rmtree(file)
        else:
          usr_input: str = input(del_question).lower()
          if usr_input == 'yes' or usr_input == 'y':
            os.remove(file)
          else:
            return Globals.exit_code

  def pwd() -> None:
    current_dir: str = os.getcwd()
    print(current_dir)

  def echo(message: list) -> None:
    formatted_out: str = ' '.join(message)
    print(formatted_out)

  def mkdir(dir_name_list: list) -> None:
    cur_dir: str = os.getcwd().replace('\\', '/')
    for dir in dir_name_list:
      for char in dir:
        if char in Globals.invaild_char_list:
          print(f'There is an invaild character in {dir}.')
          return Globals.exit_code
        else:
          continue
      os.mkdir(f'{cur_dir}/{dir}')

  def clear() -> None:
    if 'linux' in Globals.platform:
      os.system('clear')
    else:
      os.system('cls')


Interface.command_loop()
