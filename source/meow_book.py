# Meow book generater
import os, sys
import string
import random


class Globals:
  page_count: int = 400
  chars_per_line: int = 64
  line_count: int = 35


class Helper:

  @staticmethod
  def random_id() -> str:
    length: int = 8
    alphabet: list = list(string.ascii_uppercase + string.digits)
    id_list: list = []
    for i in range(length):
      id_list.append(random.choice(alphabet))
    id_list.insert(4, '-')
    return str(''.join(id_list))


def write_book():
  # TODO: Add uppercase support
  book_name: str = Helper.random_id()
  pun_list: list = ['.', '!', ',', ';']
  for page_num in range(Globals.page_count):
    for line in range(Globals.line_count):
      char_ticker: int = 0
      m_count: int = random.randint(1, 5)
      e_count: int = random.randint(1, 5)
      o_count: int = random.randint(1, 5)
      w_count: int = random.randint(1, 5)
      __count: int = random.randint(1, 3)
      meow_list: list = [m_count, e_count, o_count, w_count, __count]
      char_ticker += sum(meow_list)

      if char_ticker != 63:
        out_list: list = []
        for m in range(m_count):
          out_list.append('m')
        for e in range(e_count):
          out_list.append('e')
        for o in range(o_count):
          out_list.append('o')
        for w in range(w_count):
          out_list.append('w')

        out_list.append(random.choice(pun_list))
        for white in range(__count):
          out_list.append(' ')
        with open(f'{book_name}.txt', 'a') as file:
          # Print the meow list then a symbol
          print(''.join(out_list))
          file.write(''.join(out_list))
      else:
        with open(f'{book_name}.txt', 'a') as file:
          file.write('\n')
        continue


write_book()
