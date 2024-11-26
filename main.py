import argparse


def read_data(file_path):
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
        if row["Team"].lower() == country.lower() or row["NOC"].lower() == country.lower():
            valid_country_counter += 1
    if valid_country_counter == 0:
        return print("Sorry, You have entered inappropriate country value you should try again!")

    medalist_counter = 0
    for row in data:  # Searching for 10 medalists
        if (int(row["Year"]) == year) and (
                row["Team"].lower() == country.lower() or row["NOC"].lower() == country.lower()) and (
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
                row["Team"].lower() == country.lower() or row["NOC"].lower() == country.lower()) and (
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
    result = []
    for country, medals in sorted(country_medals.items()):
        result.append(f"{country} - Gold: {medals['Gold']} - Silver: {medals['Silver']} - Bronze: {medals['Bronze']}")
    return "\n".join(result)


def overall_command(data, countries):  # task3
    for country in countries:
        country_years = {}
        for row in data:
            if (row["Team"].lower() == country.lower() or row["NOC"].lower() == country.lower()) and (
                    row['Medal'] != 'NA'):  # Adding keys as years and medals as value to country_years.
                if row["Year"] not in country_years:
                    country_years[row["Year"]] = 0
                country_years[row["Year"]] += 1
        if len(country_years) == 0:  # Validation for incorrect country
            print(f"Sorry. There is no {country} as a country in dataset")
        else:
            max_key, max_value = max(country_years.items(),
                                     key=lambda x: x[1])  # Finding max values with its key and printing it
            print(f"{country} had its best Olympics in {max_key} with {max_value} medals.")


def interactive_mode(data):
    print("Interactive mode: Enter a country name or NOC code to get statistics, or type 'exit' to quit.")
    while True:
        user_input = input("Enter country (or 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Exiting interactive mode.")
            break

        country_data = [row for row in data if
                        row["Team"].lower() == user_input.lower() or row["NOC"].lower() == user_input.lower()]

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

def main():
    # Create the main parser
    parser = argparse.ArgumentParser(description="Analysis of medals according to the Olympic Games.")

    # Adding argument for main parser
    parser.add_argument("data_file", type=str,
                        help="Address of the file with data")  # В трьох цих місцях необхідно проробити валідацію

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

    # Create a sub-parser for the '-overall' command
    total_parser = subparsers.add_parser("overall",
                                         help="Analyzing best year Olympic for each country that you have entered")
    total_parser.add_argument("countries", type=str, nargs="+", help="Countries to analyse.")

    interactive_parser = subparsers.add_parser("interactive", help="Enter interactive mode to analyze countries.")

    # Parse the command-line arguments
    args = parser.parse_args()
    print('triggered')
    if args.command == "interactive":
        interactive_mode(read_data(args.data_file))

    if args.command == "medals":
        medals_command(read_data(args.data_file), args.country, args.year, args.output)
    elif args.command == "total":
        print(total_command(read_data(args.data_file), args.year))
    elif args.command == "overall":
        overall_command(read_data(args.data_file), args.countries)
