use std::collections::{HashMap, HashSet};

advent_of_code::solution!(6);

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
pub enum Direction {
    UP,
    RIGHT,
    DOWN,
    LEFT,
}

impl Direction {
    pub fn turn_right(&self) -> Direction {
        match self {
            Direction::UP => Direction::RIGHT,
            Direction::RIGHT => Direction::DOWN,
            Direction::DOWN => Direction::LEFT,
            Direction::LEFT => Direction::UP,
        }
    }

    pub fn next_pos(&self, pos: (i32, i32)) -> (i32, i32) {
        match self {
            Direction::UP => (pos.0 - 1, pos.1),
            Direction::RIGHT => (pos.0, pos.1 + 1),
            Direction::DOWN => (pos.0 + 1, pos.1),
            Direction::LEFT => (pos.0, pos.1 - 1),
        }
    }
}

pub fn parse_input(input: &str) -> (HashSet<(i32, i32)>, (i32, i32)) {
    let lines: Vec<&str> = input.split_whitespace().collect();
    let mut walls: HashSet<(i32, i32)> = HashSet::new();
    let mut pos: (i32, i32) = (0, 0);
    for i in 0..lines.len() {
        let line = lines[i].as_bytes();
        for j in 0..lines[i].len() {
            match line[j] {
                b'#' => {
                    walls.insert((i as i32, j as i32));
                },
                b'^' => {
                    pos = (i as i32, j as i32)
                },
                _ => ()
            }
        }
    }
    return (walls, pos)
}

pub fn pos_out_of_bounds(pos: (i32, i32), height: i32, width: i32) -> bool {
    pos.0 < 0 || pos.1 < 0 || pos.0 >= height || pos.1 >= width

}

pub fn part_one(input: &str) -> Option<u32> {
    let (walls, start) = parse_input(input);
    let rows: Vec<&str> = input.split_whitespace().collect();
    let height = rows.len() as i32;
    let width = rows[0].len() as i32;
    let mut dir: Direction = Direction::UP;
    let mut visited: HashMap<i32, HashSet<i32>> = HashMap::new();
    visited.entry(start.0).or_default().insert(start.1);

    let mut pos: (i32, i32) = (start.0.try_into().unwrap(), start.1.try_into().unwrap());
    loop {
        let new_pos = match dir {
            Direction::UP => (pos.0 - 1, pos.1),
            Direction::RIGHT => (pos.0, pos.1 + 1),
            Direction::DOWN => (pos.0 + 1, pos.1),
            Direction::LEFT => (pos.0, pos.1 - 1),
        };
        if new_pos.0 < 0 || new_pos.1 < 0 || new_pos.0 >= height || new_pos.1 >= width {
            break;
        }
        if walls.contains(&new_pos) {
            dir = dir.turn_right();
        } else {
            pos = new_pos;
            visited.entry(pos.0).or_default().insert(pos.1);
        }
    }

    return Some(visited.into_iter().fold(0, |acc, elem| acc + elem.1.len() as u32));
}

pub fn has_loop(walls: &HashSet<(i32, i32)>, height: i32, width: i32, start: (i32, i32), start_dir: Direction) -> bool {
    let mut visited: HashMap<i32, HashMap<i32, HashSet<Direction>>> = HashMap::new();
    let mut pos: (i32, i32) = (start.0.try_into().unwrap(), start.1.try_into().unwrap());
    let mut dir = start_dir;
    loop {
        let new_pos = dir.next_pos(pos);
        if pos_out_of_bounds(pos, height, width) {
            break;
        }

        if walls.contains(&new_pos) {
            dir = dir.turn_right();
        } else {
            match visited.get(&new_pos.0).and_then(|x| { x.get(&new_pos.1) }) {
                Some(dirs) => {
                    if dirs.contains(&dir) {
                        return true;
                    }
                }
                None => ()
            }

            pos = new_pos;
            visited.entry(pos.0).or_default().entry(pos.1).or_default().insert(dir);
        }
    }
    
    false
}

pub fn part_two(input: &str) -> Option<u32> {
    let (mut walls, start) = parse_input(input);
    let rows: Vec<&str> = input.split_whitespace().collect();
    let height = rows.len() as i32;
    let width = rows[0].len() as i32;
    let mut dir: Direction = Direction::UP;
    let mut visited: HashMap<(i32, i32), HashSet<Direction>> = HashMap::new();
    visited.entry(start).or_default().insert(dir);

    let mut pos: (i32, i32) = (start.0.try_into().unwrap(), start.1.try_into().unwrap());
    let mut obstructions: HashSet<(i32, i32)> = HashSet::new();
    loop {
        let new_pos = dir.next_pos(pos);
        if pos_out_of_bounds(pos, height, width) {
            break;
        }

        // if there's a wall in front of us, turn right
        if walls.contains(&new_pos) {
            dir = dir.turn_right();
        } else {
            // no wall in front of us
            // a block COULD be placed here
            walls.insert(new_pos);
            if !visited.contains_key(&new_pos) && 
                    !pos_out_of_bounds(new_pos, height, width) &&
                    (new_pos != start) && 
                    has_loop(&walls, height, width, pos, dir) {
                obstructions.insert(new_pos);
            }
            walls.remove(&new_pos);

            pos = new_pos;
            visited.entry(pos).or_default().insert(dir);
        }
    }

    return Some(obstructions.len() as u32);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(41));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(6));
    }
}
