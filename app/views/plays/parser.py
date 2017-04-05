import xml.etree.ElementTree as ET

def stageDir(content, targetFile):
    xmlstr = filter(lambda x: x != "\n", ET.tostring(content, encoding='utf8', method='text')).replace("  ", "")
    if xmlstr[0] != ',':
        targetFile.write("\n<br>\n")
    targetFile.write("<i>%s</i>" % xmlstr)

def speaker(content, targetFile):
    parents = content.findall("..")
    for parent in parents:
        if(parent.tag != "ab"):
            xmlstr = ET.tostring(content, encoding='utf8', method='text')
            targetFile.write("\n<br>\n<b>%s</b> "% filter(lambda x: x != "\n", xmlstr).replace("  ", ""))
            return

def getLines(content, targetFile):
    line = ""
    for words in content.findall("./*"):
        if ((words.tag == "{http://www.tei-c.org/ns/1.0}milestone") and (words.get('unit') == "ftln")):
            targetFile.write(filter(lambda x: x != "\n", line).replace("  ", ""))
            targetFile.write('\n<br>\n<span class="lineNum">%s</span>' % words.get('n'))
            line = ""
        elif (words.tag[0:3] == "stg"):
            stageDir(words, targetFile)
        elif(words.tag == "{http://www.tei-c.org/ns/1.0}seg"):
            getLines(words, targetFile)
        elif (words.tag != "{http://www.tei-c.org/ns/1.0}fw"):
            line += ET.tostring(words, encoding='utf8', method='text')
    targetFile.write(filter(lambda x: x != "\n", line).replace("  ", ""))


def printOneScene(scene, targetFile):
    for content in scene.iter():
        if (content.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            stageDir(content, targetFile)
        elif (content.tag == "{http://www.tei-c.org/ns/1.0}speaker"):
            speaker(content, targetFile)
        elif(content.tag == "{http://www.tei-c.org/ns/1.0}ab"):
            getLines(content, targetFile)  

def visitAct(xmlTree, targetFile):
    acts = tree.findall(".//{http://www.tei-c.org/ns/1.0}div1")
    baseIndent = "                  "
    actPattern = baseIndent + '<div class="col-sm-4">\n' + baseIndent+ '  <ul class="multi-column-dropdown">\n'

    for act in acts:
        targetFile.write(actPattern)
        targetFile.write(baseIndent+'    <li><a href="#">Act %s</a></li>\n' % act.get('n'))
        targetFile.write(baseIndent+'    <li class="divider"></li>\n')
        scenes = act.findall(".//{http://www.tei-c.org/ns/1.0}div2")
        for scene in scenes:
            idNumber = act.get('n') + "." + scene.get('n')
            targetFile.write(baseIndent + '    <li><a href="#'+idNumber+'">Scene %s</a></li>\n' % scene.get('n'))
        targetFile.write(baseIndent+'  </ul>\n'+baseIndent+'</div>\n')
        if int(act.get('n')) == 3:
            targetFile.write(baseIndent+"  </div>")


header = open("header.html", "r")
lines = header.readlines()
target = open("index.html.erb", "w")
tree = ET.parse("data.xml").getroot()
for line in lines:
    target.write(line)
    if '<div class="row">' in line:
        visitAct(tree, target)
ET.register_namespace("{http://www.tei-c.org/ns/1.0}", "http://www.tei-c.org/ns/1.0")
acts = tree.findall(".//{http://www.tei-c.org/ns/1.0}div1")
for act in acts:
    target.write("\n<h1>\nAct %s\n</h1>" % act.get('n'))
    scenes = act.findall(".//{http://www.tei-c.org/ns/1.0}div2")
    for scene in scenes:
        idNumber = act.get('n') + "." + scene.get('n')
        target.write("\n<h2 id ="+idNumber+">\nScene %s\n</h2>" % scene.get('n'))
        printOneScene(scene, target)
target.write("</div>\n</body>\n</html>")
target.close()

