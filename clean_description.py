import json
import re

path = 'C:\\Users\\Bheki Lushaba\\course-data\\uj\\descreptions25\\CBE.json'

with open(path, 'r') as file1:
    data = json.load(file1)

    for item in data:
        pattern = r'(\s*CBE(.+))'
        if 'Description' in item:
            item['Description'] = re.sub(pattern, r'', item['Description'])

with open(path, 'w') as file2:
    json.dump(data, file2, indent=2)