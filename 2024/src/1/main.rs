use std::fs::{self, File};
use std::io::{self, BufRead, BufReader};

fn read_lines(filename: &str) -> io::Result<Vec::<String>> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);

    let mut results: Vec<String> = Vec::new();
    for line in reader.lines() {
        let line = line?;
        results.push(String::from(line));
    }
    return Ok(results);
}

fn part_1(list_1: &Vec<i32>, list_2: &Vec<i32>) {
    let mut list_1_clone = list_1.clone();
    let mut list_2_clone = list_2.clone();
    list_1_clone.sort();
    list_2_clone.sort();

    let mut total: i32 = 0;
    for i in 0..list_1.len() {
        let mut dist = list_1_clone[i] - list_2_clone[i];
        dist = dist.abs();
        total += dist;
    }
    println!("{}", total);
}

fn part_2(list_1: &Vec<i32>, list_2: &Vec<i32>) {

    let mut total: i32 = 0;
    for i in list_1 {
        let mut appearances = 0;
        for j in list_2 {
            if i == j {
                appearances += 1;
            }
        }
        total += i * appearances
    }
    println!("{}", total);
}


fn main() -> io::Result<()> {
    let lines = read_lines("input.txt")?;

    let mut list_1: Vec<i32> = Vec::new();
    let mut list_2: Vec<i32> = Vec::new();

    for line in lines {
        match line.split_whitespace().collect::<Vec<&str>>()[..] {
            [i1, i2] => {
                list_1.push(i1.parse::<i32>().unwrap());
                list_2.push(i2.parse::<i32>().unwrap());
            },
            _ => println!("Shouldn't happen")
        }
    }

    part_2(&list_1, &list_2);
    Ok(())
}
