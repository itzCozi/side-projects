import os, sys
import random
import shutil
import requests

# CODE
'''
* All variable declarations must be type hinted EX: num: int = 0
* If a function has parameters each variable must have specified types
* All functions and classes use camelCase and variables use snake_case
* Functions without 'self' parameter in a class must have the @staticmethod tag
* If a variable or function uses more than one type use EX: num: int | float = 0.1
-------------- Project Specific --------------
* A book is a .txt file with 350 pages and 2560 chars per page
* A case is a .zip file filed with 10 books, file starts with ZIP
* A library is more than one case in a single file or archive, starts with LIB
'''

# TODO
'''
* Add a real word generator so i can incorporate real words
into books if a certain argument is given
* Make the unzip function actually work
* Add isinstance and all that stuff
* Add doc-strings
* COMPILE TO .EXE
'''


class Vars:

  @staticmethod
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


class Helper:

  @staticmethod
  def clear_books_from_vm(rm_zip: bool = False) -> None:  # Deletes all books from VM
    """
    Used to delete extra books after debugging

    Args:
      rm_zip (bool): If true remove .zip files too
    """
    if not isinstance(rm_zip, bool):
      Vars.error(error_type='p', var='rm_zip', type='boolean')
      return Vars.exit_code

    for item in os.listdir('/home/runner/dev'):
      if rm_zip is True and item.endswith('.zip'):
        os.remove(item)
      if item.endswith('.txt'):
        os.remove(item)

  @staticmethod
  def generateWordList():
    # Generates a random sentence for type function
    word_site = 'https://www.mit.edu/~ecprice/wordlist.10000'
    response = requests.get(word_site)
    baselist = []
    listA = []
    ticker = -1

    for i in range(random.randint(6, 16)):
      baselist.append(random.choice(response.content.splitlines()))

    for word in baselist:
      if len(word) >= 5 and len(listA) < 10:
        listA.append(word)
      else:
        pass

    for item in listA:
      if isinstance(item, bytes):
        ticker += 1
        listA[ticker] = item.decode()
    first_item = list(listA[0])
    first_item[0] = first_item[0].upper()
    listA[0] = ''.join(first_item)
    return listA

  @staticmethod
  def zip_books(file_list: list, output_path: str) -> str:
    """
    Puts items file_list into a zip file

    Args:
      file_list (list): The list of files to be archived
      output_path (str): The path to make the archive

    Returns:
      str: The path of the archive
    """
    if not isinstance(file_list, list):
      Vars.error(error_type='p', var='file_list', type='list')
      return Vars.exit_code
    if not isinstance(output_path, str):
      Vars.error(error_type='p', var='output_path', type='string')
      return Vars.exit_code

    dump_dir: str = Helper.gen_id()  # Not a case because it's removed after use
    os.mkdir(dump_dir)
    for target in file_list:
      target_file: str = target.split('\\')[-1]
      with open(target, 'rb') as file_in:
        content: bytes = file_in.read()
      with open(target_file, 'wb') as file_out:
        file_out.write(content)

    zip_file: str = shutil.make_archive(output_path, 'zip', dump_dir)
    shutil.rmtree(dump_dir)
    for file in file_list:
      os.remove(file)
    return zip_file

  @staticmethod
  def unzip_books(zip_path: str) -> str:  # Doesnt work
    """
    Unzips the given zip file

    Args:
      zip_path (list): The path to the zip file

    Returns:
      str: The path of the unzipped folder
    """
    # Puts all files in a zip file into a folder (dir)
    # https://www.geeksforgeeks.org/python-shutil-unpack_archive-method/
    if not isinstance(zip_path, str):
      Vars.error(error_type='p', var='zip_path', type='string')
      return Vars.exit_code

    #out_dir: str = f'{os.getcwd()}/{Helper.gen_id()}'.replace('\\', '/')
    #os.mkdir(out_dir)
    shutil.unpack_archive(zip_path)
    return zip_path

  @staticmethod
  def gen_id(zip: bool = False, lib: bool = False) -> str:
    """
    Generates IDs for different file types

    Args:
      zip (bool): If making id for zip file
      lib (bool): If making id for lib file

    Returns:
      str: The ID as a string
    """
    if not isinstance(zip, bool):
      Vars.error(error_type='p', var='zip', type='boolean')
      return Vars.exit_code
    if not isinstance(lib, bool):
      Vars.error(error_type='p', var='lib', type='boolean')
      return Vars.exit_code

    length: int = 14
    alphabet: list = Vars.id_alphabet_list
    id: list = []

    for num in range(length):
      char: str = random.choice(alphabet)
      id.append(char)
    if zip is True:
      for i in range(3):
        id.remove(random.choice(id))
      id.insert(4, '-')
      id.insert(0, 'ZIP')
    elif lib is True:
      for i in range(3):
        id.remove(random.choice(id))
      id.insert(4, '-')
      id.insert(0, 'LIB')
    else:
      id.insert(7, '-')
    return ''.join(id)


class Scribe:

  @staticmethod
  def make_books(amount: int = 10, output_dir: str = '') -> list:
    """
    Makes 10 (or 'n') books in current directory

    Args:
      amount (int): The amount of books to make
      output_dir (str): The path to the output directory
      from the current directory

    Returns:
      list: The list of paths to each book
    """
    book_num: int = 0
    book_list: list = []
    book_char_count: int = 0
    group_char_count: int = 0

    for book in range(amount):
      page_num: int = 0
      if output_dir != '':  # Might have to add a os.getcwd() later
        book_path: str = f'{output_dir}/{Helper.gen_id()}.txt'.replace('\\', '/')
      else:
        book_path: str = f'{Helper.gen_id()}.txt'

      for page in range(Vars.book_pg_count):
        page_list: list = []
        char_ticker: int = 0

        title_list: list = []
        title_str: str = ''.join(random.choices(Vars.alphabet, k=12))
        for i in range(52): title_list.append(' ')
        title_list.insert(int(52 / 2), title_str)
        page_list.append(''.join(title_list))  # Append title to page

        line_list: list = []

        for char in range(Vars.pg_char_count - len(page_list[0])):
          char_ticker += 1
          if char_ticker % 64 == 0:
            if len(line_list) != 64:
              for i in range(64 - len(line_list)):
                line_list.append(random.choice(Vars.alphabet))
            page_list.append(''.join(line_list))
            line_list: list = []
          line_list.append(random.choice(Vars.alphabet))

        page_num += 1
        page_char_count: int = len(''.join(page_list))
        group_char_count += page_char_count
        book_char_count += page_char_count
        if page_num == 350:
          book_num += 1
          book_list.append(book_path)
          print(
            f'\n* Book "{book_path}" #{book_num} character count: {book_char_count}'
            f'\n* Book "{book_path}" #{book_num} created with {Vars.book_pg_count} pages\n'
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

  @staticmethod
  def generate_cases(amount: int) -> str:
    """
    Zips books together into cases and library's

    Args:
      amount (int): The amount of cases in the library

    Returns:
      str: The path to the library containing each case
    """
    if not isinstance(amount, int):
      Vars.error(error_type='p', var='amount', type='integer')
      return Vars.exit_code
    if 'linux' in Vars.platform and Vars.DEV_MODE is True:  # For testing VM
      del_files: str = input('Delete all .txt and .zip files in dev? (y/n): ')
      if del_files == 'y' or del_files == 'yes': Helper.clear_books_from_vm(True)

    zip_list: list = []
    for book_cycle in range(amount):
      case_list: list = Scribe.make_books()
      if book_cycle + 1 == amount:
        print('----------------------------------------------')
      else:
        print('----------------------------------------------\n')
      zip_file: str = Helper.zip_books(case_list, Helper.gen_id(zip=True))
      zip_list.append(zip_file)

    for zip in zip_list:
      idx: int = zip_list.index(zip)
      file_name: str = '/'.join(zip.split('\\')[-3:])
      file_size: int | float = round(os.path.getsize(zip_list[idx]) / 125000, 2)
      print(f'{idx + 1}. Archive "{file_name}" is {file_size} MB')

    master_zip: str = Helper.zip_books(zip_list, Helper.gen_id(lib=True))
    master_size: int | float = round(os.path.getsize(master_zip) / 125000, 2)
    master_name: str = '/'.join(master_zip.split('\\')[-3:])
    print(f'Master archive "{master_name}" is {master_size} MB')
    print('----------------------------------------------')
    return master_zip


if __name__ == "__main__":
  Scribe.generate_cases(1)
