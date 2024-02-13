#include <stdio.h>
#include <stdlib.h>

void error(char[], int, int);
void getFile(char[]);
int getNumberOfLinesFile(char[]);

int main(){
    getFile("../code.icpl");
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

void getFile(char path[]){
    int numberOfLines = getNumberOfLinesFile(path);
    char data[numberOfLines][1000];
    FILE *file = fopen(path, "r");
    for (int i = 0; i < 3; i++){
        printf("%i", i);
    }
    printf("%i", i);

}

void error(char message[], int errorCode, int lineNumber){
    printf("Error Line n°%i : %s", lineNumber, message);
    exit(1);
}