use std::collections::{HashSet, VecDeque};

use advent_of_code::pos_out_of_bounds;

advent_of_code::solution!(18);

pub fn part_one(input: &str) -> Option<u32> {
    let size: i32 = 71;
    let u_size = size as usize;
    let mut positions: Vec<Vec<bool>> = vec![vec![false; u_size]; u_size];
    let pos_list: Vec<(usize, usize)> = input.trim().split("\n").collect::<Vec<&str>>()[0..2883].into_iter().map(|line| {
        let (y, x) = line.split_once(",").unwrap();
        (y.parse::<usize>().unwrap(), x.parse::<usize>().unwrap())
    }).collect();
    println!("{:?}", pos_list.last().unwrap());
    for pos in pos_list {
        positions[pos.0][pos.1] = true;
    }


    let mut visited: Vec<Vec<bool>> = vec![vec![false; u_size]; u_size];
    let mut queue: VecDeque<((i32, i32), u32)> = VecDeque::new();
    queue.push_back(((0, 0), 0));
    while !queue.is_empty() {
        let (pos, n) = queue.pop_front().unwrap();
        if visited[pos.0 as usize][pos.1 as usize] {
            continue;
        }

        if pos == (size - 1, size - 1) {
            return Some(n);
        }
        visited[pos.0 as usize][pos.1 as usize] = true;
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
            let new_pos = (pos.0 + dir.0, pos.1 + dir.1);
            if pos_out_of_bounds(new_pos, size, size) {
                continue
            }
            if !positions[new_pos.0 as usize][new_pos.1 as usize] {
                queue.push_back((new_pos, n + 1));
            }
        }
    }
    None
}

pub fn part_two(input: &str) -> Option<u32> {
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(22));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
