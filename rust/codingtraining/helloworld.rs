use std::io::{self, Write};

/*
fn input() -> String {
    let mut s = String::new();
    
    io::stdin()
        .read_line(&mut s)
        .expect("You didn't input your name");

    return s;
}
*/

fn main() {

    let mut s = String::new();
    
    print!("What is your name? ");

    io::stdout().flush();
    
    io::stdin()
        .read_line(&mut s)
        .expect("You did not enter your name");
    
    println!("Hello, {}, nice to meet you!", s.trim_right());
    
}
