# THIS IS OUTDATED LOOK TO https://github.com/itzCozi/Shelly FOR UPDATED VERSION
# This is written in kinda my own style with the help of the replit Python formatter
# TODO: Look over and test then reformat with black to compile and release 1.0
# TODO: Also edit save files zip with python (write a script idk have fun)

try:
  import os, sys
  import time
  import random
except Exception as e:
  print(f'ERROR: {e}')
  sys.exit(1)


class vars:
  version = '0.5 Pre-Alpha'  # Side project -> Github repo
  now = lambda: os.popen('time /t').read().replace('\n', '')
  config_file = f'{os.getcwd()}/config'.replace('\\', '/')
  platform = sys.platform
  # NULL is a string placeholder for None
  disable_config_print = 'NULL'
  linux_compatibility = 'NULL'
  disable_commands = 'NULL'
  disable_ticks = 'NULL'
  output_log = []
  user_vars = []
  ticker = 0


class lib:

  def help():
    print(f'''
------------------ Shelly Arguments ------------------
  ::quit - This will quit the program.
  ::clear - Wipes the console clean.
  ::time - Displays the time.
  ::stall(secs) - Waits a provided amount of seconds.
  ::save(file) - Saves all text to a file.
  ::load(file) - Load text from a file.
  ::log(text) - Writes given text to the console.
  ::system(cmd) - Passes a command to the computer.
  ::theme(color color) - Changes the console's color. LINUX ONLY
  ::open(file) - Displays file contents and writes all lines to file.
  ::close - Exits file and returns to normal mode.
  ::wipe - Clears all data from current file.
  ::var(name = value) - Set a variable to a value, type <name> to replace it with value.
  
 All arguments must start with '::' unless it is a special switch then it starts with '::_' though these switches
 are not documented. Once inside an open file you can use just the final three commands and nothing else, only 
 '::var', '::wipe' and '::close' are valid at that time, however after '::close' is passed all commands 
 are usable outside files. The '::load' and '::save' commands have optional parameters like files, if you
 wanted to save to a file called 'Log2.txt' type this: "::save Log2.txt" but typing: '::save' will default
 to current directory/save.txt, The load command will default to this location too if no arguments are given.
    ''')

  def clearPad():
    if vars.linux_compatibility.lower() == 'false' or vars.linux_compatibility == 'NULL':
      os.system('cls')
      vars.ticker = 0
    else:
      os.system('clear')
      vars.ticker = 0

  def checks():
    if os.path.exists(vars.config_file):
      # theme: blue white     (IMPLEMENTED)
      # number-ticks: false   (IMPLEMENTED)
      # commands: false       (IMPLEMENTED)
      # print-config: false   (IMPLEMENTED)
      # linux: true           (IMPLEMENTED)
      with open('config', 'r') as f:
        content = f.read()
        f.close()

      for line in content.splitlines():
        if 'theme' in line.lower():
          index = line.find(': ')
          theme_settings = line[index:].replace(': ', '')
          if len(theme_settings.split(' ')) == 2:
            colorA = theme_settings.split(' ')[0]
            colorB = theme_settings.split(' ')[1]
            parameter = f'::theme {colorA} {colorB}'
          else:
            colorA = theme_settings.split(' ')[0]
            parameter = f'::theme {colorA}'
          lib.changeTheme(parameter)
        elif 'linux' in line.lower():
          index = line.find(': ')
          boolean = line[index:].replace(': ', '')
          vars.linux_compatibility = boolean
        elif 'number-ticks' in line.lower():
          index = line.find(': ')
          boolean = line[index:].replace(': ', '')
          vars.disable_ticks = boolean
        elif 'commands' in line.lower():
          index = line.find(': ')
          boolean = line[index:].replace(': ', '')
          vars.disable_commands = boolean
        elif 'print-config' in line.lower():
          index = line.find(': ')
          boolean = line[index:].replace(': ', '')
          vars.disable_config_print = boolean
        else:
          continue

    if os.path.getsize(vars.config_file) != 0 and vars.disable_config_print.lower() == 'true' or vars.disable_config_print == 'NULL':
      print(f'Configured by {vars.config_file}')

    if vars.linux_compatibility.lower() == 'false' or vars.linux_compatibility == 'NULL':
      if 'linux' in vars.platform:
        print(f"\n------------------------------------------------- \
        \nTHIS PROGRAM IS DESIGNED FOR USE WITH WINDOWS. \
        \nCONTINUE WITH LINUX COMPATIBILITY MODE TOGGLED? \
        \n-------------------------------------------------")
        user_input = input('(y/n)> ')
        if user_input.lower() == 'y' or user_input.lower() == 'yes':
          print('\nYIELDING...')
          vars.linux_compatibility = 'true' ; vars.platform = 'yielded'
        elif user_input.lower() == 'n' or user_input.lower() == 'no':
          print('\nQUITTING...')
          sys.exit(1)
        else:
          print('Given input not recognized, quitting...')
          sys.exit(0)

  def createVar(text):
    if len(text.split(' ')) == 4:
      var_name = str(text.split(' ')[1])
      var_value = str(text.split(' ')[3])
    else:
      print('No value provided, Example(::var food = pizza).')

    if 'var_name' and 'var_value' in locals():
      varOBJ = f'{var_name} = {var_value}'
      vars.user_vars.append(varOBJ)
      print(f'Typing <{var_name}> will replace it with {var_value}.')

  def stall():
    if len(text.lower().split(' ')) > 1:
      if text.lower().split(' ')[1].isdigit():
        given_num = int(text.split(' ')[1])
        for i in range(given_num):
          time.sleep(1)
          print('.', end='', flush=True)
        print()
    else:
      print('No time given, Example(::stall 9) this will wait 9 seconds.')

  def quitProcess():
    if vars.linux_compatibility.lower() == 'false' or vars.linux_compatibility == 'NULL':
      shorthand = True
    else:
      shorthand = False

    if shorthand:
      os.system('Color C7')
    check = input('Are you sure you want to quit? (y/n): ')
    if check.lower() == 'yes' or check.lower() == 'y':
      print('Quitting...')
      time.sleep(1)
      if shorthand:
        os.system('Color 07')
      sys.exit(0)
    elif check.lower() == 'no' or check.lower() == 'n':
      print('Aborting...')
      time.sleep(1)
      if shorthand:
        os.system('Color 07')
    else:
      print('Given input not recognized, restarting.')
      lib.quitProcess()

  def saveText():
    if '\\' in text.lower():
      print('Please use forward-slashes (/) to separate directories.')
      return 0
    if len(text.split(' ')) > 1:
      path = text.lower().split(' ')[1]
      directory = '/'.join(text.lower().split(' ')[1].split('/')[:-1])
      file = ''.join(text.lower().split(' ')[1].split('/')[-1])

      if directory == '':
        save_file = f'{os.getcwd()}/{file}'
      elif os.path.exists(directory):
        save_file = f'{path}'
      else:
        print(f'The folder {directory} does not exist, using current directory.')
        save_file = f'{os.getcwd()}/save.txt'
        time.sleep(3)
    else:
      save_file = f'{os.getcwd()}/save.txt'
    save_file = save_file.replace('\\', '/')

    if os.path.exists(save_file):
      overwrite = input(f"File {save_file.split('/')[-1]} already exists, overwrite it? (y/n) ")
      if overwrite.lower() == 'yes' or overwrite.lower() == 'y':
        os.remove(save_file)
      elif overwrite.lower() == 'no' or overwrite.lower() == 'n':
        print('Aborting...')
        time.sleep(1)
        return 0
      else:
        print('Given input not recognized, restarting.')
        lib.saveText()
    for item in vars.output_log:
      if '::' in item:
        vars.output_log.remove(item)
    with open(save_file, 'w') as save:
      save.write('\n'.join(vars.output_log))
      save.close()
    print(f'Saved text to {save_file}')

  def loadSave():
    if '\\' in text.lower():
      print('Please use forward-slashes (/) to separate directories.')
      return 0
    if len(text.split(' ')) > 1:
      path = text.lower().split(' ')[1]
      directory = '/'.join(text.lower().split(' ')[1].split('/')[:-1])
      file = ''.join(text.lower().split(' ')[1].split('/')[-1])

      if directory == '':
        save_file = f'{os.getcwd()}/{file}'
      elif os.path.exists(directory):
        save_file = f'{path}'
      else:
        print(f'The folder {directory} does not exist.')
        save_file = f'{os.getcwd()}/save.txt'
        time.sleep(3)
    else:
      save_file = f'{os.getcwd()}/save.txt'
    save_file = save_file.replace('\\', '/')
    if os.path.exists(save_file):
      with open(save_file, 'r') as save:
        content = save.read()
        for line in content.splitlines():
          vars.ticker += 1
          vars.output_log.append(line)
          if vars.disable_ticks.lower() == 'true' or vars.disable_ticks == 'NULL':
            print(f'{vars.ticker}. {line}')
          else:
            print(f'> {line}')
        save.close()
      print(f'Loaded text from {save_file}')
    else:
      print(f'Cannot detect save file, Looking-For: {save_file}.')

  def openFile():
    try:
      if '\\' in text.lower():
        print('Please use forward-slashes (/) to separate directories.')
        return 0
      if len(text.split(' ')) > 1:
        path = text.lower().split(' ')[1]
        directory = '/'.join(text.lower().split(' ')[1].split('/')[:-1])
        file = ''.join(text.lower().split(' ')[1].split('/')[-1])
      else:
        print('Please provide a file, Example(::open C:/test.txt | ::open save.txt).')
        return 0

      def openLoop():
        while True:
          vars.ticker += 1
          if vars.disable_ticks.lower() == 'true' or vars.disable_ticks == 'NULL':
            text = input(f'{vars.ticker}. ')
          else:
            text = input('> ')
          if text.lower() == '::close':
            print(f'Closed: {file}')
            break
          elif text.lower().split(' ')[0] == '::var':
            lib.createVar(text)
          elif text.lower().split(' ')[0] == '::vars':
            if len(vars.user_vars) != 0:
              for i in vars.user_vars:
                print(i)
            else:
              print("No vars made use '::var name = value' to create vars.")
          elif text.lower().split(' ')[0] == '::wipe':
            YorN = input('Are you sure you want to wipe this file? (y/n) ')
            if YorN.lower() == 'yes' or YorN.lower() == 'y':
              open(path, 'w')
              print(f'Wiped: {file}')
            elif YorN.lower() == 'no' or YorN.lower() == 'n':
              print('Aborting...')
              time.sleep(1)
            else:
              print('Given input not recognized, aborting...')
          elif '::' in text.lower():
            print("Only the '::close', '::wipe' and '::var' command's are valid in write mode.")
          else:
            for item in text.split(' '):  # Checks for vars in text and replaces them
              if '<' and '>' in item:
                var_start = item.find('<')
                var_end = item.find('>')
                var = item[var_start:var_end].replace('<', '').replace('>', '')
                for i in vars.user_vars:
                  if var in i:
                    ripped_statement = vars.user_vars[vars.user_vars.index(i)]
                    value = ripped_statement.split(' ')[2]
                if 'value' in locals():
                  text = text.replace(f'<{var}>', value)
            if os.path.getsize(path) == 0:
              write_back = f'{text}'
            if os.path.getsize(path) != 0:
              write_back = f'\n{text}'
            with open(path, 'a') as out:
              out.write(write_back)

      if directory == '':
        if os.path.exists(f'{os.getcwd()}/{file}'):
          print(f'Opening: {file}')
          with open(path, 'r') as r:
            content = r.read()
            for line in content.splitlines():
              vars.ticker += 1
              if vars.disable_ticks.lower() == 'true' or vars.disable_ticks == 'NULL':
                print(f'{vars.ticker}. {line}')
              else:
                print(f'> {line}')
          openLoop()

        if not os.path.exists(file):
          with open(path, 'w+') as w:
            print(f'Created: {file}')
          openLoop()
      elif os.path.exists(directory):
        if os.path.exists(file):
          print(f'Opening: {file}')
          with open(path, 'r') as r:
            content = r.read()
            for line in content.splitlines():
              vars.ticker += 1
              if vars.disable_ticks.lower() == 'true' or vars.disable_ticks == 'NULL':
                print(f'{vars.ticker}. {line}')
              else:
                print(f'> {line}')
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
      return 0

  def changeTheme(param):
    # I coded this so param and text are interchangeable to account for cases where
    # the user may not have typed yet so like configured theme switches
    if not 'text' in locals():
      text = param
    elif not 'param' in locals():
      param = text
    try:
      # Cover your eyes! i'll tell you when it's over.
      if text.lower().split(' ')[1] == 'random' or param.lower().split(' ')[1] == 'random':
        background_color = random.randint(0, 7)
        foreground_color = random.randint(0, 7)

      if len(text.split(' ')) > 1 or len(param.split(' ')) > 1:
        if text.lower().split(' ')[1] == 'black' or param.lower().split(' ')[1] == 'black':
          background_color = '0'
        if text.lower().split(' ')[1] == 'blue' or param.lower().split(' ')[1] == 'blue':
          background_color = '1'
        if text.lower().split(' ')[1] == 'green' or param.lower().split(' ')[1] == 'green':
          background_color = '2'
        if text.lower().split(' ')[1] == 'cyan' or param.lower().split(' ')[1] == 'cyan':
          background_color = '3'
        if text.lower().split(' ')[1] == 'red' or param.lower().split(' ')[1] == 'red':
          background_color = '4'
        if text.lower().split(' ')[1] == 'purple' or param.lower().split(' ')[1] == 'purple':
          background_color = '5'
        if text.lower().split(' ')[1] == 'yellow' or param.lower().split(' ')[1] == 'yellow':
          background_color = '6'
        if text.lower().split(' ')[1] == 'white' or param.lower().split(' ')[1] == 'white':
          background_color = '7'

      if len(text.split(' ')) > 2 or len(param.split(' ')) > 2:
        if text.lower().split(' ')[2] == 'black' or param.lower().split(' ')[2] == 'black':
          foreground_color = '0'
        if text.lower().split(' ')[2] == 'blue' or param.lower().split(' ')[2] == 'blue':
          foreground_color = '1'
        if text.lower().split(' ')[2] == 'green' or param.lower().split(' ')[2] == 'green':
          foreground_color = '2'
        if text.lower().split(' ')[1] == 'cyan' or param.lower().split(' ')[2] == 'cyan':
          foreground_color = '3'
        if text.lower().split(' ')[2] == 'red' or param.lower().split(' ')[2] == 'red':
          foreground_color = '4'
        if text.lower().split(' ')[2] == 'purple' or param.lower().split(' ')[2] == 'purple':
          foreground_color = '5'
        if text.lower().split(' ')[2] == 'yellow' or param.lower().split(' ')[2] == 'yellow':
          foreground_color = '6'
        if text.lower().split(' ')[2] == 'white' or param.lower().split(' ')[2] == 'white':
          foreground_color = '7'
      # It's over now, you can open your eyes.

      if 'background_color' and 'foreground_color' in locals():  # Prevent unbound error
        os.system(f'Color {background_color}{foreground_color}')
      else:
        print('Given color not recognized, Example(::theme blue white).')
    except Exception as e:
      print(f'ERROR: {e}')
      time.sleep(3)
      return 0


if __name__ == '__main__':
  try:
    lib.checks()  # Handles pre-run
    while True:
      vars.ticker += 1
      if vars.disable_ticks.lower() == 'true' or vars.disable_ticks == 'NULL':
        text = input(f'{vars.ticker}. ')
      else:
        text = input('> ')

      # ARGUMENT HANDLER #
      if text.lower() == '::help':
        lib.help()

      elif text.lower() == '::quit':
        lib.quitProcess()

      elif text.lower() == '::clear':
        lib.clearPad()

      elif text.lower() == '::time':
        if vars.linux_compatibility.lower() == 'false' or vars.linux_compatibility == 'NULL':
          print(vars.now())
        else:
          os.system("date +%I:%M' '%p")  # Returns: 12:00 AM

      elif text.lower().split(' ')[0] == '::stall':
        lib.stall()

      elif text.lower().split(' ')[0] == '::save':
        lib.saveText()

      elif text.lower().split(' ')[0] == '::load':
        lib.loadSave()

      elif text.lower().split(' ')[0] == '::open':
        lib.openFile()

      elif text.lower().split(' ')[0] == '::log':
        if len(text.split(' ')) > 1:
          print(' '.join(text.split(' ')[1:]))
        else:
          print('No string provided, Example(::log Python Is Better).')

      elif text.lower().split(' ')[0] == '::system':
        if vars.disable_commands.lower() == 'true' or vars.disable_commands == 'NULL':
          if len(text.split(' ')) > 1:
            command = ' '.join(text.lower().split(' ')[1:])
            os.system(command)
          else:
            print('No command given, Example(::system time /t).')
        else:
          print('System commands have been disabled by configuration, create \
          \na config file and type (commands: false) without parentheses \
          \nto enable them or just delete the file.')

      elif text.lower().split(' ')[0] == '::theme':
        if vars.linux_compatibility.lower() == 'false' or vars.linux_compatibility == 'NULL':
          if len(text.split(' ')) > 1:
            lib.changeTheme(text)
          else:
            print('Please pass 2 colors, Example(::theme blue white).')
        else:
          print('Theme changes are prohibited in linux compatibility mode.')

      # SPECIAL SWITCHES #
      elif text.lower() == '::_reset':
        lib.clearPad()
        vars.output_log.clear()
        vars.user_vars.clear()

      elif text.lower() == '::_logged':
        if len(vars.output_log) == 0:
          print('No logged text found.')
        else:
          print('\n'.join(vars.output_log))

      elif text.lower() == '::_version':
        extension = __file__.split('\\')[-1][__file__.split('\\')[-1].find('.'):]
        # Gave me a headache coding such a stupid one liner
        directory = '/'.join(__file__.split('\\')[:-1])
        mode = extension  # Incase none of the below statements are true
        if extension == '.exe':
          mode = 'COMPILED'
        if extension == '.pyc':
          mode = 'PY-COMPILED'
        if extension == '.dll':
          mode = 'COMPILED-MODULE'
        if extension == '.py':
          mode = 'INTERPRETED'
        print(f'{vars.version} | {mode} at {directory}')

      elif text.lower().split(' ')[0] == '::_dump':
        all_vars = dir()
        for item in all_vars:
          if not item.startswith('__'):
            value = eval(item)
            print(f'{item} {type(value)} = {value}')
          else:
            print(item)

      elif '::' in text.lower().split(' ')[0]:
        print(f'The given command {text.lower().split(" ")[0]} is not valid in this mode, try opening a file.')

      else:
        vars.output_log.append(text)

  except PermissionError:
    print('Action taken without the required permissions please \
    run this program as administrator to enact attempted action.')
    time.sleep(3)
  except Exception as e:
    print(f'ERROR: {e}')
    time.sleep(3)

else:
  print(f"You can't import {__file__} you must run it.")
  sys.exit(1)