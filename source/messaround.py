import os, sys
import time
import curses
import _curses
from typing import *


class Globals:
  database: str = 'keys.db'
  # EXAMPLE "keys.db"
  # ------------------------
  # USER: cozi08, Coop4598
  # USER: admin, admin
  # ------------------------
  KEY_MAP: dict = {
    "BACKSPACE": 8,
    "TAB": 9,
    "ENTER": 10,
    "ESCAPE": 27,
    "DOWN": 258,
    "UP": 259,
    "LEFT": 260,
    "RIGHT": 261,
    "HOME": 262,
    "F1": 265,
    "F2": 266,
    "F3": 267,
    "F4": 268,
    "F5": 269,
    "F6": 270,
    "F7": 271,
    "F8": 272,
    "F9": 273,
    "F10": 274,
    "F11": 275,
    "F12": 276,
    "DELETE": 330,
    "INSERT": 331,
    "PAGEDOWN": 338,
    "PAGEUP": 339,
    "END": 358,
  }


class Helper:

  def setup() -> _curses.window:
    """
    Set up the screen

    Returns:
      _curses.window: A new screen object
    """
    scr = curses.initscr()
    curses.cbreak()
    scr.keypad(True)
    scr.clear()
    return scr

  def centeredWrite(scr: _curses.window, text: str) -> None:
    """
    Writes to the current line but centers the text

    Args:
      scr (_curses.window): The screen object
      text (str): The text to display
    """
    width = scr.getmaxyx()[1]
    scr.move(scr.getyx()[0], int(width / 2 - len(text) / 2))
    scr.addstr(text)
    scr.refresh()

  def write(scr: _curses.window, msg: str, pos: tuple = (0, 0)) -> None:
    """
    Write a message to the screen, window or pad at a position

    Args:
      scr (_curses.window): The screen object
      msg (str): The message to write
      pos (tuple): The position to write the message in, default (0, 0)
    """
    scr.addstr(int(pos[1]), int(pos[0]), msg)
    scr.refresh()

  def slowWrite(
    scr: _curses.window, text: str, pause: int = 20, pos: tuple = (0, 0)
  ) -> None:
    """
    Wrapper for curses.addstr() which writes the text slowly

    Args:
      scr (_curses.window): The screen object
      text (str): Text to output
      pause (int): Time to pause
    """
    x: int = int(pos[1])
    y: int = int(pos[0])
    height, width = scr.getmaxyx()
    for i in range(len(text)):
      scr.addstr(x, y, text[i])
      if y < width: y += 1
      if y == width: x += 1
      scr.refresh()
      curses.napms(pause)  # Waits the duration of pause in milliseconds

  def cursorBlink(scr: _curses.window, duration: int) -> None:
    """
    Blinks the cursor twice every second

    Args:
      scr (_curses.window): The curses screen object
      duration (int): The amount of seconds to blink
    """
    for i in range(duration):
      curses.curs_set(1)
      time.sleep(0.5)
      curses.curs_set(0)
      time.sleep(0.5)

  def hide_input(scr: _curses.window, hide_char: str = '*') -> str:
    """
    Hides user's input behind the hide_char symbol and returns string

    Args:
      scr (_curses.window): The screen object
      hide_char (str): A char type string that hides user's input

    Returns:
      str: The string of the hidden input
    """
    in_char = 0
    in_str = ''
    curses.noecho()
    mask = str(hide_char)
    if 'linux' in sys.platform:
      NEWLINE = 10  # ASCII integer equal to '\n'
      BACKSPACE = 127  # ASCII integer equal to backspace
    else:  # KEY_MAP is only for windows
      NEWLINE = Globals.KEY_MAP['ENTER']
      BACKSPACE = Globals.KEY_MAP['BACKSPACE']

    while in_char != NEWLINE:
      in_char = scr.getch()
      # Backspace exception
      if in_char == BACKSPACE:
        if len(in_str) > 0:
          in_str = in_str[:-1]
          cur = scr.getyx()
          scr.move(cur[0], cur[1] - 1)
          scr.clrtobot()
        else:
          continue
      elif in_char > 255:
        continue
      # Output the character
      elif in_char != NEWLINE:
        in_str += chr(in_char)
        if len(hide_char) != 0:
          scr.addch(mask)
        else:
          scr.addch(in_char)
    return in_str


def login() -> bool:
  with open(Globals.database, 'r') as f:
    content: str = f.read()
  users = {}

  for line in content.splitlines():
    if 'USER' in line:
      idx = line.find('USER: ')
      comma = line.find(',')
      user = line[idx + 6:comma].replace(' ', '')
      password = line[comma:].replace(',', '').replace(' ', '')
      users[user] = password

  scr = Helper.setup()
  trys = 0
  stage = 1
  while True:
    height, width = scr.getmaxyx()
    header_list = []
    page_title = ' LOGIN - TERMINAL '
    for i in range(width - len(page_title)):
      header_list.append('=')
    listA = []
    for i in range(
      int(round(len(header_list)/2, 0)), 
      len(header_list)
    ):
      listA.append('=')
      listB = listA.copy()
    Helper.write(scr, ''.join(listA)+page_title+''.join(listB))

    if stage == 1:
      Helper.write(scr, 'USER: ', (0, 2))
      user_name_input = Helper.hide_input(scr)

      if user_name_input in users:
        stage += 1
      else:
        Helper.slowWrite(scr, 'Invalid username.', pause=50, pos=(0, 2))
        Helper.slowWrite(scr, 'Press any key to continue...', pos=(0, 3))
        scr.getch()

    elif stage == 2:
      Helper.write(scr, 'PASS: ', (0, 2))
      user_pass_input = Helper.hide_input(scr)

      if user_pass_input in users:
        return True
      else:
        Helper.slowWrite(scr, 'Invalid password.', pause=50, pos=(0, 2))
        Helper.slowWrite(scr, 'Press any key to re-enter password...', pos=(0, 3))
        stage = 3
        scr.getch()

    scr.clear()
    trys += 1
    if stage == 3:
      stage = 2
    if trys == 4:
      Helper.slowWrite(scr, 'Too many false entries, force quitting.', pause=50)
      Helper.slowWrite(scr, 'Press any key to exit...', pos=(0, 1))
      scr.getch()
      return False


login()
