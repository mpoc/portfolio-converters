import sys
import csv
import datetime

def parse_date(date):
    try:
        date_time_obj = datetime.datetime.strptime(date, '%d %b %y, %H:%M')
        return str(date_time_obj)
    except Exception as e:
        print('Could not parse date ' + date)
        return sys.exit()

def parse_type(raw_type):
    type_dict = {
        'Investment': 'Investment',
        'Wallet deposit': 'Deposit',
        'Affiliate earnings': 'Affiliate earnings'
    }

    if raw_type in type_dict:
        return type_dict[raw_type]
    else:
        print('Could not map type ' + raw_type)
        return sys.exit()

def parse_name(raw_name, inv_type):
    return 'Deposit' if inv_type == 'Deposit' else raw_name

def parse_amount(raw_amount, inv_type):
    return "-" + raw_amount[2:] if inv_type == 'Investment' else raw_amount[2:]

def process_event(event):
    delim = ';'

    raw_date = event['Date']
    raw_name = event['Project']
    raw_amount = event['Amount']
    raw_type = event['Type']

    inv_date = parse_date(raw_date)
    inv_type = parse_type(raw_type)
    inv_name = parse_name(raw_name, inv_type)
    inv_amount = parse_amount(raw_amount, inv_type)
    inv_currency = 'EUR'
    inv_platform = 'EvoEstate'

    return inv_date + delim + inv_name + delim + inv_amount + delim + inv_currency + delim + inv_type + delim + inv_platform

def get_events():
    csv_file = sys.argv[1]

    events = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            events.append(row)

    return events

events = get_events()
for event in events:
    print(process_event(event))
