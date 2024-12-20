advent_of_code::solution!(16);

use std::{collections::{HashMap, HashSet}, hash::Hash};

use priority_queue::PriorityQueue;

pub fn turn_right(dir: (i32, i32)) -> (i32, i32) {
    match dir {
        (1, 0) => (0, 1),
        (0, 1) => (-1, 0),
        (-1, 0) => (0, -1),
        (0, -1) => (1, 0),
        _ => panic!("bad dir")
    }
}

pub fn turn_left(dir: (i32, i32)) -> (i32, i32) {
    match dir {
        (1, 0) => (0, -1),
        (0, 1) => (1, 0),
        (-1, 0) => (0, 1),
        (0, -1) => (-1, 0),
        _ => panic!("bad dir")
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    let mut grid: Vec<Vec<char>> = input.split("\n").map(|line| line.chars().collect()).collect();

    let mut pos = (0, 0);
    let mut dir = (0, 1);
    let mut found = false;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == 'S' {
                pos = (i, j);
                found = true;
                break;
            }
        }
        if found {
            break;
        }
    }

    let mut visited: HashMap<((usize, usize), (i32, i32)), i32> = HashMap::new();
    let mut queue: PriorityQueue<((usize, usize), (i32, i32), Vec<(usize, usize)>), i32> = PriorityQueue::new();
    let path: Vec<(usize, usize)> = Vec::new();
    queue.push((pos, dir, path), 0);
    loop {
        let ((curr_pos, curr_dir, curr_path), neg_score) = queue.pop().unwrap();
        /*if curr_pos == (15, 1) {
            println!("Pos: {:?}, Dir: {:?}, Score: {:?}", curr_pos, curr_dir, -neg_score);
        }*/
        if grid[curr_pos.0][curr_pos.1] == 'E' {
            return Some((-neg_score) as u32)
        }
        match visited.get(&(curr_pos, curr_dir)) {
            Some(existing_score) => {
                if neg_score <= *existing_score {
                    continue;
                }
            },
            None => ()
        }
        visited.insert((curr_pos, curr_dir), neg_score);

        let right_dir = turn_right(curr_dir);
        queue.push((curr_pos, right_dir, curr_path.clone()), neg_score - 1000);
        let left_dir = turn_left(curr_dir);
        queue.push((curr_pos, left_dir, curr_path.clone()), neg_score - 1000);
        let next_pos = (((curr_pos.0 as i32) + curr_dir.0) as usize, ((curr_pos.1 as i32) + curr_dir.1) as usize);
        if grid[next_pos.0][next_pos.1] != '#' {
            // println!("Next pos: {:?}, symbol: {:?}", next_pos, grid[next_pos.0][next_pos.1]);
            let mut new_path = curr_path.clone();
            new_path.push(next_pos);
            queue.push((next_pos, curr_dir, new_path), neg_score - 1);
        }
    }
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut grid: Vec<Vec<char>> = input.split("\n").map(|line| line.chars().collect()).collect();

    let mut pos = (0, 0);
    let mut dir = (0, 1);
    let mut found = false;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == 'S' {
                pos = (i, j);
                found = true;
                break;
            }
        }
        if found {
            break;
        }
    }

    // I could probably drastically reduce the runtime by using `visited` to merge paths as I go.
    // however I have better things to do
    let mut visited: HashMap<((usize, usize), (i32, i32)), i32> = HashMap::new();
    let mut queue: PriorityQueue<((usize, usize), (i32, i32), Vec<(usize, usize)>), i32> = PriorityQueue::new();
    let mut path: Vec<(usize, usize)> = Vec::new();
    path.push((0, 0));
    queue.push((pos, dir, path), 0);
    let mut best_paths: Vec<Vec<(usize, usize)>> = Vec::new();
    let mut best_score = 0;
    loop {
        let ((curr_pos, curr_dir, curr_path), neg_score) = queue.pop().unwrap();
        if best_score != 0 && neg_score < best_score {
            break;
        }
        if grid[curr_pos.0][curr_pos.1] == 'E' {
            best_score = neg_score;
            best_paths.push(curr_path);
            continue;
        }
        match visited.get(&(curr_pos, curr_dir)) {
            Some(existing_score) => {
                if neg_score < *existing_score {
                    continue;
                }
            },
            None => ()
        }
        visited.insert((curr_pos, curr_dir), neg_score);

        let right_dir = turn_right(curr_dir);
        queue.push((curr_pos, right_dir, curr_path.clone()), neg_score - 1000);
        let left_dir = turn_left(curr_dir);
        queue.push((curr_pos, left_dir, curr_path.clone()), neg_score - 1000);
        let next_pos = (((curr_pos.0 as i32) + curr_dir.0) as usize, ((curr_pos.1 as i32) + curr_dir.1) as usize);
        if grid[next_pos.0][next_pos.1] != '#' {
            let mut new_path = curr_path.clone();
            new_path.push(next_pos);
            queue.push((next_pos, curr_dir, new_path), neg_score - 1);
        }
    }
    let mut best_seats: HashSet<(usize, usize)> = HashSet::new();
    for path in best_paths {
        for pos in path {
            best_seats.insert(pos);
        }
    }
    
    Some(best_seats.len() as u32)

}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(7036));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(45));
    }
}
