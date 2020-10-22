import sys
import csv
import re

csv_file = sys.argv[1]

events = []
with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        events.append(row)

events = events[:-2]

def parse_date(date):
    date_regex = r"^(\d{2})\/(\d{2})\/(\d{4}) (\d{2}:\d{2})$"
    p = re.compile(date_regex)
    m = p.match(date)
    if (m == None):
        print('Could not match date ' + date)
        return sys.exit()
    else:
        return m.group(3) + '-' + m.group(2) + '-' + m.group(1) + ' ' + m.group(4)

def parse_type(raw_type):
    type_dict = {
        'Investicija': 'Investment',
        'Indėlis(Lemonway)': 'Deposit',
        'Partnerystė': 'Affiliate earnings'
    }

    if raw_type in type_dict:
        return type_dict[raw_type]
    else:
        print('Could not map type ' + raw_type)
        return sys.exit()

def parse_name(raw_name, type):
    return 'Deposit' if type == 'Deposit' else raw_name

for event in events:
    delim = ';'

    raw_date = event['Patvirtinimo data']
    raw_name = event['Projekto pavadinimas']
    raw_amount = event['Suma']
    raw_currency = event['Valiuta']
    raw_type = event['Pinigų srauto tipas']

    date = parse_date(raw_date)
    type = parse_type(raw_type)
    name = parse_name(raw_name, type)
    amount = raw_amount
    currency = raw_currency
    platform = 'EstateGuru'

    print(date + delim + name + delim + amount + delim + currency + delim + type + delim + platform)
