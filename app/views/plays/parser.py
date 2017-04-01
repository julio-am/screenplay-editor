import xml.etree.ElementTree as ET

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
				xmlstr = ET.tostring(content, encoding='utf8', method='text')
				print "Stage Directions", filter(lambda x: x != "\n", xmlstr)
			elif (content.tag == "{http://www.tei-c.org/ns/1.0}speaker"):

				xmlstr = ET.tostring(content, encoding='utf8', method='text')
				print "Speaker", filter(lambda x: x != "\n", xmlstr)
			elif(content.tag == "{http://www.tei-c.org/ns/1.0}ab"):
				
				xmlstr = ET.tostring(content, encoding='utf8', method='text')
				print "Line", filter(lambda x: x != "\n", xmlstr)




			
			