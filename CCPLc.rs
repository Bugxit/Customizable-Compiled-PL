#![allow(warnings)] 

use std::env;
use std::fs;

fn main()
{
    let argv : Vec<String> = env::args()
                                 .collect();

    if argv.len() < 2 { panic!("Please enter a file name!"); }

    //Store the file to compile & remove its comments
    let file_vector : Vec<String> = read_file(&argv[1]);
    let file_vector : Vec<(String, usize)> = remove_comments(file_vector);

    //Separate every blocks of code from the main file
    let (file_vector, filestype_vector) : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "file");
    let (file_vector, impls_vector)     : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "impl");
    let (file_vector, names_vector)     : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "name");
    let (file_vector, classes_vector)   : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "class");
    let (file_vector, enums_vector)     : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "enum");
    let (file_vector, structs_vector)   : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "struct");
    let (file_vector, functions_vector) : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "func");
    let (file_vector, macros_vector)    : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "macro");
    let (file_vector, main_settings)    : (Vec<(String, usize)>, Vec<(String, usize)>)      = get_settings(file_vector);

    let global_settings_result = handle_global_settings(main_settings);

    let handle_functions       = handle_functions(functions_vector);
}

/*
    FileIO.rs
*/

fn read_file(file_path : &str) -> Vec<String>
{
    let file_content : Vec<String> = fs::read_to_string(file_path)
                                        .expect("Error while reading file")
                                        .split("\n")
                                        .map(|s| s.to_string())
                                        .collect();
    file_content
}

/*
    FileParsing.rs
*/

//Debug: While removing comments, closing a string is not perfect : \" does not close the string but \\" does not either
fn remove_comments(file_vector : Vec<String>) -> Vec<(String, usize)>
{
    let mut new_file_vector : Vec<(String, usize)> = vec![];
    let mut ignore_next_char : bool;
    let mut is_string_opened : bool = false;
    let mut is_comment_opened : bool = false;
    let mut char_that_opened_string : char = ' ';
    let mut current_line : String = String::from("");

    'in_file: for (line_number, line) in file_vector.iter().enumerate()
    {
        ignore_next_char = false;

        if line.is_empty() { continue 'in_file; }

        'in_line: for (char_number, char_value) in line[..line.len()-1].chars().enumerate()
        {

            if ignore_next_char { ignore_next_char = false; continue 'in_line; }

            if !is_string_opened
               && !is_comment_opened 
               && "\"'".contains(char_value)
            {
                is_string_opened = true;
                char_that_opened_string = char_value;
            } 

            else if is_string_opened 
                    && !is_comment_opened 
                    && char_value == char_that_opened_string 
                    && (
                       (char_number == 0 || line.chars().nth(char_number-1).unwrap() != '\\') 
                       && (char_number <= 1 || line.chars().nth(char_number-2).unwrap() != '\\')
                       )
            {
                is_string_opened = false;
            }

            if !is_string_opened && !is_comment_opened && (char_value, line.chars().nth(char_number+1).unwrap()) == ('/', '/') { ignore_next_char = true; break 'in_line; }
            if !is_string_opened && !is_comment_opened && (char_value, line.chars().nth(char_number+1).unwrap()) == ('/', '*') { is_comment_opened = true; ignore_next_char = true; continue 'in_line; }
            else if !is_string_opened && is_comment_opened && (char_value, line.chars().nth(char_number+1).unwrap()) == ('*', '/') { is_comment_opened = false; ignore_next_char = true; continue 'in_line; }

            if !is_comment_opened { current_line += &String::from(char_value) };
        }

        if !ignore_next_char && !is_comment_opened { current_line += &String::from(line.chars().nth(line.len()-1).unwrap()); }
        
        current_line = String::from(current_line.trim());

        if !current_line.is_empty() {
            new_file_vector.push((current_line, line_number+1));
        }

        current_line = String::from("");
    }

    new_file_vector
}



fn split_blocks_from_file(file_vector : Vec<(String, usize)>, blocks_name : &str) -> (Vec<(String, usize)>, Vec<Vec<(String, usize)>>)
{
    let block_len : usize = blocks_name.len() + 1;
    let mut all_blocks_vector : Vec<Vec<(String, usize)>> = vec![];
    let mut new_file_vector : Vec<(String, usize)> = vec![];
    let mut forbiden_lines : Vec<usize> = vec![];

    'in_file: for line_info in file_vector.iter()
    {
        let (line, line_number) : (String, usize) = line_info.clone();

        if forbiden_lines.contains(&line_number)
        {
            forbiden_lines.push(line_number);
            continue 'in_file; 
        }

        let start_of_line : &str;
        if line.len() < block_len { start_of_line = &line; }
        else { start_of_line = &line[..block_len].trim(); }
        if start_of_line != blocks_name
        { 
            new_file_vector.push((line, line_number));
            forbiden_lines.push(line_number);
            continue 'in_file; 
        }

        let mut block_closed_before_file : bool = false;
        let mut new_block_vector : Vec<(String, usize)> = vec![];

        'in_block: for line_info_in_block in file_vector.iter()
        {
            let (line_in_block, line_number_in_block) : (String, usize) = line_info_in_block.clone();

            if forbiden_lines.contains(&line_number_in_block) { continue 'in_block; }

            forbiden_lines.push(line_number_in_block);
            new_block_vector.push((String::from(line_in_block.clone()), line_number_in_block));

            let start_of_line : &str;
            if line_in_block.len() < block_len + 3 { start_of_line = &line_in_block; }
            else { start_of_line = &line_in_block[..block_len + 3].trim(); }
            if start_of_line == "end".to_owned() + blocks_name { block_closed_before_file = true; break 'in_block; }
        } 

        if !block_closed_before_file{
            //Error: Reached EOF before "end{block}"
            panic!("Reached EOF while in a {}", blocks_name);
        }

        all_blocks_vector.push(new_block_vector);
    }

    (new_file_vector, all_blocks_vector)
}




fn get_settings(lines_vector: Vec<(String, usize)>) -> (Vec<(String, usize)>, Vec<(String, usize)>)
{
    let mut new_file_vector      : Vec<(String, usize)> = vec![];
    let mut main_settings_vector : Vec<(String, usize)> = vec![];

    for (line, line_number) in lines_vector
    {
        if line.chars().nth(0).unwrap() == '#' { main_settings_vector.push((line, line_number)); }
        else { new_file_vector.push((line, line_number)); }
    }

    (new_file_vector, main_settings_vector)
}

/*
    BlocksHandling.rs
*/

fn handle_global_settings(settings_vector : Vec<(String, usize)>) -> ()
{

for (setting_value, setting_position) in settings_vector
{
    let mut setting_keyword = String::new();

    for character in setting_value.chars()
    {
        if character == ' ' { break; }

        setting_keyword += &String::from(character);
    }

    println!("{}", setting_keyword);
}   

}

fn handle_functions(fn_vector : Vec<Vec<(String, usize)>>) -> ()
{

for current_function in fn_vector
{
    let mut function_declaration : String = current_function[0].0.clone();
    let declaration_len : usize = function_declaration.len(); 

    if declaration_len <= 5 { panic!("Expected name, found newline char"); } //Error: Line ends before function declaration is finished 

    let mut char_number = 5;
    let mut current_char : char;

    let mut function_name : String = String::new();
    while char_number < declaration_len { if function_declaration.chars().nth(char_number).unwrap() != ' ' { break; } char_number += 1; }
    'get_name: while char_number < declaration_len
    {
        current_char = function_declaration.chars().nth(char_number).unwrap();
        
        if current_char == ' ' { break 'get_name; }

        function_name += &String::from(current_char);

        char_number += 1;
    }

    let mut function_args_string : String = String::new();
    while char_number < declaration_len { if function_declaration.chars().nth(char_number).unwrap() != ' ' { break; } char_number += 1; }
    'get_args: while char_number < declaration_len
    {
        if char_number >= declaration_len-1 { panic!("Excpected \"->\", found Newline Character")}
        
        let (current_char, next_char) : (char, char) = (function_declaration.chars().nth(char_number).unwrap(), function_declaration.chars().nth(char_number+1).unwrap());

        if (current_char, next_char) == ('-','>') { char_number += 2; break 'get_args; }

        function_args_string += &String::from(current_char);

        char_number += 1;
    }

    let mut current_arg : String = String::new();
    let mut function_args : Vec<String> = vec![];

    'split_args: for character in function_args_string.chars()
    {
        if character != ','
        {
            current_arg += &String::from(character);
            continue 'split_args;
        }

        function_args.push(String::from(current_arg.trim()));
        current_arg = String::new();    
    }
    //Error: (arg,thing,) WHY DO YOU END ON A COMMA ?
    if current_arg.trim().is_empty() { panic!("Parameters declaration ends on a comma"); }
    function_args.push(String::from(current_arg.trim()));

    let mut function_type : String = String::new();
    while char_number < declaration_len { if function_declaration.chars().nth(char_number).unwrap() != ' ' { break; } char_number += 1; }
    'get_type: while char_number < declaration_len
    {
        current_char = function_declaration.chars().nth(char_number).unwrap();
        
        if current_char == ' ' { break 'get_type; }

        function_type += &String::from(current_char);
        char_number += 1;
    }    

    while char_number < declaration_len { if function_declaration.chars().nth(char_number).unwrap() != ' ' { break; } char_number += 1; }
    if char_number != declaration_len
    {
        //Error: Chars after end of declaration of function (-> TYPE useless)
        let error : String = String::from(&function_declaration[char_number..]);
        panic!("Expected Newline Character, but found : {}", error);
    }

    let mut function_id : String = function_name.clone();
    for argument in &function_args { function_id += &String::from(","); function_id += &argument; }    
    function_id += &String::from("->");
    function_id += &function_type;

    println!("The function name is : {function_name}");
    println!("The function type is : {function_type}");
    println!("The function ID is : {function_id}");
    println!("The function args are :");
    for i in function_args { println!("- {i}"); }
}

}

/*
    UsefulFunctions.rs
*/

fn usize_min(u1 : usize, u2 : usize) -> usize
{
    if u1 < u2
    {
        return u1;
    }

    u2
}

fn string_compare(s1 : &String, comp : Comparing, s2 : &String) -> bool
{
    let result : Comparing = 
    {

    let str_len : usize = usize_min(s1.len(), s2.len());
    let index : usize = 0;
    while index < str_len
    {
        if s1.chars().nth(index) < s2.chars().nth(index)
        {
            Comparing::LsThan;
        }

        else if s1.chars().nth(index) > s2.chars().nth(index)
        {
            Comparing::GrThan;
        }
    }

    if s1.len() == s2.len()
    {
        Comparing::EqTo;
    }
    
    if s1.len() < s2.len()
    {
        Comparing::LsThan;
    }

    Comparing::GrThan

    };

    if Comparing::GrThan == comp || Comparing::LsThan == comp || Comparing::EqTo == comp
    {
        return result == comp;
    }
    else if result == Comparing::EqTo
    {
        return true;
    }
    else if comp == Comparing::LsThanEqTo
    {
        return result == Comparing::LsThan;
    }
    else if comp == Comparing::GrThanEqTo 
    {
        return result == Comparing::GrThan;
    }

    false
}

/*
    Strcts.rs
*/

#[derive(PartialEq)]
struct BinaryTreeString
{
    name : String,
    value : NameReference,
    left_node : Box<Option<BinaryTreeString>>,
    right_node : Box<Option<BinaryTreeString>>,
}

impl BinaryTreeString
{

fn insert(&mut self, new_name : String, new_value : NameReference)
{
    if string_compare(&new_name, Comparing::LsThanEqTo, &self.name)
    {
        self.left_node =
        {match *self.left_node
        {
            Option::None => { 
                                Box::new(Option::Some(BinaryTreeString {name : new_name, value : new_value, left_node : Box::new(Option::None), right_node : Box::new(Option::None) }))
                            }
            Option::Some(mut left_node_moved) => {

                                    left_node_moved.insert(new_name, new_value);
                                    Box::new(Option::Some(left_node_moved))

                                 }
        }}
    } 

    else
    {
        match *self.right_node
        {
            Option::None => { 
                            self.right_node = Box::new(Option::Some(BinaryTreeString {name : new_name, value : new_value, left_node : Box::new(Option::None), right_node : Box::new(Option::None) }));
                            return; 
                            }
            Option::Some(mut bts) => {

                                    bts.insert(new_name, new_value)

                                 }
        }
    }
}

fn tree_to_sorted_vector(&mut self, sorting_vector : Vec<String>) -> Vec<String>
{
    //Thing
    sorting_vector = 
    {
        match *self.left_node
        {
            Option::None => { sorting_vector },
            Option::Some(bts) => { bts.tree_to_sorted_vector(sorting_vector) }
        }
    };

    sorting_vector.push(self.name.clone());

    sorting_vector = 
    {
        match *self.right_node
        {
            Option::None => { sorting_vector },
            Option::Some(bts) => { bts.tree_to_sorted_vector(sorting_vector) }
        }
    };

    sorting_vector
}

}

struct ExpressionTree
{
    function : ElementInfo,
    children : Vec<ExpressionTree>
}

struct FunctionInformations
{
    name : String,
    args : Vec<ParametersInformations>,
    return_type : String,
    id : String
}

struct ParametersInformations
{
    name : String,
    par_type : String,
    buffer : String
}

/*
    Enums.rs
*/

#[derive(PartialEq)]
enum Option<T>
{
    None,
    Some(T)
}

enum ElementInfo
{
    Unknown(String),
    Immediate(String),
    Operand(String),
    Function(String),
    Variable(String)
}

#[derive(PartialEq)]
enum NameReference
{
    File,
    Class,
    Enum,
    Struct,
    Macro,
    Function,
}

#[derive(PartialEq)]
enum Comparing
{
    EqTo,
    LsThan,
    GrThan,
    GrThanEqTo,
    LsThanEqTo,
}

/*
    ErrorHandling.rs
*/

/* 
ERROR SCHEME:
    - Compiler Error: EC°°°
    - Run-Time Error: ER°°°
*/

fn error()
{
    
}
