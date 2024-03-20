import json

path = 'C:\\Users\\Bheki Lushaba\\course-data\\uj\\descreptions25\\fada.json'

with open(path, 'r') as file1:
    data = json.load(file1)

    for item in data:
         if 'Course' in item:
            item['Course'] = item['Course'].title()


with open(path, 'w') as file2:
    json.dump(data, file2, indent=2)