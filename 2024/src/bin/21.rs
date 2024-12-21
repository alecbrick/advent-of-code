use std::{cmp::min, collections::{HashMap, VecDeque}, hash::Hash, result};
use lazy_static::lazy_static;

advent_of_code::solution!(21);


lazy_static! {
    static ref KEYPAD: HashMap<char, (i32, i32)> = {
        let mut keypad = HashMap::new();
        keypad.insert('7', (0, 0)); 
        keypad.insert('8', (0, 1)); 
        keypad.insert('9', (0, 2)); 
        keypad.insert('4', (1, 0)); 
        keypad.insert('5', (1, 1)); 
        keypad.insert('6', (1, 2)); 
        keypad.insert('1', (2, 0)); 
        keypad.insert('2', (2, 1)); 
        keypad.insert('3', (2, 2)); 
        keypad.insert('0', (3, 1)); 
        keypad.insert('A', (3, 2)); 
        keypad
    };
    static ref DIRPAD: HashMap<char, (i32, i32)> = {
        let mut keypad = HashMap::new();
        keypad.insert('^', (0, 1));
        keypad.insert('A', (0, 2));
        keypad.insert('<', (1, 0));
        keypad.insert('v', (1, 1));
        keypad.insert('>', (1, 2));
        keypad
    };
}

pub fn get_next_code_dirpad(curr_loc: (i32, i32), dest: (i32, i32)) -> Vec<char> {
    let mut y_dist = dest.0 - curr_loc.0;
    let mut x_dist = dest.1 - curr_loc.1;
    let mut next_code: Vec<char> = Vec::new();
    while x_dist != 0 || y_dist != 0 {
        if y_dist > 0 {
            next_code.push('v');
            y_dist -= 1;
        }
        else if x_dist < 0 {
            next_code.push('<');
            x_dist += 1;
        }
        else if x_dist > 0 {
            next_code.push('>');
            x_dist -= 1;
        }
        else if y_dist < 0 {
            next_code.push('^');
            y_dist += 1;
        }

    }
    next_code.push('A');
    next_code
}

pub fn get_next_codes(start: (i32, i32), dest: (i32, i32), is_keypad: bool) -> Vec<Vec<char>> {
    let mut ret = Vec::new();
    let mut queue: VecDeque<((i32, i32), Vec<char>)> = VecDeque::new();
    let blank_space = if is_keypad { (3, 0) } else { (0, 0) };
    queue.push_back((start, Vec::new()));
    while !queue.is_empty() {
        let (curr_loc, path) = queue.pop_front().unwrap();
        if curr_loc == blank_space {
            continue;
        }
        if curr_loc == dest {
            let mut last_path = path.clone();
            last_path.push('A');
            ret.push(last_path);
            continue;
        }
        let y_dist = dest.0 - curr_loc.0;
        let x_dist = dest.1 - curr_loc.1;
        let mut y_path = path.clone();
        let mut x_path = path.clone();
        if y_dist > 0 {
            y_path.push('v');
            queue.push_back(((curr_loc.0 + 1, curr_loc.1), y_path));
        }
        else if y_dist < 0 {
            y_path.push('^');
            queue.push_back(((curr_loc.0 - 1, curr_loc.1), y_path));
        }
        if x_dist > 0 {
            x_path.push('>');
            queue.push_back(((curr_loc.0, curr_loc.1 + 1), x_path));
        }
        else if x_dist < 0 {
            x_path.push('<');
            queue.push_back(((curr_loc.0, curr_loc.1 - 1), x_path));
        }
    }
    ret
}


pub fn enter_dir_code(code: &Vec<char>, n: u32, cache: &mut HashMap<(String, u32), u128>) -> u128 {
    let code_str: String = code.clone().into_iter().collect();
    if cache.contains_key(&(code_str.clone(), n)) {
        return *cache.get(&(code_str.clone(), n)).unwrap()
    }
    let mut ret: u128 = 0;
    let mut curr_loc = DIRPAD.get(&'A').unwrap();
    for c in code {
        let dest = DIRPAD.get(&c).unwrap();
        let next_codes = get_next_codes(*curr_loc, *dest, false);
        let mut min_result = 0;
        for next_code in next_codes {
            let result = if n == 0 {
                next_code.len() as u128
            } else {
                enter_dir_code(&next_code, n - 1, cache)
            };
            if min_result == 0 || result < min_result {
                min_result = result;
            }
        }

        curr_loc = dest;
        ret += min_result;
    }
    // println!("Code {:?} is {:?}", code, next_codes);
    //println!("This evaluates to {:?}.", ret);
    cache.insert((code_str, n), ret);
    ret
}

pub fn enter_code(code: &Vec<char>) -> u128 {
    // Enter a number or A.
    // Robot -> Robot -> Me

    let mut ret: u128 = 0;
    let mut curr_loc = KEYPAD.get(&'A').unwrap();
    let mut cache = HashMap::new();
    for c in code {
        let dest = KEYPAD.get(&c).unwrap();
        let next_codes = get_next_codes(*curr_loc, *dest, true);
        println!("{:?}", next_codes);
        let mut min_dir_code = 0;
        for next_code in next_codes {
            let dir_code = enter_dir_code(&next_code, 24, &mut cache);
            if min_dir_code == 0 || dir_code < min_dir_code {
                min_dir_code = dir_code;
            }
        }
        ret += min_dir_code;
        curr_loc = dest;
    }
    // println!("Code {:?} is {:?}", code, next_codes);
    ret
}

pub fn part_one(input: &str) -> Option<u128> {
    let codes: Vec<&str> = input.trim().split("\n").collect();
    let mut result = 0;
    for code in codes {
        let sequence = enter_code(&code.chars().collect());
        let complexity: u128 = code[0..3].parse::<u128>().unwrap() * sequence;
        result += complexity;
    }
    Some(result)
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
        assert_eq!(result, Some(126384));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
