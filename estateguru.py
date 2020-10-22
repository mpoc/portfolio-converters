import sys
import csv
import datetime

csv_file = sys.argv[1]

events = []
with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        events.append(row)

events = events[:-2]

def parse_date(date):
    try:
        date_time_obj = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
        return str(date_time_obj)
    except Exception as e:
        print('Could not parse date ' + date)
        return sys.exit()

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

def parse_name(raw_name, inv_type):
    return 'Deposit' if inv_type == 'Deposit' else raw_name

for event in events:
    delim = ';'

    raw_date = event['Patvirtinimo data']
    raw_name = event['Projekto pavadinimas']
    raw_amount = event['Suma']
    raw_currency = event['Valiuta']
    raw_type = event['Pinigų srauto tipas']

    inv_date = parse_date(raw_date)
    inv_type = parse_type(raw_type)
    inv_name = parse_name(raw_name, inv_type)
    inv_amount = raw_amount
    inv_currency = raw_currency
    inv_platform = 'EstateGuru'

    print(inv_date + delim + inv_name + delim + inv_amount + delim + inv_currency + delim + inv_type + delim + inv_platform)
