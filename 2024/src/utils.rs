use std::fs::File;
use std::io::{self, BufRead, BufReader};

pub fn read_lines(filename: &str) -> io::Result<Vec::<String>> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);

    let mut results: Vec<String> = Vec::new();
    for line in reader.lines() {
        let line = line?;
        results.push(String::from(line));
    }
    return Ok(results);
}

pub fn parse_ints(lines: &Vec::<String>) -> Vec::<Vec::<i32>> {
    lines.into_iter().map(|line|
        line.split_whitespace().map(|s|
            s.parse::<i32>().unwrap()
        ).collect()
    ).collect()
}
