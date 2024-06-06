
//Easier? Than importing it =)
#[derive(PartialEq)]
enum Option<T>
{
    None,
    Some(T)
}



struct ExpressionTree
{
    val_type : String,
    function : String,
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
        self.val_type = String::from("operand");
        self.function = if expression.len() > split_position { String::from(expression.chars().nth(split_position).unwrap()) } else { String::new() }; //Debug: Empty sometimes?!
        self.children.push( ExpressionTree { val_type : String::new(), function : String::new(), children: Vec::<ExpressionTree>::new() } );
        self.children.push( ExpressionTree { val_type : String::new(), function : String::new(), children: Vec::<ExpressionTree>::new() } );
        self.children[0].__init__(String::from(&expression[..split_position]), separator_vector.clone(), depth+1);
        self.children[1].__init__(String::from(&expression[split_position+1..]), separator_vector.clone(), depth+1);
        return;
    }


    self.function = expression;
}

fn height(&self, depth : i16) -> i16
{
    if self.children.len() == 0 { return depth; }
    let mut max_depth = depth;
    for child in &self.children 
    {
        let new_depth = child.height( depth+1 );
        max_depth = if new_depth > max_depth { new_depth } else { max_depth };
    }

    max_depth
}

fn len(&self) -> usize
{
    let mut size = self.function.len() + 2;
    for child in self.children.iter()
    {
        size += child.len();
    }

    size
}

fn show(&self, depth : i16) -> ()
{
    if depth > 0 { for child in &self.children { child.show(depth-1); } }
    if depth == 1 { println!(""); }
    if depth > 0 { return; }
    for _ in 0..( (self.len() - self.function.len() - 2) / 2) { print!(" "); }
    print!("{}", self.function);
    for _ in ( (self.len() - self.function.len() - 2) / 2)..self.len() { print!(" "); } 
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
    let mut root : ExpressionTree = ExpressionTree { val_type : String::new(), function: String::new()
        , children: Vec::<ExpressionTree>::new() };

    root.__init__(String::from("3*2-1+5/8"), vec![String::from("^&|"), String::from("+-"), String::from("*/%")], 0);

    println!("{} - {}", root.len(), root.height(1));
    root.show(0);
    println!("");
    for i in 1..root.height(1) { root.show(i); }
}
