import os, sys
import random
import shutil


class vars:
  id_alphabet_str: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  id_alphabet_list: list = list(id_alphabet_str)
  alphabet_str: str = 'abcdefghijklmnopqrstuvwxyz.,'
  alphabet: list = list(alphabet_str)
  pg_char_count: int = 2560
  book_pg_count: int = 350


class helper:
  def genID() -> str:
    length = 14
    alphabet = vars.id_alphabet_list
    ID = []

    for num in range(length):
      char = random.choice(alphabet)
      ID.append(char)
    ID.insert(7, '-')
    return ''.join(ID)


class scride:  # I think this means writer change later

  def makePage() -> int:
    page_num: int = 0
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
      print(f'Page #{page_num} finished. ({page_char_count} characters)')
      with open(f'{helper.genID()}.txt', 'a') as book:
        for line in page_list:
          book.write(f'{line}\n')
      

scride.makePage()
