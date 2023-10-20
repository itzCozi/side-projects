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
* Make the unzip function
* Add doc-strings
'''


def random_id() -> str:
  length: int = 8
  alphabet: list = list(string.ascii_letters + string.digits)
  id_list: list = []
  for i in range(length):
    id_list.append(random.choice(alphabet))
  id_list.insert(4, '-')
  return str(''.join(id_list))


def zip_file(target: str, archive_name: str, output_path: str = '') -> str:  # Might make this name it self and return the ID
  """
  Zips either one file or one directory

  Args:
    target (str): The file or directory to compress
    archive_name (str): The name of the .zip file
    output_path (str, optional): The path to the .zip file. Defaults to ''.

  Returns:
    str: The path to the .zip file
  """
  if archive_name[-4:] == '.zip':
    archive_name = archive_name[:-4]

  cur_dir = os.getcwd().replace('\\', '/')
  if output_path == '': output_path = cur_dir
  zip_path = f'{output_path}/{archive_name}'
  dump_dir = f'{cur_dir}/{random_id()}'
  os.mkdir(dump_dir)

  if os.path.isfile(target):
    with open(target, 'rb') as Fin:
      content = Fin.read()
    with open(f'{dump_dir}/{target}', 'wb') as Fout:
      Fout.write(content)
  elif os.path.isdir(target):
    shutil.copytree(target, f'{dump_dir}/{target.split("/")[-1]}')

  zip_file = shutil.make_archive(zip_path, 'zip', dump_dir)
  shutil.rmtree(dump_dir)
  return zip_file

def unzip_file(file_path: str, out_dir: str) -> str:
  # Have to make this work: https://www.geeksforgeeks.org/python-shutil-unpack_archive-method/
  file_path = file_path.replace('\\', '/')
  cur_dir = os.getcwd().replace('\\', '/')
  #os.mkdir(file_path.split("/")[-1][:-4])
  out_path = f'{cur_dir}/{file_path.split("/")[-1]}'

  shutil.unpack_archive(filename=file_path, format='zip')
  #return out_path



unzip_file('out.zip', 'out')
