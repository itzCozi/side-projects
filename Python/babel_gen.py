import os, sys
import random
import shutil


# CODE
'''
* All functions use camelCase and variables use snake_case
* All variable declarations must be type hinted EX: num: int = 0
* If a function has parameters each variable must have specified types
* Functions without any parameters in a class must have the @staticmethod tag
* If a variable or function uses more than one type use EX: num: int | float = 0.1
-------------- Project Specific --------------
* A book is a .txt file with 350 pages and 2560 chars per page
* A case is a .zip file filed with 10 books, file starts with ZIP
* A library is more than one case in a single file or archive, starts with LIB
'''

# TODO
'''
* Find out whats causing permissions error
* Add isinstance and all that stuff
* Add doc-strings
* COMPILE TO .EXE
'''


class vars:

  def error(error_type: str, var: str = None, type: str = None, runtime_error: str = None) -> None:
    if error_type == 'p':
      print(f'PARAMETER: Given variable {var} is not a {type}.')
    elif error_type == 'r':
      print(f'RUNTIME: {runtime_error.capitalize()}.')
    elif error_type == 'u':
      print('UNKNOWN: An unknown error was encountered.')

  exit_code: None = None
  platform: str = sys.platform
  DEV_MODE: bool = True  # Change to 'False' if on linux (or lose all your files)
  id_alphabet_str: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  id_alphabet_list: list = list(id_alphabet_str)
  alphabet_str: str = 'abcdefghijklmnopqrstuvwxyz., '
  alphabet: list = list(alphabet_str)
  pg_char_count: int = 2560
  book_pg_count: int = 350


class helper:

  def clearBooksFromVM(rm_zip: bool = False) -> None:  # Deletes all books from VM
    """
    Used to delete extra books after debugging

    Args:
      rm_zip (bool): If true remove .zip files too
    """
    if not isinstance(rm_zip, bool):
      vars.error(error_type='p', var='rm_zip', type='boolean')
      return vars.exit_code

    for item in os.listdir('/home/runner/dev'):
      if rm_zip is True:
        if item.endswith('.zip'):
          os.remove(item)
      if item.endswith('.txt'):
        os.remove(item)

  def zipBooks(file_list: list, output_path: str) -> str:
    """
    Puts items file_list into a zip file

    Args:
      file_list (list): The list of files to be archived
      output_path (str): The path to make the archive

    Returns:
      str: The path of the archive
    """
    if not isinstance(file_list, list):
      vars.error(error_type='p', var='file_list', type='list')
      return vars.exit_code
    if not isinstance(output_path, str):
      vars.error(error_type='p', var='output_path', type='string')
      return vars.exit_code

    dump_dir: str = helper.genID()  # Not a case because it's removed after use
    os.mkdir(dump_dir)
    for target in file_list:
      target_file: str = target.split('\\')[-1]
      with open(target, 'rb') as file_in:
        content: bytes = file_in.read()
      with open(f'{dump_dir}/{target_file}', 'wb') as file_out:
        file_out.write(content)

    zip_file: str = shutil.make_archive(output_path, 'zip', dump_dir)
    shutil.rmtree(dump_dir)
    for file in file_list:
      os.remove(file)
    return zip_file

  def genID(zip: bool = False, lib: bool = False) -> str:
    """
    Generates IDs for different file types

    Args:
      zip (bool): If making id for zip file
      lib (bool): If making id for lib file

    Returns:
      str: The ID as a string
    """
    if not isinstance(zip, bool):
      vars.error(error_type='p', var='zip', type='boolean')
      return vars.exit_code
    if not isinstance(lib, bool):
      vars.error(error_type='p', var='lib', type='boolean')
      return vars.exit_code

    length: int = 14
    alphabet: list = vars.id_alphabet_list
    id: list = []

    for num in range(length):
      char: str = random.choice(alphabet)
      id.append(char)
    if zip is True:
      for i in range(3):
        id.remove(random.choice(id))
      id.insert(4, '-') ; id.insert(0, 'ZIP')
    elif lib is True:
      for i in range(3):
        id.remove(random.choice(id))
      id.insert(4, '-') ; id.insert(0, 'LIB')
    else:
      id.insert(7, '-')
    return ''.join(id)


class scribe:

  @staticmethod
  def make10Books() -> list:
    """
    Makes 10 books in current directory

    Returns:
      list: The list of paths to each book
    """
    book_num: int = 0
    book_list: list = []
    book_char_count: int = 0
    group_char_count: int = 0

    for book in range(10):
      page_num: int = 0
      book_path: str = f'{helper.genID()}.txt'

      for page in range(vars.book_pg_count):
        page_list: list = []
        char_ticker: int = 0

        title_list: list = []
        title_str: str = ''.join(random.choices(vars.alphabet, k=12))
        for i in range(52): title_list.append(' ')
        title_list.insert(int(52 / 2), title_str)
        page_list.append(''.join(title_list))  # Append title to page

        line_list: list = []

        for char in range(vars.pg_char_count - len(page_list[0])):
          char_ticker += 1
          if char_ticker % 64 == 0:
            if len(line_list) != 64:
              for i in range(64 - len(line_list)):
                line_list.append(random.choice(vars.alphabet))
            page_list.append(''.join(line_list))
            line_list: list = []
          line_list.append(random.choice(vars.alphabet))

        page_num += 1
        page_char_count: int = len(''.join(page_list))
        group_char_count += page_char_count
        book_char_count += page_char_count
        if page_num == 350:
          book_num += 1
          book_list.append(book_path)
          print(
            f'\n* Book "{book_path}" #{book_num} character count: {book_char_count}'
            f'\n* Book "{book_path}" #{book_num} created with {vars.book_pg_count} pages\n'
          )
          group_char_count: int = 0
        elif page_num % 50 == 0:
          print(f'Page #{page_num} finished ({group_char_count} characters)')
          group_char_count: int = 0
        with open(book_path, 'a') as file:
          for line in page_list:
            file.write(f'{line}\n')
      book_char_count: int = 0
    return book_list

  def generateCases(amount: int) -> None:
    """
    Zips books together into cases and library's

    Args:
      amount (int): The amount of cases in the library
    """
    if not isinstance(amount, int):
      vars.error(error_type='p', var='amount', type='integer')
      return vars.exit_code
    if 'linux' in vars.platform and vars.DEV_MODE is True:  # For testing VM
      del_files: str = input('Delete all .txt and .zip files in dev? (y/n): ')
      if del_files == 'y' or del_files == 'yes': helper.clearBooksFromVM(True)

    zip_list: list = []
    for book_cycle in range(amount):
      case_list: list = scribe.make10Books()
      if book_cycle + 1 == amount:
        print('----------------------------------------------')
      else:
        print('----------------------------------------------\n')
      zip_file: str = helper.zipBooks(case_list, helper.genID(zip=True))
      zip_list.append(zip_file)

    for zip in zip_list:
      idx: int = zip_list.index(zip)
      file_name: str = '/'.join(zip.split('\\')[-3:])
      file_size: int | float = round(os.path.getsize(zip_list[idx]) / 125000, 2)
      print(f'{idx + 1}. Archive "{file_name}" is {file_size} MB')

    master_zip: str = helper.zipBooks(zip_list, helper.genID(lib=True))
    master_size: int | float = round(os.path.getsize(master_zip) / 125000, 2)
    master_name: str = '/'.join(master_zip.split('\\')[-3:])
    print(f'Master archive "{master_name}" is {master_size} MB')
    print('----------------------------------------------')


scribe.generateCases(5)
