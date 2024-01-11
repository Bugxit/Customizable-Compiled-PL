from os import system

def getFile(file : str):
    lineList = [""]

    with open(f'{file}') as file:
        lastLineReturn = False
        for line in file.readlines():
            if lastLineReturn:
                lineList.append(line)
            else:
                lineList[-1] += line
            if line[-1:] == "\n":
                lastLineReturn = True
                lineList[-1] = lineList[-1][:-1]
            else:
                lastLineReturn = False
    lineList[:] = (line for line in lineList if line != "")
    return lineList

def getKeyword(line : str):
    if line != line.lstrip():
        print('Error : getKeyword')
        exit()
    firstWord = line.split(" ", 1)[0]
    if firstWord in keywordList or firstWord:
        return firstWord

def exec(linesToExecute : list, func : str):
    for line in linesToExecute:
        globals()[line[0]](line[1], func)

def replaceWithVar(string : str, func : int):
    for variable in funcDict[func][1]:
        if str("{" + variable[0] + "}") in string:
            string = str(string.replace(str("{" + variable[0] + "}"), str(variable[1])))
    return string

def write(line : str, func : str):
    splitedLine = line.split(" ", 1)
    if splitedLine[0] != "write" or splitedLine[1][0] != '"' or splitedLine[1][-2:] != '";':
        print("Error : write")
        exit()
    print(replaceWithVar(splitedLine[1][1:][:-2], func))

def stringToList(string : str) -> list:
    if (string[0], string[-1]) == ("[", "]"):
        newList = string[1:][:-1].split(",")
    else:
        print("Error : stringToList")
        exit()
    return newList  
 
def let(line : str, func : str):
    splitedLine = line.split(" ", 5)
    if splitedLine[0] != "let" or splitedLine[2] != ":" or splitedLine[3] not in typeList or splitedLine[4] != "=" or splitedLine[5][-1] != ";":
        print("Error : let")
        exit()
    variableExistsAlready = False
    for variableTest in funcDict[func][1]:
        if variableTest[0] == splitedLine[1]:
            variableExistsAlready = True
            break
    if not variableExistsAlready and splitedLine[3] != "list":
        funcDict[func][1].append([splitedLine[1], replaceWithVar(splitedLine[5][:-1], func), splitedLine[3]])
    elif not variableExistsAlready:
        variableValue = stringToList(splitedLine[5][:-1])
        for position, tryToReplace in enumerate(variableValue):
            variableValue[position] = replaceWithVar(tryToReplace, func)
        funcDict[func][1].append([splitedLine[1], variableValue, splitedLine[3]])
    else:
        print("Error : You initialize twice the same variable")
        exit()

def const(line : str, func : str):
    splitedLine = line.split(" ", 5)
    if splitedLine[0] != "const" or splitedLine[2] != ":" or splitedLine[3] not in typeList or splitedLine[4] != "=" or splitedLine[5][-1] != ";":
        print("Error : const")
        exit()
    variableExistsAlready = False
    for variableTest in funcDict[func][1]:
        if variableTest[0] == splitedLine[1]:
            variableExistsAlready = True
            break
    if not variableExistsAlready and splitedLine[3] != "list":
        funcDict[func][1].append([splitedLine[1], replaceWithVar(splitedLine[5][:-1], func), splitedLine[3]])
    elif not variableExistsAlready:
        variableValue = stringToList(splitedLine[5][:-1])
        for position, tryToReplace in enumerate(variableValue):
            variableValue[position] = replaceWithVar(tryToReplace, func)
        funcDict[func][1].append([splitedLine[1], variableValue, splitedLine[3]])
    else:
        print("Error : You initialize twice the same constant")
        exit()

def variableIndex(varName : str, func : str):
    variableIndex = None
    for variableIndexTest, variableTest in enumerate(funcDict[func][1]):
        if variableTest[0] == varName:
            variableIndex = variableIndexTest
            break 
    return variableIndex

def var(line : str, func : str):
    splitedLine = line.split(" ", 3)
    if splitedLine[0] != "var" or splitedLine[2] not in ["=", "+=", "*=", "/="] or splitedLine[3][-1] != ";":
        print("Error : var")
        exit()
    variableIndex = None
    for variableIndexTest, variableTest in enumerate(funcDict[func][1]):
        if variableTest[0] == splitedLine[1] and type(variableTest) != type((1,1)):
            variableIndex = variableIndexTest
            break 
    if variableIndex == None:
        print(f"Error : variable {splitedLine[1]} does not exist or is not changeable")
        exit()
    if splitedLine[2] == "=" and funcDict[func][1][variableIndex][2] == "str":
        tempResult = splitedLine[3][:-1]
    elif splitedLine[2] == "=" and funcDict[func][1][variableIndex][2] in ["int", "float"]:
        tempResult = float(splitedLine[3][:-1])
    elif funcDict[func][1][variableIndex][2] == "str" and splitedLine[2] == "+=":
        tempResult = funcDict[func][1][variableIndex][1]+splitedLine[3][:-1]
    elif funcDict[func][1][variableIndex][2] == "list" and splitedLine[2] == "+=":
        tempResult = funcDict[func][1][variableIndex][1]+stringToList(splitedLine[3][:-1])
    elif funcDict[func][1][variableIndex][2] != "str" and splitedLine[2] == "+=":
        tempResult = float(funcDict[func][1][variableIndex][1]) + float(splitedLine[3][:-1])
    elif funcDict[func][1][variableIndex][2] != "str" and splitedLine[2] == "*=":
        tempResult = float(funcDict[func][1][variableIndex][1]) * float(splitedLine[3][:-1])
    elif funcDict[func][1][variableIndex][2] != "str" and splitedLine[2] == "/=":
        tempResult = float(funcDict[func][1][variableIndex][1]) / float(splitedLine[3][:-1])
    else:
        print("Error : var")
        exit()
    if funcDict[func][1][variableIndex][2] == "int":
        tempResult = int(tempResult)
    if funcDict[func][1][variableIndex][2] != "list":
        funcDict[func][1][variableIndex][1] = str(tempResult)
    else:
        funcDict[func][1][variableIndex][1] = tempResult

def call(line : str, func : str):
    splitedLine = line.split(" ", 2)
    if splitedLine[0] != "call" or splitedLine[2][-1] != ";":
        print("Error : call")
        exit()
    requiredVariableInput = splitedLine[2][:-1].split(",", len(funcDict[splitedLine[1]][2]))
    for numberVariable, requiredVariable in enumerate(funcDict[splitedLine[1]][2]):
        funcDict[splitedLine[1]][1].append([requiredVariable[0], requiredVariableInput[numberVariable], requiredVariable[1]])
    exec(refactorLines(funcDict[splitedLine[1]][0]), splitedLine[1])
    funcDict[func][1] = []

def refactorLines(file : list):
    refactoredLines = []
    forbiddenLines = []
    for lineNumber, line in enumerate(file):
        if lineNumber not in forbiddenLines:
            keyword = getKeyword(line)
            if keyword == "fn":
                splitedLineFunc = line.split(" ", 2)
                if splitedLineFunc[0] != "fn" and splitedLineFunc[2][-1] != ":":
                    print("Error : fn")
                    exit()
                funcDict[splitedLineFunc[1]] = [[], [], []]
                if splitedLineFunc[2][:-1].split(",") != ['']:
                    for requiredVar in splitedLineFunc[2][:-1].split(","):
                        splitedRequiredVar = requiredVar.split(" ", 2)
                        if splitedRequiredVar[1] != ":" or splitedRequiredVar[2] not in typeList:
                            print("Error : fn")
                            exit()
                        funcDict[splitedLineFunc[1]][2].append([splitedRequiredVar[0], splitedRequiredVar[2]])
                for newLineNumber, newLine in enumerate(file[lineNumber+1:]):
                    if newLine.lstrip() != newLine and (len(newLine)-len(newLine.lstrip()))%4 == 0:
                        funcDict[splitedLineFunc[1]][0].append(newLine[4:]) 
                        forbiddenLines.append(newLineNumber+lineNumber+1)
                    else:
                        break
            else:
                refactoredLines.append([keyword, line])
    return refactoredLines

def glob(line : str, func : str):
    splitedLine = line.split(" ", 1)
    if splitedLine[0] != "glob" or splitedLine[1][-1] != ";":
        print("Error : glob")
        exit()
    variableList = splitedLine[1].split(",")
    variableList[-1] = variableList[-1][:-1]
    for variable in variableList:
        if variableIndex(variable, func) != None:
            funcDict[func][1].pop(variableIndex(variable, func))
        funcDict[func][1].append(funcDict["global"][1][variableIndex(variable, "global")])

if __name__ == "__main__":
    keywordList = ["write", "let", "const", "var", "global"]
    typeList = ["int", "str", "float", "list"]
    userCommand = input('Enter a command:\n')
    system("clear")
    if userCommand[:4] == "run ":
        funcDict = {
            "global": [[], [], []]
        }
        file = getFile(userCommand[4:])
        refactoredLines = refactorLines(file)
        exec(refactoredLines, "global")
