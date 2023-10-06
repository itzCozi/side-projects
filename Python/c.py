# My compile, run and print to terminal script for C and C++
import os, sys
import time
from colorama import Fore, Back, Style

# CODE
'''
* All functions use camelCase and variables use snake_case
* All variable declarations must be type hinted EX: num: int = 0
* If a function has parameters each variable must have specified types
* Functions without any parameters in a class must have the @staticmethod tag
'''

# TODO
'''
* See if dragging files on top of the program show the file as a virtual argument
* Make it possible to compile multiple source files by pairing each file with the
exe name with the same index EX: sourceA.cpp sourceB.cpp programA.exe programB.exe
* COMPILE TO .EXE WHEN DONE CODING
'''


class vars:

  def error(error_type: str, var: str = None, type: str = None, runtime_error: str = None) -> None:
    if error_type == 'p':
      print(f'PARAMETER: Given variable {var} is not a {type}.')
    elif error_type == 'r':
      print(f'RUNTIME: {runtime_error.capitalize()}.')
    elif error_type == 'u':
      print('UNKNOWN: An unknown error was encountered.')
    return vars.exit_code

  exit_code: None = None
  C_compiler: str = r'c:\MinGW\bin\gcc.exe'
  CPP_compiler: str = r'c:\MinGW\bin\g++.exe'


class core:
  # Only can compile .o, .c, .cpp and .h

  @staticmethod
  def compilationCall() -> None:
    """
    Calls correct compile option
    """
    arg_table: dict = core.determineArguments()
    if 'dll_name' in arg_table:
      core.compileDLL(arg_table)
    elif 'exe_name' in arg_table:
      core.compileFiles(arg_table)
    else:
      print('Neither "exe_name" or "dll_name" is in argument list.')
      return vars.exit_code

  @staticmethod
  def determineArguments() -> dict:
    """
    Puts all vargs into a map and return it for use

    Returns:
      dict: The map of files and keys
    """
    arg_list: list = list(sys.argv)
    source_file_counter: int = 0
    object_file_counter: int = 0
    header_file_counter: int = 0
    exe_file_counter: int = 0  # Used during multi-source file compilation
    dll_file_counter: int = 0  # This to...
    file_map: dict = {}

    for arg in arg_list:
      # Need to check if one or more source files is passed and if so also check 
      # if the same number of output files is passed then group them by index

      if arg.endswith('.cpp'):
        source_file_counter += 1
        if os.file.exists(arg):
          file_map[f'source_file{source_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.c'):
        source_file_counter += 1
        if os.path.exists(arg):
          file_map[f'source_file{source_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.o'):
        object_file_counter += 1
        if os.path.exists(arg):
          file_map[f'object_file{object_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.h'):
        header_file_counter += 1
        if os.path.exists(arg):
          file_map[f'header_file{header_file_counter}']: str = arg
        else:
          vars.error(error_type='r', runtime_error='A file argument cannot be found')
          return vars.exit_code

      elif arg.endswith('.exe'):
        exe_file_counter += 1
        if not 'exe_name' in file_map:
          file_map['exe_name']: str = arg

      elif arg.endswith('.dll'):
        dll_file_counter += 1
        if not 'dll_name' in file_map:
          file_map['dll_name']: str = arg

    if exe_file_counter + dll_file_counter == 0:
      print('No executable file name given to compile too.')
      return vars.exit_code
    return file_map

  def determineCompiler(file_list: list) -> str:
    """
    Determines what compiler to use depending on source file

    Args:
      file_list (list): The list of values in the file_map

    Returns:
      str: 'gcc' for all .c files and 'g++' for .cpp files
    """
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code

    compiler_type: None = None
    for file in file_list:
      if file.endswith('.cpp'):
        compiler_type: str = 'g++'
      if file.endswith('.c'):
        compiler_type: str = 'gcc'
    return compiler_type

  def compileCountdown(hide_cursor: bool = True):
    if hide_cursor is True:
      print('\033[?25l', end='')  # Hides cursor
    print('--------------------------------------------------------------')
    for i in reversed(range(0, 4)):
      if i == 3: color = Fore.GREEN
      if i == 2: color = Fore.YELLOW
      if i == 1 or i == 0: color = Fore.RED
      print(f'Build operation starting in: {color}{i}...{Style.RESET_ALL}', end='\r')
      time.sleep(1)
    if hide_cursor is True:
      print('\033[?25h', end='')  # Shows cursor
    print('\x1b[2K', end='')

  def outputCompilerText(compiler_text: str, file_list: list, compiled_file: str) -> None:
    """
    Prints the completion text after attempted compilation

    Args:
      compiler_text (str): The output from the popen command
      file_list (list): The list of files used at compilation
      compiled_file (str): The compiled file's name
    """
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code
    if not isinstance(compiler_text, str):
      vars.error(error_type='p', var='compiler_text', type='string')
      return vars.exit_code
    if not isinstance(compiled_file, str):
      vars.error(error_type='p', var='compiled_file', type='string')
      return vars.exit_code

    if compiled_file.endswith('.exe'):
      compile_type: str = 'executable'.upper()
    else:
      compile_type: str = 'dynamic link library'.upper()

    # Really ugly console output code
    if compiler_text == '':
      file_list[-1]: str = ''
      if len(file_list) == 2:
        files: str = ''.join(file_list)
        if os.path.exists(compiled_file):
          print(
            f'\n{Fore.GREEN}!SUCCESS!{Style.RESET_ALL} Compiled file: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
        else:
          print(
            f'\n{Fore.RED}!FAILED!{Style.RESET_ALL} Attempted compile: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
      else:
        files: str = ', '.join(file_list)[:-2]
        if os.path.exists(compiled_file):
          print(
            f'\n{Fore.GREEN}!SUCCESS!{Style.RESET_ALL} Compiled file: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
        else:
          print(
            f'\n{Fore.RED}!FAILED!{Style.RESET_ALL} Attempted compile: ({files} -> {compiled_file}) | {Back.WHITE+Fore.BLACK}{compile_type}{Style.RESET_ALL}\n'
          )
    else:
      print(compiler_text)

  def compileFiles(file_map: dict) -> str:
    """
    Compiles .c, .o, .h and .cpp files into executable's

    Args:
      file_map (dict): The map of files from determineArguments()

    Returns:
      str: The compiled files path/name
    """
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    st: float = time.time()
    file_list: list = list(file_map.values())
    compiler_type: str = core.determineCompiler(file_list)
    cmd_list: list = []

    for file in file_list:
      if file.endswith('.cpp'):
        cmd_list.append(file)
      if file.endswith('.c'):
        cmd_list.append(file)
      if file.endswith('.o'):
        cmd_list.append(file)
      if file.endswith('.h'):
        cmd_list.append(file)
      if file.endswith('.exe'):
        output_file: str = file
        cmd_list.append(file)
    core.compileCountdown()

    cmd_list.insert(-1, '-o')
    cmd_list.insert(0, compiler_type)
    command: str = ' '.join(cmd_list)
    out: str = os.popen(command).read()
    core.outputCompilerText(out, file_list, output_file)
    et: float = time.time()
    print(
      f'\n{Back.MAGENTA}{compiler_type.upper()}{Style.RESET_ALL} compilation took: {Fore.BLUE}{round(et - st, 2)}{Style.RESET_ALL} seconds\n'
    )
    print('--------------------------------------------------------------')
    return output_file

  def compileDLL(file_map: dict) -> str:
    """
    Turns a .c or .cpp file into a .dll file after turning it into an object file

    Args:
      file_map (dict): The map of files from determineArguments()

    Returns:
      str: The compiled files path/name
    """
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    st: float = time.time()
    file_list: list = list(file_map.values())
    compiler_type: str = core.determineCompiler(file_list)
    passed_files: list = []
    cmd_list: list = []

    for file in file_list:
      if file.endswith('.cpp'):
        passed_files.append(file.replace('.cpp', '.o'))
        cmd_list.append(file)
      elif file.endswith('.c'):
        passed_files.append(file.replace('.c', '.o'))
        cmd_list.append(file)
      elif file.endswith('.dll'):
        passed_files.append(file)
    core.compileCountdown()

    cmd_list.insert(-1, '-c')
    cmd_list.insert(0, compiler_type)
    command: str = ' '.join(cmd_list)
    os.popen(command).read()  # No need to make 'out' var here
    cmd_list: list = []

    for file in passed_files:
      if file.endswith('.dll'):
        output_file: str = file
        cmd_list.insert(0, file)  # Put .dll in front
      elif file.endswith('.o'):
        object_file: str = file
        cmd_list.append(file)  # Add .o to any place

    cmd_list.insert(0, '-shared')
    cmd_list.insert(1, '-o')
    cmd_list.insert(0, compiler_type)
    command: str = ' '.join(cmd_list)
    out: str = os.popen(command).read()
    os.remove(object_file)  # Therefore we only return the .dll
    core.outputCompilerText(out, file_list, output_file)
    et: float = time.time()
    print(
      f'\n{Back.MAGENTA}{compiler_type.upper()}{Style.RESET_ALL} compilation took: {Fore.BLUE}{round(et - st, 2)}{Style.RESET_ALL} seconds\n'
    )
    print('--------------------------------------------------------------')
    return output_file


core.compilationCall()
