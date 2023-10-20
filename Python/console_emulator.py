# Emulates the windows terminal and cmd
import os
import sys
import signal
import shutil
import subprocess
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
* Organize Commands class so commands
without arguments are at the bottom
* Add doc-strings
* COMPILE TO .EXE
'''


class Globals:
  exit_code: None = None
  platform: str = sys.platform
  invaild_char_list: list = list('/\\:*?"<>|')
  command_map: dict = {
    "cd": 0x0,         # * Change current directory
    "ls": 0x1,         # * Display all files and dirs
    "pwd": 0x2,        # * Print the current path
    "echo": 0x3,       # * Print a string
    "clear": 0x4,      # * Clear the console
    "touch": 0x5,      # * Create a new file
    "rm": 0x6,         # * Remove or delete a file
    "mkdir": 0x7,      # * Create a new directory
    "size": 0x8,       # * Prints the size of a file or dir
    "cat": 0x9,        # * Prints the content of a file
    "kill": 0xA,       # * Kills a process by name
    "user": 0xB,       # * Prints the current user
    "mov": 0xC,        # Moves a file or dir to a new path
    "run": 0xD,        # Runs the given file
    "rename": 0xE,     # Renames the given file
    "sleep": 0xF,      # Sleep for a period of time
    "sum": 0x10,       # Print checksum of file
    "uptime": 0x11,    # Prints the uptime
    "zip": 0x12,       # Zip a file in the current dir
    "info": 0x13,      # Displays info about the file
    "dir": 0x14,       # * Shows all items in a directory
    "calc": 0x15,      # Simple calculator with eval function
    "zip": 0x16,       # Zip a file with the zip format
    "unzip": 0x17,     # Unzip a file with the zip format
    "shutdown": 0x18,  # Shutdown system after a prompt
    "###": 0x19,       # Comment simply pass when this is parsed
  }


class Helper:

  @staticmethod
  def get_PID(process: str) -> list:
    # Returns a process PID from name
    if 'linux' in Globals.platform:
      child: subprocess.Popen = subprocess.Popen(['pgrep', '-f', process], stdout=subprocess.PIPE, shell=False)
      response: bytes = child.communicate()[0]
      print(type(child), type(response))
      return [int(pid) for pid in response.split()]

    else:  # Windows way
      retlist: list = []
      output: str = os.popen(f'powershell Get-Process -Name {process}').read()
      for line in output.splitlines():
        if '  SI' in line:
          index: int = line.find('  SI')
        if '.' in line:
          difference: str = line[:index]
          proc_info: str = difference.split()[-1].replace(' ', '')
          retlist.append(proc_info)
      return retlist

  @staticmethod
  def shell_initialize() -> None:
    # Handles calling the right command and sending arguments
    commands: list = list(Globals.command_map.keys())
    loop: bool = True

    while loop is True:
      cur_dir: str = os.getcwd().replace('\\', '/')
      cmd: str = input(f'{cur_dir} $ ')
      cmd_list: list = cmd.split(' ')
      keyword: str = cmd.split(' ')[0].lower()

      if keyword == '<sys>':  # Passes cmd directly to system
        cmd_dupe: list = cmd_list.copy()
        if 'ps' in cmd_dupe:
          idx: int = cmd_dupe.index('ps')
          cmd_dupe[idx]: str = 'powershell'
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

      elif keyword == commands[8]:
        Commands.size(cmd.split(' ')[1:])

      elif keyword == commands[9]:
        Commands.cat(cmd.split(' ')[1])

      elif keyword == commands[10]:
        Commands.kill(cmd.split(' ')[1])

      elif keyword == commands[11]:
        Commands.user()

      elif keyword == commands[20]:
        if len(cmd_list) > 1:
          Commands.dir(cmd.split(' ')[1])
        else:
          Commands.dir()

      else:
        print(f'Given command {cmd} is invalid.')


class Commands:

  @staticmethod
  def cd(path: str) -> None:
    path: str = path.replace('\\', '/')

    if 'linux' in Globals.platform:
      if path == '~':
        os.chdir(os.path.expanduser('~'))
        return Globals.exit_code
      if '..' in path:
        path_list: list = list(path.split('/'))
        if len(path_list) > 1:
          path_list.pop()
        path: str = '/'.join(path_list)
        os.chdir(path)
      else:
        os.chdir(path)

    else:
      if path == 'C:' or path == '~':
        os.chdir(os.path.expanduser('C:'))
        return Globals.exit_code
      if '..' in path:
        path_list: list = list(path.split('/'))
        if len(path_list) > 1:
          path_list.pop()
        path: str = '/'.join(path_list)
        os.chdir(path)
      else:
        os.chdir(path)

  @staticmethod
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

  @staticmethod
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

  @staticmethod
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

  @staticmethod
  def size(file_name_list: list) -> None:
    for file in file_name_list:
      current_dir: str = os.getcwd().replace('\\', '/')
      file_path: str = f'{current_dir}/{file}'
      if os.path.isfile(file_path):
        byte_size: int = os.path.getsize(file_path)

      else:
        byte_size: int = 0
        for path, dirs, files in os.walk(file_path):
          for f in files:
            fp: str = os.path.join(path, f)
            byte_size += os.path.getsize(fp)

      if byte_size > 1000:  # KB
        size_type: str = 'KB'
        size: int | float = round(byte_size / 1000, 2)
      elif byte_size > 1000000:  # MB
        size_type: str = 'MB'
        size: int | float = round(byte_size / 1000000, 2)
      elif byte_size > 1000000000:  # GB
        size_type: str = 'GB'
        size: int | float = round(byte_size / 1000000000, 2)
      else:
        size_type: str = 'Bytes'
        size: int | float = round(byte_size, 2)

      print(f'{file} is {size} {size_type}')

  @staticmethod
  def dir(directory: str = '') -> None:
    ticker: int = 0
    if directory == '':
      directory: str = os.getcwd()
    directory: str = directory.replace('\\', '/')

    for item in os.listdir(directory):
      ticker += 1
      if os.path.isdir(item):
        color: str = Fore.YELLOW
      else:
        color: str = Fore.WHITE

      if ticker == 3:
        print(f'{color}{item}{Style.RESET_ALL}')
        ticker: int = 0
        new_line: bool = False
      else:
        print(f'{color}{item}{Style.RESET_ALL}', end='  ')
        new_line: bool = True
    if new_line is True:
      print()

  @staticmethod
  def kill(process: str) -> None:
    if '.exe' in process:
      process: str = process[:-4]
    PID_list: list = Helper.get_PID(process)

    for PID in PID_list:
      os.kill(int(PID), signal.SIGTERM)
      print(f'Killed process: {PID}')
    print(f'Killed all processes under the {process} parent process.')

  @staticmethod
  def cat(file_name: str) -> None:
    file_name: str = file_name.replace('\\', '/')
    cur_dir: str = os.getcwd().replace('\\', '/')

    try:
      with open(file_name) as f:
        content: str = f.read()
    except FileNotFoundError:
      print(f'Given file {file_name} cannot be found in {cur_dir}.')
      return Globals.exit_code

    print(content)

  # ----- Smaller Functions ----- #

  @staticmethod
  def touch(file_name: str) -> None:
    current_dir: str = os.getcwd().replace('\\', '/')
    with open(f'{current_dir}/{file_name}', 'x') as file:
      file.close()

  @staticmethod
  def echo(message: list) -> None:
    formatted_out: str = ' '.join(message)
    print(formatted_out)

  @staticmethod
  def user() -> None:
    current_user: str = os.getlogin()
    print(current_user)

  @staticmethod
  def clear() -> None:
    if 'linux' in Globals.platform:
      os.system('clear')
    else:
      os.system('cls')

  @staticmethod
  def pwd() -> None:
    current_dir: str = os.getcwd()
    print(current_dir)


Helper.shell_initialize()
