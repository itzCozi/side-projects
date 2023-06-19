try:
  import os, sys
  import random
  import string
  import time
except Exception as e:
  print(f'ERROR: {e}')
  time.sleep(5)
  sys.exit(1)

now = lambda: time.strftime('%H:%M')


def genID():
  lenght = 8
  buffer = random.randint(3, 8)
  alphabet = list(string.ascii_letters + string.digits + string.digits)
  ID = []

  for i in range(buffer):
    random.shuffle(alphabet)

  for num in range(lenght):
    char = random.choice(alphabet)
    ID.append(char)
  return ''.join(ID)


def createBundle(main_folder, amount):
  main_dir = f'{os.getcwd()}/{amount}xBUNDLES'.replace('\\', '/')
  os.mkdir(main_dir)
  for wave in range(amount):
    if not os.path.exists(main_folder):
      print(f'ERROR: Cannot find {main_folder} because it does not exist.')
      sys.exit(1)

    print(f'\nBUNDLE NUMBER - #{wave+1}\n')

    size = random.randint(15, 25)
    buffer = size * 3
    out_dir = f"{main_dir}/BUNDLE#{genID()}"
    folder_content = []
    iterated = []
    subfolders = []
    bin = []
    os.mkdir(out_dir)
    for dirpath, dirnames, filenames in os.walk(main_folder):
      subfolders.append(dirpath)

    for enum in range(buffer):
      for r, d, f in os.walk(random.choice(subfolders)):
        if len(f) != 0:
          path = f'{r}/{random.choice(f)}'.replace('\\', '/')
          bin.append(path)

    for cycle in range(size):
      selected = random.choice(bin)
      if selected not in iterated:
        folder_content.append(selected)
      iterated.append(selected)

    for file in folder_content:
      if not os.path.exists(file):
        print(f'ERROR: Cannot find {file} because it does not exist.')
        sys.exit(1)
      extension = os.path.splitext(file)[1]

      if extension != '.txt':
        print(f"{file.split('/')[-1]} - {now()}")
        with open(file, 'rb') as f:
          content = f.read()
        with open(f"{out_dir}/{genID()}{extension}", 'wb') as out_file:
          out_file.write(content)

  print(f'\nALL BUNDLES HAVE BEEN CREATED AT: {main_dir}')


createBundle('<BUNDLE-FOLDER>', 5)
