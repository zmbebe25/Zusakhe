# Assuming 'data' is a list of lines read from a text file where each module's name appears right before the line that starts with 'Module credits'.

modules = []
with open('UP Data/Faculty-VET.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()

for i in range(1, len(data)):  # Start from 1 since we look back at i-1
    line = data[i].strip()
    if line.startswith('Qualification Undergraduate'):
        name = data[i-1].strip()  # Get the name from the previous line
        modules.append(name)

with open('UP Data/Faculty-VET.txt', 'w', encoding='utf-8') as file:
    for module in modules:
        file.write(module + '\n')

print(modules)
