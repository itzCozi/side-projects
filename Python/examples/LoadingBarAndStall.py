import time
import threading as THC # Peak humor


def loadingBar(duration, endMsg=None, symbol=None):
  if not isinstance(duration, int):
    raise Exception('duration variable must be a integer')
  if endMsg != None:
    if not isinstance(endMsg, str):
      raise Exception('endMsg variable must be a string')
  else:
    endMsg = 'Operation Finished.'
  if symbol != None:
    if not isinstance(symbol, str):
      raise Exception('symbol variable must be a string')
  else:
    symbol = '#'
  cycle_time = round(duration / 100, 2)
  bar = [
    '[',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
    ']'
  ]
  
  def innerBar():
    ticker = 0
    clear = '\x1b[2K'
    for cycle in range(0, 100):
      ticker += 1
      bar[ticker] = symbol
      percent = f' {ticker}%\r'
      print(''.join(bar), end=percent)
      time.sleep(cycle_time)
    print(clear, end='\r') ; print(endMsg)
  thread = THC.Thread(innerBar())
  thread.start() ; thread.join()


def stall(duration):
  if not isinstance(duration, int):
    raise Exception('duration variable must be a integer')

  def innerStall(arg):
    for cycle in range(arg):
      print('|', end='\r') ; time.sleep(0.15)
      print('/', end='\r') ; time.sleep(0.15)
      print('-', end='\r') ; time.sleep(0.15)
      print('\\', end='\r') ; time.sleep(0.15)
  thread = THC.Thread(innerStall(duration))
  thread.start() ; thread.join()

loadingBar(34)