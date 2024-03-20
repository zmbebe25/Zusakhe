import json

def compare_and_add(jfile1, jfile2, output_file):
    with open(jfile1, 'r', encoding='utf-8') as file1, open(jfile2, 'r', encoding='utf-8') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    for item2 in data2:
        for item1 in data1:
            if 'Code' in item2 and 'Code' in item1:
                if len(item1['Code']) >= 1:
                    for i in range(len(item1['Code'])):
                        if item1['Code'][i] == item2['Code']:
                            item2['Description'] = item1.get('Description', "")
            


    with open(output_file, 'w', encoding='utf-8') as jfile:
        json.dump(data2, jfile, indent=2)

descriptions = 'C:\\Users\\Bheki Lushaba\\course-data\\tut\\descriptions24\\faculty+descriptions\\management.json'
module_data = 'C:\\Users\\Bheki Lushaba\\course-data\\tut\\descriptions24\\management.json'
combined = 'C:\\Users\\Bheki Lushaba\\course-data\\tut\\descriptions24\\management.json'
compare_and_add(descriptions, module_data, combined)
