## (C/I)Customizable Programming Language
## Summary :
* [Go](#what-is-cpl-exactly) - What is CPL?
* [Go](#get-started-with-cpl) - How to get started with CPL?
* [Go](#write-code-in-cpl) - How to write code in CPL?
* [Go](#use-intern-features-of-cpl) - How to use intern features of CPL?
* [Go](#how-does-cpl-work) - How does CPL work?

/!\Please excuse any syntaxical or grammatical error, english is <b>NOT</b> my native language...
## What is CPL exactly?
### - What does CPL stands for?
  As you might have seen in the title, CPL stands for :
```
Customizable Programming Language
```
### - Why "Customizable"?
  As the name might suggest, the main attribute of CPL is to be "Customizable".
  <br>However, most of you already asked yourself what "Customizable" means for a programing language?
  <br>Don't worry, it is as easy as it can get : Every element (grammar, etc) CPL uses can be changed in to whatever you want
  <br>For example:
  ```
write ("Hello, world!");
  ```
  <br> And:
```
dontwrite (-Hello, world!-)/
```
<br>These two examples both work the same but they just have different settings (first example uses default settings):
```
write  ->  dontwrite
  "    ->      -
  ;    ->      /
```

### - What if my friend and I don't use the same settings?
  When learning about the customizable feature of CPL you probably thought it could bring some 
  <br>issues. (We all have that one friend who would like to use the weirdest grammar possible)
  <br>To address this issue, there exists a feature which automaticaly changes the grammar in a CPL file to your own grammar.
  <br>In case you want to learn more about doing this : please follow [this link](#use-intern-features-of-cpl)

### - In what language is CPL developed?
  As you may have noticed while looking at this repository, CPL is developed in multiple programming languages
  <br>such as Python or C (Comming soon...)
  <br>What differentiates them are that some versions are Compiled and others are Interpreted(Python...)
  
### - What version should I choose?
  Your last option should be the Python version because it a test version used to, well, test features.
  <br>In my opinion (and it matters alot) the best version is the C version(Still comming soon...).
  
### - Who is working on the CPL project?
  Sadly, I (aka Bugxit) am working alone on the CPL project, which explains the lack of updates and new features.
  <br>But, being alone doesn't mean you can't produce things as good as a team (or does it?). 
  <br>I am still taking this project seriously and I am trying my best to make this PL the best it can be!

## Get started with CPL!
## Write code in CPL:
### The Keywords :
#### Summary:
- [Go](#write) - Write
- [Go](#int) - Int
- [Go](#var) - Var

#### Key informations:
All keywords are written using the default settings & [ ] indicate the part the developper can modify.
<br>Also some features are not disponible in every version of CPL, for example:
<br>[Int8](#int) does not exist in PyCPL (Python does not allow the utilisation of signed-integers)
#### Write:
Format :
```
write ([String Object]);
```
Description :
The write keyword takes a [String Object](#string-object) as an input and shows it in the console.
Example:
```
write ("Hello, world!");
  
```
It will give us the following output:
```console
Hello, world!
```
#### Int:
Format:
```
Int8  [String Object] = [Integer Object];
Int16 [String Object] = [Integer Object];
Int32 [String Object] = [Integer Object];
Int   [String Object] = [Integer Object];
```
Description:
The int keyword indicates the program to store the value represented by [[Integer Object](#integer-object)] under the name 
<br>specified as a [[String Object](#string-object)]. The number that may follow the keyword (8 ; 16 or 32) indicates the maximum number of bits
<br>the programm will need to use to store the specified value.
Example:
```
Int8 IntOne = 13;
write (f"{IntOne}");
```
We use the "write" keyword to show the value associated to IntOne ; This programm returns us the following output :
```console
13
```
### The Objects:
- [Go](#string-object) - String Object
- [Go](#integer-object) - Integer Object
- [Go](#boolean-object) - Boolean Object
#### Key informations:

#### String Object:

#### Integer Object:

## Use intern features of CPL: 
## How does CPL work?
