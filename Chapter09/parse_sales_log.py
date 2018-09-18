import os
import openpyxl
import argparse
from sale_log import SaleLog


def get_logs_from_file(shop, log_filename):
    '''
    Based on a file, obtain and parse all logs
    Return a list of SaleLog objects
    '''
    with open(log_filename) as logfile:
        logs = [SaleLog.parse(shop=shop, text_log=log)
                for log in logfile]

    return logs


def main(log_dir, output_filename):
    logs = []
    for dirpath, dirnames, filenames in os.walk(log_dir):
        for filename in filenames:
            # The shop is the last directory
            shop = os.path.basename(dirpath)
            fullpath = os.path.join(dirpath, filename)
            logs.extend(get_logs_from_file(shop, fullpath))

    # Create and save the Excel sheet
    xlsfile = openpyxl.Workbook()
    sheet = xlsfile['Sheet']

    # Write the first row
    sheet.append(SaleLog.row_header())
    for log in logs:
        sheet.append(log.row())

    xlsfile.save(output_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(type=str, dest='log_directory')
    parser.add_argument('-o', type=str, dest='output_file',
                        default='result.xlsx')

    args = parser.parse_args()

    main(args.log_directory, args.output_file)
