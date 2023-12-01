# File/Folder compression script -> .exe
# 7-Zip Path: C:\Program Files\7-Zip
# 7z cmd examples: https://7ziphelp.com/7zip-command-line
# Types of compression: 7z, zip, gzip, gztar (tb or tarball)
# EX: ./gunz -7z test/source   (only arg without '-' is the path)
# EX: ./gunz -gz test.txt      (compresses test.txt with gunzip)

import os, sys
import platform
import subprocess

# TODO
'''
* Re-build and release new version
'''


class gunz:

  class _Vars:
    error_code: None = None
    platform = sys.platform
    gz_compression_lvl: str = '-6'  # Argument to pass to gunzip for compression level

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


# Entry point / Anti-import statement
if __name__ == '__main__':
  gunz.arg_handler()
else:
  print(f'ERROR: You cannot import "{__file__}".')
  sys.exit(1)
