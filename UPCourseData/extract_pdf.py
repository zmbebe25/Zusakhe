import PyPDF2


def extract_text():
    handbook_path = "C:\\Users\\Bheki Lushaba\\Desktop\\HandBooks\\Faculty-LAW-Full.pdf"  # Change to the path of the handbook
    with open(handbook_path, 'rb') as f1:
        text = PyPDF2.PdfReader(f1)
        text_pdf = ''

        for page in range(222, 350):  # Start of modules and end of modules
            txt = text.pages[page]
            text_pdf += txt.extract_text()

            string_to_remove = "University"
            string2_to_remove = "357"  # Change number to the last page of the PDF
            new_text = text_pdf.replace(string_to_remove, '\n\n\n\n\n')
            clean_text = new_text.replace(string2_to_remove, '\n\n\n\n\n')

        with open("Law.txt", 'w', encoding="utf-8") as file:
            file.write(clean_text)

    print("Extracted!!")

extract_text()