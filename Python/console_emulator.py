# Emulates the windows terminal and cmd
import os
import sys


class Globals:
  current_working_dir: str = os.getcwd()
  command_map: dict = {
    "cd": 1,
    "ls": 2,
    "echo": 3,
    "clear" | "cls": 4,  # i want cls and clear to both be 4
    "touch": 5,  # Creates a file
    "rm": 6  # Removes a file
  }