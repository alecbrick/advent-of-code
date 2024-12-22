use std::collections::{HashSet, VecDeque};

use advent_of_code::{pos_out_of_bounds, turn_left, turn_right};

advent_of_code::solution!(12);

pub fn count_sides(grid: &Vec<Vec<char>>, start_pos: (i32, i32), start_dir: (i32, i32), visited_sides: &mut HashSet<((i32, i32), (i32, i32))>) -> u32 {
    // count sides (part 2)
    // We must start in an upper-left corner.
    // If not, we would have seen the region sooner.

    // Update: Oh NO. Islands have sides, too.
    // We need to compute the border side count, as well as the side count for each island.
    // This is fine - we just need to run the side count algorithm on each island we find.
    // The problem is making sure we don't rerun the algorithm when necessary.
    let mut pos = start_pos;
    let mut side_count = 0;
    let height = grid.len() as i32;
    let width = grid[0].len() as i32;
    let region_char = grid[start_pos.0 as usize][start_pos.1 as usize];

    // We start facing right.
    let mut dir = start_dir;
    loop {
        let left_dir = turn_left(dir);
        let left_pos = (pos.0 + left_dir.0, pos.1 + left_dir.1);
        visited_sides.insert((pos, left_pos));
        let straight_pos = (pos.0 + dir.0, pos.1 + dir.1);
        if !pos_out_of_bounds(left_pos, height, width) && grid[left_pos.0 as usize][left_pos.1 as usize] == region_char {
            // turn left
            dir = left_dir;
            pos = left_pos;
            side_count += 1;
        } 
        else if pos_out_of_bounds(straight_pos, height, width) || grid[straight_pos.0 as usize][straight_pos.1 as usize] != region_char {
            // turn right
            dir = turn_right(dir);
            side_count += 1;
        } else {
            // go straight
            pos = straight_pos;
        }
        if pos == start_pos && dir == start_dir {
            break;
        }
    }
    side_count
}

pub fn find_region(grid: &Vec<Vec<char>>, i: usize, j: usize, visited: &mut Vec<Vec<bool>>) -> (u32, u32, u32) {
    let region_char = grid[i][j];
    let curr_y = i as i32;
    let curr_x = j as i32;
    let height = grid.len() as i32;
    let width = grid[0].len() as i32;

    let mut area: u32 = 0;
    let mut perimeter: u32 = 0;

    let mut queue = VecDeque::new();
    queue.push_back((curr_y, curr_x));

    let mut visited_sides = HashSet::new();
    let mut side_count = count_sides(grid, (curr_y, curr_x), (0, 1), &mut visited_sides);

    while let Some((y, x)) = queue.pop_front() {
        let (uy, ux) = (y as usize, x as usize);
        if visited[uy][ux] {
            continue;
        }
        visited[uy][ux] = true;
        area += 1;
        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)] {
            let (next_y, next_x) = (y + dir.0, x + dir.1);
            if pos_out_of_bounds((next_y, next_x), height, width) || grid[next_y as usize][next_x as usize] != region_char {
                perimeter += 1;
                // Run side count here, too.
                if !visited_sides.contains(&((y, x), (next_y, next_x))) {
                    side_count += count_sides(grid, (y, x), turn_right(dir), &mut visited_sides);

                }
            } else {
                queue.push_back((next_y, next_x));
            }
        }
    }

    println!("Area {:?} has side count {:?}.", region_char, side_count);

    (perimeter, area, side_count)
}

pub fn part_one(input: &str) -> Option<u32> {
    let grid: Vec<Vec<char>> = input.trim().split("\n").map(|line| line.chars().collect()).collect();
    let height = grid.len();
    let width = grid[0].len();
    let mut visited = vec![vec![false; width]; height];

    let mut price = 0;
    for i in 0..height {
        for j in 0..width {
            if !visited[i][j] {
                // find the plot starting here
                let (perimeter, area, _) = find_region(&grid, i, j, &mut visited);
                price += perimeter * area;
            }
        }
    }
    Some(price)
}

pub fn part_two(input: &str) -> Option<u32> {
    let grid: Vec<Vec<char>> = input.trim().split("\n").map(|line| line.chars().collect()).collect();
    let height = grid.len();
    let width = grid[0].len();
    let mut visited = vec![vec![false; width]; height];

    let mut price = 0;
    for i in 0..height {
        for j in 0..width {
            if !visited[i][j] {
                // find the plot starting here
                let (_, area, side_count) = find_region(&grid, i, j, &mut visited);
                price += side_count * area;
            }
        }
    }
    Some(price)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }

    #[test]
    fn test_part_two() {
        let result: Option<u32> = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(1206));
    }
}
