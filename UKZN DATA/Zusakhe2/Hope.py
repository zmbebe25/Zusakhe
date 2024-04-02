import re
import json

def convert_to_json(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define keywords to extract
    keywords = ["Module Name", "Module Code", "Corequisite", "Prerequisite Requirement", "Prerequisite Modules", "Aim", "Content", "Assessment"]

    # Split content into paragraphs
    paragraphs = re.split(r'\n\s*\n', content)

    # Process each paragraph
    modules = []
    for paragraph in paragraphs:
        module_info = {}
        current_keyword = None

        lines = paragraph.split('\n')
        for line in lines:
            for keyword in keywords:
                pattern = re.compile(rf'{keyword}:\s*(.*?)(?=\n|$)', re.DOTALL)
                match = pattern.match(line)
                if match:
                    if keyword == "Module Code":
                        module_info[keyword] = match.group(1).split()[0]  # Extract only the module code
                    else:
                        module_info[keyword] = match.group(1).strip()
                    current_keyword = keyword
                    break
            else:
                # If no keyword is found, append to the current keyword's value
                if current_keyword:
                    module_info[current_keyword] += f' {line.strip()}'

        # If a new paragraph starts, save the current module and reset variables
        if not paragraph.isspace() and module_info:
            modules.append(module_info)

    # Write the result to a JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(modules, json_file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    input_path = "ukzn/Zusakhe2/CollegeofAgricultureandEngineering Science.txt"
    output_path = "ukzn/Zusakhe2/CollegeofAgricultureandEngineering Science.json"
    convert_to_json(input_path, output_path)
    print(f"Conversion complete. Result saved to {output_path}")
