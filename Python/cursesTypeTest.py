# Make a type speed tester thing with curses in python and make a UI where you can select things like with the arrow keys and enter https://youtu.be/zwMsmBsC1GM
# DISCLAIMER: Curses hates windows os use linux for best results

try:
  import os, sys
  import curses
  import colorama
  from colorama import Fore, Back, Style
except Exception as e:
  print('Win32 uses a diffrent library, run \'pip install windows-curses\' to fix this.')
  sys.exit(1)


window = curses.initscr()
curses.noecho()
curses.cbreak()


class helper:
  
  def exit():
    # Safely exits and restore terminal to initial settings
    curses.endwin()
  
  def slowWrite(scr, text, pause):
    # Wrapper for curses.addstr() which writes the text slowly
    for char in text:
      scr.addstr(char)
      scr.refresh()
      curses.napms(pause)  # Waits the duration of pause in milliseconds
  
  def centeredWrite(scr, text):
    # Writes to the current line but centers the text
    width = scr.getmaxyx()[1]
    scr.move(scr.getyx()[0], int(width / 2 - len(text) / 2))
    scr.addstr(text)
    scr.refresh()
  
  def maxSize(window):
    # Returns the width and height of the screen
    height, width = window.getmaxyx()
    return height, width


def menu(scr):
  # Add this function to helper call it 'ezmenu' or something
  h,w = helper.maxSize(scr)
  menu_items = ['PLAY', 'OPTIONS', 'EXIT']
  
  def printMenu(selected_row):
    for item in menu_items:
      index = menu_items.index(item)
      x = int(w/2 - len(item)/2)
      y = int(h/2 - len(menu_items)/2 + index)
      if index == selected_row:
        scr.addstr(y, x, item, curses.A_STANDOUT)
      else:  
        scr.addstr(y, x, item)
    scr.refresh()
  
  curses.curs_set(0)
  scr.keypad(True)
  current_row = 0
  printMenu(current_row)
  loop = True

  while loop == True:
    key = scr.getch()
    scr.clear()
    
    if key == curses.KEY_UP and current_row > 0:
      current_row -= 1
    elif key == curses.KEY_DOWN and current_row < len(menu_items)-1:
      current_row += 1
    elif key in [10, 13]:
      selected = menu_items[current_row]
      break
    
    printMenu(current_row)
  
  return selected
      

def typeTester(scr):  # The 'PLAY' function
  test_string = 'Type this if you can.'
  helper.slowWrite(scr, test_string, 20)
  scr.getch()
  
curses.wrapper(typeTester)