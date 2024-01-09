from os import system

def main():
    global variableList
    userCommand = input('Enter a command:\n')
    if userCommand[:4] == "run ":
        system("cls")
        file = getFile(userCommand[4:])
        variableList = []
        for line in file:
            keyword = getKeyword(line, 0)
            if keyword in keywordList:
                globals()[keyword](line)
            elif keyword[0] == "Error":
                print(keyword[1])
                exit()
    
def getFile(file : str):
    lineList = [""]

    with open(f'{file}') as file:
        for line in file.readlines():
            if line[-1:] == "\n":
                lineList.append(line[:-1])
            else:
                lineList[-1] += line
    if lineList[0] == "":
        lineList = lineList[1:]
    
    return lineList

def getKeyword(line : str, tabulationNumber : int):

    for position in range(tabulationNumber*4):
        if line[position] != " ":
            return ["Error", f"Line X: Missing a tabulation"]
    line = line[tabulationNumber*4:]

    tempKeyword = ""

    for letter in line:
        if letter not in [" ", ";"]:
            tempKeyword += letter
        elif tempKeyword in keywordList:
            return tempKeyword

    return ["Error", f"Line X : Line not complete"]

def write(line : str):
    if line[:6] != "write ":
        return ["Error", f"Line X : syntax error"]
    elif (line[6] == '"' or line[6]+line[7] == 'f"') and line[-2:] == '";':
        print(line[7:][:-2])
    else:
        print("error")
    
def let(line : str):
    simplifiedLine = line.split(" ")
    if simplifiedLine[0] != "let" or simplifiedLine[1] != ":" or simplifiedLine[4] != "=" or simplifiedLine[5][-1] != ";":
        return ["Error", f"Line X : syntax error"]
    else:
        variableList.append([simplifiedLine[3], simplifiedLine[5][:-1], simplifiedLine[2]])



if __name__ == "__main__":
    keywordList = ["write", "let"]
    exec = main()
    print(variableList)
    if exec != None:
        print("Comming soon!")