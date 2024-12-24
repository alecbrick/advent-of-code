use std::io;
use advent_of_code::utils::read_lines;

fn in_bounds(height: i32, width: i32, y: i32, x: i32) -> bool {
    if y < 0 || x < 0 {
        return false;
    }
    if y >= height || x >= width {
        return false;
    }
    return true;
}

fn part_1(lines: &Vec<String>) {
    let mut total = 0;
    let search_string = "XMAS";
    let height: i32 = lines.len().try_into().unwrap();
    let width: i32 = lines[0].len().try_into().unwrap();
    for i in 0..lines.len() {
        for j in 0..lines[0].len() {
            for dir_y in -1..2 {
                for dir_x in -1..2 {
                    let mut curr = 0;
                    let mut curr_y: i32 = i.try_into().unwrap();
                    let mut curr_x: i32 = j.try_into().unwrap();
                    let mut found = false;
                    while curr < search_string.len() {
                        if !in_bounds(height, width, curr_y, curr_x) {
                            break;
                        }
                        let usize_y: usize = curr_y.try_into().unwrap();
                        let usize_x: usize = curr_x.try_into().unwrap();
                        if lines[usize_y].as_bytes()[usize_x] != search_string.as_bytes()[curr] {
                            break;
                        }
                        curr_y += dir_y;
                        curr_x += dir_x;
                        curr += 1;
                        if curr == 4 {
                            found = true;
                            break;
                        }
                    }
                    if found {
                        total += 1;
                    }
                }
            }
        }
    }
    println!("{}", total)
}


fn part_2(lines: &Vec<String>) {
    let search_string = "MAS";
    let height: i32 = lines.len().try_into().unwrap();
    let width: i32 = lines[0].len().try_into().unwrap();

    let mut a_counts = vec![vec![0; lines[0].len()]; lines.len()];

    for i in 0..lines.len() {
        for j in 0..lines[0].len() {
            for dir_y in [-1, 1] {
                for dir_x in [-1, 1] {
                    let mut curr = 0;
                    let mut curr_y: i32 = i.try_into().unwrap();
                    let mut curr_x: i32 = j.try_into().unwrap();
                    let mut found = false;
                    let mut a_y: usize = 0;
                    let mut a_x: usize = 0;
                    while curr < search_string.len() {
                        if !in_bounds(height, width, curr_y, curr_x) {
                            break;
                        }
                        let usize_y: usize = curr_y.try_into().unwrap();
                        let usize_x: usize = curr_x.try_into().unwrap();
                        if lines[usize_y].as_bytes()[usize_x] != search_string.as_bytes()[curr] {
                            break;
                        }
                        // if this is the a:
                        if curr == 1 {
                            a_y = usize_y;
                            a_x = usize_x;
                        }
                        curr_y += dir_y;
                        curr_x += dir_x;
                        curr += 1;
                        if curr == search_string.len() {
                            found = true;
                            break;
                        }
                    }
                    if found {
                        a_counts[a_y][a_x] += 1
                    }
                }
            }
        }
    }
    let mut total = 0;
    for i in 0..lines.len() {
        for j in 0..lines[0].len() {
            if a_counts[i][j] == 2 {
                total += 1;
            }
        }
    }
    println!("{}", total)
}


fn main() -> io::Result<()> {
    let lines = read_lines("data/inputs/04.txt")?;
    part_1(&lines);
    part_2(&lines);
    Ok(())
}
