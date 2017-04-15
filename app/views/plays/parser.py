import xml.etree.ElementTree as ET

"""
elemToString
This takes in content, a node, and returns the inner text
"""
def elemToString(content):
    return ET.tostring(content, encoding='utf8', method='text')

"""
cleanElemToString
This takes in content, a node, and returns the inner text with only one space between
words and no line breaks
"""
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
"""
printSingleLine
This writes a string to file after removing extra spaces and all line breaks
This takes in line, a string, and targetFile, a file object with write privileges.
"""
def printSingleLine(line, targetFile):
    targetFile.write(filter(lambda x: x != "\n", line).replace("  ", ""))

"""
outerLvlStageDir 
This gets the stage directions that are not in the middle of a line and writes them to our file.
This takes in content, a stage directions XML node, and a targetFile, the file object with write privileges.
"""
def outerLvlStageDir(content, targetFile):
    # Because there is no parent function for elementTree, we had to make our own
    parents = content.findall("..")
    for parent in parents:
        # This checks that the stage direction is not in a line
        if(parent.tag != "ab"):
            xmlstr = cleanElemToString(content)            
            # If the stage direction starts with a comma, we write on the same line as the character name
            if xmlstr[0] != ',':
                targetFile.write("\n<br>\n")
                targetFile.write("<i>%s</i>" % xmlstr)
                return

"""
stageDirInLine 
This gets the stage directions in the middle of a line and writes them to our file.
This takes in content, a stage directions XML node,  and a targetFile, the file object with write privileges.
"""
def stageDirInLine(content, targetFile):
    xmlstr = cleanElemToString(content)
    # If the stage direction starts with a comma, we write on the same line as the character name
    if xmlstr[0] != ',':
        targetFile.write("\n<br>\n")
        targetFile.write("<i>%s</i>" % xmlstr)
    else:
        targetFile.write("<i>%s</i>" % xmlstr)

"""
speaker
This writes the speaker's name to file and returns it to use as the key for the dictionary.
This takes in content, a speaker node, and a targetFile, a file object with write privileges.
"""
def speaker(content, targetFile):
        xmlstr = cleanElemToString(content)
        targetFile.write("\n<br>\n<b>%s</b> "% xmlstr)
        return xmlstr

"""
getLines
This will write all the lines that one character speaks and the in-line stage directions to a file.
It takes in content, a node with tag 'ab', and a targetFile, a file object with write privilege.
"""
def getLines(content, targetFile):
    line = ""
    numLines = 0
    listOfSD = []
    for words in content.findall("./*"):
        # If the child is a milestone, it prints out the previous line, the next line number, and resets
        if ((words.tag == "{http://www.tei-c.org/ns/1.0}milestone") and (words.get('unit') == "ftln")):
            numLines += 1
            printSingleLine(line, targetFile)
            targetFile.write('\n<br>\n<span class="lineNum">%s</span>' % words.get('n')[4:])
            line = ""
        # If the child node is a q or seg, those are wrappers, so we need to go one level deeper
        elif((words.tag == "{http://www.tei-c.org/ns/1.0}q") or (words.tag == "{http://www.tei-c.org/ns/1.0}seg")):
            getLines(words, targetFile)
        # If the child is a stage, we should print the line and then print the stage direction
        elif (words.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            printSingleLine(line, targetFile)
            line = ""
            stageDirInLine(words, targetFile)
            listOfSD = listOfSD + [words.get('n')]
        elif(words.tag == "{http://www.tei-c.org/ns/1.0}seg"):
            getLines(words, targetFile)
        # Any other tag that is not fw is a word, space, or punctuation that should be added to the line
        elif (words.tag != "{http://www.tei-c.org/ns/1.0}fw"):
            line += ET.tostring(words, encoding='utf8', method='text')
    # Because we never hit a final milestone after reading in the last line, we need to print it out
    printSingleLine(line, targetFile)
    return (numLines, listOfSD)

"""
printOneScene
This will write a single scene as we want it formatted and update the character line dictionary.
It takes in a scene (div2) node, a file to write to, and a dicitionary that holds the lines characters.
"""
def writeOneScene(scene, targetFile, dictionary):
    curSpeaker = ""
    lines = 0
    listOfSD = []
    # This goes through every node in the scene, hence the need for outerLvlStageDir and stageDirInLine
    for content in scene.iter():
        # If we get a stage direction at this level, it should be an outer level one
        if (content.tag == "{http://www.tei-c.org/ns/1.0}stage"):
            if content.get('n') not in listOfSD:
                stageDirInLine(content, targetFile)
        # If we get a speaker, we need to update the current speaker
        elif (content.tag == "{http://www.tei-c.org/ns/1.0}speaker"):
            curSpeaker = speaker(content, targetFile)
        # If we get an 'ab' tag, this is the start of a line for curSpeaker
        elif(content.tag == "{http://www.tei-c.org/ns/1.0}ab"):
            numLinesAndSD = getLines(content, targetFile)
            lines = numLinesAndSD[0]
            listOfSD += numLinesAndSD[1]
            # Writes the line to the targetFile and updates the character dictionary
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
write out the proper HTML to make a navbar based on those assumptions.
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
        # Every 3 acts, we will create a new row
        if int(act.get('n')) == 3:
            targetFile.write(secondLvl+"</div>")
            
            
dictionary = {}
header = open("header.html", "r")
lines = header.readlines()
target = open("index.html.erb", "w")
tree = ET.parse("MND.xml").getroot()

# Write the header to index file first, using the visitor parser at the appropriate place
for line in lines:
    target.write(line)
    if '<div class="row">' in line:
        visitAct(tree, target)

# Start by finding all the acts, noted with div1's
acts = tree.findall(".//{http://www.tei-c.org/ns/1.0}div1")

for act in acts:
    target.write("\n<h1>\nAct %s\n</h1>" % act.get('n'))
    # Find all the scenes in the act. Each has the tag div2
    scenes = act.findall(".//{http://www.tei-c.org/ns/1.0}div2")
    
    for scene in scenes:
        # idNumber is the id attribute so the navigation works.
        # It reflects the ActNumber.SceneNumber numbering of Shakespeare plays
        idNumber = act.get('n') + "." + scene.get('n')
        target.write("\n<h2 id ="+idNumber+">\nScene %s\n</h2>" % scene.get('n'))
        writeOneScene(scene, target, dictionary)
target.write("</div>\n</body>\n</html>")
target.close()

chars = open("characters.html", "w")
chars.write("<DOCTYPE! HTML>\n<html>")
chars.write('<center>\n<table style="width:50%">\n')
chars.write("<tr><th><b>Character Name</b></th><th><b>Number of Lines</b></th></tr>")
chars.write('<table style="width:100%">\n')

# In a table we output the name of the character from the dictionary
# and the number of lines they spoke
for key in dictionary:
    chars.write('<tr><td>%s</td>\n' % key)
    chars.write('<td>%d</td></tr>\n' % dictionary[key])
chars.write("</table></center>")


