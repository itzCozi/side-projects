# Emulates the Windows terminal and cmd
# Find old iPhone and charge it for school

import os
import sys
import time
import ctypes
import signal
import shutil
import hashlib
import subprocess
from colorama import Fore, Back, Style

# CODE
'''
* All variable declarations must be type hinted EX: num: int = 0
* All paths use '/' to separate dirs instead of '\' like windows
* If a function has parameters each variable must have specified types
* All classes use CamelCase and variables / functions use snake_case
* When assigning parameters in functions dont use spaces between equals sign
* Functions without 'self' parameter in a class must have the @staticmethod tag
* Whenever in a formatted string use double quotes and then single quotes to end
* References to variables must be in double quotes EX: (var: "5" is not a number)
* If a variable or function uses more than one type use EX: num: int | float = 0.1
* When outputting a message like info or an error end the print statement with a period
'''

# TODO
'''
https://stackoverflow.com/questions/11352855/communication-between-two-computers-using-python-socket
* Add comment support and if '#' in line make 
all chars after '#' green to signal a comment
* Add help command for all commands
* COMPILE TO .EXE
'''


class Globals:
  exit_code: None = None
  question_ticker: int = 0
  platform: str = sys.platform
  invaild_char_list: list = list('/\\:*?"<>|')
  help_message: str = '''
      Command          Description          Arguments

  cd       |  Change directory from current dir      |  path: str
  ls       |  Lists all items in the current dir     |  N/A
  pwd      |  Print the current working directory    |  N/A
  echo     |  Output all characters to console       |  message: [str]
  clear    |  Clear the whole terminal to blank      |  N/A
  touch    |  Create a new file from current dir     |  file_name: str
  rm       |  Delete a file                          |  file_list: [str]
  mkdir    |  Make a new directory                   |  dir_name_list: [str]
  size     |  Output the size of the file            |  file_name_list: [str]
  cat      |  Print the contents of the file         |  file_name: str
  kill     |  Kill a process by name                 |  process: str
  user     |  Prints the current user                |  N/A
  mov      |  Move a file or dir to a new path       |  source_path: str, destination_path: str
  run      |  Open a file using the native program   |  file_path: str
  rename   |  Rename a file or dir                   |  target_file: str, new_name: str
  sleep    |  Stalls for a duration of seconds       |  duration: int
  sum      |  Prints hash of a file to terminal      |  file_name: str
  uptime   |  Outputs the current uptime             |  N/A
  date     |  Print the current date                 |  N/A
  time     |  Print the current time                 |  N/A
  info     |  Outputs info about the item            |  file_path: str
  dir      |  Briefly prints all items in a dir      |  directory: str
  help     |  Prints this menu                       |  N/A
  calc     |  A simple calculator                    |  expression: str
  '''
  # they are accurate to the functions arguments
  # I know this is ugly but its so readable it should
  # be a PEP8 standard for maps over like 20 items long
  command_map: dict = {
    "cd":              0,              # * Change current directory
    "ls":              1,              # * Display all files and dirs
    "pwd":             2,              # * Print the current path
    "echo":            3,              # * Print a string
    "clear":           4,              # * Clear the console
    "touch":           5,              # * Create a new file
    "rm":              6,              # * Remove or delete a file
    "mkdir":           7,              # * Create a new directory
    "size":            8,              # * Prints the size of a file or dir
    "cat":             9,              # * Prints the content of a file
    "kill":            10,             # * Kills a process by name
    "user":            11,             # * Prints the current user
    "mov":             12,             # * Moves a file or dir to a new path
    "run":             13,             # * Runs the given file
    "rename":          14,             # * Renames the given file
    "sleep":           15,             # * Sleep for a period of time
    "sum":             16,             # * Print checksum of file
    "uptime":          17,             # * Prints the uptime
    "date":            18,             # * Prints the current date
    "time":            19,             # * Prints the current time
    "info":            20,             # * Displays info about the file
    "dir":             21,             # * Shows all items in a directory
    "help":            22,             # * Displays all commands with args and desc
    "calc":            23,             # * Simple calculator with eval function

    "zip":             24,             # Zip a file with the zip format
    "unzip":           25,             # Unzip a file with the zip format
    "shutdown":        26,             # Shutdown system after a prompt
    "#":               27,             # Comment simply pass when this is parsed
    "dupe":            28,             # Duplicate a file or directory
    "get-pid":         29,             # Prints process id from process name
    "get-name":        30,             # Prints the name of the process from PID
    "locate":          31,             # Loops file system until file is found
    "source":          32,             # Run commands from a file '.'
    "duration":        33              # Measure total command / program run time
  }


class Helper:

  @staticmethod
  def shell_initialize() -> None:
    """
    Handles calling the right command and sending arguments
    """
    loop: bool = True

    while loop is True:
      try:
        cur_dir: str = os.getcwd().replace('\\', '/')
        if Globals.question_ticker == 0:
          command: str = input(f'{Back.GREEN + Fore.BLACK}{cur_dir}{Style.RESET_ALL}\n$ ')
        else:
          command: str = input(f'\n{Back.GREEN + Fore.BLACK}{cur_dir}{Style.RESET_ALL}\n$ ')

        Globals.question_ticker += 1
        Helper.switch_case(command)
      except Exception as e:
        print(f'Unknown exception occurred: \n{e}\n')

  @staticmethod
  def switch_case(cmd: str) -> None:
    """
    The shell_initialize switch case for user input

    Args:
      cmd (str): The user input from shell_initialize()
    """
    try:
      # Suggested by Sam Perlmutter (FRC Team: 3506)
      # Didn't know switch cases existed in Python
      # until he made fun of my spaghetti code
      cmd_list: list = cmd.split(' ')
      keyword: str = cmd_list[0].lower()

      match keyword:
        case '<sys>':  # Passes cmd directly to system
          cmd_dupe: list = cmd_list.copy()
          if 'ps' in cmd_dupe:
            idx: int = cmd_dupe.index('ps')
            cmd_dupe[idx]: str = 'powershell'
          subprocess.call(' '.join(cmd_dupe[1:]), shell=True)

        case 'cd':
          Commands.cd(cmd_list[1])

        case 'ls':
          Commands.ls()

        case 'pwd':
          Commands.pwd()

        case 'echo':
          Commands.echo(cmd_list[1:])

        case 'clear':
          Commands.clear()

        case 'touch':
          Commands.touch(cmd_list[1])

        case 'rm':
          Commands.rm(cmd_list[1:])

        case 'mkdir':
          Commands.mkdir(cmd_list[1:])

        case 'size':
          Commands.size(cmd_list[1:])

        case 'cat':
          Commands.cat(cmd_list[1])

        case 'kill':
          Commands.kill(cmd_list[1])

        case 'user':
          Commands.user()

        case 'mov':
          Commands.mov(cmd_list[1], cmd_list[2])

        case 'run':
          Commands.run(cmd_list[1])

        case 'rename':
          Commands.rename(cmd_list[1], cmd_list[2])

        case 'sleep':
          Commands.sleep(cmd_list[1])

        case 'sum':
          Commands.sum(cmd_list[1])

        case 'uptime':
          Commands.uptime()

        case 'date':
          Commands.date()

        case 'time':
          Commands.time()

        case 'info':
          Commands.info(cmd_list[1])

        case 'dir':
          if len(cmd_list) > 1:
            Commands.dir(cmd_list[1])
          else:
            Commands.dir()

        case 'help':
          Globals.question_ticker: int = 0
          print(Globals.help_message)

        case 'calc':
          Commands.calc(cmd_list[1])

        case 'source':
          Commands.source(cmd_list[1])

        # ----- Blank Input and Wildcard ----- #
        case '':
          pass
        case _:  # An 'else' statement
          print(f'Given command: "{cmd}" is invalid.')

    except IndexError:
      print(f'Given command: "{cmd}" requires an argument.')
    except Exception as e:
      print(f'Unknown exception occurred: \n{e}\n')

  @staticmethod
  def get_file_size(file_name: str) -> tuple:
    """
    Returns the size of the files / directories given

    Args:
      file_name (str): The name of the file to get size of

    Returns
      tuple: The files path, size and size type
    """
    current_dir: str = os.getcwd().replace('\\', '/')
    file_path: str = f'{current_dir}/{file_name}'
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

    return file_name, size, size_type

  @staticmethod
  def get_name(pid: int) -> str:
    """
    Return the name from the PID

    Args:
      pid (int): The target processes ID

    Returns:
      str: The name of the process
    """
    if 'linux' in Globals.platform:
      process_name: str = os.popen(f'ps -p {pid} -o comm=').read()
    else:
      out: str = os.popen(f'tasklist /fi "pid eq {pid}"').read()
      out_list: list = out.splitlines()
      for line in out_list:
        if '.exe' in line:
          idx: int = line.find('.')
          process_name: str = line[:idx + 4]
    if 'process_name' in locals():
      return process_name
    else:
      print(f'Given process ID: "{pid}" is not assigned to an active process.')
      return Globals.exit_code

  @staticmethod
  def get_PID(process: str) -> list:
    """
    Returns a process PID from name

    Args:
      process (str): The processes name

    Returns:
      list: A list of all child processes PIDs
    """
    if 'linux' in Globals.platform:
      child: subprocess.Popen = subprocess.Popen(
        ['pgrep', '-f', process],
        stdout=subprocess.PIPE,
        shell=False
      )
      response: bytes = child.communicate()[0]
      return [int(pid) for pid in response.split()]

    else:  # Windows way
      ret_list: list = []
      output: str = os.popen(f'powershell Get-Process -Name {process}').read()
      for line in output.splitlines():
        if '  SI' in line:
          index: int = line.find('  SI')
        if '.' in line:
          if 'index' in locals():
            difference: str = line[:index]
            proc_info: str = difference.split()[-1].replace(' ', '')
            ret_list.append(proc_info)
          else:
            print(f'Given process: "{process}" is not active.')
            return Globals.exit_code
      return ret_list


class Commands:

  @staticmethod
  def cd(path: str) -> None:
    """
    Change directory to path

    Args:
      path (str): The path to cd to
    """
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
    """
    List all items in the current directory
    """
    directory: str = os.getcwd().replace('\\', '/')
    dir_items: list = os.listdir(directory)
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
    """
    Remove / delete all files in a list

    Args:
      file_list (list): A list made by shell_init()
    """
    for file in file_list:
      del_question: str = f'Are you sure you want to delete {file}? (y/n): '

      if os.path.exists(file):
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
      else:
        print(f'Cannot find given file: "{file}".')
        return Globals.exit_code

  @staticmethod
  def mkdir(dir_name_list: list) -> None:
    """
    Create a directory or directories

    Args:
      dir_name_list (list): A list of all dirs to make
    """
    cur_dir: str = os.getcwd().replace('\\', '/')
    for directory in dir_name_list:
      for char in directory:
        if char in Globals.invaild_char_list:
          print(f'There is an invaild character in "{directory}".')
          return Globals.exit_code
        else:
          continue
      os.mkdir(f'{cur_dir}/{directory}')

  @staticmethod
  def size(file_name_list: list) -> None:
    """
    Print the size of the files / directories given

    Args:
      file_name_list (list): A list of all file names to get size of
    """
    for file in file_name_list:
      ret_tuple: tuple = Helper.get_file_size(file)
      file: str = ret_tuple[0]
      size: int | float = ret_tuple[1]
      size_type: str = ret_tuple[2]

      print(f'{file} is {size} {size_type}')

  @staticmethod
  def dir(directory: str = '') -> None:
    """
    Print all files and folders in current dir or a specified path

    Args:
      directory (str): An optional directory if not using current
    """
    ticker: int = 0
    if directory == '':
      directory: str = os.getcwd()
    if len(os.listdir(directory)) == 0:
      print(f'The current directory: "{directory}" is empty.')
      return Globals.exit_code
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
    """
    Kills a process

    Args:
      process (str): The target processes name
    """
    if '.exe' in process:
      process: str = process[:-4]
    pid_list: list = Helper.get_PID(process)
    if pid_list is None:
      return Globals.exit_code

    for PID in pid_list:
      os.kill(int(PID), signal.SIGTERM)
      print(f'Killed process: "{PID}"')
    print(f'Killed all processes under the "{process}" parent process.')

  @staticmethod
  def cat(file_name: str) -> None:
    """
    Output the contents of a file to the console

    Args:
      file_name (str): The name of the file to print
    """
    file_name: str = file_name.replace('\\', '/')
    cur_dir: str = os.getcwd().replace('\\', '/')

    if os.path.exists(file_name):
      if os.path.isfile(file_name):
        with open(file_name) as f:
          content: str = f.read()

      else:
        print(f'"{file_name}" is not a file.')
        return Globals.exit_code
    else:
      print(f'Given file: "{file_name}" cannot be found in "{cur_dir}".')
      return Globals.exit_code

    print(content)

  @staticmethod
  def source(file_path: str) -> None:
    """
    Run commands from a file and output to console

    Args:
      file_path (str): The path to the source file
    """
    file_path: str = file_path.replace('\\', '/')

    if os.path.isfile(file_path):
      with open(file_path, 'r') as file:
        content: str = file.read()
      f_content: list = content.splitlines()
    else:
      print(f'Given file: "{file_path}" cannot be found or is not a file.')
      return Globals.exit_code

    for line in f_content:
      Helper.switch_case(line)

  @staticmethod
  def mov(source_path: str, destination_path: str) -> None:
    """
    Moves a file or directory to a new location

    Args:
      source_path (str): The file to be moved
      destination_path (str): Where to output the file
    """
    source_path: str = source_path.replace('\\', '/')

    if os.path.exists(destination_path):
      print(f'Destination "{destination_path}" already exists.')
      return Globals.exit_code

    if os.path.exists(source_path):
      if os.path.isfile(source_path):
        shutil.copyfile(source_path, destination_path)
      elif os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path)
    else:
      print(f'File: "{source_path}" doesnt exist.')
      return Globals.exit_code

  @staticmethod
  def uptime() -> None:
    """
    Prints uptime on windows
    """
    if 'linux' in Globals.platform:
      print('The \'uptime\' command is not supported on linux.')
      return Globals.exit_code
    lib: ctypes.WinDLL = ctypes.windll.kernel32
    t: int = lib.GetTickCount64()
    t: int = int(str(t)[:-3])
    # Cant type hint tuples so theses are standard
    mins, sec = divmod(t, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)
    print(f'{days} days, {hour:02}:{mins:02}')

  @staticmethod
  def sum(file_name: str) -> None:
    """
    Outputs the check sum of a file

    Args:
      file_name (str): The target files name
    """
    file: str = file_name.replace('\\', '/')
    obj = hashlib.sha1()  # Weird type

    with open(file, 'rb') as Fin:
      chunk: bytes = 0
      while chunk != b'':
        chunk: bytes = Fin.read(1024)
        obj.update(chunk)
    print(f'{file.split("/")[-1]} hash: {obj.hexdigest()}')

  @staticmethod
  def sleep(duration: str) -> None:
    """
    Sleep / stall for a period of time

    Args:
      duration (str): The duration of seconds to wait
    """
    if duration.isdigit():
      for i in reversed(range(1, int(duration) + 1)):
        if i == int(duration):
          message: str = f'Sleeping for {i} seconds...\r'
        elif i == 1:
          message: str = f'Sleeping for {i} more second...\n\r'
        else:
          message: str = f'Sleeping for {i} more seconds...\r'

        str_length: int = len(message)
        if str_length > len(str(i)):
          print('\x1b[2K', end=message)
        else:
          print(message, end='')
        time.sleep(1)

    else:
      print('Given variable: "duration" is not a integer.')
      return Globals.exit_code

  @staticmethod
  def info(file_path: str) -> None:
    file_path: str = file_path.replace('\\', '/')

    if os.path.exists(file_path):
      if os.path.isfile(file_path):
        ret_tuple: tuple = Helper.get_file_size(file_path)
        file: str = ret_tuple[0]
        size: int | float = ret_tuple[1]
        size_type: str = ret_tuple[2]
        file_type: str = 'file'
        print(f'{file_type.capitalize()}: {file} | {size} {size_type}')

      elif os.path.isdir(file_path):
        ret_tuple: tuple = Helper.get_file_size(file_path)
        file: str = ret_tuple[0]
        size: int | float = ret_tuple[1]
        size_type: str = ret_tuple[2]
        file_type: str = 'directory'
        print(f'{file_type.capitalize()}: {file} | {size} {size_type}')
    else:
      print(f'File: "{file_path}" doesnt exist.')
      return Globals.exit_code

  # ----- Smaller Functions ----- #

  @staticmethod
  def time() -> None:
    """
    Prints the current time
    """
    if 'linux' in Globals.platform:
      current_time: str = os.popen("date +%I:%M' '%p").read().replace('\n', '')
    else:
      current_time: str = os.popen('time /t').read().replace('\n', '')
    print(current_time)

  @staticmethod
  def date() -> None:
    """
    Prints the current date
    """
    if 'linux' in Globals.platform:
      date: str = os.popen("date +%m/%d/%Y").read().replace('\n', '')
    else:
      date: str = os.popen('date /t').read().replace('\n', '')
    print(date)

  @staticmethod
  def calc(expression: str) -> None:
    """
    A simple calculator

    Args:
      expression (str): A math operation EX: (4+4)
    """
    try:
      print(eval(expression))
    except Exception as e:
      print(f'Expression: "{expression}" is not a valid math operation.\n{e}\n')
      return Globals.exit_code

  @staticmethod
  def rename(target_file: str, new_name: str) -> None:
    """
    Renames the target file to a new name

    Args:
      target_file (str): The file to be renamed
      new_name (str): What to rename to target to
    """
    target_file: str = target_file.replace('\\', '/')
    if len(target_file.split('/')) > 1:
      new_name: str = f'{"".join(target_file.split("/")[:-1])}/{new_name}'
    if target_file.split('/')[-1] == '':
      new_name: str = f'{target_file.split("/")[0]}/{new_name}'

    if os.path.exists(target_file):
      os.rename(target_file, new_name)
    else:
      print(f'File: "{target_file}" doesnt exist.')
      return Globals.exit_code

  @staticmethod
  def run(file_path: str) -> None:
    """
    Execute a given file

    Args:
      file_path (str): The path to the target file
    """
    if os.path.exists(file_path):
      if 'linux' in Globals.platform:
        subprocess.call(f'./{file_path}', shell=True)
      else:
        os.startfile(file_path)
    else:
      print(f'File: "{file_path}" doesnt exist.')
      return Globals.exit_code

  @staticmethod
  def touch(file_name: str) -> None:
    """
    Create a new file

    Args:
      file_name (str): What to name to new file / where to put it
    """
    current_dir: str = os.getcwd().replace('\\', '/')
    with open(f'{current_dir}/{file_name}', 'x') as file:
      file.close()

  @staticmethod
  def echo(message: list) -> None:
    """
    Print a message

    Args:
      message (list): A list of user input split by spaces
    """
    formatted_out: str = ' '.join(message)
    out_list: list = list(formatted_out)
    length: int = len(out_list)
    if out_list[0] == '\'' or out_list[0] == '"':
      out_list[0] = ''
    if out_list[length - 1] == '\'' or out_list[length - 1] == '"':
      out_list[0] = ''

    print(''.join(out_list))

  @staticmethod
  def user() -> None:
    """
    Prints current user
    """
    current_user: str = os.getlogin()
    print(current_user)

  @staticmethod
  def clear() -> None:
    """
    Clears the console
    """
    Globals.question_ticker: int = 0
    if 'linux' in Globals.platform:
      subprocess.call('clear', shell=True)
    else:
      subprocess.call('cls', shell=True)

  @staticmethod
  def pwd() -> None:
    """
    Print the current working directory
    """
    current_dir: str = os.getcwd()
    print(current_dir)


Helper.shell_initialize()
