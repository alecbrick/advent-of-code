use std::{collections::{HashMap, VecDeque}, hash::Hash};

use advent_of_code::pos_out_of_bounds;

advent_of_code::solution!(20);

pub fn part_one(input: &str) -> Option<u32> {
    let grid: Vec<&str> = input.split("\n").collect();

    let height = grid.len();
    let width = grid[0].len();
    let i_height = height as i32;
    let i_width = width as i32;

    let mut start = (0, 0);
    let mut end = (0, 0);
    let mut walls: Vec<Vec<bool>> = vec![vec![false; width]; height];
    for i in 0..grid.len() {
        let chars: Vec<char> = grid[i].chars().collect();
        for j in 0..grid[0].len() {
            if chars[j] == 'S' {
                start = (i, j);
            }
            if chars[j] == 'E' {
                end = (i, j);
            }
            if chars[j] == '#' {
                walls[i][j] = true;
            }
        }
    }
    println!("Start / End: {:?} / {:?}", start, end);

    let mut visited: Vec<Vec<bool>> = vec![vec![false; width]; height];
    let mut distances: Vec<Vec<i32>> = vec![vec![-1; width]; height];
    let mut queue: VecDeque<((i32, i32), u32)> = VecDeque::new();
    queue.push_back(((end.0 as i32, end.1 as i32), 0));
    while !queue.is_empty() {
        let (pos, n) = queue.pop_front().unwrap();
        if visited[pos.0 as usize][pos.1 as usize] {
            continue;
        }
        distances[pos.0 as usize][pos.1 as usize] = n as i32;

        visited[pos.0 as usize][pos.1 as usize] = true;
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
            let new_pos = (pos.0 + dir.0, pos.1 + dir.1);
            if pos_out_of_bounds(new_pos, i_height, i_width) {
                continue
            }
            if !walls[new_pos.0 as usize][new_pos.1 as usize] {
                queue.push_back((new_pos, n + 1));
            }
        }
    }

    println!("{:?}", distances);
    
    let mut total = 0;
    for i in 0..height {
        let int_i = i as i32;
        for j in 0..width {
            let int_j = j as i32;
            if walls[i][j] {
                continue;
            }
            for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
                let mid_pos = (int_i + dir.0, int_j + dir.1);
                let new_pos = (int_i + dir.0 * 2, int_j + dir.1 * 2);
                if pos_out_of_bounds(new_pos, i_height, i_width) {
                    continue
                }
                if !walls[mid_pos.0 as usize][mid_pos.1 as usize] {
                    continue;
                }
                let this_distance = distances[i][j];
                let that_distance = distances[new_pos.0 as usize][new_pos.1 as usize];
                if this_distance == -1 || that_distance == -1 {
                    continue;
                }
                if this_distance - that_distance - 2 >= 100 {
                    total += 1;
                }
            }
        }
    }
    Some(total)
}

pub fn part_two(input: &str) -> Option<u32> {
    let grid: Vec<&str> = input.split("\n").collect();

    let height = grid.len();
    let width = grid[0].len();
    let i_height = height as i32;
    let i_width = width as i32;

    let mut start = (0, 0);
    let mut end = (0, 0);
    let mut walls: Vec<Vec<bool>> = vec![vec![false; width]; height];
    for i in 0..grid.len() {
        let chars: Vec<char> = grid[i].chars().collect();
        for j in 0..grid[0].len() {
            if chars[j] == 'S' {
                start = (i, j);
            }
            if chars[j] == 'E' {
                end = (i, j);
            }
            if chars[j] == '#' {
                walls[i][j] = true;
            }
        }
    }
    println!("Start / End: {:?} / {:?}", start, end);

    let mut visited: Vec<Vec<bool>> = vec![vec![false; width]; height];
    let mut distances: Vec<Vec<i32>> = vec![vec![-1; width]; height];
    let mut queue: VecDeque<((i32, i32), u32)> = VecDeque::new();
    queue.push_back(((end.0 as i32, end.1 as i32), 0));
    while !queue.is_empty() {
        let (pos, n) = queue.pop_front().unwrap();
        if visited[pos.0 as usize][pos.1 as usize] {
            continue;
        }
        distances[pos.0 as usize][pos.1 as usize] = n as i32;

        visited[pos.0 as usize][pos.1 as usize] = true;
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
            let new_pos = (pos.0 + dir.0, pos.1 + dir.1);
            if pos_out_of_bounds(new_pos, i_height, i_width) {
                continue
            }
            if !walls[new_pos.0 as usize][new_pos.1 as usize] {
                queue.push_back((new_pos, n + 1));
            }
        }
    }

    
    let mut total = 0;
    let mut distance_to_count: HashMap<i32, u32> = HashMap::new();
    for i in 0..height {
        println!("i is {:?}", i);
        let int_i = i as i32;
        for j in 0..width {
            let int_j = j as i32;
            if walls[i][j] {
                continue;
            }
            for height_diff in -20..21 {
                for width_diff in -20..21 {
                    let total_travel = num::Signed::abs(&height_diff) + num::Signed::abs(&width_diff);
                    if total_travel > 20 {
                        continue;
                    }
                    if height_diff == 0 {
                        println!("{:?} {:?}", i, end);
                    }
                    /*
                    if height_diff == 0 && i == end.0 {
                        println!("height moment");
                        if (j < end.1 && (end.1 as i32) < int_j + width_diff) ||
                        (j > end.1 && (end.1 as i32) > int_j + width_diff) {
                            if width_diff.abs() > 18 {
                                continue
                            }
                        }
                    }
                    if width_diff == 0 && j == end.1 {
                        if (i < end.0 && (end.0 as i32) < int_i + height_diff) ||
                        (i > end.0 && (end.0 as i32) > int_i + height_diff) {
                            if height_diff.abs() > 18 {
                                continue
                            }
                        }
                    }
                    */

                    let new_pos = (int_i + height_diff, int_j + width_diff);
                    if pos_out_of_bounds(new_pos, i_height, i_width) {
                        continue;
                    }

                    let u_new_pos = (new_pos.0 as usize, new_pos.1 as usize);
                    if walls[u_new_pos.0][u_new_pos.1] {
                        continue;
                    }
                    let this_distance = distances[i][j];
                    let that_distance = distances[u_new_pos.0][u_new_pos.1];
                    let diff = this_distance - that_distance - total_travel;
                    if diff >= 100 {
                        match distance_to_count.get(&diff) {
                            Some(n) => distance_to_count.insert(diff, n + 1),
                            None => distance_to_count.insert(diff, 1),
                        };
                        total += 1;
                    }
                }
            }
        }
    }
    Some(total)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(5));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(41));
    }
}
