"""
General functions
"""
def getInfos(func : dict) -> None:
    global alphabetL, alphabetU, varsInfo, typeList, funcInfos
    alphabetL, alphabetU = [chr(i) for i in range(ord('a'),ord('z')+1)], [chr(i).upper() for i in range(ord('a'),ord('z')+1)]
    funcInfos, varsInfo = func, {'global' : {}}
    typeList = ['int', 'str' ,'float', 'bool', 'list', 'dict']

def error(message : str, lineNumber : int | None = 'Not specified') -> None:
    print(f'Error LN°{lineNumber} -> {message}')
    exit()

def getKeyword(line : str, lineNumber : int | None = 'Not specified') -> str:
    splitedLine = line.split(" ", 1)
    keywordsList = ['write', 'int', 'var', 'let', 'transform', 'pass', 'function', 'call', 'class', 'for', 'if', 'elif', 'else']
    if len(splitedLine) == 1:
        if splitedLine[0][-1] == ";":
            splitedLine[0] = splitedLine[0][:-1]
        if splitedLine[0] not in keywordsList:
            error('Keyword used does not exist', lineNumber)
        else:
            return splitedLine[0]
    else:
        endMark = False
        if splitedLine[0] in ['write', 'int', 'var', 'let', 'transform', 'pass', 'call']:
            endMark = True
        if splitedLine[0] not in keywordsList:
            error('Keyword used does not exist', lineNumber)
        elif line[-1] != ";" and endMark:
            error('Syntax error : line is never marked as finished', lineNumber)
        else:
            return splitedLine[0]

def executeFile(file : dict, function : str) -> None:
    lastCondition = None
    forbiddenLines = []
    for position, lineNumber in enumerate(file.keys()):
        if lineNumber not in forbiddenLines:
            keyword = getKeyword(file[lineNumber], lineNumber)
            if keyword not in ['for', 'if', 'elif', 'else']:
                lastCondition = None
                globals()['keyword_' + str(keyword)](file[lineNumber], lineNumber, function)
            elif keyword == 'for':
                lastCondition = None
                splitedLine = file[lineNumber].split(" ", 3)
                if splitedLine[2] != "in":
                    error("Syntax error", lineNumber)
                forFile = {}
                for line in list(file.keys())[position+1:]:
                    textLine = file[line]
                    if textLine != textLine.lstrip() and (len(textLine)-len(textLine.lstrip()))%4 == 0:
                        forFile[line] = textLine[4:]
                        forbiddenLines.append(line)
                    else:
                        break
                varsInfo[function][splitedLine[1]] = {}
                for forVar in listObject(splitedLine[3], function, lineNumber):
                    varsInfo[function][splitedLine[1]]["value"] = forVar
                    executeFile(forFile, function)
            elif keyword in ['if', 'elif', 'else']:
                splitedLine = file[lineNumber].split(" ", 1)
                ifFile = {}
                for line in list(file.keys())[position+1:]:
                    textLine = file[line]
                    if textLine != textLine.lstrip() and (len(textLine)-len(textLine.lstrip()))%4 == 0:
                        ifFile[line] = textLine[4:]
                        forbiddenLines.append(line)
                    else:
                        break
                varsInfo[function][splitedLine[1]] = {}
                if boolObject(splitedLine[1][:-1], function, lineNumber) and keyword == 'if':
                    lastCondition = True
                    executeFile(ifFile, function)
                elif boolObject(splitedLine[1][:-1], function, lineNumber) and keyword == 'elif' and not lastCondition:
                    lastCondition = True
                    executeFile(ifFile, function)
                elif keyword == 'else' and not lastCondition:
                    lastCondition = None
                    executeFile(ifFile, function)
                elif keyword == 'elif' and lastCondition:
                    pass
                else:
                    lastCondition = False

def reassembleWords(textList : list) -> list:
    for position, letter in enumerate(textList):
        if letter == 'a' and textList[position+1] == 'n' and textList[position+2] == 'd':
            textList[position] = 'and'
        elif letter == 'o' and textList[position+1] == 'r':
            textList[position] = 'or'
    return textList

def boolObject(text : str, function : str, lineNumber : int) -> bool:
    textList = getRidOfString(text)
    newText = ""
    for position, letter in enumerate(text):
        if letter == " " and textList[position] == "":
            newText += letter
        elif letter != " ":
            newText += letter
    text = newText
    textList = getRidOfString(text)
    if '(' in textList:
        beforeParentheses = ""
        inParentheses = ""
        openedParentheses = 0
        for position, letter in enumerate(text):
            if letter == '(' and textList[position] != "":
                openedParentheses += 1
                continue
            elif letter == ')' and openedParentheses != 1 and textList[position] != "":
                openedParentheses -= 1
                continue
            elif letter == ')' and openedParentheses == 1 and textList[position] != "":
                return boolObject(beforeParentheses + str(boolObject(inParentheses, function, lineNumber)) + text[position+1:], function, lineNumber)
            elif letter == ')' and openedParentheses == 0 and textList[position] != "":
                error("You cannot close a parentheses which was never opened", lineNumber)
            
            if openedParentheses == 0:
                beforeParentheses += letter
            elif openedParentheses != 0:
                inParentheses += letter

    textList = reassembleWords(textList)
    if 'and' in textList:
        splitedText = [text[:textList.index('and')], text[textList.index('and')+3:]]
        splitedTextListZ = reassembleWords(getRidOfString(splitedText[0]))
        splitedTextListO = reassembleWords(getRidOfString(splitedText[1]))
        if 'or' in splitedTextListZ:
            splitedText[0] = [splitedText[0][:splitedTextListZ.index('or')+2], splitedText[0][splitedTextListZ.index('or')+2:]]
        else:
            splitedText[0] = ['', splitedText[0]]
        if 'and' in splitedTextListO:
            return boolObject(splitedText[0][0]+str(boolObject(splitedText[0][1], function, lineNumber) and boolObject(splitedText[1][:splitedTextListO.index('and')], function, lineNumber))+splitedText[1][splitedTextListO.index('and'):], function, lineNumber)
        elif 'or' in splitedTextListO:
            return boolObject(splitedText[0][0]+str(boolObject(splitedText[0][1], function, lineNumber) and boolObject(splitedText[1][:splitedTextListO.index('or')], function, lineNumber))+splitedText[1][splitedTextListO.index('or'):], function, lineNumber)
        else:
            return boolObject(splitedText[0][0]+str(boolObject(splitedText[0][1], function, lineNumber) and boolObject(splitedText[1], function, lineNumber)), function, lineNumber)
        
    elif 'or' in textList:
        splitedText = [text[:textList.index('or')], text[textList.index('or')+2:]]
        splitedTextList = reassembleWords(getRidOfString(splitedText[1]))
        if 'or' in splitedTextList[1]:
            return boolObject(str(boolObject(splitedText[0], function, lineNumber) or boolObject(splitedText[1][:splitedTextList.index('or')], function, lineNumber))+splitedText[1][splitedTextList.index('or')+2:], function, lineNumber)
        else:
            return boolObject(str(boolObject(splitedText[0], function, lineNumber) or boolObject(splitedText[1], function, lineNumber)), function, lineNumber)

    elif '=' in textList and textList[textList.index("=")+1] == "=":
        splitedText = [text[:textList.index("=")], text[textList.index("=")+2:]]
        if letObject(splitedText[0], function, lineNumber) == letObject(splitedText[1], function, lineNumber):
            return True
        else:
            return False
        
    if text in ["True", True]:
        return True
    else:
        return False
    
def strObject(text : str, function : str, lineNumber) -> str:
    if text == "":
        return ''
    stringOpened = False
    newText = ""
    openedChar = ""
    for letter in text:
        if letter in ["'", '"'] and not stringOpened:
            stringOpened = True
            openedChar = letter
        elif letter == openedChar and stringOpened:
            stringOpened = False
        
        if not stringOpened and letter == "+":
            newText += ","
        elif not stringOpened and letter == ";":
            newText += '," ",'
        elif stringOpened or (letter != " " and not stringOpened):
            newText += letter

    text = newText
    textList = getRidOfString(text)
    if "," in textList:
        splitedText = [text[:textList.index(",")], text[textList.index(",")+1:]]
        splitedTextList = getRidOfString(splitedText[1])
        if "," in splitedTextList:
            return strObject('"'+strObject(splitedText[0], function, lineNumber)+strObject(splitedText[1][:splitedTextList.index(",")], function, lineNumber)+'",'+splitedText[1][splitedTextList.index(",")+1:], function, lineNumber)
        else:
            return strObject('"'+strObject(splitedText[0], function, lineNumber)+strObject(splitedText[1], function, lineNumber)+'"', function, lineNumber)
    
    elif text[0] == "f" and text[1]==text[-1] and text[1] in ['"', "'"]:
        for var in list(varsInfo[function].keys()):
            if "{"+f"{var}"+"}" in text:
                text = text.replace("{"+f"{var}"+"}", str(varsInfo[function][var]["value"]))
        return text[2:-1]
    
    elif text[0] == text[-1] and text[0] in ['"', "'"]:
        return text[1:-1]
    
    else:
        error("A string must be declared with : '' or "+'""', lineNumber)

def letObject(text : str, function : str, lineNumber : int):
    for var in list(varsInfo[function].keys()):
        if var in text:
            text = text.replace(str(var), str(varsInfo[function][var]["value"]))
    return text

def getRidOfString(text : str) -> list:
    stringOpened = False
    textList = []
    openedChar = ""

    for letter in text:
        if letter in ["'", '"'] and not stringOpened:
            stringOpened = True
            openedChar = letter
        elif letter == openedChar and stringOpened:
            stringOpened = False
        
        if stringOpened:
            textList.append("")
        else:
            textList.append(letter)
    return textList

def getSplitedOperation(splitedText : list) -> list:
    for letter in splitedText[0][::-1]:
        if letter in ["+", "*", "-", "/", "%", "//"]:
            splitedText[0] = splitedText[0][::-1].split(letter)[::-1]
            splitedText[0][0] += letter
            break
    if len(splitedText[0]) == 1 or type(splitedText[0]) != list:
        splitedText[0] = ['', splitedText[0]]
    for letter in splitedText[1]:
        if letter in ["+", "*", "-", "/", "%", "//"]:
            splitedText[1] = splitedText[1].split(letter)
            splitedText[1][1] = letter + splitedText[1][1]
            break
    if len(splitedText[1]) == 1 or type(splitedText[1]) != list:
        splitedText[1] = [splitedText[1], '']
    return splitedText

def intObject(text : str, function : str, lineNumber) -> int:
    return int(floatObject(text, function, lineNumber))

def floatObject(text : str, function : str, lineNumber) -> float:
    text = text.replace(" ", "")
    for var in varsInfo[function].keys():
        text = text.replace(var, str(varsInfo[function][var]["value"]))
    if '(' in text:
        beforeParentheses = ""
        inParentheses = ""
        openedParentheses = 0
        for position, letter in enumerate(text):
            if letter == '(':
                openedParentheses += 1
                continue
            elif letter == ')' and openedParentheses != 1:
                openedParentheses -= 1
                continue
            elif letter == ')' and openedParentheses == 1:
                return floatObject(beforeParentheses + str(floatObject(inParentheses, function, lineNumber)) + text[position+1:], function, lineNumber)
            elif letter == ')' and openedParentheses == 0:
                error("You cannot close a parentheses which was never opened", lineNumber)
            
            if openedParentheses == 0:
                beforeParentheses += letter
            elif openedParentheses != 0:
                inParentheses += letter

    if '**' in text:
        splitedText = text.split("**", 1)
        splitedText = getSplitedOperation(splitedText)
        return floatObject(splitedText[0][0]+str(floatObject(splitedText[0][1], function, lineNumber)**floatObject(splitedText[1][0], function, lineNumber))+splitedText[1][1], function, lineNumber)
    
    if '//' in text:
        splitedText = text.split("//", 1)
        splitedText = getSplitedOperation(splitedText)
        return floatObject(splitedText[0][0]+str(floatObject(splitedText[0][1], function, lineNumber)//floatObject(splitedText[1][0], function, lineNumber))+splitedText[1][1], function, lineNumber)
    
    if '%' in text:
        splitedText = text.split("%", 1)
        splitedText = getSplitedOperation(splitedText)
        return floatObject(splitedText[0][0]+str(floatObject(splitedText[0][1], function, lineNumber)%floatObject(splitedText[1][0], function, lineNumber))+splitedText[1][1], function, lineNumber)

    elif '*' in text or '/' in text:
        for letter in text:
            if letter == '*':
                splitedText = text.split("*", 1)
                operator = '*'
                break
            elif letter == '/':
                splitedText = text.split("/", 1)
                operator = '/'
                break
        splitedText = getSplitedOperation(splitedText)
        if operator == '*':
            return floatObject(splitedText[0][0]+str(floatObject(splitedText[0][1], function, lineNumber)*floatObject(splitedText[1][0], function, lineNumber))+splitedText[1][1], function, lineNumber)
        elif operator == '/':
            divider = floatObject(splitedText[1][0], function, lineNumber)
            if divider == 0:
                error("Even though I'm the best PL in the world, I cannot divide by 0...", lineNumber)
            return floatObject(splitedText[0][0]+str(floatObject(splitedText[0][1], function, lineNumber)/divider)+splitedText[1][1], function, lineNumber)

    elif '+' in text or '-' in text:
        for letter in text:
            if letter == '+':
                splitedText = text.split("+", 1)
                operator = '+'
                break
            elif letter == '-':
                splitedText = text.split("-", 1)
                operator = '-'
                break
        splitedText = getSplitedOperation(splitedText)
        if operator == '+':
            return floatObject(splitedText[0][0]+str(floatObject(splitedText[0][1], function, lineNumber)+floatObject(splitedText[1][0], function, lineNumber))+splitedText[1][1], function, lineNumber)
        elif operator == '-':
            return floatObject(splitedText[0][0]+str(floatObject(splitedText[0][1], function, lineNumber)-floatObject(splitedText[1][0], function, lineNumber))+splitedText[1][1], function, lineNumber)
        
    else:
        return float(text)

def listObject(text : str, function : str, lineNumber : int) -> list:
    if "range" in text:
        for var in varsInfo[function].keys():
            if var in text:
                return [x for x in range(int(varsInfo[function][var]["value"]))]
        return [x for x in range(int(text[(len(text)-5):-2]))]
    return list(text[1:-2].replace(" ", "").split(","))

"""
Keyword functions
"""

def keyword_pass(line : str, lineNumber : int, function : str) -> None:
    pass

def keyword_call(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 2)
    if splitedLine[1] in funcInfos.keys():
        varsInfo[splitedLine[1]] = {}
        splitedLine[2] = splitedLine[2].replace(" ", "")
        splitedLine[2] = splitedLine[2][1:][:-2].split(",")
        if splitedLine[2] == ['']:
            splitedLine[2] = []
        elif '' in splitedLine[2]:
            error("An argument cannot be empty", lineNumber)
        if len(splitedLine[2]) == len(funcInfos[splitedLine[1]]["args"]):
            for varNumber, var in enumerate(splitedLine[2]):
                varsInfo[splitedLine[1]][funcInfos[splitedLine[1]]["args"][varNumber]["name"]] = {}
                varsInfo[splitedLine[1]][funcInfos[splitedLine[1]]["args"][varNumber]["name"]]["type"] = funcInfos[splitedLine[1]]["args"][varNumber]["type"]
                varsInfo[splitedLine[1]][funcInfos[splitedLine[1]]["args"][varNumber]["name"]]["value"] = globals()[funcInfos[splitedLine[1]]["args"][varNumber]["type"] + "Object"](var, function, lineNumber)
            executeFile(funcInfos[splitedLine[1]]["algo"], splitedLine[1])
        else:
            error(f'Function : {splitedLine[1]} expects {len(funcInfos[splitedLine[1]]["args"])} arguments and got {len(splitedLine[2])}', lineNumber)
        varsInfo.pop(splitedLine[1])
    else:
        error("You cannot call a function that does not exist", lineNumber)

def keyword_write(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 1)
    toPrintObject = splitedLine[1][:-1]
    if toPrintObject[0] != '(' or toPrintObject[-1] != ')':
        error('You must use parentheses to specify the text you want to print', lineNumber)
    print(strObject(toPrintObject[1:-1], function, lineNumber))

def keyword_int(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] != "=":
        error("You must use the define symbol in order to define an integer", lineNumber)
    elif splitedLine[1].lower() in varsInfo[function].keys():
        error("You cannot create a variable with the name of an already existing variable", lineNumber)
    for nameLetter in splitedLine[1]:
        if nameLetter not in alphabetL+alphabetU:
            error("The name of a variable must only contain letters", lineNumber)
    try:
        varsInfo[function][splitedLine[1].lower()] = {"value" : intObject(splitedLine[3][:-1], function, lineNumber), "type" : "int"}
    except:
        error("The value specified is not of the correct type", lineNumber)

def keyword_let(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] != "=":
        error("You must use the define symbol in order to define a let variable", lineNumber)
    elif splitedLine[1].lower() in varsInfo[function].keys():
        error("You cannot create a variable with the name of an already existing variable", lineNumber)
    for nameLetter in splitedLine[1]:
        if nameLetter not in alphabetL+alphabetU:
            error("The name of a variable must only contain letters", lineNumber)
    try:
        varsInfo[function][splitedLine[1].lower()] = {"value" :splitedLine[3][:-1], "type" : "let"}
    except:
        error("The value specified is not of the correct type", lineNumber)

def keyword_var(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] != "=":
        error("You must use the define symbol in order to define an integer", lineNumber)
    elif splitedLine[1].lower() not in varsInfo[function].keys():
        error("You cannot modify a variable with the name of an already existing variable", lineNumber)
    try:
        if varsInfo[function][splitedLine[1].lower()]["type"] == "int":
            varsInfo[function][splitedLine[1].lower()]["value"] = intObject(splitedLine[3][:-1], function, lineNumber)
    except:
        error("The value specified is not of the correct type", lineNumber)
    
def keyword_transform(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] != "->":
        error("You must use the transformation symbol in order to transform a let variable", lineNumber)
    elif splitedLine[1].lower() not in varsInfo[function].keys():
        error("You cannot transform a variable which does not exist", lineNumber)
    elif splitedLine[3][:-1] not in typeList:
        error("You must specify an existing type to transform a let variable", lineNumber)
    try:
        newLetType = splitedLine[3][:-1]
        if newLetType == "int":
            varsInfo[function][splitedLine[1].lower()]["value"] = int(varsInfo[function][splitedLine[1].lower()]["value"])
            varsInfo[function][splitedLine[1].lower()]["type"] = f'let-{newLetType}'
    except:
        error("The value you tried to transform does not support the specified type", lineNumber)   