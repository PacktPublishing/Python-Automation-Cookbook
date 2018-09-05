import requests
import parse

NAMES = [
    'John Smyth',
    'Michael Craig',
    'Poppy-Mae Pate',
    'Vivienne Rennie',
    'Fathima Mccabe',
    'Mai Cordova',
    'Rocío García',
    'Roman Sullivan',
    'John Paul Smith',
    "Séamus O'Carroll",
    'Keagan Berg',
]

sorted_names = []
for name in NAMES:
    data = {
        'custname': name,
    }
    # Request the name from the server
    # ERROR step 2. Using .get when it should be .post
    # (old) result = requests.get('http://httpbin.org/post', json=data)
    result = requests.post('http://httpbin.org/post', json=data)
    if result.status_code != 200:
        raise Exception(f'Error accessing server: {result}')
    # Obtain a raw name
    # ERROR Step 11. Obtain the value from a raw value. Use
    # the decoded JSON instead
    # raw_result = result.json()['data']
    # Extract the name from the result
    # full_name = parse.search('"custname": "{name}"', raw_result)['name']
    raw_result = result.json()['json']
    full_name = raw_result['custname']
    # Split it into first name and last name
    # ERROR step 6. split only two words. Some names has middle names
    # (old) first_name, last_name = full_name.split()
    first_name, last_name = full_name.rsplit(maxsplit=1)
    ready_name = f'{last_name}, {first_name}'
    # Add the name in last_name, first_name format to the list
    sorted_names.append(ready_name)

# Properly sort the list and display the result
sorted_names.sort()
print(sorted_names)
