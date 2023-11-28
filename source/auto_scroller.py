# Scrolls automatically on Windows ONLY

import os
import time
import keyboard
import win32api
from win32con import *


class Controller:

  @staticmethod
  def MOUSESCROLL(axis: str, dist: int, x: int = 0, y: int = 0) -> None | bool:
    if axis == 'v' or axis == 'vertical':
      win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, dist, 0)
    elif axis == 'h' or axis == 'horizontal':
      win32api.mouse_event(MOUSEEVENTF_HWHEEL, x, y, dist, 0)
    else:
      return False

  @staticmethod
  def scrollMouse(direction: str, amount: int, dx: int = 0, dy: int = 0) -> None:
    """
    Scrolls mouse up, down, right and left by a certain amount

    Args:
      direction (str): The way to scroll, valid inputs: (
        up, down, right, left
      )
      amount (int): How much to scroll has to be at least 1
      dx (int, optional): The mouse's position on the x-axis
      dy (int, optional): The mouse's position on the x-axis
    """
    if direction == 'up':
      Controller.MOUSESCROLL('vertical', amount, dx, dy)
    elif direction == 'down':
      Controller.MOUSESCROLL('vertical', -amount, dx, dy)
    elif direction == 'right':
      Controller.MOUSESCROLL('horizontal', amount, dx, dy)
    elif direction == 'left':
      Controller.MOUSESCROLL('horizontal', -amount, dx, dy)


def scroll_loop() -> None:
  for i in reversed(range(1, 6)):
    print(f'Loop starting in {i}...\r', end='')
    time.sleep(1)
  print('\x1b[2K', end='')
  print('Started press \'alt\' to halt.')
  os.popen('start "" https://instagram.com')  # Simple example

  while True:
    if keyboard.is_pressed('alt'):
      break
    Controller.scrollMouse('down', 15)
    time.sleep(0.1)

  os.system("taskkill /im brave.exe /f")
  print('Loop halted, press \'ctrl\' to restart.')
  time.sleep(2)
  while True:
    if keyboard.is_pressed('ctrl'):
      scroll_loop()
    time.sleep(0.2)


scroll_loop()
