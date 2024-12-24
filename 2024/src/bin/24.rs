use std::collections::{HashMap, HashSet};

advent_of_code::solution!(24);

pub fn compute(output: &str, states: &mut HashMap<String, bool>, logic: &HashMap<&str, (&str, &str, &str)>) -> bool {
    if let Some(x) = states.get(output) {
        return *x
    }

    let inputs = logic.get(output).unwrap();
    let i1_result = compute(inputs.0, states, logic);
    let i2_result = compute(inputs.2, states, logic);
    let result = match inputs.1 {
        "AND" => i1_result && i2_result,
        "OR" => i1_result || i2_result,
        "XOR" => i1_result ^ i2_result,
        _ => panic!("unknown op")
    };
    states.insert(output.to_string(), result);

    result
}

pub fn part_one(input: &str) -> Option<u128> {
    let (states_str, logic_str) = input.trim().split_once("\n\n").unwrap();
    let mut states: HashMap<String, bool> = states_str.split("\n").fold(HashMap::new(), |mut acc, state| {
        let (str, value) = state.split_once(": ").unwrap();
        let bool_val = if value == "0" { false } else { true };
        acc.insert(str.to_string(), bool_val);
        acc
    });

    let logic: HashMap<&str, (&str, &str, &str)> = logic_str.split("\n").fold(HashMap::new(), |mut acc, logic| {
        let logic_vec: Vec<&str> = logic.split(" ").collect();
        let v1 = logic_vec[0];
        let op = logic_vec[1];
        let v2 = logic_vec[2];
        let out = logic_vec[4];
        acc.insert(out, (v1, op, v2));
        acc
    });

    let mut total = 0;
    println!("{:?}", logic);
    for (output, _) in logic.iter() {
        let result = compute(output, &mut states, &logic);
        if result && output.starts_with("z") {
            let value: u32 = output[1..].parse().unwrap();
            total += 2_u128.pow(value)
            
        }
    }

    Some(total)
}

pub fn print_logic(output: &str, logic: &HashMap<&str, (&str, &str, &str)>, visited: &mut HashSet<String>) {
    if visited.contains(output) {
        return;
    }
    visited.insert(output.to_string());
    let z_logic = logic.get(&(output)).unwrap();
    println!("{}: {:?}", output, z_logic);
    if logic.contains_key(z_logic.0) {
        print_logic(z_logic.0, logic, visited);
    }
    if logic.contains_key(z_logic.2) {
        print_logic(z_logic.2, logic, visited);
    }
}


pub fn part_two(input: &str) -> Option<u32> {
    let (_, logic_str) = input.trim().split_once("\n\n").unwrap();

    let logic: HashMap<&str, (&str, &str, &str)> = logic_str.split("\n").fold(HashMap::new(), |mut acc, logic| {
        let logic_vec: Vec<&str> = logic.split(" ").collect();
        let v1 = logic_vec[0];
        let op = logic_vec[1];
        let v2 = logic_vec[2];
        let out = logic_vec[4];
        acc.insert(out, (v1, op, v2));
        acc
    });

    let mut visited: HashSet<String> = HashSet::new();
    for i in 0..46 {
        let z_str = format!("z{:0>2}", i);
        print_logic(&z_str, &logic, &mut visited);
        println!("");
    }
    None
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
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
