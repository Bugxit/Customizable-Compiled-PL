#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

void error(char[], int, int);
void simplifyFile(char[], char[]);
int getNumberOfLinesFile(char[]);
char * removeString(char[]);

int main(){
    simplifyFile("code.icpl", "simpcode.icpl");
}

int getNumberOfLinesFile(char path[]){
    FILE *file = fopen(path, "r");
    if (file == NULL) error("Could not open the file", 0,-1);
    int numberOfLines = 1;
    char c;
    do {
        c = fgetc(file);
        if (c == '\n') numberOfLines++;
    } while (c != EOF && numberOfLines != 2147483647);
    if (numberOfLines == 2147483647) error("File too long... HOW DID YOU WRITE 2147483647 LINES?", 0, -1);
    fclose(file);
    return numberOfLines;
}

void simplifyFile(char path[], char destination[]){
    FILE *oldFile = fopen(path, "r");
    if (oldFile == NULL) error("Could not open the original file", 0,-1);
    if (access(destination, F_OK) == 0) remove(destination);
    FILE *simplifiedFile = fopen(destination, "w");
    int oldFileLineNumber = getNumberOfLinesFile(path);
    int lineNumber = 0;
    char currentLine[1000];
    bool isToIgnore;
    while (!feof(oldFile) && !ferror(oldFile)){
        currentLine[0] = '\0';
        isToIgnore = true;
        fgets(currentLine, 1000, oldFile);
        for (int i = 0; i < strlen(currentLine); i++){
            if (!isspace(currentLine[i]) && currentLine[i] != EOF){
                isToIgnore = false;
                break;
            }
        }
        if (isToIgnore == 0) fprintf(simplifiedFile, "%i-%s",lineNumber, currentLine);
        lineNumber++;
    }
    fclose(oldFile);
    fclose(simplifiedFile);
}

char * removeString(char line[]){
    return line;
}
void error(char message[], int errorCode, int lineNumber){
    printf("Error Line n°%i : %s", lineNumber, message);
    exit(1);
}
