import xml.etree.ElementTree as ET

#def turnFileIntoText(file):
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

tree = ET.parse("data.xml").getroot()
ET.register_namespace("{http://www.tei-c.org/ns/1.0}", "http://www.tei-c.org/ns/1.0")
acts = tree.findall(".//{http://www.tei-c.org/ns/1.0}div1")
for act in acts:
	print "Act", act.get('n')
	for scene in act.findall(".//{http://www.tei-c.org/ns/1.0}div2"):
		print "Scene", scene.get('n')
		for content in scene.iter():
			if (content.tag == "{http://www.tei-c.org/ns/1.0}stage"):
				string = ""
				#for word in content.iter():
					#string += str(word.text)
				xmlstr = ET.tostring(content, encoding='utf8', method='text')
				#indent(xmlstr)
				print "Stage Directions", filter(lambda x: x != "\n", xmlstr)
			elif (content.tag == "{http://www.tei-c.org/ns/1.0}speaker"):
				# speakerName = ""
				# line =""
				# for word in content[0].iter():
				# 	speakerName += str(word.text)
				# print "Speaker", speakerName
				# for word in content[1].iter():
				# 	line+= str(word.text)
				# print "Line", line
				xmlstr = ET.tostring(content, encoding='utf8', method='text')
				#indent(xmlstr)
				print "Speaker", filter(lambda x: x != "\n", xmlstr)
			elif(content.tag == "{http://www.tei-c.org/ns/1.0}ab"):
				
				xmlstr = ET.tostring(content, encoding='utf8', method='text')
				#indent(xmlstr)
				print "Line", filter(lambda x: x != "\n", xmlstr)




			
			