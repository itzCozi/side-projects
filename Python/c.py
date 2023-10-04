# My compile, run and print to terminal script for C and C++
import os, sys


class globals:
  exit_code = None
  C_compiler = r'c:\MinGW\bin\gcc.exe'
  CP_compiler = r'c:\MinGW\bin\g++.exe'  # CP is a shorthand for C plus plus (C++)
  compiler_type = None  # Changes during runtime depending on C or C++ file

class main:
  # I just like classes
  
  try:
    if __file__.endswith('.py'):
      arg1 = sys.argv[1].lower()
      arg2 = sys.argv[2].lower()
    if __file__.endswith('.exe'):
      arg1 = sys.argv[0].lower()
      arg2 = sys.argv[1].lower()
  except:
    pass
  
  def compileFile1(exe_name: str, source_file: str) -> None:
    if '.exe' in exe_name:
      exe_name = exe_name.replace('.exe', '')

    if source_file.endswith('.c'):
      source_file = source_file.replace('.c', '')
      cmd = f'{globals.C_compiler} {source_file}.c -o {exe_name}.exe'
      print(cmd)
      os.system(cmd)

    elif source_file.endswith('.cpp'):
      source_file = source_file.replace('.cpp', '')
      cmd = f'{globals.CP_compiler} {source_file}.cpp -o {exe_name}.exe'
      print(cmd)
      os.system(cmd)
      
  def standardCompile():
    source_file_name = main.arg1
    executable_name = main.arg2
    main.compileFile1(executable_name, source_file_name)

main.standardCompile()