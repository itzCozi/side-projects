# File/Folder compression script -> .exe
# 7-Zip Path: C:\Program Files\7-Zip
# 7z cmd examples: https://7ziphelp.com/7zip-command-line | https://www.dotnetperls.com/7-zip-examples
# Types of compression: 7z, zip, gzip, gztar (tb or tarball)
# EX: ./gunz -7z test/source   (only arg without '-' is the path)
# EX: ./gunz -gz test.txt      (compresses test.txt with gunzip)

import os, sys
import platform
import requests
import subprocess

# TODO
'''
* Convert os.system and os.popen to subprocess calls
'''


class Helper:

  def download(url: str, newpath: str) -> None:
    file_content: requests.models.Response = requests.get(url)
    open(newpath, 'wb').write(file_content.content)
    print(f'Downloaded file to: "{newpath}"')

  def get_current_dir() -> str:
    return os.getcwd().replace('\\', '/')

  def get_time() -> str:
    if 'linux' in Gunz._Vars.platform:
      out: str = os.popen("date +%I:%M' '%p").read().replace('\n', '')
    else:
      out: str = os.popen('time /t').read().replace('\n', '')
    return out


class Gunz:

  class _Vars:
    error_code: None = None
    platform = sys.platform
    gz_compression_lvl: str = '-6'  # Argument to pass to gunzip for compression level
    win_zip7_path: str = 'C:/Program Files/7-Zip'

  @staticmethod
  def arg_handler() -> None:
    try:
      if __file__.endswith('.py'):
        arg1 = sys.argv[1].lower()
        arg2 = sys.argv[2]
      if __file__.endswith('.exe'):
        arg1 = sys.argv[0].lower()
        arg2 = sys.argv[1]
    except Exception:
      pass

    try:
      match arg1:

        case '-7z':  # Compress a file or folder with '7z'
          ...

        case '-zip':  # Compress a file or folder with 'zip'
          ...

        case '-gz':  # Compress a file or folder with 'gunzip'
          ...

        case '-tb' | '-tarball': # Compress a file or folder with 'tape archive'
          ...

        case _:  # Else statement
          print(f'ERROR: The given argument: "{arg1}" is not recognized.')
          sys.exit(1)

    except PermissionError:
      print('ERROR: Action executed without required permissions.')
      sys.exit(1)
    except Exception as e:
      print(f'ERROR: A runtime error occurred, is the process running? \n{e}\n')
      sys.exit(1)

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
          Helper._download('https://www.7-zip.org/a/7z2301-x64.msi', Helper.get_current_dir())
          if os.path.exists(f'{Helper.get_current_dir}/7z2301-x64.msi'):
            os.system('powershell ./7z2301-x64.msi')  # Attempt to run installer
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

          

# Entry point / Anti-import statement
if __name__ == '__main__':
  Gunz.arg_handler()
else:
  print(f'ERROR: You cannot import "{__file__}".')
  sys.exit(1)
