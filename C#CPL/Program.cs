using System.Configuration.Assemblies;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Threading.Tasks.Dataflow;

/*
Main Functions :
*/

Dictionary<string, string> getCodeFile(string path = "../code.icpl"){
    string[] rawFile = File.ReadAllLines($"{path}");
    Dictionary<int, string> finalFile = new Dictionary<int, string>();
    for (int index = 0; index < rawFile.Length; index++){
        if (!string.IsNullOrWhiteSpace(rawFile[index]) && rawFile[index].Substring(0, 2) != "//"){
            finalFile.Add(index+1, rawFile[index].TrimEnd());
        }
    }
    return finalFile;
}

void executeFile(Dictionary<string, string> file, string function = "main"){
    foreach (KeyValuePair<string, string> line in file){
        string keyword = getKeyword(line);
        callKeyword(keyword, line.Value, function, line.Key);
    }
}

string getKeyword(KeyValuePair<string, string> line){
    string[] keywords = {"write"};
    Dictionary<string, char> endMarkKeywords = new Dictionary<string, char> {{"write", ';'}};
    string[] splitedLine = line.Value.Split(" ", 2);
    if (!keywords.Contains(splitedLine[0])){
        error(0, line.Key);
    }
    if (line.Value[line.Value.Length-1] != endMarkKeywords[splitedLine[0]]){
        error(0, line.Key);
    }
    return splitedLine[0];
}

void error(int code, int lineNumber = -1){
    Console.WriteLine($"Error LN°{lineNumber} - {code}");
    System.Environment.Exit(0);
}

/*
Keywords :
*/

void callKeyword(string keyword, string line, string function, int lineNumber){
    switch (keyword)
    {
        case "write":
            keyword_write(line.Split(" ", 2)[1], function, lineNumber);
            break;
        
        case "int32":
            keyword_int32(line.Split(" ", 2)[1], function, lineNumber);
            break;
    }
}

void keyword_write(string line, string function, int lineNumber){
    if (line.Length < 2){
        error(0, lineNumber);
    }
    if (line[0] != '(' || line[line.Length-2] != ')'){
        error(0, lineNumber);
    }
    Console.Write(stringObject(line).Substring(1, line.Length-3));
}

void keyword_int32(string line, string function, int lineNumber){
    string[] splitedLine = line.Split(" ", 3);
    if (splitedLine.Length != 3){
        error(0, lineNumber);
    }
    if (splitedLine[1] != "=" || splitedLine[2][splitedLine[2].Length-1] != ';'){
        error(0, lineNumber);
    }
    if (!Infos.alphabetL.Contains(splitedLine[2][0]) && !Infos.alphabetU.Contains(splitedLine[2][0])){
        error(0, lineNumber);
    }
}

/*
Objects :
*/

string stringObject(string element){
    return element;
}

long integerObject(string element){
    long number = Convert.ToInt64(element);
    return number;
}

/*
Main :
*/

executeFile(getCodeFile());
class Infos
{
    public static string alphabetL = "abcdefghijklmnopqrstuvwxyz";
    public static string alphabetU = "ABCDEFGHIJKLMOPQRSTUVWXYZ";
    public static Dictionary<string, Dictionary<string, string>> varsInfo;
    public static Dictionary<string, Dictionary<string, Dictionary<string, string>>> funcInfo;
}