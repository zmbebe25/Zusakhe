import re

def jprerequisite(example):

    expression = r"[A-Z]+\d{1}|[A-Z]+\d{2}[A-Z]+\d{1}"
    matches = re.search(expression, example)

    if matches:
        text1 = example.splitlines()
        for e in range(len(text1)):
            line_text = example[e]
            if "or" in line_text:
                modules = []
                text = line_text.split("or")
                for i in range(len(text)):
                    module = {"Course": text[i]}

                    if "and" in module["Course"]:
                        new_module = []
                        new_text = text[i].split("and")
                        for j in range(len(new_text)):
                            module1 = {"Course": new_text[j]}
                            new_module.append(module1)
                            module = {"$and": new_module}

                    elif "," in module["Course"]:
                        new_module = []
                        new_text = text[i].split(",")
                        for j in range(len(new_text)):
                            module1 = {"Course": new_text[j]}
                            new_module.append(module1)
                            module = {"$and": new_module}

                    modules.append(module)
                MODULES = [{"$or": modules}]
                value = MODULES
                current_course_data[key] = value


            elif "and" in line_text:
                modules = []
                text = line_text.split("and")
                for i in range(len(text)):
                    module = {"Course": text[i]}

                    if "or" in module["Course"]:
                        new_module = []
                        new_text = text[i].split("or")
                        for j in range(len(new_text)):
                            module1 = {"Course": new_text[j]}
                            new_module.append(module1)
                            module = {"$or": new_module}

                    elif "," in module["Course"]:
                        new_module = []
                        new_text = text[i].split(",")
                        for j in range(len(new_text)):
                            module1 = {"Course": new_text[j]}
                            new_module.append(module1)
                            module = new_module

                    modules.append(module)
                MODULES = [{"$and": modules}]
                value = MODULES
                current_course_data[key] = value


            elif "," in line_text:
                modules = []
                text = line_text.split(',')
                for i in range(len(text)):
                    module = {"Course": text[i]}
                    modules.append(module)
                MODULES = [modules]
                value = MODULES
                current_course_data[key] = value


            else:
                value = [{"Course": example}]
                current_course_data[key] = value

    else:
        txt = ''
        text = example.splitlines()
        for i in range(len(text)):
            txt += text[i]
        value = [{"Comment": txt}]
        current_course_data[key] = value


example1 = "ABC1002 and PRE9013 and MED4505; Only for Bsc(Medical Science)"
example2 = "ABC9420, MED9313, SMO4141, PRY6791"
example3 = """
                BOK 280, GNK 288, BOK 284, GPS 280, GNK 283, GNK 286, (BOK 281 or (BOK 285,
                BOK 287)), LCP 280
           """
example4 = "ABC9420, MED9313, SMO4141, PRY6791 and MEE5555"
example5 = "BDO 121, BDO 214 GS, BDO 224 GS (Except for Business Management students)"
example6 = "ABC9420 or MED9313, SMO4141, PRY6791 and MEE5555"
example7 = ""
example8 = ""
example9 = ""
example10 = ""


print(jprerequisite(example6))