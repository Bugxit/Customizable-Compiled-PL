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
        if line[:5] == "func ":                
            lineStr = remStr(line)
            opBrack = 0
            brackAlrdOpen = False
            funcName, funcArgs, argsFn = "", "", -1
            for cN, char in enumerate(lineStr[5:]):
                if char == '(': opBrack, brackAlrdOpen = opBrack + 1, True
                elif char == ')': opBrack += -1
                if not brackAlrdOpen: funcName += line[cN+5]
                else: funcArgs += line[cN+5]
                if opBrack == 0 and brackAlrdOpen: 
                    argsFn = cN+5
                    break
            if opBrack != 0 or not brackAlrdOpen: exit(1)
            funcName = funcName.strip()
            if opBrack != 0 or '(' not in lineStr[5:]: exit(1)

            funcType = line[argsFn+1:].strip()
            if funcType[:2] != "->": exit(1)
            funcType = funcType[2:].strip()

            funcArgs = [funcArgs]
            while ',' in remStr(funcArgs[-1]):
                remArgs = remStr(funcArgs[-1])
                funcArgs.append(funcArgs[-1][remArgs.index(",")+1:])
                funcArgs[-2] = funcArgs[-2][:remArgs.index(",")]

            if funcName in list(funcDict.keys()) and (funcType != funcDict[funcName]["type"] or funcArgs != funcDict[funcName]["args"]): 
                print("error")
                exit(1)
            elif funcName not in list(funcDict.keys()): funcDict[funcName] = {'type' : funcType, 'args' : funcArgs, 'lines' : []}
            opBrack = 1
            forbidLines.append(lineNumber+1)
            for lN, l in enumerate(sFileArray[lineNumber+2:]):
                forbidLines.append(lN+lineNumber+2)
                if l == '{':  opBrack += 1
                elif l == '}': opBrack += -1
                if opBrack == 0: break
                funcDict[funcName]['lines'].append(l)
        else:
            pass
            """
            varType = line.split(' ', 1)[0]
            varName = line[:-1].split(' ')[-1]
            if varName in list(globalVars.keys()):
                print("error")
                exit(1)
            globalVars[varName] = {"type": varType}
            """

    if "main" not in list(funcDict.keys()): 
        print("error")
        exit(1)

    print(funcDict)

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
            newArray.append("\tmov rdi, [rsp+8]")
            newArray.append("\tsyscall")

    sFileArray = newArray

    with open(oFile, 'w') as file: 
        for line in sFileArray: file.write(f'{line}\n')

def evalLines(oArray : list, stateName : str) -> list[str]:
    retArray = []
    forNumber = 0
    forbidLines = []
    
    for lN, line in enumerate(oArray): 
        if line[:3] == "for":
            forArgs = line.split('(', 1)[1].rsplit(')', 1)[0]
            forArgs = [forArgs[:remStr(forArgs).index(';')+1].strip(), forArgs[remStr(forArgs).index(';')+1:]]
            forArgs = [forArgs[0], forArgs[1][:remStr(forArgs[1]).index(';')+1].strip(), forArgs[1][remStr(forArgs[1]).index(';')+1:]]
            retArray.append(f'\t{forArgs[0]}')
            retArray.append(f'{stateName}for__{forNumber}:')
            retArray.append(f'\t{forArgs[1]}')
            forNumber += 1
            for line in oArray[lN:]: pass #Check lines in for loop
        else: retArray.append(f'\t{line}')

    return retArray

def remStr(oriStr) -> str:
    retStr = ""
    strOpen = False
    strOpenChar = ""
    for char in oriStr:
        if not strOpen and char in ["'", '"']:
            strOpenChar, strOpen = char, True
            retStr += char
            continue
        elif strOpen and char == strOpenChar: strOpen = False

        if strOpen: retStr += " "
        else: retStr += char

    return retStr

if __name__ == "__main__":
    main('file.cpl', 'oFile.asm')