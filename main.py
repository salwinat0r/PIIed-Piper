from anonympy.pdf import pdfAnonymizer

def data_anonymizer(file):
    anonym = pdfAnonymizer(path_to_pdf = file,
                        pytesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                        poppler_path = r"C:\Users\salwy\Downloads\poppler-0.68.0_x86 (1)\poppler-0.68.0\bin")

    anonym.anonymize(output_path = 'output.pdf',
                        remove_metadata = True,
                        fill = 'black',
                        outline = 'black')