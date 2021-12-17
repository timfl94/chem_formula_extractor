from lxml import etree
from definitions import *
import logging
from chemdataextractor.doc import Document, Table, Paragraph, Text, Figure, Heading

NAMESPACE: str = "{http://www.w3.org/XML/1998/namespace}"


def clean_xml(xml_file: str) -> etree.ElementTree:
    with open(XML_FILES + "test.xml", "r") as file:
        xml_doc = file.read()
        xml_tree = etree.fromstring(xml_doc)

    # Remove the namespace url from element name
    for elem in xml_tree.iter():
        try:
            elem.tag = etree.QName(elem).localname
        except ValueError:
            logging.warning(f"Element {elem.tag} has no name.")
    etree.cleanup_namespaces(xml_tree)

    # Remove reference elements
    for elem in xml_tree.xpath("//ref"):
        elem.getparent().remove(elem)

    return xml_tree

def xml_to_cde_doc(xml_tree: etree.ElementTree):
    headings, figures_desc, tables_desc, text_list = [], [], [], []
    for heading in xml_tree.xpath("//head"):
        headings.append(str(heading.text))
    
    for figure in xml_tree.xpath("//figure[contains(@xml:id, 'fig')]"):
        figure_desc = str(figure.find("figDesc").text)
        figures_desc.append(figure_desc)

    for table in xml_tree.xpath("//figure[@type='table']"):
        table_desc = str(table.find("figDesc").text)
        tables_desc.append(table_desc)

    for text in xml_tree.xpath("//p"):
        text_str = str(text.text)
        text_list.append(text_str)

    cde_elements = [Heading(heading) for heading in set(headings)]
    cde_elements.extend([Text(fig) for fig in figures_desc])
    cde_elements.extend([Text(table) for table in tables_desc])
    cde_elements.extend([Text(text) for text in text_list])

    cde_doc = Document(elements=cde_elements)
    return cde_doc


if __name__ == "__main__":
    xml = clean_xml(XML_FILES + "test.xml")
    doc = xml_to_cde_doc(xml)
