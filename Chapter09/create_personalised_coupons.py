# IMPORTS
import hashlib
import re
import csv
from random import choice

CHARACTERS = 'ACEFGHJKLMNPRTUVWXY379'


# FUNCTIONS
def random_code(digits):
    # All possibilities, except the letters and numbers that can
    # be confusing ( 0 and O, etc )
    digits = [choice(CHARACTERS) for _ in range(digits)]
    return ''.join(digits)


def checksum(code1, code2):
    m = hashlib.sha256()
    m.update(code1.encode())
    m.update(code2.encode())
    checksum = int(m.hexdigest()[:2], base=16)
    digit = CHARACTERS[checksum % len(CHARACTERS)]
    return digit


def check_code(code):
    # Divide the code in its parts
    CODE = r'(\w{4})-(\w{5})-(\w)(\w)$'
    match = re.match(CODE, code)
    if not match:
        return False

    # Check the checksum
    code1, code2, check1, check2 = match.groups()
    expected_check1 = checksum(code1, code2)
    expected_check2 = checksum(code2, code1)

    if expected_check1 == check1 and expected_check2 == check2:
        return True

    return False


def generate_code():
    code1 = random_code(4)
    code2 = random_code(5)
    check1 = checksum(code1, code2)
    check2 = checksum(code2, code1)

    return f'{code1}-{code2}-{check1}{check2}'


# SET UP TASK
BATCHES = 500_000, 300_000, 200_000
TOTAL_NUM_CODES = sum(BATCHES)
NUM_TRIES = 3


# GENERATE CODES

codes = set()
for _ in range(TOTAL_NUM_CODES):
    code = generate_code()
    for _ in range(NUM_TRIES):
        code = generate_code()
        if code not in codes:
            break

    else:
        raise Exception('Run out of tries generating a code')

    codes.add(code)

    assert check_code(code)
    print(f'Code: {code}')


# CREATE AND SAVE BATCHES
for index, batch_size in enumerate(BATCHES, 1):
    batch = [(codes.pop(),) for _ in range(batch_size)]
    filename = f'codes_batch_{index}.csv'
    with open(filename, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerows(batch)

assert 0 == len(codes)
