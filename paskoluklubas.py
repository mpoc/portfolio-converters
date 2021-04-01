import sys
import csv
import datetime
import re
import zipfile
import io

def parse_date(date):
    try:
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return str(date_time_obj)
    except Exception as e:
        print('Could not parse date ' + date)
        return sys.exit()

def parse_type(raw_type):
    type_dict = {
        r"^Investicija į kreditą „[A-Z0-9]+“$": 'Investment',
        r"^[A-Z0-9-]+ Sąskaitos papildymas$": 'Deposit',
        r"^Investicijos [A-Z0-9]+ kredito dalies grąžinimas$": 'Loan return',
        r"^Investicijos [A-Z0-9]+ palūkanų grąžinimas$": 'Interest',
        r"^Investicijos [A-Z0-9]+ grąžinimas atsisakius vartojimo paskolos$": 'Loan decline',
        r"^Partnerystės programos išmoka$": 'Affiliate earnings',
        r"^Užtikrinimo fondo mokestis už investiciją į kreditą „[A-Z0-9]+“$": 'Buyback guarantee',
        r"^Tarpininkavimo mokestis už investicijos [A-Z0-9]+ gautą įmoką$": 'Broker fee',
        r"^Investicijos [A-Z0-9]+ kredito dalies grąžinimas iš užtikrinimo fondo$": 'Loan return', # Could change type to Buyback loan return
        r"^Investicijos [A-Z0-9]+ palūkanų grąžinimas iš užtikrinimo fondo$": 'Interest', # Could change type to Buyback interest
        r"^Investicijos [A-Z0-9]+ vėlavimo palūkanų grąžinimas$": 'Interest', # Could change to Late interest
        r"^Apmokėjimas už reikalavimo teisės perleidimą$": 'Buyback return' # Could change to Investmant sale
    }

    for regex in type_dict:
        p = re.compile(regex)
        m = p.match(raw_type)
        if (m != None):
            return type_dict[regex]

    print('Could not map type for ' + raw_type)
    return sys.exit()

def parse_amount(raw_amount):
    if (raw_amount[0] == '+'):
        return raw_amount[1:]
    elif (raw_amount[0] == '-'):
        return raw_amount
    else:
        print("Could not parse amount (amount: " + raw_amount + ")")
        return sys.exit()

def process_event(event):
    delim = ';'

    raw_date = event['Data']
    raw_name = event['Mokėjimo paskirtis']
    raw_amount = event['Apyvarta']

    inv_date = parse_date(raw_date)
    inv_type = parse_type(raw_name)
    inv_name = raw_name
    inv_amount = parse_amount(raw_amount)
    inv_currency = 'EUR'
    inv_platform = 'Paskolų klubas'

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
    zip_filename = sys.argv[1]

    events = []
    # Open the zip file
    with zipfile.ZipFile(zip_filename) as zip_file:
        # Open the only file in the zip (the csv export)
        csv_filename = zip_file.namelist()[0]
        with zip_file.open(csv_filename) as csv_file:
            # Convert the opened csv export from ZipExtFile to TextIOWrapper
            csv_file_wrapper = io.TextIOWrapper(csv_file, newline='')

            csv_file_wrapper.readline()
            csv_file_wrapper.readline()
            csv_file_wrapper.readline()

            reader = csv.DictReader(csv_file_wrapper, delimiter=',', quotechar='"')
            for row in reader:
                events.append(row)

    events = events[1:-3]

    return events

events = get_events()
processed_events = list(map(process_event, events))

for event in processed_events:
    print(event)
