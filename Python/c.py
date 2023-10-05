# My compile, run and print to terminal script for C and C++
import os, sys

# TODO's
'''
* All functions use camelCase and variables use snake_case
* See if dragging files on top of the program show the file
as a virtual argument
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


class main:
  # Only can compile .o, .c, .cpp and .h -> .EXE (NOT .DLL)

  @staticmethod
  def compilationCall() -> None:
    arg_table = main.determineArguments()
    if 'dll_name' in arg_table:
      main.compileDLL(arg_table)
    elif 'exe_name' in arg_table:
      main.compileFiles(arg_table)
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

  def outputCompilerText(compiler_text: str, file_list: list, compile_type: str) -> None:
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code
    if not isinstance(compiler_text, str):
      vars.error(error_type='p', var='compiler_text', type='string')
      return vars.exit_code
    if not isinstance(compile_type, str):
      vars.error(error_type='p', var='compile_type', type='string')
      return vars.exit_code

    if compiler_text == '':
      file_list[-1] = ''
      if len(file_list) == 2:
        files = ''.join(file_list)
        print(f'Compiled files: {files} -> {compile_type.upper()}')
      else:
        files = ', '.join(file_list)[:-2]
        print(f'Compiled files: {files} -> {compile_type.upper()}')

  def compileFiles(file_map: dict) -> None:
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    file_list = list(file_map.values())
    compiler_type = main.determineCompiler(file_list)
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
        cmd_list.append(file)

    cmd_list.insert(-1, '-o')
    cmd_list.insert(0, compiler_type)
    command = ' '.join(cmd_list)
    out = os.popen(command).read()
    main.outputCompilerText(out, file_list, 'exe')

  def compileDLL(file_map: dict) -> None:
    # https://stackoverflow.com/questions/705501/how-do-i-compile-a-cpp-source-file-into-a-dll
    # Turns a .c or .cpp file into a .dll file after turning it
    # into a object_file (described in the stack overflow question)
    if not isinstance(file_map, dict):
      vars.error(error_type='p', var='file_map', type='dict')
      return vars.exit_code

    file_list = list(file_map.values())
    compiler_type = main.determineCompiler(file_list)
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

    cmd_list.insert(-1, '-c')
    cmd_list.insert(0, compiler_type)
    command = ' '.join(cmd_list)
    out = os.popen(command).read()
    cmd_list = []

    for file in passed_files:
      if file.endswith('.dll'):
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
    main.outputCompilerText(out, file_list, 'dll')


main.compilationCall()
