import api

def getInfoFile(fileName : str, type : str) -> dict[dict, dict]:
    infoFileDict = {
        "keywordInfo" : {},
        "infoKeyword" : {},
        "infoLenght" : {},
    }
    if type == 'grammar':
        infoList = ['write', 'int']
    elif type == 'settings':
        infoList = ['endLine', 'comments']
    with open(f'{fileName}.ccpl') as infoFile:
        infoFile = infoFile.readlines()
    for line in infoFile:
        if line[-1:] == "\n":
            line = line[:-1]
        splitedLine = line.split(" ", 4)
        if splitedLine[0] in infoList and splitedLine[1] == ":=" and (type != 'settings' or (splitedLine[3] == '->' and int(splitedLine[4]) == len(splitedLine[2]))):
            infoFileDict["keywordInfo"][splitedLine[2]] = splitedLine[0]
            infoFileDict["infoKeyword"][splitedLine[0]] = splitedLine[2]
            if type == 'settings':
                infoFileDict["infoLenght"][splitedLine[0]] = int(splitedLine[4])

    return infoFileDict

def getCodeFile(fileName : str, filePath : str | None = '') -> list:
    finalFile = {}
    with open(f'{filePath}{fileName}.ccpl') as codeFile:
        codeFile = codeFile.readlines()
    for lineNumber, line in enumerate(codeFile):
        line = line.rstrip()
        if line not in ['', '\n'] and (line.lstrip())[:settingsDict['infoLenght']['comments']] != settingsDict['infoKeyword']['comments']:
            if line[-1:] == '\n':
                finalFile[lineNumber+1] = line[:-1]
            else:
                finalFile[lineNumber+1] = line

    return finalFile 

def executeFile(file : list) -> None:
    for lineNumber in file.keys():
        keyword = api.getKeyword(file[lineNumber], lineNumber)
        getattr(api, 'keyword_' + keyword)

if __name__ == "__main__":
    grammarDict = getInfoFile('grammar', 'grammar')
    settingsDict = getInfoFile('settings', 'settings')
    api.getInfos(grammarDict, settingsDict)
    codeFile = getCodeFile('code')
    executeFile(codeFile)