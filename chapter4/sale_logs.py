from datetime import datetime

SALE_LOG = '[{date}] - SALE - PRODUCT: {product} - PRICE: ${price:05.2f}'
'- NAME: {name} - DISCOUNT: {discount}%'


class SaleLog(object):

    def __init__(self, date, product_id, price, product_name, discount=None):
        self.date = date
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.discount = discount

    def print(self):
        log = SALE_LOG.format(date=self.date,
                              product=self.product_id,
                              price=self.price,
                              name=self.product_name,
                              discount=self.discount)
        print(log)


if __name__ == '__main__':
    log = SaleLog(datetime.now().isoformat(), 1345, 9.99, 'Family pack', 0)
    log.print()
