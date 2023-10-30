try:
  import time
  import random
  import os, sys
  import keyboard
  import pyautogui as pyauto
except ModuleNotFoundError as e:  # If you dont have a package installed
  e = str(e)
  idx = e.find('named')
  missing_package = e[idx:].replace('named ', '').replace('\'', '')
  print('-----------------------------------------------------------------------')
  print(f'Package \'{missing_package}\' failed to import if you have Python installed \
  \nyou can install the package by typing the below command into \'cmd\':')
  print(f'pip install {missing_package}')
  print('-----------------------------------------------------------------------')


class globals:
  cycle_count = 0
  clear_line = '\x1b[2K'  # This just clears the line
  mouse_list = ['left', 'right']
  key_list = 'wasd'


def loop():
  clear = lambda: os.system('cls')
  clear()  # Jus clears the console
  print('\n -------  Anti AFK ------- \n')

  for i in range(1, 6):
    print(f'Loop starting in {i}...\r', end='')
    time.sleep(1)
  print(globals.clear_line, end='')
  print('Started press \'alt\' to halt.')

  while True:
    # Key that will be pressed
    key = random.choice(globals.key_list)
    mouse = random.choice(globals.mouse_list)
    print(f'Inputs sent: {globals.cycle_count}\r', end='')
    globals.cycle_count += 1

    if keyboard.is_pressed('win'):
      print('Windows key pressed, stalling.')
      time.sleep(5)
    if keyboard.is_pressed('alt'):
      break

    pyauto.mouseDown(button=mouse)
    keyboard.press(key)
    time.sleep(1)

  print('Loop halted, press \'alt\' to restart.')
  user_input = input('> ')
  if user_input.lower() == 'start':
    loop()
  else:
    print('\nInput not recognized, quitting...')
    time.sleep(2)
    sys.exit(0)


if __name__ == '__main__':
  try:
    loop()
  except KeyboardInterrupt:
    print('\nQuitting...')
    time.sleep(2)
    sys.exit(0)
else:
  print(f'You cannot import {__file__}.')
  sys.exit(1)
