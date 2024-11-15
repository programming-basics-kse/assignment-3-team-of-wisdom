import argparse

# Загальний парсер для, в які входять аргументи команд
parser = argparse.ArgumentParser(description="Analysis of medals according to the Olympic Games.")
parser.add_argument("data_file", type=str, help="Address of the file with data")# В трьох цих місцях необхідно проробити валідацію
subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

# Підкоманда -medals
