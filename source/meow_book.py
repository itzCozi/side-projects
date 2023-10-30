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
  # TODO: Add newlines support
  # TODO: Add punction
  # TODO: Add uppercase support
  book_name: str = Helper.random_id() + '.txt'
  pun_list: list = ['.', '!', ',', ';']
  for page_num in range(Globals.page_count):
    for line in range(Globals.line_count):
      line_list: list = []
      line_chars: int = 0

      while line_chars > Globals.chars_per_line:
        m_count: int = random.randint(1, 5)
        e_count: int = random.randint(1, 5)
        o_count: int = random.randint(1, 5)
        w_count: int = random.randint(1, 5)
        __count: int = random.randint(1, 3)
        char_count += m_count + e_count + o_count + w_count + __count

        if char_count > 63:
          for i in range(m_count): line_list.append('m')
          for i in range(e_count): line_list.append('e')
          for i in range(o_count): line_list.append('o')
          for i in range(w_count): line_list.append('w')
          for i in range(__count): line_list.append(' ')
        else:
          line_list.append('\n')
          with open(book_name, 'a') as file:
            file.write(''.join(line_list))
          char_count: int = 0


write_book()
