import fitz  # PyMuPDF
import unicodedata
import re

class PDFParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = None

    def load(self):
        """
        Opens the PDF file.
        Why? We keep the file open only as long as needed to save memory.
        """
        try:
            self.doc = fitz.open(self.file_path)
            print(f"✅ Opened PDF: {self.file_path} with {len(self.doc)} pages.")
        except Exception as e:
            print(f"❌ Error opening PDF: {e}")
            raise

    def clean_text(self, text):
        """
        The 'Janitor' function.
        1. Normalizes unicode characters (fixes weird PDF symbols).
        2. Replaces multiple spaces/newlines with a single space.
        Why? Embeddings work best on continuous, natural language flow.
        """
        # Step 1: Fix broken unicode (e.g., turns "ﬁ" into "fi")
        text = unicodedata.normalize('NFKC', text)
        
        # Step 2: Remove headers/footers (naive approach - adjust regex as needed)
        # This removes lines that look like just numbers (Page numbers)
        text = re.sub(r'\n\d+\n', '\n', text)
        
        # Step 3: Collapse whitespace
        # "Hello    world\nHow are you?" -> "Hello world How are you?"
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def extract(self):
        """
        The main worker.
        Iterates pages, extracts text, and cleans it.
        Returns a list of dictionaries (one per page).
        """
        if not self.doc:
            self.load()
        
        pages_content = []
        
        for page_num, page in enumerate(self.doc):
            # extract raw text
            raw_text = page.get_text()
            
            # clean it
            cleaned_text = self.clean_text(raw_text)
            
            # Why store page_num?
            # So the AI can cite its sources later! ("Found on page 5")
            if cleaned_text: # Only save if there is text
                pages_content.append({
                    "page": page_num + 1,
                    "text": cleaned_text,
                    "source": self.file_path
                })
                
        return pages_content

# --- TESTING BLOCK ---
# This allows us to run this file directly to test it without running the whole app.
if __name__ == "__main__":
    # REPLACE THIS with your actual PDF filename
    sample_pdf = r"data\pdfs\sample.pdf" 
    
    # Check if file exists first!
    import os
    if not os.path.exists(sample_pdf):
        print(f"⚠️  Please put a PDF file at: {sample_pdf}")
    else:
        parser = PDFParser(sample_pdf)
        data = parser.extract()
        
        # Print the first 500 characters of the first page to verify
        print("\n--- PREVIEW OF PAGE 1 ---")
        print(data[0]['text'][:500])
        print("...")