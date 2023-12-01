# File/Folder compression script -> .exe
# Comprsses files to .gz and folders to .tar.gz
# 7z cmd examples: https://7ziphelp.com/7zip-command-line | https://www.dotnetperls.com/7-zip-examples
# tar in windows: https://stackoverflow.com/questions/37595511/how-to-create-tar-file-on-windows-os
# Types of compression: gz, gztar (tb or tarball)
# EX: ./gunz test/source
# EX: ./gunz test.txt

import time
import os, sys
import platform
import requests
import tarfile
import subprocess

# TODO
'''
* Convert os.system and os.popen to subprocess calls
'''


class Helper:

  @staticmethod
  def download(url: str, newpath: str) -> None:
    file_content: requests.models.Response = requests.get(url)
    open(newpath, 'wb').write(file_content.content)
    print(f'Downloaded file to: "{newpath}"')

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
    win_zip7_path: str = 'C:/Program Files/7-Zip'

  @staticmethod
  def arg_handler() -> None:
    try:
      if __file__.endswith('.py'):
        arg1 = sys.argv[1]          # File name
        arg2 = sys.argv[2].lower()  # Switch arg
      if __file__.endswith('.exe'):
        arg1 = sys.argv[0]          # File name
        arg2 = sys.argv[2].lower()  # Switch arg
    except Exception:
      pass

    if os.path.isfile(arg1):
      Gunz.zip_file(arg2)


  @staticmethod
  def prechecks() -> None:
    # Check 1
    if 'win' in Gunz._Vars.platform:
      if not os.path.exists(Gunz._Vars.win_zip7_path):
        install_promt = input(
          f'ERROR: Cannot find 7zip on system, want to install it? (Y/n): '
        ).lower()
        _7zip_download: str = 'https://www.7-zip.org/download.html'
        if install_promt == 'y' or install_promt == 'yes':
          Helper.download('https://www.7-zip.org/a/7z2301-x64.msi', f'{Helper.get_current_dir()}/7zip.msi')
          if os.path.exists(f'{Helper.get_current_dir()}/7zip.msi'):
            os.system('powershell ./7zip.msi')  # Attempt to run installer
            print(f'Attempted installer run AT: {Helper.get_time()}')
            print(
              f'----------------------------------------------------------------- \
              \nIf this worked please run through the installer, if not please \
              \nrun download the installer manually at the following: \
              \n{_7zip_download} \
              \n-----------------------------------------------------------------'
            )
          else:
            print(f'Automated install failed install manually at: {_7zip_download}')
        else:
          print(
            f'Skipping 7zip install, you will need to download it at: \
            \n{_7zip_download}'
          )

  @staticmethod
  def zip_file(file_path: str) -> str:
    # Scrap all of this and use this: https://stackoverflow.com/questions/8156707/gzip-a-file-in-python
    if not os.path.exists(file_path):
      print(f'ERROR: Given file: "{file_path}" does not exist.')
      return Gunz._Vars.exit_code
    file_path: str = file_path.replace('\\', '/')
    archive_name: str = f'{file_path.split("/")[-1][:file_path.split("/")[-1].find(".")]}.7z'
    prev_size: float = round(os.path.getsize(file_path), 2)

    if 'win' in Gunz._Vars.platform:
      command = [
        'powershell',
        '-Command',
        f'cd "{Gunz._Vars.win_zip7_path}" ; ./7z a "{archive_name}" "{file_path}"'
      ]
      subprocess.run(command, shell=True)
      new_size: float = round(os.path.getsize(archive_name), 2)
      size_reduction: float = round(prev_size / new_size, 2)
      print(f'Successfully zipped file: "{file_path}" to {size_reduction}% of its previous size')

# Entry point / Anti-import statement
if __name__ == '__main__':
  Gunz.zip_file(f'{os.getcwd()}/c.py')#Gunz.arg_handler()
else:
  print(f'ERROR: You cannot import "{__file__}".')
  sys.exit(1)
