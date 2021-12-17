import chemdataextractor as cde
from chemdataextractor import reader
from definitions import XML_FILES, HTML_FILES, PDF_FILES

def read_xml(xml_file: str) -> cde.Document:
    with open(XML_FILES + xml_file, "rb") as file:
        document = cde.Document.from_file(file, readers=[reader.XmlReader()])
    return document

def read_html(html_file: str) -> cde.Document:
    with open(HTML_FILES + html_file, "rb") as file:
        document = cde.Document.from_file(file, readers=[reader.AcsHtmlReader()])
    return document

def read_pdf(pdf_file: str) -> cde.Document:
    with open(PDF_FILES + pdf_file, "rb") as file:
        document = cde.Document.from_file(file)
    return document

if __name__ == "__main__":
    doc = read_html("test.html")

