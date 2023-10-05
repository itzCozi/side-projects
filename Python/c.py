# My compile, run and print to terminal script for C and C++
import os, sys
import time
from colorama import Fore, Back, Style

# TODO's
'''
* All functions use camelCase and variables use snake_case
* See if dragging files on top of the program show the file
as a virtual argument
* See if i can add a function to write cmake files to compile mitlipe source files
https://stackoverflow.com/questions/5950395/makefile-to-compile-multiple-c-programs
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

  exit_code = None
  C_compiler = r'c:\MinGW\bin\gcc.exe'
  CPP_compiler = r'c:\MinGW\bin\g++.exe'


class core:
  # Only can compile .o, .c, .cpp and .h

  @staticmethod
  def compilationCall() -> None:
    arg_table = core.determineArguments()
    if 'dll_name' in arg_table:
      core.compileDLL(arg_table)
    elif 'exe_name' in arg_table:
      core.compileFiles(arg_table)
    else:
      print('Neither "exe_name" or "dll_name" is not in argument list.')

  @staticmethod
  def determineArguments() -> dict:
    arg_list = list(sys.argv)
    source_file_counter = 0
    object_file_counter = 0
    header_file_counter = 0
    exe_file_counter = 0
    file_map = {}

    for arg in arg_list:
      if arg.endswith('.cpp'):
        source_file_counter += 1
        file_map[f'source_file{source_file_counter}'] = arg
      elif arg.endswith('.c'):
        source_file_counter += 1
        file_map[f'source_file{source_file_counter}'] = arg
      elif arg.endswith('.o'):
        object_file_counter += 1
        file_map[f'object_file{object_file_counter}'] = arg
      elif arg.endswith('.h'):
        header_file_counter += 1
        file_map[f'header_file{header_file_counter}'] = arg
      elif arg.endswith('.exe'):
        exe_file_counter += 1
        file_map['exe_name'] = arg
      elif arg.endswith('.dll'):
        exe_file_counter += 1
        file_map['dll_name'] = arg
    if exe_file_counter == 0 or exe_file_counter > 1:
      print('No executable name given to compile to or more than 1 name given.')
    return file_map

  def determineCompiler(file_list: list) -> str:
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code

    compiler_type = None
    for file in file_list:
      if file.endswith('.cpp'):
        compiler_type = 'g++'
      if file.endswith('.c'):
        compiler_type = 'gcc'
    return compiler_type

  def outputCompilerText(compiler_text: str, file_list: list, compiled_file: str) -> None:
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
      compile_type = 'executable'.upper()
    else:
      compile_type = 'dynamic link library'.upper()

    if compiler_text == '':
      file_list[-1] = ''
      if len(file_list) == 2:
        files = ''.join(file_list)
        print(f'\n{Fore.GREEN}!SUCCESS!{Style.RESET_ALL} Compiled file: ({files} -> {compiled_file}) | {compile_type}\n')
      else:
        files = ', '.join(file_list)[:-2]
        print(f'\n{Fore.GREEN}!SUCCESS!{Style.RESET_ALL} Compiled file: ({files} -> {compiled_file}) | {compile_type}\n')
    else:
      print(compiler_text)

  def compileFiles(file_map: dict) -> str:
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    st = time.time()
    file_list = list(file_map.values())
    compiler_type = core.determineCompiler(file_list)
    cmd_list = []

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
        output_file = file
        cmd_list.append(file)
    for i in reversed(range(1, 4)):
      print(f'Build operation starting in: {i}', end='\r')
      time.sleep(1)
    print('\x1b[2K', end='')

    cmd_list.insert(-1, '-o')
    cmd_list.insert(0, compiler_type)
    command = ' '.join(cmd_list)
    out = os.popen(command).read()
    core.outputCompilerText(out, file_list, output_file)
    et = time.time()
    print(f'\nCompilation took: {et-st} seconds\n')
    return output_file

  def compileDLL(file_map: dict) -> str:
    # https://stackoverflow.com/questions/705501/how-do-i-compile-a-cpp-source-file-into-a-dll
    # Turns a .c or .cpp file into a .dll file after turning it
    # into a object_file (described in the stack overflow question)
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    st = time.time()
    file_list = list(file_map.values())
    compiler_type = core.determineCompiler(file_list)
    passed_files = []
    cmd_list = []

    for file in file_list:
      if file.endswith('.cpp'):
        passed_files.append(file.replace('.cpp', '.o'))
        cmd_list.append(file)
      elif file.endswith('.c'):
        passed_files.append(file.replace('.c', '.o'))
        cmd_list.append(file)
      elif file.endswith('.dll'):
        passed_files.append(file)
    for i in reversed(range(1, 4)):
      print(f'Build operation starting in: {i}', end='\r')
      time.sleep(1)
    print('\x1b[2K', end='')

    cmd_list.insert(-1, '-c')
    cmd_list.insert(0, compiler_type)
    command = ' '.join(cmd_list)
    out = os.popen(command).read()
    cmd_list = []

    for file in passed_files:
      if file.endswith('.dll'):
        output_file = file
        cmd_list.insert(0, file)  # Put .dll infront
      elif file.endswith('.o'):
        object_file = file
        cmd_list.append(file)  # Add .o to any place

    cmd_list.insert(0, '-shared')
    cmd_list.insert(1, '-o')
    cmd_list.insert(0, compiler_type)
    command = ' '.join(cmd_list)
    out = os.popen(command).read()
    os.remove(object_file)  # Therefore we only return the .dll
    core.outputCompilerText(out, file_list, output_file)
    et = time.time()
    print(f'\nCompilation took: {et-st} seconds\n')
    return output_file


core.compilationCall()
