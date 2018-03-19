use std::io::{self, Write};

fn main() {
    let mut s = String::new();

    print!("What is the input string? ");
    io::stdout().flush();

    io::stdin()
        .read_line(&mut s)
        .expect("You didn't input any string.");

    s = s.trim_right().to_string();
    
    if s.len() <= 0 {
        println!("You didn't input any string.")
    } else {
        println!("Homer has {} characters.", s.len());
    }
}
