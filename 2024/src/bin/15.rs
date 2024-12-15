advent_of_code::solution!(15);

pub fn dir_to_vec(dir: char) -> (i32, i32) {
    match dir {
        '^' => {(-1, 0)}
        '>' => {(0, 1)}
        'v' => {(1, 0)}
        '<' => {(0, -1)}
        _ => {(0, 0)}
    }
}

pub fn move_and_update_grid(pos: (usize, usize), dir: (i32, i32), grid: &mut Vec<Vec<char>>) -> bool {
    let pos_int = (pos.0 as i32, pos.1 as i32);
    let next_spot_int = (pos_int.0 + dir.0, pos_int.1 + dir.1);
    let next = (next_spot_int.0 as usize, next_spot_int.1 as usize);

    let n = grid[next.0][next.1];
    if n == '#' {
        return false;
    } else if n == '.' {
        grid[next.0][next.1] = grid[pos.0][pos.1];
        grid[pos.0][pos.1] = '.';
        return true;
    } else {
        let result = move_and_update_grid(next, dir, grid);
        if !result {
            false
        } else {
            grid[next.0][next.1] = grid[pos.0][pos.1];
            grid[pos.0][pos.1] = '.'; 
            true
        }
    }
}

pub fn move_and_update_grid_2(pos: (usize, usize), dir: (i32, i32), grid: &mut Vec<Vec<char>>) -> bool {
    let pos_int = (pos.0 as i32, pos.1 as i32);
    let next_spot_int = (pos_int.0 + dir.0, pos_int.1 + dir.1);
    let next = (next_spot_int.0 as usize, next_spot_int.1 as usize);

    let n = grid[next.0][next.1];
    if n == '#' {
        return false;
    } else if n == '.' {
        grid[next.0][next.1] = grid[pos.0][pos.1];
        grid[pos.0][pos.1] = '.';
        return true;
    } else if dir.0 == 0 {
        let result = move_and_update_grid(next, dir, grid);
        if !result {
            false
        } else {
            grid[next.0][next.1] = grid[pos.0][pos.1];
            grid[pos.0][pos.1] = '.'; 
            true
        }
    } else {
        let next_2 = if n == '[' {
            (next.0, next.1 + 1)
        } else {
            (next.0, next.1 - 1)
        };
        let result_1 = move_and_update_grid_2(next, dir, grid);
        let result_2 = move_and_update_grid_2(next_2, dir, grid);
        if !(result_1 && result_2) {
            false
        } else {
            grid[next.0][next.1] = grid[pos.0][pos.1];
            grid[pos.0][pos.1] = '.'; 
            true
        }
    }
}

pub fn print_grid(grid: &Vec<Vec<char>>) {
    for row in grid {
        let row_str: String = row.into_iter().collect();
        println!("{:?}", row_str);
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    let (grid_str, moves) = input.split_once("\n\n").unwrap();

    let mut grid: Vec<Vec<char>> = grid_str.split("\n").map(|line| line.chars().collect()).collect();

    let mut pos = (0, 0);
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == '@' {
                pos = (i, j);
                grid[i][j] = '.';
            }
        }
    }

    for dir in moves.chars() {
        let vec = dir_to_vec(dir);
        if move_and_update_grid(pos, vec, &mut grid) {
            // update position
            let pos_int = (pos.0 as i32, pos.1 as i32);
            let next_spot_int = (pos_int.0 + vec.0, pos_int.1 + vec.1);
            pos = (next_spot_int.0 as usize, next_spot_int.1 as usize);
        }
    }

    let mut ret = 0;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == 'O' {
                ret += 100 * i + j;
            }
        }
    }
    Some(ret.try_into().unwrap())
}

pub fn part_two(input: &str) -> Option<u32> {
    let (grid_str, moves) = input.split_once("\n\n").unwrap();

    // expand the grid
    let mut grid: Vec<Vec<char>> = grid_str.split("\n").map(|line| {
        line.chars().flat_map(|c| {
            match c {
                '#' => ['#', '#'],
                '.' => ['.', '.'],
                'O' => ['[', ']'],
                '@' => ['@', '.'],
                _ => panic!("illegal character"),
            }
        }).collect()
    }).collect();

    let mut pos = (0, 0);
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == '@' {
                pos = (i, j);
                grid[i][j] = '.';
            }
        }
    }

    for dir in moves.chars() {
        let vec = dir_to_vec(dir);
        let mut test_grid = grid.clone();
        if move_and_update_grid_2(pos, vec, &mut test_grid) {
            // update position
            let pos_int = (pos.0 as i32, pos.1 as i32);
            let next_spot_int = (pos_int.0 + vec.0, pos_int.1 + vec.1);
            pos = (next_spot_int.0 as usize, next_spot_int.1 as usize);
            grid = test_grid
        }
        /*
        grid[pos.0][pos.1] = '@';
        print_grid(&grid);
        grid[pos.0][pos.1] = '.';
        */
    }

    let mut ret = 0;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == '[' {
                ret += 100 * i + j;
            }
        }
    }
    Some(ret.try_into().unwrap())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(10092));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(9021));
    }
}
