use std::fs::OpenOptions;
use std::io::Write;

use regex::Regex;

advent_of_code::solution!(14);

pub fn part_one(input: &str) -> Option<u32> {
    let re = Regex::new(r"-?\d+").unwrap();
    let nums: Vec<Vec<i128>> = input.trim().split("\n").map(|config| {
        re.find_iter(config).map(|m| {
            m.as_str().parse().unwrap()
        }).collect()
    }).collect();

    let height = 103;
    let width = 101;

    let mut quadrants = [0, 0, 0, 0];
    for config in nums {
        let pos = (config[0], config[1]);
        let vel = (config[2], config[3]);

        let next_pos = ((pos.0 + vel.0 * 100).rem_euclid(width), (pos.1 + vel.1 * 100).rem_euclid(height));
        if next_pos.0 < width / 2 {
            if next_pos.1 < height / 2 {
                quadrants[0] += 1;
            } else if next_pos.1 > height / 2 {
                quadrants[1] += 1;
            }
        } else if next_pos.0 > width / 2 {
            if next_pos.1 < height / 2 {
                quadrants[2] += 1;
            } else if next_pos.1 > height / 2 {
                quadrants[3] += 1;
            }
        }
    }

    Some(quadrants.iter().fold(1, |acc, e| e * acc))
}

pub fn board_is_interesting(board: &Vec<Vec<char>>, re: &Regex) -> bool {
    let board_str = board.iter().flatten().collect::<String>();
    re.is_match(&board_str)
}

pub fn print_board(board: &Vec<Vec<char>>, i: usize) {
    let mut file = OpenOptions::new()
        .append(true)
        .create(true)
        .open("14_output.txt").unwrap();
    writeln!(file, "{}", i);
    for row in board {
        let row_str: String = row.iter().collect();
        writeln!(file, "{}", row_str);
    }
    writeln!(file, "");
}

pub fn part_two(input: &str) -> Option<u32> {
    let re = Regex::new(r"-?\d+").unwrap();
    let mut nums: Vec<Vec<i32>> = input.trim().split("\n").map(|config| {
        re.find_iter(config).map(|m| {
            m.as_str().parse().unwrap()
        }).collect()
    }).collect();

    let height: i32 = 103;
    let width: i32 = 101;

    let cool_re = Regex::new(r"\*\*\*\*\*").unwrap();

    for i in 1..50000 {
        let mut board = vec![vec!['.'; width as usize]; height as usize];
        let mut new_nums = Vec::new();
        for config in nums {
            let pos = (config[0], config[1]);
            let vel = (config[2], config[3]);

            let next_pos = ((pos.0 + vel.0).rem_euclid(width), (pos.1 + vel.1).rem_euclid(height));
            board[next_pos.1 as usize][next_pos.0 as usize] = '*';
            new_nums.push(vec![next_pos.0, next_pos.1, vel.0, vel.1]);
        }
        nums = new_nums;

        if board_is_interesting(&board, &cool_re) {
            print_board(&board, i);
        }
    }

    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(12));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
