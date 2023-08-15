import PyPDF2
import tkinter as tk
from tkinter import filedialog
from transformers import pipeline

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text_list = [page.extract_text() for page in reader.pages]
        text = ''.join(text_list)
        return text

def perform_ner(text):
    ner_pipeline = pipeline("ner")
    entities = ner_pipeline(text)
    return entities

def browse_files():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        ner_results = []
        for file_path in file_paths:
            text = extract_text_from_pdf(file_path)
            ner_results.extend(perform_ner(text))
        text_box.delete('1.0', tk.END)
        for entity in ner_results:
            text_box.insert(tk.END, f"{entity['entity']}: {entity['word']}\n")

def on_click(event):
    browse_files()

root = tk.Tk()
root.title("PDF Reader")

browse_button = tk.Button(root, text="Browse")
browse_button.bind("<Button-1>", on_click)
browse_button.pack()

text_box = tk.Text(root, height=20, width=50)
text_box.pack()

root.mainloop()