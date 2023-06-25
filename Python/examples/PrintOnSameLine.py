import time

lenght = 20
clear = '\x1b[2K'  # Clears line

for second in range(lenght):
  print(f'Seconds left: {lenght-second}', end='\r')
  time.sleep(1)  # Stall for one second
  if second + 1 != lenght:  # If end of loop
    print(end=clear)  # Dont clear line
print()  # Print EndOfProcess chars '> '
