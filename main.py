import argparse

# Загальний парсер для, в які входять аргументи команд
parser = argparse.ArgumentParser(description="Analysis of medals according to the Olympic Games.")
parser.add_argument("data_file", type=str, help="Address of the file with data")# В трьох цих місцях необхідно проробити валідацію
subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

# Підкоманда -medals
medals_parser = subparsers.add_parser("medals", help="Analyze medals for a specific country and year")
medals_parser.add_argument("country", type=str, help="Country name or NOC code (e.g., 'USA' or 'United States')")
medals_parser.add_argument("year", type=int, help="Year of the Olympic Games")
medals_parser.add_argument("-output", type=str, help="Optional file to save the results")
args = parser.parse_args()
