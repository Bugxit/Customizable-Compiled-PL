
//Easier? Than importing it =)
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

struct ExpressionTree
{
    function : ElementInfo,
    children : Vec<ExpressionTree>
}

impl ExpressionTree
{

fn __init__(&mut self, expression : String, separator_vector: Vec<String>, depth : i16) -> ()
{
    let ( expression, split_position, separator_vector )
    = parse_once(expression, separator_vector);
    
    if split_position != Option::None
    {
        let Option::Some(split_position) = split_position else { return; }; 
        self.function = if expression.len() > split_position { ElementInfo::Operand(String::from(expression.chars().nth(split_position).unwrap())) } else { ElementInfo::Operand(String::new()) }; //Debug: Empty sometimes?!
        self.children.push( ExpressionTree { function : ElementInfo::Unknown(String::new()), children: Vec::<ExpressionTree>::new() } );
        self.children.push( ExpressionTree { function : ElementInfo::Unknown(String::new()), children: Vec::<ExpressionTree>::new() } );
        self.children[0].__init__(String::from(&expression[..split_position]), separator_vector.clone(), depth+1);
        self.children[1].__init__(String::from(&expression[split_position+1..]), separator_vector.clone(), depth+1);
        return;
    }

    let mut function_name : String = String::new();
    let mut split_position : usize = 0;

    while split_position < expression.len()
    {
        let current_char = expression.chars().nth(split_position).unwrap();
        if current_char == '(' { continue; }
        function_name += &String::from(current_char);
        split_position += 1;
    }

    if function_name == expression
    {
        //Can be a variable (remember that the value can start with 0x / 0b)
        self.function = ElementInfo::Immediate(expression.clone());
    } 
    else if function_name.len() == 0
    {
        let (mut start, mut end) : (usize, usize) = (0, function_name.len()-1);
        while start < end && function_name.chars().nth(start).unwrap() == '(' && function_name.chars().nth(end).unwrap() == ')'
        {
            start += 1;
            end -= 1;
        }
        
        //Error here if start = 0... We have a problem...
        self.__init__(String::from(&function_name[start..end+1]), vec![String::from("^&|"), String::from("+-"), String::from("*/%")], depth);
    
    } 
    else 
    {
        self.function = ElementInfo::Function(expression.clone());
    }

    //self.function = ElementInfo::Unknown(expression.clone());
}

}


fn parse_once(expression : String, mut separator_vector: Vec<String>) -> (String, Option<usize>, Vec<String>)
{
    while separator_vector.len() > 0
    {

        let mut is_string_opened : bool = false;
        let mut is_parentheses_opened : bool = false;
        let mut char_that_opened_string : char = ' ';
        let mut opened_parentheses_count : i16 = 0; //Also check for { & [

        for (char_number, char_value) in expression.chars().enumerate()
        {
            if !is_string_opened && "\"'".contains(char_value) //Debug : verify espace sequence
            {
                is_string_opened = true;
                char_that_opened_string = char_value;
            } 
            else if is_string_opened && char_value == char_that_opened_string
            {
                is_string_opened = false;
            }

            if !is_string_opened && char_value == '('
            {
                if is_parentheses_opened { opened_parentheses_count += 1; }
                else { is_parentheses_opened = true ; opened_parentheses_count = 1; }
            }
            else if !is_string_opened && is_parentheses_opened && char_value == ')'
            {
                opened_parentheses_count -= 1;
                if opened_parentheses_count == 0 { is_parentheses_opened = false; }
            }

            if !is_parentheses_opened && !is_string_opened && separator_vector[0].contains(char_value)
            {
                return (expression, Option::Some(char_number), separator_vector);
            }
        }

        separator_vector.remove(0);
    }            

    (expression, Option::None, separator_vector)
}

fn main()
{
    let mut root : ExpressionTree = ExpressionTree { function : ElementInfo::Unknown(String::new()), 
                                                     children: Vec::<ExpressionTree>::new() };

    root.__init__(String::from("3*2-1+5/8"), vec![String::from("^&|"), String::from("+-"), String::from("*/%")], 0);
}
