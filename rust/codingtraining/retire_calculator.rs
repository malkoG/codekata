use std::io::{self, Write};
use std::time::SystemTime;

fn main() {
    let mut from = String::new();
    let mut to = String::new();
    
    print!("What is your current age? ");

    io::stdout().flush();
    
    io::stdin()
        .read_line(&mut from);

    print!("At what age would you like to retire? ");

    io::stdout().flush();

    io::stdin()
        .read_line(&mut to);

    let now = from.parse::<i32>().unwrap();
    let future = to.parse::<i32>().unwrap();

    let sys_time = SystemTime::now();

    let current_date = (systim / (1000*60*60*24*365)) + 1970;
    let diff = future - now;
    
    println!("It's {}, so you can retire in {}.", current_date, current_date + diff);
    
}
