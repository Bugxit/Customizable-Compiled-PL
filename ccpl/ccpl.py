import api

def getFunc(file : dict):
    forbiddenLines = []
    oneFunc = False
    returnFile = {}
    for keyNumber, lineNumber in enumerate(file.keys()):
        if lineNumber not in forbiddenLines:
            splitedLine = file[lineNumber].split(" ", 2)
            if splitedLine[0] == "function":
                openedParentheses = 1
                breaker = False
                forbiddenLines = [lineNumber]
                funcDict = {}
                for checkLineNumber in list(file.keys())[keyNumber+1:]:
                    for letter in file[checkLineNumber]:
                        if letter == "{":
                            openedParentheses += 1
                        elif letter == "}" and openedParentheses != 1:
                            openedParentheses -= 1
                        elif letter == "}" and openedParentheses == 1:
                            breaker = True
                            openedParentheses = 0
                            lastLine = checkLineNumber
                            break
                    forbiddenLines.append(checkLineNumber)
                    funcDict[checkLineNumber] = file[checkLineNumber][4:]
                    if breaker:
                        break
                if funcDict[lastLine] == "" or funcDict[lastLine].lstrip() == "}":
                    funcDict.pop(lastLine)
                elif funcDict[lastLine][-1] == "}":
                    funcDict[lastLine] = funcDict[lastLine][:-1]
                else:
                    api.error("A function can only end at the end of a line")
                funcInfos[splitedLine[1]] = {"args" : []}
                funcInfos[splitedLine[1]]["algo"] = funcDict

                splitedLine[2] = splitedLine[2].replace(" ", "")
                splitedLine[2] = splitedLine[2][1:][:-2].split(",")
                for var in splitedLine[2]:
                    if ":" in var:
                        splitedVar = var.split(":", 1)
                    else:
                        splitedVar = [var, "let"]
                    funcInfos[splitedLine[1]]["args"].append({"type" : splitedVar[1], "name" : splitedVar[0]})

                oneFunc = True
    for lineNumber in file.keys():
        if lineNumber not in forbiddenLines:
            returnFile[lineNumber] = file[lineNumber]
    if oneFunc:
        return returnFile
    else:
        return None

def getCodeFile(fileName : str, filePath : str | None = '') -> dict:
    global funcInfos
    funcInfos = {}
    finalFile = {}
    with open(f'{filePath}{fileName}.ccpl') as codeFile:
        codeFile = codeFile.readlines()
    for lineNumber, line in enumerate(codeFile):
        line = line.rstrip()
        if line not in ['', '\n'] and (line.lstrip())[:2] != '//':
            if line[-1:] == '\n':
                finalFile[lineNumber+1] = line[:-1]
            else:
                finalFile[lineNumber+1] = line
    while True:
        newFinalFile = getFunc(finalFile)
        if newFinalFile == None:
            break
        else:
            finalFile = newFinalFile

    return finalFile 

if __name__ == "__main__":
    codeFile = getCodeFile('code')
    api.getInfos(funcInfos)
    api.executeFile(codeFile, 'global')