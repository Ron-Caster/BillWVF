import tkinter as tk
from tkinter import ttk, filedialog
import spacy

class PDFExtractorGUI:
    def __init__(self, master):
        self.master = master
        master.title("PDF Extractor")

        self.file_path = ""

        self.file_label = ttk.Label(master, text="No file selected.")
        self.file_label.grid(row=0, column=0, padx=10, pady=10)

        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

        self.extraction_tool_label = ttk.Label(master, text="Select Extraction Tool:")
        self.extraction_tool_label.grid(row=1, column=0, padx=10, pady=10)

        self.extraction_tool_var = tk.StringVar()
        self.extraction_tool_options = ["PDFMiner", "PyMuPDF", "PyPDF4"]
        self.extraction_tool_dropdown = ttk.OptionMenu(master, self.extraction_tool_var, self.extraction_tool_options[0], *self.extraction_tool_options)
        self.extraction_tool_dropdown.grid(row=1, column=1, padx=10, pady=10)

        self.transformer_label = ttk.Label(master, text="Select Transformer:")
        self.transformer_label.grid(row=2, column=0, padx=10, pady=10)

        self.transformer_var = tk.StringVar()
        self.transformer_options = ["SpaCy"]
        self.transformer_dropdown = ttk.OptionMenu(master, self.transformer_var, self.transformer_options[0], *self.transformer_options)
        self.transformer_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.extract_button = ttk.Button(master, text="Extract Text", command=self.extract_text)
        self.extract_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.text_box = tk.Text(master, height=20, width=100)
        self.text_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.processed_text_box = tk.Text(master, height=10, width=100)
        self.processed_text_box.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_label.config(text=self.file_path)

    def extract_text(self):
        extraction_tool = self.extraction_tool_var.get()

        if extraction_tool == "PDFMiner":
            text = self.extract_text_with_pdfminer()
        elif extraction_tool == "PyMuPDF":
            text = self.extract_text_with_pymupdf()
        elif extraction_tool == "PyPDF4":
            text = self.extract_text_with_pypdf4()
        else:
            text = "Invalid Extraction Tool selected."

        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, text)

        transformer = self.transformer_var.get()

        if transformer == "SpaCy":
            processed_text = self.process_text_with_spacy(text)
        else:
            processed_text = "Invalid Transformer selected."

        self.processed_text_box.delete('1.0', tk.END)
        self.processed_text_box.insert(tk.END, processed_text)

    def extract_text_with_pdfminer(self):
        import pdfminer.high_level
        with open(self.file_path, 'rb') as file:
            text = pdfminer.high_level.extract_text(file, page_numbers=None, maxpages=0, password=None)
            return text

    def extract_text_with_pymupdf(self):
        import fitz
        with fitz.open(self.file_path) as doc:
            text_list = [page.get_text() for page in doc]
            text = ''.join(text_list)
            return text

    def extract_text_with_pypdf4(self):
        import PyPDF4
        with open(self.file_path, 'rb') as file:
            reader = PyPDF4.PdfFileReader(file)
            text_list = [page.extractText() for page in reader.pages]
            text = ''.join(text_list)
            return text

    def process_text_with_spacy(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        entities = [(ent.label_, ent.text) for ent in doc.ents]
        processed_text = ""
        for entity in entities:
            processed_text += f"{entity[0]}: {entity[1]}\n"
        return processed_text

root = tk.Tk()
pdf_extractor = PDFExtractorGUI(root)
root.mainloop()