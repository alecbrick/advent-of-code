use std::io;
use advent_of_code::utils::{parse_ints, read_lines};


fn is_good(line: &Vec<i32>) -> bool {
    let mut is_decreasing = true;
    let mut is_increasing = true;
    let mut good_diffs = true;
    for i in 0..line.len() - 1 {
        let val_a: i32 = line[i];
        let val_b: i32 = line[i + 1];
        let diff = val_b - val_a;
        if diff <= 0 {
            is_increasing = false;
        }
        if diff >= 0 {
            is_decreasing = false;
        }
        if diff.abs() < 1 || diff.abs() > 3 {
            good_diffs = false;
        }
    }
    if good_diffs && (is_decreasing || is_increasing) {
        return true;
    }
    return false;
}

fn part_1(lines: &Vec<Vec<i32>>) {
    let mut good_lines = 0;
    for line in lines {
        if is_good(&line) {
            good_lines += 1;
        }
    }
    println!("{}", good_lines)
}

fn is_good_2(line: &Vec<i32>) -> bool {
    let mut is_decreasing = true;
    let mut is_increasing = true;
    let mut good_diffs = true;
    let mut i = 0;
    while i < line.len() - 1 {
        let val_a: i32 = line[i];
        let val_b: i32 = line[i + 1];
        let diff = val_b - val_a;
        if diff <= 0 {
            is_increasing = false;
        }
        if diff >= 0 {
            is_decreasing = false;
        }
        if diff.abs() < 1 || diff.abs() > 3 {
            good_diffs = false;
        }
        if !(good_diffs && (is_decreasing || is_increasing)) {
            // failed, drop it
            let mut cloned_line = line.clone();
            cloned_line.remove(i);
            if is_good(&cloned_line) {
                return true;
            }
            if i > 0 {
                cloned_line = line.clone();
                cloned_line.remove(i - 1);
                if is_good(&cloned_line) {
                    return true;
                }
            }
            cloned_line = line.clone();
            cloned_line.remove(i + 1);
            if is_good(&cloned_line) {
                return true;
            }
            return false;
        }
        i += 1;
    }
    return true;
}

fn part_2(lines: &Vec<Vec<i32>>) {
    let mut good_lines = 0;
    for line in lines {
        if is_good_2(&line) {
            good_lines += 1
        }
    }
    println!("{}", good_lines)
}


fn main() -> io::Result<()> {
    let lines = read_lines("data/inputs/02.txt")?;
    let parsed_lines = parse_ints(&lines);
    part_2(&parsed_lines);
    Ok(())
}
