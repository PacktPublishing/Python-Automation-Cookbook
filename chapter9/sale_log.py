import parse
from decimal import Decimal
import delorean


class SaleLog(object):

    def __init__(self, timestamp, product_id, price, name, discount,
                 shop=None):
        self.timestamp = timestamp
        self.product_id = product_id
        self.price = price
        self.name = name
        self.discount = discount
        self.shop = shop

    def __repr__(self):
        return '<SaleLog ({}, {}, {})>'.format(self.timestamp,
                                               self.product_id,
                                               self.price)

    @classmethod
    def row_header(cls):
        HEADER = ('Timestamp', 'Shop', 'Product Id', 'Name', 'Price',
                  'Discount')
        return HEADER

    def row(self):
        return (self.timestamp.datetime.isoformat(), self.shop,
                self.product_id, self.name, self.price,
                '{}%'.format(self.discount))

    @classmethod
    def from_row(cls, row):
        timestamp_str, shop, product_id, name, raw_price, discount_str = row
        timestamp = delorean.parse(timestamp_str)
        discount = parse.parse('{:d}%', discount_str)[0]
        # Round to remove possible rounding errors in Excel
        price = round(Decimal(raw_price), 2)

        return cls(timestamp=timestamp, product_id=product_id,
                   price=price, name=name, discount=discount,
                   shop=shop)

    @classmethod
    def parse(cls, shop, text_log):
        '''
        Parse from a text log with the format
        [<Timestamp>] - SALE - PRODUCT: <product id> - PRICE: $<price> - NAME: <name> - DISCOUNT: <discount>%
        to a SaleLog object
        '''
        def price(string):
            return Decimal(string)

        def isodate(string):
            return delorean.parse(string)

        FORMAT = ('[{timestamp:isodate}] - SALE - PRODUCT: {product:d} '
                  '- PRICE: ${price:price} - NAME: {name:D} '
                  '- DISCOUNT: {discount:d}%')

        formats = {'price': price, 'isodate': isodate}
        result = parse.parse(FORMAT, text_log, formats)

        return cls(timestamp=result['timestamp'],
                   product_id=result['product'],
                   price=result['price'],
                   name=result['name'],
                   discount=result['discount'],
                   shop=shop)
