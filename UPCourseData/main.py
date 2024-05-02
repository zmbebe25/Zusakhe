import re
import json
from period import period_format
from duration import duration_format

with open("Law.txt", 'r', encoding="utf-8") as file:
    text = file.read()
    #print(text)
    #For the code of the module
    expression1 = r'\(([A-Z]+\s\d{3})\)'
    match_code = re.findall(expression1, text)
    code = [matches.replace(' ','') for matches in match_code]

    #For the name of the module
    expression2 = r'((.)+)\s\([A-Z]+\s\d{3}\)'
    match_name = re.findall(expression2, text)

    #For the credits of the module
    expression3 = r'Module credits ([0-9]+\.[0-9]+)'
    match_credits = re.findall(expression3, text)

    #For the nqf of the module
    expression4 = 'NQF Level ([0-9]+)'
    match_nqf = re.findall(expression4, text)

    #For undergrad or postgrad
    expression5 = r'Qualification ([A-z]+)'
    match_grad = re.findall(expression5, text)

    #For the description of the module
    expression6 = r'(?<=Module content)(.*?)(?=\ Qualification\b|$)'
    match_content = re.findall(expression6, text)

    #For the duration of the module
    expression7 = 'Period of presentation ((.)+)'
    match_duration = re.findall(expression7, text)

    #For the prerequisites of the module
    expression8 = re.compile(r'Prerequisites ((.)+)', re.DOTALL) # Make the regex pick from above header
    match_prerequisite = re.findall(expression8, text)

    #For the description of the module
    expression9 = 'Module content(\n(.*?)+)\n(.)+\n(.)+'
    match_description = re.findall(expression9, text)

MODULE = []
with open('UP_Law.json', 'w', encoding="utf-8") as f2:
    for i in range(128):
        module = {"University": "University of Pretoria","Code": code[i],"Course": match_name[i][0],"Description": match_description[i][0]+1,"Credits": match_credits[i],"NQF": match_nqf[i],"Qualification": match_grad[i],"Duration": match_duration[i][0]}
        MODULE.append(module)
    MODULE2 = [mymodule for mymodule in MODULE if mymodule['Qualification'] == 'Undergraduate']
    json.dump(MODULE2, f2, indent=4)
print("Saved to 'UP_Law.json'")
