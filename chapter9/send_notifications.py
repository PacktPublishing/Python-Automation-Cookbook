import argparse
import configparser
import os.path
import csv
import delorean
import requests
from twilio.rest import Client


def send_phone_notification(entry, config):
    ACCOUNT_SID = config['TWILIO']['ACCOUNT_SID']
    AUTH_TOKEN = config['TWILIO']['AUTH_TOKEN']
    FROM = config['TWILIO']['FROM']
    coupon = entry['Code']
    TO = entry['Target']
    text = f'Congrats! Here is a redeemable coupon! {coupon}'

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(body=text, from_=FROM, to=TO)
    except Exception as err:
        return 'ERROR'

    return 'SENT'


def send_email_notification(entry, config):
    KEY = config['MAILGUN']['KEY']
    DOMAIN = config['MAILGUN']['DOMAIN']
    FROM = config['MAILGUN']['FROM']
    TO = entry['Target']
    name = entry['Name']
    auth = ('api', KEY)
    coupon = entry['Code']
    text = f'Congrats! Here is a redeemable coupon! {coupon}'

    data = {
        'from': f'Sender <{FROM}>',
        'to': f'{name} <{TO}>',
        'subject': 'You have a coupon!',
        'text': text,
    }
    response = requests.post(f"https://api.mailgun.net/v3/{DOMAIN}/messages",
                             auth=auth, data=data)
    breakpoint()
    if response.status_code == 200:
        return 'SENT'

    return 'ERROR'


def invalid_method(entry, config):
    return 'INVALID_METHOD'


def send_notification(entry, send, config):
    if not send:
        return entry

    # Route each of the notifications
    METHOD = {
        'PHONE': send_phone_notification,
        'EMAIL': send_email_notification,
    }
    method = METHOD.get(entry['Contact Method'], invalid_method)
    result = method(entry, config)

    entry['Timestamp'] = delorean.utcnow().datetime.isoformat()
    entry['Status'] = result
    return entry


def save_file(notif_file, data):
    '''
    Overwrite the file with the new information
    '''

    # Start at the start of the file
    notif_file.seek(0)

    header = data[0].keys()
    writer = csv.DictWriter(notif_file, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)

    # Be sure to write to disk
    notif_file.flush()


def main(data, codes, notif_file, config, send):
    # Go through each line that is not sent
    for index, entry in enumerate(data):
        if entry['Status'] == 'SENT':
            continue

        if not entry['Code']:
            if not codes:
                msg = ('The file is missing codes, and no code file '
                       'has been defined')
                raise Exception(msg)
            entry['Code'] = codes.pop()

        entry = send_notification(entry, send, config)
        data[index] = entry

        # Save the data into the file
        save_file(notif_file, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(type=argparse.FileType('r+'), dest='notif_file',
                        help='notifications file')
    parser.add_argument('-c', '--codes', type=argparse.FileType('r'),
                        help='Optional file with codes. If present, the '
                             'file will be populated with codes. '
                             'No codes will be sent')
    parser.add_argument('--config', type=str, dest='config_file',
                        default='config.ini',
                        help='config file (detaulf config.ini)')
    args = parser.parse_args()

    # Read configuration
    if not os.path.isfile(args.config_file):
        print(f'Config file {args.config_file} is missing. Aborting')
        exit(1)
    with open(args.config_file) as fp:
        config = configparser.ConfigParser()
        config.read_file(fp)

    # Read data
    reader = csv.DictReader(args.notif_file)
    data = list(reader)

    codes = None
    send = True
    if args.codes:
        codes = [code_line[0] for code_line in csv.reader(args.codes)]
        send = False

    main(data=data, codes=codes, notif_file=args.notif_file,
         config=config, send=send)
