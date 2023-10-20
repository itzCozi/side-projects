# Decentralized My Eyes Only


import os
import sys
import random
import string
import shutil
import pyminizip

# CODE
'''
* All variable declarations must be type hinted EX: num: int = 0
* If a function has parameters each variable must have specified types
* All functions and classes use camelCase and variables use snake_case
* Functions without 'self' parameter in a class must have the @staticmethod tag
* If a variable or function uses more than one type use EX: num: int | float = 0.1
'''

# TODO
'''
* Make a password zip function so i can put
the file zips into the password protected
archive
* Add doc-strings
'''


def random_id() -> str:
  length: int = 8
  alphabet: list = list(string.ascii_uppercase + string.digits)
  id_list: list = []
  for i in range(length):
    id_list.append(random.choice(alphabet))
  id_list.insert(4, '-')
  return str(''.join(id_list))


def zip_file(target: str, output_path: str = '') -> str:
  """
  Zips either one file or one directory

  Args:
    target (str): The file or directory to compress
    output_path (str, optional): The path to the '.zip' file. Defaults to ''.

  Returns:
    str: The path to the .zip file
  """
  cur_dir = os.getcwd().replace('\\', '/')
  if output_path == '': output_path = cur_dir
  zip_path = f'{output_path}/{random_id()}'
  dump_dir = f'{cur_dir}/{random_id()}'
  os.mkdir(dump_dir)

  if os.path.isfile(target):
    with open(target, 'rb') as file_in:
      content = file_in.read()
    with open(f'{dump_dir}/{target}', 'wb') as file_out:
      file_out.write(content)
  elif os.path.isdir(target):
    shutil.copytree(target, f'{dump_dir}/{target.split("/")[-1]}')

  zip_file = shutil.make_archive(zip_path, 'zip', dump_dir)
  shutil.rmtree(dump_dir)
  return zip_file.replace('\\', '/')


def unzip_file(file_path: str) -> str:
  """
  Unzip an archive to a folder named after it 

  Args:
    file_path (str): The path to the '.zip' file

  Returns:
    str: The path to the directory
  """
  cur_dir = os.getcwd().replace('\\', '/')
  out_dir = f'{cur_dir}/{file_path.split("/")[-1][:-4]}'
  shutil.unpack_archive(file_path, out_dir, 'zip')
  return out_dir


zip_file('Coop-OS')
