# Make a type speed tester thing with curses in python and make a UI where you can select things like with the arrow keys and enter https://youtu.be/zwMsmBsC1GM
# DISCLAIMER: Curses hates windows os use linux for best results
# TODO: Link the menu to functions and fix colors on writeAndHighlight

try:
  import os, sys
  import curses
  import random
  import requests
except Exception as e:
  print('Win32 uses a diffrent library, run \'pip install windows-curses\' to fix this.')
  sys.exit(1)

VALID_COLORS = {
  'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
}
window = curses.initscr()
window.keypad(True)
curses.noecho()
curses.cbreak()


class helper:

  def generateSentence():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
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
      raise Exception('message variable must be a string type')
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
    # Writes letters slowley and highlights a char
    # WARN: The 'color' variable does nothing as of now
    if color not in VALID_COLORS:
      raise Exception('color variable was given a invaild color')
    else:
      curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    for char in range(len(list)):
      if list.index(list[char]) < index and char < index:
        scr.attron(curses.color_pair(1))
        scr.addstr(list[char])
        scr.attroff(curses.color_pair(1))
      else:
        scr.addstr(list[char])
      scr.refresh()

  def centeredWrite(scr, text, slow):
    # Writes to the current line but centers the text
    # TODO: Make this better and write in the middle of screen not top
    if not isinstance(slow, bool):
      raise Exception('slow parameter must be a boolean')
    width = scr.getmaxyx()[1]
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
      # Maybe make this say gibberish like animal crossing
      helper.centeredWrite(scr, 'YOU DID IT!', True)
      break
    elif key == ord(string[ticker]):  # Converts to ASCII
      ticker += 1
      scr.clear()
      helper.writeAndHighlight(scr, list(string), ticker, 'green')
    else:
      continue
  curses.wrapper(typeTester)


curses.wrapper(typeTester)
