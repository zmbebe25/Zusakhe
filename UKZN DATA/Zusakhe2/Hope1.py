import json

input_json = [
    {
        "Module Name": "Agribusiness Research Project & Seminar",
        "Module Code": "AGBU791",
        "Corequisite": "AGEC740 and (ANSI711 or AGPS791 or (BIOL722 and BIOL723)).",
        "Aim": "To equip students with the ability to: (a) critically review literature, write scientific papers, and formally present and defend their work, and (b) integrate theory and techniques covered in earlier modules.",
        "Content": "This module integrates topics covered in earlier modules. For the project, students must identify a relevant research problem, develop models to test hypotheses, collect and analyse data, interpret results, recommend how to solve the problem, and prepare a comprehensive research report.",
        "Assessment": "Presentation of 1 paper (33%), research report (67%)."
    },
    {
        "Module Name": "Introduction to Agricultural Economics",
        "Module Code": "AGEC210",
        "Aim": "(a) To understand the key economic principles of production, market demand and supply and how these principles can assist farm decision-makers in making improved decisions, and (b) to learn key accounting principles to develop a sound farm record-keeping system.",
        "Content": "Market demand for agricultural products. Market supply of agricultural products. Price movements. The firm (farm) as a decision-making unit. Production functions of the farm business. Determining the optimum level of production. Farm costs of production. Agricultural input substitution. Decisions on the choice of agricultural products. Practicals: Elementary farm accounting.",
        "Assessment": "2 class tests (33%); 3 h exam (67%)."
    }
]

def convert_assessment_format(assessment_str):
    assessments = []
    
    for part in assessment_str.split(';'):
        if '"' in part:
            name = part.split('"')[1].strip()
        elif ':' in part:
            name = part.split(':')[1].split(';')[0].strip()
        else:
            continue
        
        type = part.split()[-2].capitalize()
        weight = part.split()[-1].strip(')').strip('%')
        assessments.append({"Name": name, "Type": type, "Weight": f"{weight}%"})

    return assessments

def convert_module_format(module):
    module["Assessment"] = convert_assessment_format(module["Assessment"])
    return module

converted_modules = [convert_module_format(module) for module in input_json]

# Print the converted JSON
print(json.dumps(converted_modules, indent=2))
