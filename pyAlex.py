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
    if firstWord in keywordList:
        return firstWord
    
def exec(linesToExecute : list, func : str):
    for line in linesToExecute:
        globals()[line[0]](line[1], func)

def write(line : str, func : str):
    splitedLine = line.split(" ", 1)
    if splitedLine[0] != "write" or splitedLine[1][0] != '"' or splitedLine[1][-2:] != '";':
        print("Error : write")
        exit()
    textToPrint = splitedLine[1][1:][:-2]
    for variable in funcDict[func][1]:
        if str("{" + variable[0] + "}") in textToPrint:
            textToPrint = textToPrint.replace(str("{" + variable[0] + "}"), variable[1])
    print(textToPrint)
    
def let(line : str, func : str):
    splitedLine = line.split(" ")
    if splitedLine[0] != "let" or splitedLine[2] != ":" or splitedLine[4] != "=" or splitedLine[5][-1] != ";":
        print("Error : let")
        exit()
    else:
        funcDict[func][1].append([splitedLine[1], splitedLine[5][:-1], splitedLine[3]])



if __name__ == "__main__":
    keywordList = ["write", "let"]
    userCommand = input('Enter a command:\n')
    system("clear")
    if userCommand[:4] == "run ":
        funcDict = {
            "global": [[], []]
        }
        file = getFile(userCommand[4:])
        refactoredLines = []
        for line in file:
            keyword = getKeyword(line)
            refactoredLines.append([keyword, line])
        exec(refactoredLines, "global")
