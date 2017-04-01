import xml.etree.ElementTree as ET

#def turnFileIntoText(file):
tree = ET.parse("data.xml").getroot()
print tree.find('.//body')