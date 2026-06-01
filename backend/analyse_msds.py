#again to test the chatbot and improve performance by extracting product names from the MSDS documents. This can help in generating more specific questions and answers related to the products mentioned in the MSDS.
import os
import re
from pypdf import PdfReader

DOCS_PATH = r"C:\Users\arkob\Downloads\intern\MRC\docs"

products = []

PATTERNS = [
    r"Product Name\s*(.*?)\s*Product Code",
    r"Product Name\s*(.*?)\s*Recommended Use",
    r"Product Name:\s*(.*?)\s*Product Description",
    r"PRODUCT NAME:\s*(.*?)\s*(?:Product Description|PRODUCT DESCRIPTION)",
    r"Product:\s*(.*?)\s*Product Use",
    r"Product:\s*([^\n\r]+)"
]

for filename in os.listdir(DOCS_PATH):

    if not filename.endswith(".pdf"):
        continue

    filepath = os.path.join(DOCS_PATH, filename)

    try:
        reader = PdfReader(filepath)

        first_page = reader.pages[0].extract_text() or ""

        found = False

        for pattern in PATTERNS:
            match = re.search(pattern, first_page, re.IGNORECASE | re.DOTALL)

            if match:
                product = match.group(1).strip()
                products.append((product, filename))
                found = True
                break

        if not found:
            products.append(("NOT FOUND", filename))

    except Exception as e:
        products.append((f"ERROR: {e}", filename))

for product, filename in products:
    print(f"{product} --> {filename}")