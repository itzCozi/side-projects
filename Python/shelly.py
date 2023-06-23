import os, sys
import time


class vars:
  now = lambda: os.popen('time /t').read().replace('\n', '')
  output_log = []
  ticker = 0


class lib:

  def saveText():
    save_file = f'{os.getcwd()}/save.txt'
    for item in vars.output_log:
      if '::' in item:
        vars.output_log.remove(item)
    with open(save_file, 'w') as save:
      save.write('\n'.join(vars.output_log))
      save.close()

  def quitProcess():
    print('Quitting...')
    time.sleep(3)
    sys.exit(0)

  def loadSave():
    save_file = f'{os.getcwd()}/save.txt'
    with open(save_file, 'r') as save:
      content = save.read()
      for line in content.splitlines():
        vars.ticker += 1
        vars.output_log.append(line)
        print(f'{vars.ticker}. {line}')
      save.close()

  def clearPad():
    os.system('cls')
    vars.ticker = 0


if __name__ == '__main__':
  while True:
    vars.ticker += 1
    text = input(f'{vars.ticker}. ')

    ### ARGUMENT HANDLER ###
    if text.lower() == '::save':
      lib.saveText()

    elif text.lower() == '::load':
      lib.loadSave()

    elif text.lower() == '::quit':
      lib.quitProcess()

    elif text.lower() == '::clear':
      lib.clearPad()

    elif text.lower() == '::time':
      print(vars.now())

    elif text.lower().split(' ')[0] == '::system':
      os.system(f"{' '.join(text.lower().split(' ')[1:])}")

    elif text.lower().split(' ')[0] == '::open':
      try:
        path = text.lower().split(' ')[1]
        directory = '/'.join(text.lower().split(' ')[1].split('/')[:-1])
        file = '/'.join(text.lower().split(' ')[1].split('/')[-1:])

        def openLoop():
          while True:
            vars.ticker += 1
            text = input(f'{vars.ticker}. ')
            if text.lower() == '::close':
              print(f'Closed: {file}')
              break
            else:
              if os.path.getsize(path) == 0:
                writeback = f'{text}'
              if os.path.getsize(path) != 0:
                writeback = f'\n{text}'
              with open(path, 'a') as out:
                out.write(writeback)

        if directory == '':
          if os.path.exists(f'{os.getcwd()}/{file}'):
            with open(path, 'r') as r:
              content = r.read()
              for line in content.splitlines():
                vars.ticker += 1
                print(f'{vars.ticker}. {line}')
            openLoop()

          if not os.path.exists(file):
            with open(path, 'w+') as w:
              print(f'Created: {file}')
            openLoop()
        elif os.path.exists(directory):
          if os.path.exists(file):
            with open(path, 'r') as r:
              content = r.read()
              for line in content.splitlines():
                vars.ticker += 1
                print(f'{vars.ticker}. {line}')
            openLoop()

          if not os.path.exists(file):
            with open(path, 'w+') as w:
              print(f'Created: {file}')
            openLoop()
        else:
          print(f'The folder {directory} does not exist.')
          time.sleep(3)

      except Exception as e:
        print(f'ERROR: {e}')
        time.sleep(3)

    elif text.lower().split(' ')[0] == '::theme':
      try:
        if text.lower().split(' ')[1] == 'black':
          background_color = '0'
        if text.lower().split(' ')[1] == 'blue':
          background_color = '1'
        if text.lower().split(' ')[1] == 'green':
          background_color = '2'
        if text.lower().split(' ')[1] == 'red':
          background_color = '4'
        if text.lower().split(' ')[1] == 'purple':
          background_color = '5'
        if text.lower().split(' ')[1] == 'yellow':
          background_color = '6'
        if text.lower().split(' ')[1] == 'white':
          background_color = '7'

        if text.lower().split(' ')[2] == 'black':
          foreground_color = '0'
        if text.lower().split(' ')[2] == 'blue':
          foreground_color = '1'
        if text.lower().split(' ')[2] == 'green':
          foreground_color = '2'
        if text.lower().split(' ')[2] == 'red':
          foreground_color = '4'
        if text.lower().split(' ')[2] == 'purple':
          foreground_color = '5'
        if text.lower().split(' ')[2] == 'yellow':
          foreground_color = '6'
        if text.lower().split(' ')[2] == 'white':
          foreground_color = '7'
        if 'background_color' and 'foreground_color' in locals():
          os.system(f'Color {background_color}{foreground_color}')
        else:
          print('Given color not recognized, Example(::theme blue white).')
      except Exception as e:
        print(f'ERROR: {e}')
        time.sleep(3)

    else:
      vars.output_log.append(text)

else:
  print(f"You can't import {__file__} you must run it.")
  time.sleep(3)
  sys.exit(1)
