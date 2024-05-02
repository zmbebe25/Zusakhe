import re

text = """
Strategic leadership and management 302 (GAD 302)
Qualification Undergraduate
Module credits 11.00
NQF Level 07
Programmes AdvDip in General Management
AdvDip in General Management

Prerequisites No prerequisites.
Contact time 14 contact hours
Language of tuition Module is presented in English
Department Gordon Institute of Business Science
Period of presentation Semester 1 and Semester 2
Module content
Senior managers have unique leadership challenges. As the custodians of strategy, the pioneers who deal with
environmental and organisational complexities, and the visionaries who look to the future and drive
organisational vision all eyes are on them to take the organisation and its people into a brighter future. They
also need to consider the long-term wellbeing of the organisation, gearing it for sustainable success in the world
of tomorrow.
Business strategy 303 (GAD 303)
Qualification Undergraduate
Module credits 11.00
NQF Level 07
Programmes AdvDip in General Management
AdvDip in General Management

Prerequisites No prerequisites.
Contact time 14 contact hours
Language of tuition Module is presented in English
Department Gordon Institute of Business Science
Period of presentation Semester 1 or Semester 2
Module content
Strategic management is the art and science of formulating, implementing and evaluating cross-functional
decisions that will enable the student to achieve its objectives. It involves the strategic thinking, systematic
analysis of factor affecting the organisation, identification and clarification of objectives, nurturing policies and
strategies to achieve these objectives, and acquiring and making available resources to implement the policies
and strategies to achieve objectives.

Another module with similar format...

"""

# Use a regular expression to match the "Prerequisites" section
prerequisites_pattern = re.compile(r'Prerequisites (.+?)\.', re.DOTALL)

# Find all matches in the text
matches = prerequisites_pattern.findall(text)

# Extracted prerequisites
prerequisites_list = [match.strip() for match in matches]

# Print the extracted prerequisites
for prerequisites in prerequisites_list:
    print(prerequisites)