import argparse
import csv


def read_data(file_path):
    """Читання даних із файлу."""
    try:
        with open(file_path, 'r', encoding='utf8') as file:
            header = file.readline().strip().split('\t')
            data = [dict(zip(header, line.strip().split('\t'))) for line in file]
        return data
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено. Перевірте правильність шляху.")
        exit()
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        exit()


def validate_year(data, year):
    """Перевірка, чи існує рік в даних."""
    if not any(int(row["Year"]) == year for row in data):
        print(f"Помилка: рік {year} відсутній у даних. Спробуйте інший рік.")
        return False
    return True


def validate_country(data, country):
    """Перевірка, чи існує країна в даних."""
    if not any(row["Team"].lower() == country.lower() or row["NOC"].lower() == country.lower() for row in data):
        print(f"Помилка: країна '{country}' відсутня у даних. Спробуйте іншу країну.")
        return False
    return True


def medals_command(data, country, year, output_file=None):
    """Аналіз медалей для заданої країни та року."""
    if not validate_year(data, year) or not validate_country(data, country):
        return

    medalists = {}
    country_medals = {"Gold": 0, "Silver": 0, "Bronze": 0}

    for row in data:
        if int(row["Year"]) == year and (
                row["Team"].lower() == country.lower() or row["NOC"].lower() == country.lower()) and row[
            "Medal"] != 'NA':
            if row["Name"] not in medalists:
                medalists[row["Name"]] = (row["Sport"], row["Medal"])
            country_medals[row["Medal"]] += 1

    if not medalists:
        print(f"У {year} році країна '{country}' не здобула жодної медалі.")
        return

    # Вивід результатів
    print("Список перших 10 медалістів:")
    for i, (name, details) in enumerate(medalists.items()):
        print(f"{i + 1}. {name} - {details[0]} - {details[1]}")
        if i == 9:  # Показуємо максимум 10
            break

    print("\nЗагальна кількість медалей:")
    for medal, count in country_medals.items():
        print(f"{medal}: {count}")

    # Запис результатів у файл
    if output_file:
        try:
            with open(output_file, 'w') as file:
                for name, details in medalists.items():
                    file.write(f"{name} - {details[0]} - {details[1]}\n")
                for medal, count in country_medals.items():
                    file.write(f"{medal}: {count}\n")
            print(f"Результати збережено у файл '{output_file}'.")
        except Exception as e:
            print(f"Помилка запису у файл: {e}")


def total_command(data, year):
    """Аналіз медалей для всіх країн у заданому році."""
    if not validate_year(data, year):
        return

    country_medals = {}

    for row in data:
        if int(row["Year"]) == year and row["Medal"] != 'NA':
            country = row["Team"]
            if country not in country_medals:
                country_medals[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            country_medals[country][row["Medal"]] += 1

    print(f"Медалі за рік {year}:")
    for country, medals in sorted(country_medals.items()):
        print(f"{country} - Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}")


def overall_command(data, countries):
    """Найуспішніший рік для кожної країни."""
    for country in countries:
        if not validate_country(data, country):
            continue

        year_medals = {}

        for row in data:
            if (row["Team"].lower() == country.lower() or row["NOC"].lower() == country.lower()) and row[
                "Medal"] != 'NA':
                year = int(row["Year"])
                if year not in year_medals:
                    year_medals[year] = 0
                year_medals[year] += 1

        if year_medals:
            best_year = max(year_medals, key=year_medals.get)
            print(f"{country}: найуспішніший рік - {best_year} ({year_medals[best_year]} медалей).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Аналіз даних Олімпійських ігор.")
    parser.add_argument("data_file", type=str, help="Файл з даними")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Команда medals
    medals_parser = subparsers.add_parser("medals", help="Аналіз медалей для конкретної країни та року")
    medals_parser.add_argument("country", type=str, help="Країна або NOC")
    medals_parser.add_argument("year", type=int, help="Рік")
    medals_parser.add_argument("-output", type=str, help="Файл для збереження результатів")

    # Команда total
    total_parser = subparsers.add_parser("total", help="Аналіз медалей для всіх країн у році")
    total_parser.add_argument("year", type=int, help="Рік")

    # Команда overall
    overall_parser = subparsers.add_parser("overall", help="Найуспішніший рік для кожної країни")
    overall_parser.add_argument("countries", type=str, nargs="+", help="Список країн")

    args = parser.parse_args()
    data = read_data(args.data_file)

    if args.command == "medals":
        medals_command(data, args.country, args.year, args.output)
    elif args.command == "total":
        total_command(data, args.year)
    elif args.command == "overall":
        overall_command(data, args.countries)
