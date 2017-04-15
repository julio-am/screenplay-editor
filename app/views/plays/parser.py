import xml.etree.ElementTree as ET

def elemToString(content):
    return ET.tostring(content, encoding='utf8', method='text')

def cleanElemToString(content):
    string = elemToString(content)
    return filter(lambda x: x != "\n", string).replace("  ", "")

def stageDirElem(content):
    string = ""
    for children in content.findall("./*"):
        if children.tag == "{http://www.tei-c.org/ns/1.0}lb":
            string += "\n"
        else:
            toString = ET.tostring(children, encoding='utf8', method='text')
            string += filter(lambda x: x != "\n", toString).replace("  ", "")
    return string

def printSingleLine(line, targetFile):
    targetFile.write(filter(lambda x: x != "\n", line).replace("  ", ""))

def stageDirInLine(content, targetFile):
    xmlstr = stageDirElem(content)
    if xmlstr[0] != ',':
        targetFile.write("\n<br>\n")
        targetFile.write("<i>%s</i>" % xmlstr)
    else:
        targetFile.write("<i>%s</i>" % xmlstr)

def speaker(content, targetFile):
        xmlstr = cleanElemToString(content)
        targetFile.write("\n<br>\n<b>%s</b> "% xmlstr)
        return xmlstr

def getLines(content, targetFile):
    line = ""
    numLines = 0
    listOfSD = []
    for words in content.findall("./*"):
        if ((words.tag == "{http://www.tei-c.org/ns/1.0}milestone") and (words.get('unit') == "ftln")):
            numLines += 1
            printSingleLine(line, targetFile)
            targetFile.write('\n<br>\n<span class="lineNum">%s</span>' % words.get('n')[4:])
            line = ""
        elif((words.tag == "{http://www.tei-c.org/ns/1.0}q")):
            getLines(words, targetFile)
        elif (words.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            printSingleLine(line, targetFile)
            line = ""
            stageDirInLine(words, targetFile)
            listOfSD = listOfSD + [words.get('n')]
        elif(words.tag == "{http://www.tei-c.org/ns/1.0}seg"):
            getLines(words, targetFile)
        elif (words.tag != "{http://www.tei-c.org/ns/1.0}fw"):
            line += ET.tostring(words, encoding='utf8', method='text')
    printSingleLine(line, targetFile)
    return (numLines, listOfSD)

"""
printOneScene
This will write a single scene as we want it formatted
It takes in a scene and a targetFile.
"""
def writeOneScene(scene, targetFile, dictionary):
    curSpeaker = ""
    lines = 0
    listOfSD = []
    for content in scene.iter():
        if (content.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            if content.get('n') not in listOfSD:
                stageDirInLine(content, targetFile)
        elif (content.tag == "{http://www.tei-c.org/ns/1.0}speaker"):
            curSpeaker = speaker(content, targetFile)
        elif(content.tag == "{http://www.tei-c.org/ns/1.0}ab"):
            numLinesAndSD = getLines(content, targetFile)
            lines = numLinesAndSD[0]
            listOfSD += numLinesAndSD[1]
            if curSpeaker not in dictionary:
                dictionary[curSpeaker] = lines
            else:
                dictionary[curSpeaker] += lines


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


dictionary = {}
header = open("header.html", "r")
lines = header.readlines()
target = open("index.html.erb", "w")
tree = ET.parse("MND.xml").getroot()
for line in lines:
    target.write(line)
    if '<div class="row">' in line:
        visitAct(tree, target)
acts = tree.findall(".//{http://www.tei-c.org/ns/1.0}div1")
for act in acts:
    target.write("\n<h1>\nAct %s\n</h1>" % act.get('n'))
    scenes = act.findall(".//{http://www.tei-c.org/ns/1.0}div2")
    for scene in scenes:
        idNumber = act.get('n') + "." + scene.get('n')
        target.write("\n<h2 id ="+idNumber+">\nScene %s\n</h2>" % scene.get('n'))
        writeOneScene(scene, target, dictionary)
target.write("</div>\n</body>\n</html>")
target.close()

chars = open("characters.html", "w")
chars.write("<DOCTYPE! HTML>\n<html>")
chars.write('<center>\n<table style="width:50%">\n')
chars.write("<tr><th><b>Character Name</b></th><th><b>Number of Lines</b></th></tr>")
for key in dictionary:
    chars.write('<tr><td>%s</td>\n' % key)
    chars.write('<td>%d</td></tr>\n' % dictionary[key])
chars.write("</table></center>")


