
text = "My name is\nBheki And my surname is\nLushaba"
txt = ''
new_text = text.splitlines()
for i in range(len(new_text)):
    txt += f"{new_text[i]} "

print(txt)