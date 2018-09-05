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
    result = requests.post('http://httpbin.org/post', json=data)
    if result.status_code != 200:
        raise Exception('Error accessing server')
    raw_result = result.json()['data']
    full_name = parse.search('"custname": "{name}"', raw_result)['name']
    first_name, last_name = full_name.split()
    ready_name = f'{last_name}, {first_name}'
    sorted_names.append(ready_name)

sorted_names.sort()
print(sorted_names)
