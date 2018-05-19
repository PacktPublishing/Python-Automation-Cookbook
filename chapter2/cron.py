import argparse
import sys
from datetime import datetime
import configparser


def main(number, other_number, output):
    result = number * other_number
    print(f'[{datetime.now()}] The result is {result}', file=output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='config', type=argparse.FileType('r'),
                        help='config file',
                        default='/etc/automate.ini')
    parser.add_argument('-o', dest='output', type=argparse.FileType('a'),
                        help='output file',
                        default=sys.stdout)

    args = parser.parse_args()
    if args.config:
        config = configparser.ConfigParser()
        config.read_file(args.config)
        # Transforming values into integers
        args.n1 = int(config['DEFAULT']['n1'])
        args.n2 = int(config['DEFAULT']['n2'])

    main(args.n1, args.n2, args.output)
