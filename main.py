import argparse
import os


def validate_file(file_path):
    """Checks the existence of a file and basic requirements for its structure."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf8') as file:
        header = file.readline().strip().split('\t')
        if not header:
            raise ValueError("The file does not contain a header.")
        for line_number, line in enumerate(file, start=2):
            values = line.strip().split('\t')
            if len(values) != len(header):
                raise ValueError(f"The string {line_number} has an incorrect number of values.")


def read_data(file_path):
    """Reads a file and returns data as a list of dictionaries."""
    validate_file(file_path)  # validation
    with open(file_path, 'r', encoding='utf8') as file:
        header = file.readline().strip().split('\t')
        data = []
        for line in file:
            values = line.strip().split('\t')
            data.append(dict(zip(header, values)))
    return data


def medals_command(data, country, year, output_file="", ):  # task1
    ten_athlete_medalist = {}

    valid_year_counter = 0  # Validation for year
    for row in data:
        if year == int(row["Year"]):
            valid_year_counter += 1
    if valid_year_counter == 0:
        return print("Sorry, You have entered inappropriate year value you should try again!")

    valid_country_counter = 0  # Validation for country
    for row in data:
        if row["Team"].lower().replace(' ', '') == country.lower().strip().replace(' ', '') or row[
            "NOC"].lower().replace(' ', '') == country.lower().strip().replace(' ', ''):
            valid_country_counter += 1
    if valid_country_counter == 0:
        return print("Sorry, You have entered inappropriate country value you should try again!")

    medalist_counter = 0
    for row in data:  # Searching for 10 medalists
        if (int(row["Year"]) == year) and (
                row["Team"].lower().replace(' ', '') == country.lower().strip().replace(' ', '') or row[
            "NOC"].lower().replace(' ', '') == country.lower().strip().replace(' ', '')) and (
                row['Medal'] != 'NA'):
            ten_athlete_medalist[row["Name"]] = [row["Sport"], row["Medal"]]
            medalist_counter += 1
        if medalist_counter == 10:
            break
    if medalist_counter < 10:  # Validation if there are less than 10 medalists
        return print(
            f"Sorry, This country have less than 10 athletes with medals. It only has {medalist_counter} athletes ")

    country_medals = {}
    for row in data:  # Summing up information about country medals
        if (int(row["Year"]) == year) and (
                row["Team"].lower().replace(' ', '') == country.lower().strip().replace(' ', '') or row[
            "NOC"].lower().replace(' ', '') == country.lower().strip().replace(' ', '')) and (
                row['Medal'] != 'NA'):
            country_in_loop = row["Team"]
            if country_in_loop not in country_medals:
                country_medals[country_in_loop] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            country_medals[country_in_loop][row['Medal']] += 1

    for name, sport_medal in ten_athlete_medalist.items():  # Printing result of function
        print(f"{name} - {sport_medal[0]} - {sport_medal[1]}")
    print(country_medals)

    if output_file is None:
        pass
    elif output_file == "":
        pass
    else:
        with open(output_file, "w") as file:  # Writing into file all information from function
            for name, sport_medal in ten_athlete_medalist.items():
                file.write(f"{name} - {sport_medal[0]} - {sport_medal[1]}\n")
            for country, medals in sorted(country_medals.items()):
                file.write(f"{country} - {medals['Gold']} - {medals['Silver']} - {medals['Bronze']}\n")
    return ten_athlete_medalist, country_medals


def total_command(data, year):  # task2
    country_medals = {}
    for row in data:
        if int(row['Year']) == year and row['Medal'] != 'NA':
            country = row['Team']
            if country not in country_medals:
                country_medals[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            country_medals[country][row['Medal']] += 1

    header = f"{'Country':<30}{'Gold':<10}{'Silver':<10}{'Bronze':<10}"
    separator = "-" * len(header)
    result = [header, separator]

    for country, medals in sorted(country_medals.items()):
        result.append(
            f"{country:<30}{medals['Gold']:<10}{medals['Silver']:<10}{medals['Bronze']:<10}"
        )

    return "\n".join(result)


def overall_command(data, countries):  # Task 3
    for country in countries:
        country_data = [
            row for row in data
            if (row["Team"].lower().replace(' ', '') == country.lower().strip().replace(' ', '') or row[
                "NOC"].lower().replace(' ', '') == country.lower().strip().replace(' ', ''))
               and row['Medal'] != 'NA'
        ]
        if not country_data:
            print(f"Sorry. There is no data for {country} in the dataset.")
            continue

        country_years = {}
        for row in country_data:
            year = row["Year"]
            country_years[year] = country_years.get(year, 0) + 1

        max_key, max_value = max(country_years.items(), key=lambda x: x[1])

        print(f"{country:<15} | Best Year: {max_key:<5} | Total Medals: {max_value:<3}")


def interactive_mode(data):
    print("Interactive mode: Enter a country name or NOC code to get statistics, or type 'exit' to quit.")
    while True:
        user_input = input("Enter country (or 'exit' to quit): ").strip()
        if user_input.lower().strip().replace(' ', '') == 'exit':
            print("Exiting interactive mode.")
            break

        country_data = [row for row in data if
                        row["Team"].lower().replace(' ', '') == user_input.lower().strip().replace(' ', '') or row[
                            "NOC"].lower().replace(' ', '') == user_input.lower().strip().replace(' ', '')]

        if not country_data:
            print(f"No data found for country '{user_input}'. Please try again.")
            continue

        # First participation
        first_participation = min(country_data, key=lambda x: int(x["Year"]))
        first_year = first_participation["Year"]
        first_city = first_participation["City"]
        print(f"First participation: {first_year} in {first_city}")

        # Best and worst Olympics
        year_medals = {}
        for row in country_data:
            year = int(row["Year"])
            if row["Medal"] != "NA":
                if year not in year_medals:
                    year_medals[year] = 0
                year_medals[year] += 1

        if year_medals:
            best_year = max(year_medals, key=year_medals.get)
            worst_year = min(year_medals, key=year_medals.get)
            print(f"Most successful Olympics: {best_year} with {year_medals[best_year]} medals")
            print(f"Least successful Olympics: {worst_year} with {year_medals[worst_year]} medals")
        else:
            print("No medals won by this country.")

        # Average medals per Olympics
        total_medals = sum(year_medals.values())
        total_olympics = len(set(row["Year"] for row in country_data))
        avg_medals = total_medals / total_olympics if total_olympics > 0 else 0
        print(f"Average medals per Olympics: {avg_medals:.2f}")

        # Average medals by type
        medal_types = {"Gold": 0, "Silver": 0, "Bronze": 0}
        for row in country_data:
            if row["Medal"] in medal_types:
                medal_types[row["Medal"]] += 1

        avg_gold = medal_types["Gold"] / total_olympics if total_olympics > 0 else 0
        avg_silver = medal_types["Silver"] / total_olympics if total_olympics > 0 else 0
        avg_bronze = medal_types["Bronze"] / total_olympics if total_olympics > 0 else 0
        print(f"Average Gold medals: {avg_gold:.2f}, Silver: {avg_silver:.2f}, Bronze: {avg_bronze:.2f}")
        print("-" * 50)


def validate_country(country, data):
    """Validate if the country or NOC code exists in the data."""
    valid_country = False
    for row in data:
        if row["Team"].lower().replace(' ', '') == country.lower().strip().replace(' ', '') or row[
            "NOC"].lower().replace(' ', '') == country.lower().strip().replace(' ', ''):
            valid_country = True
            break
    if not valid_country:
        raise ValueError(f"Invalid country or NOC code: {country}. Please check the input and try again.")


def validate_year(year, data):
    """Validate if the year exists in the data."""
    valid_year = False
    for row in data:
        if int(row["Year"]) == year:
            valid_year = True
            break
    if not valid_year:
        raise ValueError(f"Invalid year: {year}. No Olympic data found for this year.")


# Parsing command-line arguments
parser = argparse.ArgumentParser(description="Analysis of medals according to the Olympic Games.")
parser.add_argument("data_file", type=str, help="Address of the file with data")
parser.add_argument("-medals", nargs=2, metavar=("Country", "Year"),
                    help="Analyze medals for a specific country and year")
parser.add_argument("-output", type=str, metavar="File_output",
                    help="Optional file to save the results only for medals")
parser.add_argument("-total", nargs=1, metavar="Year", help="Analyze medals for a specific country and year")
parser.add_argument("-overall", type=str, nargs="+", metavar="Country",
                    help="Analyzing best year Olympic for each country that you have entered")
parser.add_argument("-interactive", action="store_const", const=True,
                    help="Enter interactive mode to analyze countries.")
# Parse the command-line arguments
args = parser.parse_args()

# Read data file
try:
    validate_file(args.data_file)
    data = read_data(args.data_file)
except (FileNotFoundError, ValueError) as e:
    print(e)
    exit()

# Process the different commands

if args.medals is not None:
    try:
        validate_country(args.medals[0], data)
        validate_year(int(args.medals[1]), data)
        medals_command(data, args.medals[0], int(args.medals[1]), args.output)
    except (ValueError, KeyError) as e:
        print(e)
elif args.total is not None:
    try:
        validate_year(int(args.total[0]), data)
        print(total_command(data, int(args.total[0])))
    except ValueError as e:
        print(e)
elif args.overall is not None:
    try:
        for country in args.overall:
            validate_country(country, data)
        overall_command(data, args.overall)
    except ValueError as e:
        print(e)
elif args.interactive:
    interactive_mode(data)
