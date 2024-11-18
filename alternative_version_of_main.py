
def read_data(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        header = file.readline().strip().split('\t')
        data = []
        for line in file:
            values = line.strip().split('\t')
            data.append(dict(zip(header, values)))
    return data


def analyze_total(data, year):
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


data = read_data("data.tsv")
print(analyze_total(data, 2000))