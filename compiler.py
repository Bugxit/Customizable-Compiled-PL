from sys import argv
from os import path

def getInputFile(filePath : str) -> list[str]:
    with open(filePath, "r") as inputFile: fileArray =  inputFile.readlines()
    
    if fileArray == -1: print("An error occured while reading the file") ; exit(1)

    return [line.strip() for line in fileArray if line.strip()]

def splitFileSettings(fileArray : list[str]) -> list[str]:
    settingsArr = []
    remainderArr = []
    for line in fileArray: 
        if line[0] == '#': settingsArr.append(line)
        else: remainderArr.append(line)

    return settingsArr, remainderArr

def separateClasses(codeArray: list[str]) -> list[str]:
    classesList = []
    remainderArr = []
    inClassesLines = []
    for lineNumber, line in enumerate(codeArray):
        if lineNumber in inClassesLines: continue
        if line[:5].lower() == "class":
            classesList.append([])
            classClosed = False
            for classLineNumber, classLine in enumerate(codeArray[lineNumber:]):
                inClassesLines.append(lineNumber + classLineNumber)
                classesList[-1].append(classLine)
                if classLine[:8].lower() == "endclass": classClosed = True ; break
            if not classClosed: print("Classe did not end before file") ; exit(1)
        else: remainderArr.append(line)

    return classesList, remainderArr

if __name__ == "__main__":
    if len(argv) < 3: print("Not enough inputs!") ; exit(1)
    argv = argv[1:]
    if not path.isfile(argv[0]): print("Input file does not exist") ; exit(1)
    if path.isfile(argv[1]): 
        if input(f"Are you sure you want to delete {argv[1]}? [Y/N]\n").lower() != "y": exit(1)
        
    inputFileArray = getInputFile(argv[0])

    settingsArray, codeFileArray = splitFileSettings(inputFileArray)
    del inputFileArray

    classesArray, codeFileArray = separateClasses(codeFileArray)

    print(settingsArray, classesArray, codeFileArray, sep=" - ")