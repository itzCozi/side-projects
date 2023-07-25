# Make a type speed tester thing with curses in python and make a UI where you can select things like with the arrow keys and enter https://youtu.be/zwMsmBsC1GM
# DISCLAIMER: Curses hates windows os use linux for best results
# TODO: Make the options function

try:
  import os, sys
  import curses
  import random
  import requests
except Exception:
  print('Win32 uses a diffrent library, run \'pip install windows-curses\' to fix this.')
  sys.exit(1)

VALID_COLORS = {
  'black': curses.COLOR_BLACK,
  'red': curses.COLOR_RED,
  'green': curses.COLOR_GREEN,
  'yellow': curses.COLOR_YELLOW,
  'blue': curses.COLOR_BLUE,
  'magenta': curses.COLOR_MAGENTA,
  'cyan': curses.COLOR_CYAN,
  'white': curses.COLOR_WHITE
}
GIBBERISH = [
  '°', 'ξ', 'Ø', '¨', '∩', 'Φ', 'φ', '⏅',
  'Ξ', '«', '»', '◊', '±', '⊗', '∴', '☍',
  'ส','┌', 'ª', '‰', '¤', 'ð', '⚭', '⏦'
]
window = curses.initscr()
window.keypad(True)
curses.noecho()
curses.cbreak()


class helper:

  def gibberishGenerator():
    # Returns a random gibberish string
    length = random.randint(30, 100)
    ret_value = []
    chance = 0.26  # Chance to add spaces
    ticker = 0

    for i in range(length):
      char = random.choice(GIBBERISH)
      ret_value.append(char)
    for cycle in range(length):
      ticker += 1
      if ticker >= length:
        return ''.join(ret_value)
      elif random.random() < chance and ret_value[ticker - 1] != ' ':
        ret_value[ticker] = ' '
      else:
        continue

  def colorInterpreter(color):
    # Interprets colors for writeAndHighlight()
    if color.lower() == 'black':
      return curses.COLOR_BLACK
    elif color.lower() == 'red':
      return curses.COLOR_RED
    elif color.lower() == 'green':
      return curses.COLOR_GREEN
    elif color.lower() == 'yellow':
      return curses.COLOR_YELLOW
    elif color.lower() == 'blue':
      return curses.COLOR_BLUE
    elif color.lower() == 'magenta':
      return curses.COLOR_MAGENTA
    elif color.lower() == 'cyan':
      return curses.COLOR_CYAN
    elif color.lower() == 'white':
      return curses.COLOR_WHITE
    else:
      raise Exception('Given parameter color is not valid')

  def generateSentence():
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

    ret_string = ' '.join(listA)
    return ret_string + '.'

  def EZLog(message):  # Cant print when using curses so...
    if not isinstance(message, str):
      raise Exception('Message variable must be a string type')
    if os.path.exists('log.txt'):
      with open('log.txt', 'a') as Fout:
        Fout.write(f'{message}\n')
        Fout.close()
    else:
      with open('log.txt', 'w') as Fout2:
        Fout2.write(f'{message}\n')
        Fout2.close()

  def exit():
    # Safely exits and restore terminal to initial settings
    curses.endwin()

  def slowWrite(scr, text, pause):
    # Wrapper for curses.addstr() which writes the text slowly
    for char in text:
      scr.addstr(char)
      scr.refresh()
      curses.napms(pause)  # Waits the duration of pause in milliseconds

  def writeAndHighlight(scr, list, index, color):
    # Writes letters and highlights a char or multiple
    if color.lower() not in VALID_COLORS:
      raise Exception('Color variable was given a invaild color')
    else:
      foreground = helper.colorInterpreter(color)
      curses.init_pair(1, foreground, curses.COLOR_BLACK)

    for char in range(len(list)):
      if list.index(list[char]) < index and char < index:
        scr.attron(curses.color_pair(1))
        scr.addstr(list[char])
        scr.attroff(curses.color_pair(1))
      else:
        scr.addstr(list[char])
      scr.refresh()

  def centeredWrite(scr, text, slow, newLine=None):
    # Writes to the current line but centers the text
    # TODO: Make this better and write in the middle of screen not top
    if not isinstance(slow, bool):
      raise Exception('Slow parameter must be a boolean')
    width = scr.getmaxyx()[1]
    if newLine != None:
      scr.move(scr.getyx()[0] + 1, int(width / 2 - len(text) / 2))
    else:
      scr.move(scr.getyx()[0], int(width / 2 - len(text) / 2))
    if slow == True:
      for char in text:
        scr.addstr(char)
        scr.refresh()
        curses.napms(20)
    else:
      scr.addstr(text)
      scr.refresh()

  def maxSize(window):
    # Returns the width and height of the screen
    height, width = window.getmaxyx()
    return height, width


def menu(scr):
  # Add this function to helper call it 'ezmenu' or something
  h, w = helper.maxSize(scr)
  menu_items = ['PLAY', 'OPTIONS', 'EXIT']

  def printMenu(selected_row):
    for item in menu_items:
      index = menu_items.index(item)
      x = int(w / 2 - len(item) / 2)
      y = int(h / 2 - len(menu_items) / 2 + index)
      if index == selected_row:
        scr.addstr(y, x, item, curses.A_STANDOUT)
      else:
        scr.addstr(y, x, item)
    scr.refresh()

  curses.curs_set(0)
  current_row = 0
  printMenu(current_row)
  loop = True

  while loop == True:
    key = scr.getch()
    scr.clear()

    if key == curses.KEY_UP and current_row > 0:
      current_row -= 1
    elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
      current_row += 1
    elif key in [10, 13]:
      selected = menu_items[current_row]
      break

    printMenu(current_row)

  return selected


def typeTester(scr):  # The 'PLAY' function
  scr.clear()
  string = helper.generateSentence()
  helper.slowWrite(scr, string, 20)
  loop = True
  ticker = 0

  while loop == True:
    key = scr.getch()
    if ticker == len(string):
      scr.clear()
      helper.centeredWrite(scr, helper.gibberishGenerator(), True)
      helper.centeredWrite(scr, 'Press any key to continue...', True, True)
      scr.getch()
      break
    elif key == ord(string[ticker]):  # Converts to ASCII
      ticker += 1
      scr.clear()
      helper.writeAndHighlight(scr, list(string), ticker, 'green')
    else:
      continue
  curses.wrapper(typeTester)


def driver(scr):
  choice = menu(scr)
  if choice == 'PLAY':
    typeTester(scr)
  elif choice == 'OPTIONS':
    raise Exception('Not implemented yet')  # Have to code this function
  elif choice == 'EXIT':
    sys.exit(0)


curses.wrapper(driver)
