import sys
import csv
import datetime

def parse_date(date):
    try:
        date_time_obj = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
        return str(date_time_obj)
    except Exception as e:
        print('Could not parse date ' + date)
        return sys.exit()

def parse_type(raw_type, raw_state):
    type_dict = {
        'Investicija': 'Investment',
        'Indėlis(Lemonway)': 'Deposit',
        'Partnerystė': 'Affiliate earnings',
        'Palūkanos': 'Interest'
    }

    if (raw_type in type_dict) and (type_dict[raw_type] == 'Investment') and (raw_state == 'Grąžinta'):
        return 'Loan decline'
    elif raw_type in type_dict:
        return type_dict[raw_type]
    else:
        print('Could not map type ' + raw_type)
        return sys.exit()

def parse_name(raw_name, inv_type):
    return 'Deposit' if inv_type == 'Deposit' else raw_name

def parse_amount(raw_amount, inv_type):
    # Currently, if there's a loan return, the amount is just set to zero. This
    # is because in the account balance in EstateGuru, instead of having two
    # events, one for investment and one for loan return. However, there is only
    # one, which shows up as "Returned" and has the amount, however the
    # transaction type is still investment. Ideally this would be edited to have
    # two separate events for investment and loan return instead of just setting
    # the amount to 0 and effectively ignoring the event entirely.
    if inv_type == 'Investment':
        return "-" + raw_amount
    elif inv_type == 'Loan decline':
        return '0'
    else:
        return raw_amount

def process_event(event):
    delim = ';'

    raw_date = event['Patvirtinimo data']
    raw_name = event['Projekto pavadinimas']
    raw_amount = event['Suma']
    raw_currency = event['Valiuta']
    raw_type = event['Pinigų srauto tipas']
    raw_state = event['Pinigų srauto būsena']

    inv_date = parse_date(raw_date)
    inv_type = parse_type(raw_type, raw_state)
    inv_name = parse_name(raw_name, inv_type)
    inv_amount = parse_amount(raw_amount, inv_type)
    inv_currency = raw_currency
    inv_platform = 'EstateGuru'

    inv_details = [
        inv_date,
        inv_name,
        inv_amount,
        inv_currency,
        inv_type,
        inv_platform
    ]
    return delim.join(inv_details)

def get_events():
    csv_file = sys.argv[1]

    events = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            events.append(row)

    events = events[:-2]

    return events

events = get_events()
processed_events = list(map(process_event, events))

for event in processed_events:
    print(event)
