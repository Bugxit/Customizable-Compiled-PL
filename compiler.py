from sys import argv
from os import path

###############
###UTILITIES###
###############

def splitWithoutStrings(inputString : str, splitChar : str,  maxSplit: int | None = -1) -> list[str]:
    stringIsOpen = False
    charThatOpenedString = ""

    splitedStringList = [""]

    for charValue in inputString:
        if not stringIsOpen and charValue in ["'", '"']: stringIsOpen, charThatOpenedString = True, charValue
        elif stringIsOpen and charValue == charThatOpenedString: stringIsOpen = False

        if charValue == splitChar: 
            splitedStringList.append("")
            maxSplit -= 1
            if maxSplit == 0: break
        else: splitedStringList[-1] += charValue
        
    return [string.strip() for string in splitedStringList]

#############
###Classes###
#############

class Func:
    def __init__(self, name, parameters, returnType, innerCode) -> None:
        self.name = name
        self.parameters = parameters
        self.returnType = returnType
        self.innerCode = innerCode

####################
###Main Functions###
####################

def getInputFile(filePath : str) -> tuple[list[str], list[int]]:
    with open(filePath, "r") as inputFile: fileArray =  inputFile.readlines()
    
    if fileArray == -1: print("An error occured while reading the file") ; exit(1)

    return [line.strip() for line in fileArray if line.strip()], [lineNumber+1 for lineNumber in range(len(fileArray)) if fileArray[lineNumber].strip()]

def removeCommentsInFile(fileArray : list[str], lineNumberArray : list[int]) -> tuple[list[str], list[int]]:
    commentsRemovedArray = []

    skipNextChar = False
    stringIsOpen = False
    commentIsOpen = False
    charThatOpenedString = ""

    for line in fileArray:
        currentLineValue = ""
        for charPosistion, charValue in enumerate(line):
            if skipNextChar: skipNextChar = False ; continue

            if not stringIsOpen and not commentIsOpen and charValue in ["'", '"']: charThatOpenedString, stringIsOpen = charValue, True
            elif stringIsOpen and not commentIsOpen and charValue == charThatOpenedString: stringIsOpen = False

            if charPosistion != len(line) - 1:
                if not commentIsOpen and not stringIsOpen and f'{charValue}{line[charPosistion+1]}' == '//': break
                elif not commentIsOpen and not stringIsOpen and f'{charValue}{line[charPosistion+1]}' == '/*': commentIsOpen, skipNextChar = True, True ; continue
                elif commentIsOpen and not stringIsOpen and f'{charValue}{line[charPosistion+1]}' == '*/': commentIsOpen, skipNextChar = False, True ; continue

            if not commentIsOpen: currentLineValue += charValue

        commentsRemovedArray.append(currentLineValue) 

    return [line.strip() for line in commentsRemovedArray if line.strip()], [lineNumberArray[lineNumber] for lineNumber in range(len(lineNumberArray)) if commentsRemovedArray[lineNumber].strip()]

def separateFileSettings(fileArray : list[str]) -> tuple[list[str], list[str]]:
    settingsArr = []
    remainderArr = []
    for line in fileArray: 
        if line[0] == '#': settingsArr.append(line)
        else: remainderArr.append(line)

    return settingsArr, remainderArr

def separateClasses(codeArray: list[str]) -> tuple[list[str], list[str]]:
    classesList = []
    remainderArr = []
    inClassesLines = []
    for lineNumber, line in enumerate(codeArray):
        if lineNumber in inClassesLines: continue
        if line[:6].lower().rstrip() == "class":
            classesList.append([])
            classClosed = False
            for classLineNumber, classLine in enumerate(codeArray[lineNumber:]):
                inClassesLines.append(lineNumber + classLineNumber)
                classesList[-1].append(classLine)
                if classLine[:9].lower().rstrip() == "endclass": classClosed = True ; break
            if not classClosed: print('Reached EOF before class ended') ; exit(1)
        else: remainderArr.append(line)

    return classesList, remainderArr

def separateFunctions(codeArray : list[str]) -> tuple[list[Func], list[str]]:
    functionsList = []
    remainderArr = []
    inFunctionsLines = []

    for lineNumber, line in enumerate(codeArray):
        if lineNumber in inFunctionsLines: continue
        if line[:5].lower().rstrip() == "func":

            functionName, functionParameters, functionReturnType = getFunctionInformations(line)

            currentFunctionCode = []

            functionClosed = False
            for functionLineNumber, functionLine in enumerate(codeArray[lineNumber:]):
                inFunctionsLines.append(lineNumber + functionLineNumber)
                currentFunctionCode.append(functionLine)
                if functionLine[:8].lower().rstrip() == "endfunc": functionClosed = True ; break
            if not functionClosed: print("Reached EOF before function ended") ; exit(1)

            functionsList.append(Func(functionName, functionParameters, functionReturnType, currentFunctionCode))

        else: remainderArr.append(line)

        return functionsList, remainderArr

def getFunctionInformations(functionDefinitionLine : str) -> tuple[str, str, str]:
    functionInformations = functionDefinitionLine[5:]

    functionName = ""
    while functionInformations[:1].lstrip(" "):
        functionName += functionInformations[0]
        functionInformations = functionInformations[1:]

    if not functionName: print("You must specify a function name") ; exit(0)
    
    functionInformations = functionInformations.lstrip()

    functionParameters = ""
    while functionInformations[:2] != "->":
        functionParameters += functionInformations[0]
        functionInformations = functionInformations[1:]

    if not functionParameters: print("You must specify function parameters") ; exit(0)
    functionParameters = splitWithoutStrings(functionParameters, ",")

    functionReturnType = functionInformations[2:].lstrip()
    
    if not functionReturnType: print("You must specify a function return type") ; exit(0)

    return functionName, functionParameters, functionReturnType

############
### Main ###
############

if __name__ == "__main__":
    if len(argv) < 3: print("Not enough inputs!") ; exit(1)
    argv = argv[1:]
    if not path.isfile(argv[0]): print("Input file does not exist") ; exit(1)
    if path.isfile(argv[1]): 
        if input(f"Are you sure you want to delete {argv[1]}? [Y/N]\n").lower() != "y": exit(1)
        
    inputFileArray, inputFileLineNumberArray = getInputFile(argv[0])

    inputFileArray, inputFileLineNumberArray = removeCommentsInFile(inputFileArray, inputFileLineNumberArray)


    settingsArray, codeFileArray = separateFileSettings(inputFileArray)
    del inputFileArray

    classesArray, codeFileArray = separateClasses(codeFileArray)
    functionsArray, codeFileArray = separateFunctions(codeFileArray)

    print(settingsArray, classesArray, functionsArray, codeFileArray, sep=" - ")