#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

void error(char[], int, int);
void simplifyFile(char[], char[]);
int getNumberOfLinesFile(char[]);
void writeFileWithoutComments(char[][1000], char[], int);

int main(){
    simplifyFile("code.icpl", "simpcode.icpl");
}

int getNumberOfLinesFile(char path[]){
    FILE *file = fopen(path, "r");
    if (file == NULL) error("Could not open the file\n", 0,-1);
    int numberOfLines = 1;
    char c;
    do {
        c = fgetc(file);
        if (c == '\n') numberOfLines++;
    } while (c != EOF && numberOfLines != 2147483647);
    if (numberOfLines == 2147483647) error("File too long... HOW DID YOU WRITE 2147483647 LINES?\n", 0, -1);
    fclose(file);
    return numberOfLines;
}

void writeFileWithoutComments(char file[][1000], char destination[], int oldFileLineNumber){
    if (access(destination, F_OK) == 0) remove(destination);
    FILE *simplifiedFile = fopen(destination, "w");
    bool stringOpened = false;
    bool commentOpened = false;
    bool ignoreNextChar = false;
    int zeroToWrite;
    int maxZero = floor(log10(oldFileLineNumber));
    for (int lineNumber = 0; lineNumber < oldFileLineNumber; lineNumber++){
        zeroToWrite = (lineNumber != 0) ? maxZero - floor(log10(lineNumber)) : maxZero;
        printf("%d", zeroToWrite);
        for (int zeroRequired = 0; zeroRequired < zeroToWrite; zeroRequired++){fprintf(simplifiedFile, "0");}
        fprintf(simplifiedFile, "%d -", lineNumber+1);
        for (int charNumber = 0; charNumber < strlen(file[lineNumber]); charNumber++){
            if (!commentOpened && file[lineNumber][charNumber] == '\"') stringOpened = !stringOpened;
            if (!stringOpened && !commentOpened && file[lineNumber][charNumber] == '/' && file[lineNumber][charNumber+1] == '/') break;
            if (!stringOpened && !commentOpened && file[lineNumber][charNumber] == '/' && file[lineNumber][charNumber+1] == '*') commentOpened = true;
            if (commentOpened && file[lineNumber][charNumber] == '/' && file[lineNumber][charNumber+1] == '*') commentOpened = false, ignoreNextChar = true;
            if (file[lineNumber][charNumber] == '\n') break;
            if (!commentOpened && !ignoreNextChar){
                fprintf(simplifiedFile, "%c", file[lineNumber][charNumber]);
                ignoreNextChar = false;
            }
        }
    fprintf(simplifiedFile, "\n");
    }
    fclose(simplifiedFile);
}

void simplifyFile(char path[], char destination[]){
    FILE *oldFile = fopen(path, "r");
    if (oldFile == NULL) error("Could not open the original file\n", 0,-1);
    int oldFileLineNumber = getNumberOfLinesFile(path);
    int lineNumber = 0;
    char fileArray[oldFileLineNumber][1000];
    while (!feof(oldFile) && !ferror(oldFile)){
        fgets(fileArray[lineNumber], 1000, oldFile);
        lineNumber++;
    }
    fclose(oldFile);
    writeFileWithoutComments(fileArray, destination, oldFileLineNumber);
}


void error(char message[], int errorCode, int lineNumber){
    printf("Error Line n°%i : %s", lineNumber, message);
    exit(1);
}
