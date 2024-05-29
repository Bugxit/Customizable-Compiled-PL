use std::env;
use std::fs;

fn main(){
    let argv : Vec<String> = env::args()
                                 .collect();

    if argv.len() < 2 { panic!("Please enter a file name!"); }

    let file_vector : Vec<String> = read_file(&argv[1]);
    let file_vector : Vec<(String, usize)> = remove_comments(file_vector);
    let (file_vector, classes_vector)   : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "class");
    let (file_vector, structs_vector)   : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "struct");
    let (file_vector, functions_vector) : (Vec<(String, usize)>, Vec<Vec<(String, usize)>>) = split_blocks_from_file(file_vector, "func");


    //Debug: print content of vars
    for vec_line in classes_vector   { println!("#NEWCLASS:"); for line in vec_line { let (line_value, line_number) = line; println!("{line_number} - {line_value}"); } }
    for vec_line in structs_vector   { println!("#NEWSTRUCT:"); for line in vec_line { let (line_value, line_number) = line; println!("{line_number} - {line_value}"); } }
    for vec_line in functions_vector { println!("#NEWFUNC:"); for line in vec_line { let (line_value, line_number) = line; println!("{line_number} - {line_value}"); } }
    println!("#MAINFILE:"); for line in file_vector { let (line_value, line_number) = line; println!("{line_number} - {line_value}"); }
}

fn split_blocks_from_file(file_vector : Vec<(String, usize)>, blocks_name : &str) -> (Vec<(String, usize)>, Vec<Vec<(String, usize)>>){

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


fn read_file(file_path : &str) -> Vec<String>{
    let file_content : Vec<String> = fs::read_to_string(file_path)
                                        .expect("Error while reading file")
                                        .split("\n")
                                        .map(|s| s.to_string())
                                        .collect();
    file_content
}

fn remove_comments(file_vector : Vec<String>) -> Vec<(String, usize)>{
    let mut new_file_vector : Vec<(String, usize)> = vec![];

    let mut ignore_next_char : bool;
    let mut is_string_opened : bool = false;
    let mut is_comment_opened : bool = false;
    let mut char_that_opened_screen : char = ' ';
    let mut current_line : String = String::from("");

    'in_file: for (line_number, line) in file_vector.iter().enumerate()
    {
        ignore_next_char = false;

        if line.is_empty() { continue 'in_file; }

        'in_line: for (char_number, char_value) in line[..line.len()-1].chars().enumerate()
        {

            if ignore_next_char { ignore_next_char = false; continue 'in_line; }

            if !is_string_opened && !is_comment_opened && "\"'".contains(char_value)
            {
                is_string_opened = true;
                char_that_opened_screen = char_value;
            } 

            else if is_string_opened && !is_comment_opened && char_value == char_that_opened_screen && /*Verify escape sequence*/ (char_number == 0 || line.chars().nth(char_number-1).unwrap() != '\\')
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
