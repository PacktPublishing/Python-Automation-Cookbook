import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def bubble_sort(alist):
    logging.info(f'Sorting the list: {alist}')
    for passnum in reversed(range(len(alist) - 1)):
        for i in range(passnum):
            if alist[i] > alist[i + 1]:
                alist[i], alist[i + 1] = alist[i + 1], alist[i]
            logging.debug(f'alist: {alist}')

    logging.info(f'Sorted list     : {alist}')
    return alist


assert [1, 2, 3, 4, 7, 10] == bubble_sort([3, 7, 10, 2, 4, 1])
