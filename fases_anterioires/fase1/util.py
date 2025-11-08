import os

def limpar_terminal():
  os.system("clear" if os.name == "posix" else "cls")
