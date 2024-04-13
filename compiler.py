def main(sFile, oFile):
    with open(sFile, 'r') as file: tempFileArray = file.readlines()

    sFileArray = []
    skipChar = False
    strOpen = False
    commOpen = False
    strOpenChar = ""
    curLine = ""
    for line in tempFileArray:
        line = line.strip()
        for charPos, char in enumerate(line):
            if skipChar:
                skipChar = False 
                continue
            if not strOpen and not commOpen and char in ["'", '"']:
                strOpenChar = char
                strOpen = True
            elif strOpen and not commOpen and char == strOpenChar: strOpen = False

            if charPos != len(line) - 1:
                if not commOpen and not strOpen and f'{char}{line[charPos+1]}' == '//': break
                elif not commOpen and not strOpen and f'{char}{line[charPos+1]}' == '/*': commOpen, skipChar = True, True
                elif commOpen and not strOpen and f'{char}{line[charPos+1]}' == '*/': commOpen, skipChar = False, True

            if not strOpen and not commOpen and char in ['{', '}']:
                if curLine.strip() != "": sFileArray.append(curLine)
                sFileArray.append(char)
                curLine = ""
                continue

            if not strOpen and not commOpen and char == ";" and curLine[:3] != "for":
                if curLine.strip() != "": sFileArray.append(f'{curLine}{char}')
                curLine = ""
                continue

            if not commOpen: curLine += char

    funcDict = {}
    globalVars = {}
    forbidLines = []

    for lineNumber, line in enumerate(sFileArray):
        if lineNumber in forbidLines: continue
        if line[:4] == "func":
            lineStr = remStr(line)
            funcName = lineStr[4:].split('(', 1)[0].strip()
            funcType = lineStr.split('->')[-1].strip()
            funcArgs = ""

            if funcName in list(funcDict.keys()): 
                if funcType != funcDict[funcName]["type"] or funcArgs != funcDict[funcName]["args"]: 
                    print("error")
                    exit(1)
            else: funcDict[funcName] = {'type' : funcType, 'args' : funcArgs, 'lines' : []}
            opBrack = 1
            forbidLines.append(lineNumber+1)
            for lN, l in enumerate(sFileArray[lineNumber+2:]):
                forbidLines.append(lN+lineNumber+2)
                if l == '{':  opBrack += 1
                elif l == '}': opBrack += -1
                if opBrack == 0: break
                funcDict[funcName]['lines'].append(l)
        else:
            varType = line.split(' ', 1)[0]
            varName = line[:-1].split(' ')[-1]
            if varName in list(globalVars.keys()):
                print("error")
                exit(1)
            globalVars[varName] = {"type": varType}

    if "main" not in list(funcDict.keys()): 
        print("error")
        exit(1)

    didSmt = False
    newArray = []
    newArray.append("global __main__")
    newArray.append("section .data")
    for varName in list(globalVars.keys()):
        newArray.append(f'\t{varName} {globalVars[varName]["type"]}')
    newArray.append("section .text")
    for funcName in list(funcDict.keys()):
        newArray.append(f'__{funcName}__:')
        for line in evalLines(funcDict[funcName]['lines'], f'__{funcName}__'): newArray.append(line)
        if funcName != "main": newArray.append(f'\tret')
        else: 
            newArray.append("\tmov rax, 60")
            newArray.append("\tmov rdi, 0")
            newArray.append("\tsyscall")

    sFileArray = newArray

    print(sFileArray)

    with open(oFile, 'w') as file: 
        for line in sFileArray: file.write(f'{line}\n')

def evalLines(oArray : list, stateName : str) -> list[str]:
    newArray = []
    forNumber = 0
    forbidLines = []
    
    for line in oArray: 
        if line[:3] == "for":
            if '(' not in line: 
                print("error")
                exit(1)
            forArgs = line.split('(', 1)[1]
            forArgs = [forArgs[:remStr(forArgs).index(';')+1].strip(), forArgs[remStr(forArgs).index(';')+1:]]
            forArgs= [forArgs[0], forArgs[1][:remStr(forArgs[1]).index(';')+1].strip(), forArgs[1][remStr(forArgs[1]).index(';')+1:]]
            forArgs = [forArgs[0], forArgs[1], forArgs[2][:remStr(forArgs[2]).index(')')].strip()] #Il doit y avoir un problème ! On retrouve les paranthèses dans les calculs !
            newArray.append(f'\t{forArgs[0]}')
            newArray.append(f'{stateName}for__{forNumber}:')
            newArray.append(f'\t{forArgs[1]}')
            forNumber += 1
            #ici marquer les lignes
        else: newArray.append(f'\t{line}')

    return newArray

def remStr(oriStr) -> str:
    retStr = ""
    strOpen = False
    strOpenChar = ""
    for char in oriStr:
        if not strOpen and char in ["'", '"']:
            strOpenChar = char
            strOpen = True
            retStr += char
            continue
        elif strOpen and char == strOpenChar: strOpen = False

        if strOpen: retStr += " "
        else: retStr += char

    return retStr


if __name__ == "__main__":

    main('file.cpl', 'oFile.asm')