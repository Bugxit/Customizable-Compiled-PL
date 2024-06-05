
//Easier? Than importing it =)

#[derive(PartialEq)]
enum Option<T>
{
    None,
    Some(T)
}



struct ExpressionTree
{
    val_type : &str,
    function : String,
    children : Vec<ExpressionTree>
}

impl ExpressionTree
{

fn __init__(&mut self, expression : String, separator_vector: Vec<String>) -> ()
{
    let ( new_function, split_position, separator_vector )
    = parse_once(expression, separator_vector);

    self.function = new_function;
    let Option::Some(a) = split_position else { 
                                                self.children.push( ExpressionTree { val_type : "", function: String::from(""), children: Vec::<ExpressionTree>::new() } )
                                                self.children.push( ExpressionTree { val_type : "", function: String::from(""), children: Vec::<ExpressionTree>::new() } )
                                                self.children[0].__init__(expression[..1], separator_vector.copy())
                                                self.children[1].__init__(expression[])
                                                return; };

    self.children.push( ExpressionTree { })

}

}



fn parse_once(expression : String, mut separator_vector: Vec<String>) -> (String, Option<usize>, Vec<String>)
{
    while separator_vector.len() > 0
    {

        let mut is_string_opened : bool = false;
        let mut is_parentheses_opened : bool = false;
        let mut char_that_opened_string : char = ' ';
        let mut opened_parentheses_count : i16 = 0;

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
                return (String::from(char_value), Option::Some(char_number), separator_vector);
            }
        }

        separator_vector.remove(0);
    }            

    return (expression, Option::None, separator_vector) //DEBUG 0 should be changed (Option enum)
}

fn main()
{
    let mut root : ExpressionTree = ExpressionTree { val_type : "", function: String::from(""), children: Vec::<ExpressionTree>::new() };

    root.__init__(String::from("1+1"), vec![String::from("^&|"), String::from("+-"), String::from("*/%")]);
}
