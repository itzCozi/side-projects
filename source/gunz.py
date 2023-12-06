# DESCRIPTION
# File/Folder compression script -> .exe
# Comprsses files to .gz and folders to .tar.gz
# Types of compression: gz, gzt (tb or tarball), zip
# EX: ./gunz test/source
# EX: ./gunz test.txt

# LINKS / REFERENCES
# 7z cmd examples: https://7ziphelp.com/7zip-command-line | https://www.dotnetperls.com/7-zip-examples
# tar in windows: https://stackoverflow.com/questions/37595511/how-to-create-tar-file-on-windows-os


import time
import os, sys
import platform
import tarfile
import gzip


# TODO
'''
* Add password protected zip with the '-p' arg
* Make it so it will extract to a path if given by user args
'''


class Helper:

  @staticmethod
  def get_current_dir() -> str:
    return os.getcwd().replace('\\', '/')

  @staticmethod
  def get_time() -> str:
    if 'linux' in Gunz._Vars.platform:
      out: str = os.popen("date +%I:%M' '%p").read().replace('\n', '')
    else:
      out: str = os.popen('time /t').read().replace('\n', '')
    return out


class Gunz:
  class _Vars:
    exit_code: None = None
    platform = sys.platform

  @staticmethod
  def arg_handler() -> None:
    try:
      if __file__.endswith('.py'):
        arg1 = sys.argv[1]          # File name
        arg2 = sys.argv[2].lower()  # Switch arg (-): -extract
      if __file__.endswith('.exe'):
        arg1 = sys.argv[0]          # File name
        arg2 = sys.argv[2].lower()  # Switch arg (-): -help
    except Exception:
      pass

    # -h   |  outputs help string (needs to be made)
    # -z   |  use .zip format instead of gz or tar
    # -p   |  for a password protected archive
    # -lvl |  what level to compress the item to
    # TODO: Check if arg2 is a file name too if so make
    # the output archive name arg2

    if os.path.isfile(arg1):
      if tarfile.is_tarfile(arg1):
        Gunz.unzip_tarball(arg1)       # Decompress tarballs with unzip_tarball
      elif arg1.endswith('.gz'):
        Gunz.unzip_file(arg1)          # Unzip gz files with unzip_file
      else:
        Gunz.zip_file(arg1)            # Zip unzipped files with zip_file

    elif os.path.isdir(arg1):
      Gunz.zip_directory(arg1)         # Zip unzipped directorys with zip_directory

  @staticmethod
  def zip_directory(dir_path: str, archive_name: str = '') -> str:
    """
    Zips a directory to a .tgz file EX: test -> test.tgz

    Args:
      dir_path (str): Path of the input directory

    Returns:
      str: The path of the output archive
    """
    if not os.path.exists(dir_path):
      print(f'ERROR: Given directory: "{dir_path}" does not exist.')
      return Gunz._Vars.exit_code

    dir_path: str = dir_path.replace('\\', '/')
    cur_directory: str = Helper.get_current_dir()
    if archive_name == '':
      archive_name: str = f'{cur_directory}/{dir_path.split("/")[-1]}.tgz'

    with tarfile.open(archive_name, 'w:gz') as archive:
      archive.add(f'{dir_path}/')

  @staticmethod
  def unzip_tarball(archive_path: str) -> str:
    # TODO: Make it so it will extract to a path if given by user args
    """
    Unzips a directory to a its original state EX: test.tgz -> test

    Args:
      archive_path (str): Path of the input archive

    Returns:
      str: The path of the output directory
    """
    if not os.path.exists(archive_path):
      print(f'ERROR: Given archive: "{archive_path}" does not exist.')
      return Gunz._Vars.exit_code

    archive_path: str = archive_path.replace('\\', '/')
    with tarfile.open(archive_path, 'r:gz') as tarball:
      tarball.extractall()

  @staticmethod
  def zip_file(file_path: str, archive_name: str = '') -> str:
    """
    Zips a file to a .gz file EX: test.txt -> test.txt.gz

    Args:
      file_path (str): Path of the input file

    Returns:
      str: The path of the output file
    """
    if not os.path.exists(file_path):
      print(f'ERROR: Given file: "{file_path}" does not exist.')
      return Gunz._Vars.exit_code

    file_path: str = file_path.replace('\\', '/')
    cur_directory: str = Helper.get_current_dir()
    prev_size: float = os.path.getsize(file_path)
    if archive_name == '':
      archive_name: str = f'{cur_directory}/{file_path.split("/")[-1]}.gz'

    with open(file_path, 'rb') as fin, gzip.open(archive_name, 'wb') as fout:
      fout.writelines(fin)

    new_size: float = os.path.getsize(archive_name)
    size_reduction: float = round(prev_size / new_size, 2)
    print(f'Successfully compressed file: "{file_path}" to {size_reduction}% of its previous size.')
    return archive_name

  @staticmethod
  def unzip_file(file_path: str) -> str:
    # TODO: Make it so it will extract to a path if given by user args
    """
    Unzips a file to its original state EX: test.txt.gz -> test.txt

    Args:
      file_path (str): Path of the input '.gz' file

    Returns:
      str: The path of the output archive
    """
    if not os.path.exists(file_path):
      print(f'ERROR: Given file: "{file_path}" does not exist.')
      return Gunz._Vars.exit_code

    file_path: str = file_path.replace('\\', '/')
    cur_directory: str = Helper.get_current_dir()
    prev_size: float = os.path.getsize(file_path)
    file_archive_name: str = file_path.split("/")[-1]
    out_file_name: str = f'{cur_directory}/{file_archive_name[:file_archive_name.find(".gz")]}'

    with gzip.open(file_path, 'rb') as fin, open(out_file_name, 'wb') as fout:
      fout.writelines(fin)

    new_size: float = os.path.getsize(file_path.replace('.gz', ''))
    size_increase: float = round(prev_size / new_size, 2)
    print(f'Successfully uncompressed archive: "{file_path}" to {size_increase}x its previous size.')
    return file_path


# Entry point / Anti-import statement
if __name__ == '__main__':
  Gunz.arg_handler()
else:
  print(f'ERROR: You cannot import "{__file__}".')
  sys.exit(1)
