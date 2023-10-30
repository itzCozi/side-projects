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
  # TODO: Add diffrent lenghts of meows
  # TODO: Add newlines support
  # TODO: Add punction
  # TODO: Add uppercase support
  book_name: str = Helper.random_id()
  pun_list: list = ['.', '!', ',', ';']
  for page_num in range(Globals.page_count):
    for line in range(Globals.line_count):
      line_list: list = []
      for char in range(Globals.chars_per_line):
        prev_char: str = line_list[char - 1] if char > 0 else ''
        match prev_char:
          case '' | ' ':
            line_list.append('m')
          case 'm':
            line_list.append('e')
          case 'e':
            line_list.append('o')
          case 'o':
            line_list.append('w')
          case 'w':
            line_list.append(' ')
      print(''.join(line_list))


write_book()
