import xml.etree.ElementTree as ET

def elemToString(content):
    return ET.tostring(content, encoding='utf8', method='text')

def cleanElemToString(content):
    string = elemToString(content)
    return filter(lambda x: x != "\n", string).replace("  ", "")

def printSingleLine(line, targetFile):
    targetFile.write(filter(lambda x: x != "\n", line).replace("  ", ""))

def outerLvlStageDir(content, targetFile):
    parents = content.findall("..")
    for parent in parents:
        if(parent.tag != "ab"):
            xmlstr = cleanElemToString(content)
            if xmlstr[0] != ',':
                targetFile.write("\n<br>\n")
                targetFile.write("<i>%s</i>" % xmlstr)
                return

def stageDirInLine(content, targetFile):
    xmlstr = cleanElemToString(content)
    if xmlstr[0] != ',':
        targetFile.write("\n<br>\n")
        targetFile.write("<i>%s</i>" % xmlstr)

def speaker(content, targetFile):
        xmlstr = cleanElemToString(content)
        targetFile.write("\n<br>\n<b>%s</b> "% xmlstr)

def getLines(content, targetFile):
    line = ""
    for words in content.findall("./*"):
        if ((words.tag == "{http://www.tei-c.org/ns/1.0}milestone") and (words.get('unit') == "ftln")):
            printSingleLine(line, targetFile)
            targetFile.write('\n<br>\n<span class="lineNum">%s</span>' % words.get('n'))
            line = ""
        elif (words.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            printSingleLine(line, targetFile)
            line = ""
            stageDirInLine(words, targetFile)
        elif(words.tag == "{http://www.tei-c.org/ns/1.0}seg"):
            getLines(words, targetFile)
        elif (words.tag != "{http://www.tei-c.org/ns/1.0}fw"):
            line += ET.tostring(words, encoding='utf8', method='text')
    printSingleLine(line, targetFile)

"""
printOneScene
This will write a single scene as we want it formatted
It takes in a scene and a targetFile.
"""
def writeOneScene(scene, targetFile):
    for content in scene.iter():
        if (content.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            outerLvlStageDir(content, targetFile)
        elif (content.tag == "{http://www.tei-c.org/ns/1.0}speaker"):
            speaker(content, targetFile)
        elif(content.tag == "{http://www.tei-c.org/ns/1.0}ab"):
            getLines(content, targetFile)  

"""
visitAct
This is a visitor parser to create a custom navigation bar for any play we use. 
It requires an xmlTree that has acts noted by div1 and scenes noted by div2, like the Folger
XML versions of the plays. It also requires a file to write to. Hopefully, this is the file
that we're writing to all along.
This will go through and find all the acts and scenes based on those assumptions. It will
write out the proper HTML to make a navbar based on those assumptions
"""
def visitAct(xmlTree, targetFile):
    acts = tree.findall(".//{http://www.tei-c.org/ns/1.0}div1")
    baseIndent = " " * 14
    secondLvl = baseIndent + "  "
    thirdLvl = secondLvl + "  "
    actPattern = baseIndent + '<div class="col-sm-4">\n' + secondLvl+ '<ul class="multi-column-dropdown">\n'

    for act in acts:
        targetFile.write(actPattern)
        targetFile.write(thirdLvl+'<li><a href="#">Act %s</a></li>\n' % act.get('n'))
        targetFile.write(thirdLvl+'<li class="divider"></li>\n')
        scenes = act.findall(".//{http://www.tei-c.org/ns/1.0}div2")
        for scene in scenes:
            idNumber = act.get('n') + "." + scene.get('n')
            targetFile.write(thirdLvl + '<li><a href="#'+idNumber)
            targetFile.write('">Scene %s</a></li>\n' % scene.get('n'))
        targetFile.write(secondLvl+'</ul>\n'+baseIndent+'</div>\n')
        if int(act.get('n')) == 3:
            targetFile.write(secondLvl+"</div>")


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
        writeOneScene(scene, target)
target.write("</div>\n</body>\n</html>")
target.close()

