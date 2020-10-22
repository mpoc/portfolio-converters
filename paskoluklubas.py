import sys
import datetime
import json
import re

def parse_date(date):
    try:
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        return str(date_time_obj)
    except Exception as e:
        print('Could not parse date ' + date)
        return sys.exit()

def parse_type(raw_type):
    type_dict = {
        r"^Investicija į kreditą „[A-Z0-9]+“$": 'Investment',
        r"^Sąskaitos \"[A-Z0-9]+\" papildymas$": 'Deposit',
        r"^Investicijos [A-Z0-9]+ kredito dalies grąžinimas$": 'Loan return',
        r"^Investicijos [A-Z0-9]+ palūkanų grąžinimas$": 'Interest',
        r"^Investicijos [A-Z0-9]+ grąžinimas atsisakius vartojimo paskolos$": 'Loan decline'
    }

    for regex in type_dict:
        p = re.compile(regex)
        m = p.match(raw_type)
        if (m != None):
            return type_dict[regex]

    print('Could not map type for ' + raw_type)
    return sys.exit()

def parse_amount(raw_debit, raw_credit):
    if (raw_debit == ''):
        return raw_credit
    elif (raw_credit == ''):
        return "-" + raw_debit
    else:
        print("Could not parse amount (debit: " + raw_debit + "credit: " + raw_credit + ")")
        sys.exit()

print("Paste your PK events and hit Ctrl-D:")
events_raw = sys.stdin.read()
events = json.loads(events_raw)

for event in events:
    delim = ';'

    raw_date = event['date']
    raw_name = event['name']
    raw_debit = event['debit']
    raw_credit = event['credit']

    inv_date = parse_date(raw_date)
    inv_type = parse_type(raw_name)
    inv_name = raw_name
    inv_amount = parse_amount(raw_debit, raw_credit)
    inv_currency = 'EUR'
    inv_platform = 'Paskolų klubas'

    print(inv_date + delim + inv_name + delim + inv_amount + delim + inv_currency + delim + inv_type + delim + inv_platform)
