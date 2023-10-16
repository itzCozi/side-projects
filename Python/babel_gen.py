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
'''

# TODO
'''
* Add compression function to compress 10 books into a archive
'''


class vars:
  id_alphabet_str: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  id_alphabet_list: list = list(id_alphabet_str)
  alphabet_str: str = 'abcdefghijklmnopqrstuvwxyz., '
  alphabet: list = list(alphabet_str)
  pg_char_count: int = 2560
  book_pg_count: int = 350


class helper:
  def genID(zip: bool = False) -> str:
    length = 14
    alphabet = vars.id_alphabet_list
    ID = []

    for num in range(length):
      char = random.choice(alphabet)
      ID.append(char)
    if zip is True:
      for i in range(3): ID.remove(random.choice(ID))
      ID.insert(4, '-')
      ID.insert(0, 'ZIP')
    else:
      ID.insert(7, '-')
    return ''.join(ID)


class scride:  # I think this means writer change later

  def makeBook() -> int:
    page_num: int = 0
    book_path: str = f'{helper.genID()}.txt'
    for page in range(vars.book_pg_count):
      page_list: list = []
      char_ticker: int = 0

      title_str: str = ''.join(random.choices(vars.alphabet, k=12))
      title_list: list = []
      spacer_length: int = 52
      for i in range(spacer_length): title_list.append(' ')
      title_list.insert(int(spacer_length/2), title_str)
      page_list.append(''.join(title_list))  # Append title to page

      line_list = []

      for char in range(vars.pg_char_count - len(page_list[0])):
        char_ticker += 1
        if char_ticker % 64 == 0:
          if len(line_list) != 64:
            for i in range(64 - len(line_list)):
              line_list.append(random.choice(vars.alphabet))
          page_list.append(''.join(line_list))
          line_list = []
        line_list.append(random.choice(vars.alphabet))

      page_num += 1
      page_char_count: int = len(''.join(page_list))
      if page_num == 350:
        print(f'Book "{book_path}" created with {vars.book_pg_count} pages.')
      else:  
        print(f'Page #{page_num} finished. ({page_char_count} characters)')
      with open(book_path, 'a') as book:
        for line in page_list:
          book.write(f'{line}\n')


scride.makeBook()
def clearBooksFromVM() -> None:  # Deletes all books from replit VM
  for item in os.listdir('/home/runner/dev'):
    if item.endswith('.txt'): os.remove(item)