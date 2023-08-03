# Make a type speed tester thing with curses in python and make a UI where you can select things like with the arrow keys and enter https://youtu.be/zwMsmBsC1GM
# DISCLAIMER: Curses hates windows os use linux for best results
# DISCLAIMER: Test the 'esc' -> home function on windows-curses!!
# TODO: Maybe make a way to highlight wrong or miss-typed chars to red instead of ignoring it
try:
  import os, sys
  import curses
  import random
  import requests
except Exception:
  print('Win32 uses a diffrent library, run \'pip install windows-curses\' to fix this.')
  sys.exit(1)


### Ease Of Use ###
def throw(message):
  raise Exception(message)
NULL = None
###################

VALID_COLORS = [
  'black',
  'red',
  'green',
  'yellow',
  'blue',
  'magenta',
  'cyan',
  'white'
]
GIBBERISH = [
  '°', 'ξ', 'Ø', '¨', '∩', 'Φ', 'φ', '⏅',
  'Ξ', '«', '»', '◊', '±', '⊗', '∴', '⏦',
  '☍', 'ส', '┌', 'ª', '‰', '¤', 'ð', '⚭'
]

# First lines ran (setup terminal)
window = curses.initscr()
window.keypad(True)
curses.noecho()
curses.cbreak()


class globals:
  toggle_gibberish = True  # True = on / False = off
  foreground = curses.COLOR_GREEN
  background = curses.COLOR_BLACK


class helper:
  
  def clear():
    if 'linux' in sys.platform: os.system('clear')
    else: os.system('cls')

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
      throw('Given parameter color is not valid')

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
    # Only used in dev for unit testing
    if not isinstance(message, str):
      throw('Message variable must be a string type')
    if os.path.exists('log.txt'):
      with open('log.txt', 'a') as Fout:
        Fout.write(f'{message}\n')
        Fout.close()
    else:
      with open('log.txt', 'w') as Fout2:
        Fout2.write(f'{message}\n')
        Fout2.close()

  def exit():
    # Restores terminal to initial settings and safely exits
    curses.endwin()
    print('Program exited successfully, terminal restored to default.')
    sys.exit(0)

  def slowWrite(scr, text, pause):
    # Wrapper for curses.addstr() which writes the text slowly
    for char in text:
      scr.addstr(char)
      scr.refresh()
      curses.napms(pause)  # Waits the duration of pause in milliseconds

  def writeAndHighlight(scr, list, index):
    # Writes letters and highlights a char or multiple
    curses.init_pair(1, globals.foreground, globals.background)

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
    if not isinstance(slow, bool):
      throw('Slow parameter must be a boolean')
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


class menuBranch:  # Functions that menu() braches to

  def typeTester(scr):  # The 'PLAY' function
    scr.clear()
    string = helper.generateSentence()
    helper.slowWrite(scr, string, 20)
    loop = True
    ticker = 0

    while loop == True:
      key = scr.getch()
      if key == 27:  # If key is 'esc' go home
        driver(scr)
      elif ticker == len(string):  # If user typed entire string
        scr.clear()
        if globals.toggle_gibberish == True:
          helper.centeredWrite(scr, helper.gibberishGenerator(), True)
        helper.centeredWrite(scr, 'Press any key to continue...', True, True)
        scr.getch()
        break
      elif key == ord(string[ticker]):  # If user's key == correct key
        ticker += 1
        scr.clear()
        helper.writeAndHighlight(scr, list(string), ticker)
      else:
        continue
    curses.wrapper(menuBranch.typeTester)  # Recalls itself

  def userConfig(scr):  # The 'OPTIONS' function
    scr.clear()
    h, w = helper.maxSize(scr)
    options_items = ['HIGHLIGHT COLOR', 'FOREGROUND COLOR', 'POST-PLAY GIBBERISH', 'BACK']

    def printMenu(selected_row, list):
      for item in list:
        index = list.index(item)
        x = int(w / 2 - len(item) / 2)
        y = int(h / 2 - len(list) / 2 + index)
        if index == selected_row:
          scr.addstr(y, x, item, curses.A_STANDOUT)
        else:
          scr.addstr(y, x, item)
      scr.refresh()

    curses.curs_set(0)
    current_row = 0
    printMenu(current_row, options_items)
    loop = True

    while loop == True:
      key = scr.getch()
      scr.clear()

      if key == curses.KEY_UP and current_row > 0:
        current_row -= 1
      elif key == curses.KEY_DOWN and current_row < len(options_items) - 1:
        current_row += 1
      elif key in [10, 13]:
        selected = options_items[current_row]
        break

      printMenu(current_row, options_items)

    # I dont wanna code rn but i am just going to print
    # the colors and get inputs after i restore terminal
    # to default using curses.endwin() [3/3]
    def getColorInput():
      helper.clear()  # Cant use scr.clear() cuz of curses.endwin()
      for item in VALID_COLORS:
        print(item)
      choice = input('\nPlease pick from the above colors: ')
      return choice

    curses.endwin()
    if selected == options_items[0]:
      color = getColorInput()
      if color not in VALID_COLORS:
        getColorInput()
      else:
        globals.background = helper.colorInterpreter(color)
        print(f'Background color updated to {color}.')
        input('Press \'Enter\' to continue...')

    elif selected == options_items[1]:
      color = getColorInput()
      if color not in VALID_COLORS:
        getColorInput()
      else:
        globals.foreground = helper.colorInterpreter(color)
        print(f'Foreground color updated to {color}.')
        input('Press \'Enter\' to continue...')

    elif selected == options_items[2]:
      if globals.toggle_gibberish == True:
        globals.toggle_gibberish = False ; res = 'OFF'
      else:
        globals.toggle_gibberish = True ; res = 'ON'
      print(f'Post-play gibberish update to {res}.')
      input('Press \'Enter\' to continue...')

    elif selected == options_items[3]:
      driver(scr)
    helper.clear() 
    driver(scr)


def menu(scr):
  # Add this function to helper call it 'ezmenu' or something
  scr.clear()
  h, w = helper.maxSize(scr)
  menu_items = ['PLAY', 'OPTIONS', 'EXIT']

  def printMenu(selected_row, list):
    for item in list:
      index = list.index(item)
      x = int(w / 2 - len(item) / 2)
      y = int(h / 2 - len(list) / 2 + index)
      if index == selected_row:
        scr.addstr(y, x, item, curses.A_STANDOUT)
      else:
        scr.addstr(y, x, item)
    scr.refresh()

  curses.curs_set(0)
  current_row = 0
  printMenu(current_row, menu_items)
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

    printMenu(current_row, menu_items)

  return selected


def driver(scr):
  choice = menu(scr)
  if choice == 'PLAY':
    menuBranch.typeTester(scr)
  elif choice == 'OPTIONS':
    menuBranch.userConfig(scr)
  elif choice == 'EXIT':
    helper.exit()


curses.wrapper(driver)
