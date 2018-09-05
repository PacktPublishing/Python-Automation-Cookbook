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
    result = requests.get('http://httpbin.org/post', json=data)
    if result.status_code != 200:
        raise Exception('Error accessing server')
    # Obtain a raw name
    raw_result = result.json()['data']
    # Extract the name from the result
    full_name = parse.search('"custname": "{name}"', raw_result)['name']
    # Split it into first name and last name
    first_name, last_name = full_name.split()
    ready_name = f'{last_name}, {first_name}'
    # Add the name in last_name, first_name format to the list
    sorted_names.append(ready_name)

# Properly sort the list and display the result
sorted_names.sort()
print(sorted_names)
