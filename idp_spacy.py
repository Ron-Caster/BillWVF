import PyPDF2
import spacy

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text_list = [page.extract_text() for page in reader.pages]
        text = ''.join(text_list)
        return text

def perform_ner(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = [(ent.label_, ent.text) for ent in doc.ents]
    return entities

def browse_files():
    file_paths = input("Enter the file paths (separated by commas): ").split(",")
    if file_paths:
        ner_results = []
        for file_path in file_paths:
            text = extract_text_from_pdf(file_path.strip())
            ner_results.extend(perform_ner(text))
        for entity in ner_results:
            print(f"{entity[0]}: {entity[1]}")

browse_files()