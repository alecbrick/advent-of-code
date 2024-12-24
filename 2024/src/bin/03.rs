use regex::Regex;
use std::io;
use advent_of_code::utils::read_lines;

fn part_1(lines: &Vec<String>) {
    let re = Regex::new(r"mul\((\d+)\,(\d+)\)").unwrap();
    let result = re.find("mul(123,456)");
    println!("regex found {:?}", result);
    let mut sum = 0;
    for line in lines {
        for capture in re.captures_iter(line) {
            let i1 = capture[1].parse::<i32>().unwrap();
            let i2 = capture[2].parse::<i32>().unwrap();
            sum += i1 * i2
        }
    }
    println!("{}", sum);
}


fn part_2(lines: &Vec<String>) {
    let re = Regex::new(r"mul\((\d+)\,(\d+)\)|don't\(\)|do\(\)").unwrap();
    let result = re.find("do()");
    println!("regex found {:?}", result);
    let mut sum = 0;
    let mut mul_enabled = true;
    for line in lines {
        for capture in re.captures_iter(line) {
            if capture[0].starts_with("mul") {
                if mul_enabled {
                    let i1 = capture[1].parse::<i32>().unwrap();
                    let i2 = capture[2].parse::<i32>().unwrap();
                    sum += i1 * i2
                }
            } else if capture[0].starts_with("don't") {
                mul_enabled = false;
            } else {
                mul_enabled = true;
            }
        }
    }
    println!("{}", sum);
}


fn main() -> io::Result<()> {
    let lines = read_lines("data/inputs/03.txt")?;
    part_1(&lines);
    part_2(&lines);
    Ok(())
}
