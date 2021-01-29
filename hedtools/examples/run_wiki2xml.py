"""Example for how to convert from mediawiki format to xml format"""
from shutil import move
from hed.schema import wiki2xml
from hed.schema import schema_validator

if __name__ == '__main__':
    hed_wiki_url = 'https://raw.githubusercontent.com/hed-standard/hed-specification/master/HED-generation3-schema.mediawiki'
    local_hed_file = None
    xml_location, errors = wiki2xml.convert_hed_wiki_2_xml(hed_wiki_url, local_wiki_file=local_hed_file)
    schema_validator.get_printable_issue_string(validation_issues=errors, title="Errors in HED-generation3-schema.mediawiki")
    if xml_location:
        move(xml_location, "output.xml")