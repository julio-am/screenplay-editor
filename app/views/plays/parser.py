import xml.etree.ElementTree as ET

def stageDir(content, target):
    xmlstr = ET.tostring(content, encoding='utf8', method='text')
    target.write("\n<br>\nStage Directions %s" % filter(lambda x: x != "\n", xmlstr).replace("  ", ""))

def speaker(content, target):
    xmlstr = ET.tostring(content, encoding='utf8', method='text')
    target.write("\n<br>\nSpeaker ")
    target.write(filter(lambda x: x != "\n", xmlstr).replace("  ", ""))

def getLines(content, target):
    line = ""
    for words in content.findall("./*"):
        if ((words.tag == "{http://www.tei-c.org/ns/1.0}milestone") and (words.get('unit') != "page")):
            target.write(filter(lambda x: x != "\n", line).replace("  ", ""))
            target.write("\n<br>\n%s " % words.get('n'))
            line = ""
        elif (words.tag != "{http://www.tei-c.org/ns/1.0}fw"):
            line += ET.tostring(words, encoding='utf8', method='text')
    target.write(filter(lambda x: x != "\n", line).replace("  ", ""))


def printOneScene(scene, target):
    for content in scene.iter():
        if (content.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            stageDir(content, target)
        elif (content.tag == "{http://www.tei-c.org/ns/1.0}speaker"):
            speaker(content, target)
        elif(content.tag == "{http://www.tei-c.org/ns/1.0}ab"):
            getLines(content, target)  

header = open("header.html", "r")
lines = header.readlines()
target = open("index.html.erb", "w")
target.truncate()
for line in lines:
    target.write(line)
tree = ET.parse("data.xml").getroot()
ET.register_namespace("{http://www.tei-c.org/ns/1.0}", "http://www.tei-c.org/ns/1.0")
acts = tree.findall(".//{http://www.tei-c.org/ns/1.0}div1")
for act in acts:
    target.write("\n<h1>\nAct %s\n</h1>" % act.get('n'))
    for scene in act.findall(".//{http://www.tei-c.org/ns/1.0}div2"):
        target.write("\n<h2>\nScene %s\n</h2>" % act.get('n'))
        printOneScene(scene, target)
target.write("</body>\n</html>")
target.close()

