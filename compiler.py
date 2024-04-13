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
    forbidLines = []

    for lineNumber, line in enumerate(sFileArray):
        if lineNumber in forbidLines: continue
        if line[:4] == "func":
            lineStr = remStr(line)
            funcName = lineStr[4:].split('(', 1)[0].strip()
            funcType = lineStr.split('->')[-1].strip()
            funcArgs = ""

            if funcName in list(funcDict.keys()): 
                if funcType != funcDict[funcName]["type"] or funcArgs != funcDict[funcName]["args"]: exit(1)
            else: funcDict[funcName] = {'type' : funcType, 'args' : funcArgs, 'lines' : []}
            opBrack = 1
            for l in sFileArray[lineNumber+2:]:
                if l == '{':  opBrack += 1
                elif l == '}': opBrack += -1
                if opBrack == 0: break
                funcDict[funcName]['lines'].append(l)

    if "main" not in list(funcDict.keys()): exit(1)

    with open(oFile, 'w') as file:
        file.write("global __func__main:")
        for line in sFileArray: file.write(f'{line}\n') 

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