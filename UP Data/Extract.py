import pdfplumber

pdf_path = "C:/Users/Zusakhe Mbebe/Downloads/Faculty-VET.pdf"
output_path = 'C:/Users/Zusakhe Mbebe/Downloads/Zusakhe/UP Data/Faculty-VET.txt'

def extract_text_from_pdf(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

extract_text_from_pdf(pdf_path, output_path)
