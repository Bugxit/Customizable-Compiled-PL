use std::env;
use std::fs;

fn main(){
    let argv : Vec<String> = env::args()
                                 .collect();

    if argv.len() < 2 { panic!("Please enter a file name!"); }

    let (mut file_vector, file_line_number_vector) : (Vec<String>, Vec<usize>);

    file_vector = read_file(&argv[1]);

    (file_vector, file_line_number_vector) = remove_comments(file_vector);

    let thing = split_classes_from_file(file_vector, file_line_number_vector);

    for vec_line in thing
    {
        println!("#NEWCLASS:");

        for line in vec_line
        {
            println!("{line}");
        }
    }

    //for (line_n, line) in file_vector.iter().enumerate() { println!("{} - {}", file_line_number_vector[line_n] ,line); }
}

fn split_classes_from_file(file_vector : Vec<String>, _file_line_number_vector : Vec<usize>) -> Vec<Vec<String>>{

    let mut all_classes_vector : Vec<Vec<String>> = vec![];

    let mut forbiden_lines : Vec<usize> = vec![];

    'in_file: for (line_number, line) in file_vector.iter().enumerate() 
    {
        let start_of_line : &str;
        if line.len() < 5
        { 
            forbiden_lines.push(line_number);
            continue 'in_file; 
        }
        start_of_line = &line[..6].trim();
        if start_of_line != "class" || forbiden_lines.contains(&line_number)
        { 
            forbiden_lines.push(line_number);
            continue 'in_file; 
        }

        let mut new_class_vector : Vec<String> = vec![];

        'in_class: for (line_number_in_class, line_in_class) in file_vector.iter().enumerate()
        {
            if forbiden_lines.contains(&line_number_in_class) { continue 'in_class; }

            forbiden_lines.push(line_number_in_class);
            new_class_vector.push(String::from(line_in_class));

            let start_of_line : &str;
            if line_in_class.len() < 9 { start_of_line = line_in_class; }
            else { start_of_line = &line_in_class[..9].trim(); }
            if start_of_line == "endclass" { break 'in_class; }
        } 

        all_classes_vector.push(new_class_vector);
    }

    all_classes_vector
}


fn read_file(file_path : &str) -> Vec<String>{
    let file_content : Vec<String> = fs::read_to_string(file_path)
                                        .expect("Error while reading file")
                                        .split("\n")
                                        .map(|s| s.to_string())
                                        .collect();
    file_content
}

fn remove_comments(file_vector : Vec<String>) -> (Vec<String>, Vec<usize>){
    let mut new_file_vector : Vec<String> = vec![];
    let mut new_line_number_vector : Vec<usize> = vec![];

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
            new_file_vector.push(current_line);
            new_line_number_vector.push(line_number+1);
        }

        current_line = String::from("");
    }

    (new_file_vector, new_line_number_vector)
}
