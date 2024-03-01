from sys import argv
from os import mkdir, path
from shutil import rmtree
import verify

def getKeyword(line : str) -> str:
    keyword = line.split(' ', 1)[0].split('(', 1)[0]
    return keyword

def getFile(path : str) -> list[str]:
    file = open(path, "r")
    fileArray = []
    keywordArray = []
    ignoreNextChar = False
    currentLine = ''
    commentOpened = False
    stringOpened = False
    stringOpenedChar = ''
    for line in file:
        line = line.rstrip() + ' '
        for charPos, char in enumerate(line[:-1]):
            if ignoreNextChar:
                ignoreNextChar = False
                continue
            elif not stringOpened and not commentOpened and char in ["'", '"']:
                stringOpened = True
                stringOpenedChar = char
            elif stringOpened and not commentOpened and char == stringOpenedChar:
                stringOpened = False
            elif not commentOpened and not stringOpened and char == '/' and line[charPos+1] == '/':
                break
            elif not commentOpened and not stringOpened and char == '/' and line[charPos+1] == '*':
                commentOpened = True
                ignoreNextChar = True
            elif commentOpened and not stringOpened and char == '*' and line[charPos+1] == '/':
                commentOpened = False
                ignoreNextChar = True
            elif not stringOpened and not commentOpened and char in [';', '{', '}']:
                fileArray.append(f"{currentLine}{char}")
                keywordArray.append(getKeyword(currentLine))
                getattr(verify, f'keyword_{keywordArray[-1]}')
                currentLine = ''
                continue
            if not commentOpened:
                currentLine += char
    if currentLine.strip() != '':
        exit(1)
    return [fileArray, keywordArray]

if __name__ == "__main__":
    if len(argv) != 3:
        exit(1)
    fileArray = getFile(argv[1])
    keywordArray, fileArray = fileArray[1], fileArray[0]
    if path.exists("./CcpCompileFolder"):
        rmtree("./CcpCompileFolder")
    mkdir("./CcpCompileFolder")
    inBlockCode = False
    currentCodeBlock = {"name" : "main", "type" : "func"}
    dataFile = open(f"./CcpCompileFolder/main.func", 'a')
    for lineNumber, line in enumerate(fileArray):
        keyword = keywordArray[lineNumber]
        if keyword in ["func", "class"]:
            pass
        else:
            dataFile.write(line+'\n')