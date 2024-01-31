def getInfos(grammar : dict, settings : dict) -> None:
    global grammarDict, settingsDict
    grammarDict, settingsDict = grammar, settings

def error(message : str, lineNumber : int | None = 'Not specified') -> None:
    print(f'Error LN°{lineNumber} -> {message}')
    exit()

def getKeyword(line : str, lineNumber : int | None = 'Not specified') -> str:
    splitedLine = line.split(" ", 1)
    print(line[-settingsDict['infoLenght']['endLine']:])
    if splitedLine[0] in grammarDict['keywordInfo'].keys() and line[-settingsDict['infoLenght']['endLine']:] != settingsDict['infoKeyword']['endLine']:
        return splitedLine[0]
    else:
        error('Keyword used does not exist', lineNumber)