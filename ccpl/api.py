"""
General functions
"""
def getInfos(grammar : dict, settings : dict) -> None:
    global grammarDict, settingsDict, alphabetL, alphabetU, varsInfo, typeList
    grammarDict, settingsDict, alphabetL, alphabetU, varsInfo, typeList = grammar, settings, [chr(i) for i in range(ord('a'),ord('z')+1)], [chr(i).upper() for i in range(ord('a'),ord('z')+1)], {'global' : {}}, ['int', 'str' ,'float', 'bool', 'list', 'dict']

def error(message : str, lineNumber : int | None = 'Not specified') -> None:
    print(f'Error LN°{lineNumber} -> {message}')
    exit()

def getKeyword(line : str, lineNumber : int | None = 'Not specified') -> str:
    splitedLine = line.split(" ", 1)
    if len(splitedLine) == 1:
        if splitedLine[0] not in grammarDict['keywordInfo'].keys():
            error('Keyword used does not exist', lineNumber)
        else:
            return splitedLine[0]
    else:
        if splitedLine[0] in ['write', 'int', 'var']:
            endMark = True
        if splitedLine[0] not in grammarDict['keywordInfo'].keys():
            error('Keyword used does not exist', lineNumber)
        elif line[-settingsDict['infoLenght']['endLine']:] != settingsDict['infoKeyword']['endLine'] and endMark:
            error('Syntax error : line is never marked as finished', lineNumber)
        else:
            return splitedLine[0]

def stringObject(text : str) -> str:
    return text

def executeFile(file : list, function : str) -> None:
    for lineNumber in file.keys():
        keyword = getKeyword(file[lineNumber], lineNumber)
        globals()['keyword_' + grammarDict['keywordInfo'][keyword]](file[lineNumber], lineNumber, function)
        print(varsInfo)
"""
Keyword functions
"""

def keyword_pass(line : str, lineNumber : int, function : str) -> None:
    print('DO NOT USE THAT U UKWAT')
    pass

def keyword_write(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 1)
    toPrintObject = splitedLine[1][:-settingsDict['infoLenght']['endLine']]
    if toPrintObject[0] != '(' or toPrintObject[-1] != ')':
        error('You must use parentheses to specify the text you want to print', lineNumber)
    print(toPrintObject[1:-1])

def keyword_int(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] != settingsDict["infoKeyword"]["defineSymbol"]:
        error("You must use the define symbol in order to define an integer", lineNumber)
    elif splitedLine[1].lower() in varsInfo[function].keys():
        error("You cannot create a variable with the name of an already existing variable", lineNumber)
    for nameLetter in splitedLine[1]:
        if nameLetter not in alphabetL+alphabetU:
            error("The name of a variable must only contain letters", lineNumber)
    try:
        varsInfo[function][splitedLine[1].lower()]["value"] = {"value" :int(splitedLine[3][:-settingsDict['infoLenght']['endLine']]), "type" : "int"}
    except:
        error("The value specified is not of the correct type", lineNumber)

def keyword_let(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] != settingsDict["infoKeyword"]["defineSymbol"]:
        error("You must use the define symbol in order to define a let variable", lineNumber)
    elif splitedLine[1].lower() in varsInfo[function].keys():
        error("You cannot create a variable with the name of an already existing variable", lineNumber)
    for nameLetter in splitedLine[1]:
        if nameLetter not in alphabetL+alphabetU:
            error("The name of a variable must only contain letters", lineNumber)
    try:
        varsInfo[function][splitedLine[1].lower()] = {"value" :splitedLine[3][:-settingsDict['infoLenght']['endLine']], "type" : "let"}
    except:
        error("The value specified is not of the correct type", lineNumber)

def keyword_var(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] == settingsDict["infoKeyword"]["defineSymbol"]:
        elif splitedLine[1].lower() not in varsInfo[function].keys():
            error("You cannot modify a variable which does not exist", lineNumber)
        try:
            varType = varsInfo[function][splitedLine[1].lower()]["type"]
            if varType == "int":
                varsInfo[function][splitedLine[1].lower()]["value"] = int(splitedLine[3][:-settingsDict['infoLenght']['endLine']])
        except:
            error("The value specified is not of the correct type", lineNumber)
    elif splitedLine[2] in [settingsDict['infoKeyword']['multiplication']+settingsDict['infoKeyword']['defineSymbol'], settingsDict['infoKeyword']['addition']+settingsDict['infoKeyword']['defineSymbol'], settingsDict['infoKeyword']['substraction']+settingsDict['infoKeyword']['defineSymbol'], settingsDict['infoKeyword']['division']+settingsDict['infoKeyword']['defineSymbol']]:
        if varsInfo[function][splitedLine[1].lower()]["type"] not in ["int", "float"] and splitedLine[2] != settingsDict['infoKeyword']['addition']+settingsDict['infoKeyword']['defineSymbol']:
            error(f'{varsInfo[function][splitedLine[1].lower()]["type"]} objects does not support short modification')
        #*, /, +, - in function of the used thing in splitedLine[2]
        if splitedLine[2] == 
            
    else:
        error("You must use the define symbol in order to define an integer", lineNumber)

    
def keyword_transform(line : str, lineNumber : int, function : str) -> None:
    splitedLine = line.split(" ", 3)
    if splitedLine[2] != settingsDict["infoKeyword"]["transformSymbol"]:
        error("You must use the transformation symbol in order to transform a let variable", lineNumber)
    elif splitedLine[1].lower() not in varsInfo[function].keys():
        error("You cannot transform a variable which does not exist", lineNumber)
    elif splitedLine[3][:-settingsDict['infoLenght']['endLine']] not in typeList:
        error("You must specify an existing type to transform a let variable", lineNumber)
    try:
        newLetType = splitedLine[3][:-settingsDict['infoLenght']['endLine']]
        if newLetType == "int":
            varsInfo[function][splitedLine[1].lower()]["value"] = int(varsInfo[function][splitedLine[1].lower()]["value"])
    except:
        error("The value you tried to transform does not support the specified type", lineNumber)