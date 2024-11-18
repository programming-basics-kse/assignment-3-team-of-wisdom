import argparse

# Create the main parser
parser = argparse.ArgumentParser(description="Analysis of medals according to the Olympic Games.")

# Adding argument for main parser
parser.add_argument("data_file", type=str, help="Address of the file with data")  # В трьох цих місцях необхідно проробити валідацію

# Create sub-parsers
subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

# Create a sub-parser for the '-medals' command
medals_parser = subparsers.add_parser("medals", help="Analyze medals for a specific country and year")
medals_parser.add_argument("country", type=str, help="Country name or NOC code (e.g., 'USA' or 'United States')")
medals_parser.add_argument("year", type=int, help="Year of the Olympic Games")
medals_parser.add_argument("-output", type=str, help="Optional file to save the results")

# Create a sub-parser for the '-total' command
total_parser = subparsers.add_parser("total", help="Analyze medals during a whole year for all countries")
total_parser.add_argument("year", type=int, help="Year of Olympic games")

# Parse the command-line arguments
args = parser.parse_args()


def read_data(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        header = file.readline().strip().split('\t')
        data = []
        for line in file:
            values = line.strip().split('\t')
            data.append(dict(zip(header, values)))
    return data

def medals_command(data):
    pass

def total_command(data, year):
    country_medals = {}
    for row in data:
        if int(row['Year']) == year and row['Medal'] != 'NA':
            country = row['Team']
            if country not in country_medals:
                country_medals[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            country_medals[country][row['Medal']] += 1
    result = []
    for country, medals in sorted(country_medals.items()):
        result.append(f"{country} - {medals['Gold']} - {medals['Silver']} - {medals['Bronze']}")
    return "\n".join(result)

while True:
    args = parser.parse_args()
    if args.command == "medals":
        print(medals_command(read_data(args.data_file)))
    elif args.command == "total":
        print(total_command(read_data(args.data_file),args.year))


