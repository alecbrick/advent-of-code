use std::collections::VecDeque;

advent_of_code::solution!(10);

pub fn pos_out_of_bounds(pos: (i32, i32), height: i32, width: i32) -> bool {
    pos.0 < 0 || pos.1 < 0 || pos.0 >= height || pos.1 >= width

}

pub fn compute_score(grid: &Vec<Vec<u32>>, i: usize, j: usize) -> u32 {
    let height = grid.len();
    let width = grid[0].len();
    let mut visited: Vec<Vec<bool>> = vec![vec![false; width]; height];
    let mut score = 0;
    let mut queue: VecDeque<(i32, i32)> = VecDeque::new();
    queue.push_back((i as i32, j as i32));
    while !queue.is_empty() {
        let pos = queue.pop_front().unwrap();
        let u_pos = (pos.0 as usize, pos.1 as usize);
        if visited[u_pos.0][u_pos.1] {
            continue;
        }
        visited[u_pos.0][u_pos.1] = true;
        
        let num = grid[u_pos.0][u_pos.1];
        if num == 9 {
            score += 1;
        }

        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
            let new_pos = (pos.0 + dir.0, pos.1 + dir.1);
            if pos_out_of_bounds(new_pos, height as i32, width as i32) {
                continue
            }
            let u_new_pos = (new_pos.0 as usize, new_pos.1 as usize);
            let new_num = grid[u_new_pos.0][u_new_pos.1];
            if new_num == num + 1 {
                queue.push_back(new_pos);
            }
        }
    }
    score
}

pub fn compute_rating(grid: &Vec<Vec<u32>>, i: usize, j: usize) -> u32 {
    let height = grid.len();
    let width = grid[0].len();
    let mut score = 0;
    let mut queue: VecDeque<(i32, i32)> = VecDeque::new();
    queue.push_back((i as i32, j as i32));
    while !queue.is_empty() {
        let pos = queue.pop_front().unwrap();
        let u_pos = (pos.0 as usize, pos.1 as usize);
        
        let num = grid[u_pos.0][u_pos.1];
        if num == 9 {
            score += 1;
        }

        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
            let new_pos = (pos.0 + dir.0, pos.1 + dir.1);
            if pos_out_of_bounds(new_pos, height as i32, width as i32) {
                continue
            }
            let u_new_pos = (new_pos.0 as usize, new_pos.1 as usize);
            let new_num = grid[u_new_pos.0][u_new_pos.1];
            if new_num == num + 1 {
                queue.push_back(new_pos);
            }
        }
    }
    score
}

pub fn part_one(input: &str) -> Option<u32> {
    let grid: Vec<Vec<u32>> = input.split("\n").map(|line| {
        line.chars().map(|c| {
            c.to_digit(10).unwrap()
        }).collect()
    }).collect();

    let mut scores = 0;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == 0 {
                scores += compute_score(&grid, i, j)
            }
        }
    }

    Some(scores)
}

pub fn part_two(input: &str) -> Option<u32> {
    let grid: Vec<Vec<u32>> = input.split("\n").map(|line| {
        line.chars().map(|c| {
            c.to_digit(10).unwrap()
        }).collect()
    }).collect();

    let mut scores = 0;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == 0 {
                scores += compute_rating(&grid, i, j)
            }
        }
    }

    Some(scores)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(36));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(81));
    }
}
