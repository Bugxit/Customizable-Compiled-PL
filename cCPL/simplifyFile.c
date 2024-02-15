#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>

void error(char[], int, int);
int getNumberOfLines(FILE*);
void simplifyFile(char[], char[]);
char * trimEnd(char[]);

int main(){
    simplifyFile("code.icpl", "simpcode.icpl");
}

void error(char message[], int errorCode, int lineNumber){
    printf("Error Line n°%i : %s", lineNumber, message);
    exit(1);
}

int getNumberOfLines(FILE *file){
    int numberOfLines = 1;
    char c;
    do {
        c = fgetc(file);
        if (c == '\n') numberOfLines++;
    } while (c != EOF && numberOfLines != 2147483647);
    if (numberOfLines == 2147483647) error("File too long.\n", 0, -1);
    fclose(file);
    return numberOfLines;
}

void simplifyFile(char source[], char destination[]){
    FILE *sourceFile = fopen(source, "r");
    if (sourceFile == NULL) error("Could not open the original file\n", 0,-1);
    int sourceLineNumber = getNumberOfLines(sourceFile);
    
    int lineNumber = 0;
    char fileArray[sourceLineNumber][1000];
    while (!feof(sourceFile) && !ferror(sourceFile)){
        fgets(fileArray[lineNumber], 1000, sourceFile);
        lineNumber ++;
    }
    fclose(sourceFile);

    if (access(destination, F_OK) == 0) remove(destination);
    FILE *destinationFile = fopen(destination, "w");
    char currentLine[1000];
    bool commentOpened = false;
    bool stringOpened = false;
    bool ignoreNextChar = false;
    for (lineNumber = 0; lineNumber < sourceLineNumber; lineNumber++){
        strcpy(currentLine, trimEnd(fileArray[lineNumber]));
        if (currentLine[0] == '\0' || currentLine[0] == '\n') continue;
        for (int charNumber = 0; charNumber < strlen(currentLine); charNumber++){
            if (!commentOpened && currentLine[charNumber] == '\"') stringOpened = !stringOpened;
            if (!stringOpened && !commentOpened && currentLine[charNumber] == '/' && currentLine[charNumber+1] == '/') break;
            if (!stringOpened && !commentOpened && currentLine[charNumber] == '/' && currentLine[charNumber+1] == '*') commentOpened = true;
            if (commentOpened && currentLine[charNumber] == '*' && currentLine[charNumber+1] == '/') commentOpened = false, ignoreNextChar = true;
            if (currentLine[charNumber] == '\n') break;
            if (!commentOpened && !ignoreNextChar) putc(currentLine[charNumber], destinationFile);
            ignoreNextChar = false;
        }
    }
}

char * trimEnd(char string[1000]){
    bool returnIn = false;
    for (int charNumber = strlen(string)-1; charNumber >= 0; charNumber--){
        if (string[charNumber] == '\n') returnIn = true;
        if (string[charNumber] != '\0' && string[charNumber] != ' ' && string[charNumber] != '\n') break;
        if (returnIn && charNumber != 1000){string[charNumber] = '\n', string[charNumber+1] = '\0';} else {string[charNumber] = '\0';}
    }
    return string;
}
