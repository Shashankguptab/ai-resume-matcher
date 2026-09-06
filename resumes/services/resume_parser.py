from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    reader=PdfReader(file_path)  #opeans the pdf

    text=""

    for page in reader.pages:  #may contain multiple pages so we loop though every page
        page_text=page.extract_text()  #extracts readable text from the page

        if page_text:
            text+=page_text + "\n"  #we combine all the page text into one large string
    return text