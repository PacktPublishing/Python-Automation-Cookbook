import os
import openpyxl
import fpdf
import argparse
import delorean
import PyPDF2
from collections import defaultdict
from sale_log import SaleLog
import matplotlib.pyplot as plt
from itertools import islice

A4_INCHES = (11.69, 8.27)


def generate_summary(logs):
    '''
    Generate a summary, according to the received logs

    The summary has:

    {
        'start_time': start_time,
        'end_time': end_time,
        'total_income': total_income,
        'average_discount': average_discount,
        'units': units,
        'by_product': <only if more than one product is present.
                       Returns a dictionary of {product: summary}>
    }

    Note that the summary of a product won't contain the 'by_product' field
    '''
    total_income = sum(log.price for log in logs)
    start_time = min(log.timestamp for log in logs)
    end_time = max(log.timestamp for log in logs)
    average_discount = sum(log.discount for log in logs) / len(logs)
    units = len(logs)

    # Group by product and get summaries
    products = defaultdict(list)
    for log in logs:
        products[log.name].append(log)

    summary = {
        'start_time': start_time,
        'end_time': end_time,
        'total_income': total_income,
        'average_discount': average_discount,
        'units': units,
    }

    if len(products) > 1:
        by_product = {name: generate_summary(logs)
                      for name, logs in products.items()}
        summary['by_product'] = by_product

    return summary


def aggregate_by_day(logs):
    '''
    Aggregate logs by day

    returns a list of:
        (day, summary)
    '''
    days = []
    day = [logs[0]]
    for log in logs[1:]:
        end_of_day = day[0].timestamp.end_of_day
        if log.timestamp.datetime > end_of_day:
            # A new day
            days.append(day)
            day = []
        day.append(log)

    # Generate a summary by day
    def date_string(log):
        return log.timestamp.truncate('day').datetime.strftime('%d %b')

    summaries = [
        (date_string(day[0]), generate_summary(day))
        for day in days
    ]
    return summaries


def aggregate_by_shop(logs):
    '''
    Aggregate logs by shop

    returns a list of:
        (shop, summary)
    '''
    # Aggregate the results by shop
    by_shop = defaultdict(list)
    for log in logs:
        by_shop[log.shop].append(log)

    # Generate a summary by day
    summaries = [(shop, generate_summary(logs))
                 for shop, logs in by_shop.items()]
    return summaries


def graph(full_summary, products, temp_file, skip_labels=1):
    '''
    Generate a page with two graph rows from a summary:
        - Top row with Total income by product as an stacked bar graph
        - A row with X graphs by units, one for each product

    The X axis will be the tag of the summary.

    full_summary: a list of [(tags, summary)]
    products: All the available products
    temp_file: Temporal file name to strore a PDF with the graphs
    skip_labels: An optional number to skip labels, to improve
                 readability. Default 1 (show all)
    '''
    # Display the sales by day
    pos = list(range(len(full_summary)))
    units = [summary['units'] for day, summary in full_summary]

    income_by_product = []
    units_per_product = []
    # Store the aggregated income to display the bars
    baselevel = None
    default = {
        'total_income': 0,
        'units': 0,
    }
    max_units = 0
    for product in products:
        product_income = [
            summary['by_product'].get(product, default)['total_income']
            for day, summary in full_summary
        ]
        product_units = [summary['by_product'].get(product, default)['units']
                         for day, summary in full_summary]
        if not baselevel:
            baselevel = [0 for _ in range(len(full_summary))]

        income_by_product.append((product, product_income, baselevel))
        units_per_product.append((product, product_units))
        max_units = max(max(product_units), max_units)

        baselevel = [product + bottom
                     for product, bottom in zip(product_income, baselevel)]

    labels = [day for day, summary in full_summary]

    plt.figure(figsize=A4_INCHES)

    plt.subplot(2, 1, 1)
    plt.ylabel('Income by product')
    for name, product, baseline in income_by_product:
        plt.bar(pos, product, bottom=baseline)

    plt.legend([name for name, _, _ in income_by_product])
    plt.xticks(pos[::skip_labels], labels[::skip_labels])

    max_units += 1

    num_products = len(units_per_product)
    for index, (product, units) in enumerate(units_per_product):
        plt.subplot(2, num_products, num_products + index + 1)
        plt.ylabel('Total units {} sold'.format(product))
        plt.ylim(ymax=max_units)
        plt.bar(pos, units)
        # Display only on on each skip labels
        plt.xticks(pos[::skip_labels], labels[::skip_labels])

    plt.savefig(temp_file)
    return temp_file


def create_summary_brief(summary, temp_file):
    '''
    Write a PDF page with the summary information, in the specified temp_file
    '''
    document = fpdf.FPDF()
    document.set_font('Times', '', 12)
    document.add_page()
    TEMPLATE = '''
    Report generated at {now}
    Covering data from {start_time} to {end_time}


    Summary
    -------
    TOTAL INCOME: $ {income}
    TOTAL UNIT: {units} units
    AVERAGE DISCOUNT: {discount}%
    '''

    def format_full_tmp(timestamp):
        return timestamp.datetime.isoformat()

    def format_brief_tmp(timestamp):
        return timestamp.datetime.strftime('%d %b')

    text = TEMPLATE.format(now=format_full_tmp(delorean.utcnow()),
                           start_time=format_brief_tmp(summary['start_time']),
                           end_time=format_brief_tmp(summary['end_time']),
                           income=summary['total_income'],
                           units=summary['units'],
                           discount=summary['average_discount'])

    document.multi_cell(0, 6, text)
    document.ln()
    document.output(temp_file)
    return temp_file


def main(input_file, output_file):
    xlsfile = openpyxl.load_workbook(input_file)
    sheet = xlsfile['Sheet']

    def row_to_dict(header, row):
        return {header: cell.value for cell, header in zip(row, header)}

    # islice skips the first row, the header
    data = [SaleLog.from_row([cell.value for cell in row])
            for row in islice(sheet, 1, None)]

    # Generate a full summary, by day, and by shop
    total_summary = generate_summary(data)
    products = total_summary['by_product'].keys()
    summary_by_day = aggregate_by_day(data)
    summary_by_shop = aggregate_by_shop(data)

    # Compose the PDF with a brief summary and all the graphs
    summary_file = create_summary_brief(total_summary, 'summary.pdf')
    by_day_file = graph(summary_by_day, products, 'by_day.pdf', 7)
    by_shop_file = graph(summary_by_shop, products, 'by_shop.pdf')

    # Group all the pdfs into a single file
    pdfs = [summary_file, by_day_file, by_shop_file]
    pdf_files = [open(filename, 'rb') for filename in pdfs]
    output_pdf = PyPDF2.PdfFileWriter()
    for pdf in pdf_files:
        reader = PyPDF2.PdfFileReader(pdf)
        output_pdf.appendPagesFromReader(reader)

    # Write the resulting PDF
    with open(output_file, "wb") as out_file:
        output_pdf.write(out_file)

    # Close the files
    for pdf in pdf_files:
        pdf.close()

    # clean the temp files
    for pdf_filename in pdfs:
        os.remove(pdf_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(type=str, dest='input_file')
    parser.add_argument(type=str, dest='output_file')
    args = parser.parse_args()
    main(args.input_file, args.output_file)
