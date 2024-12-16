use std::collections::HashMap;
use num::bigint::BigUint;

advent_of_code::solution!(11);

struct Node {
    value: u128,
    steps: u32,
    left: u128,
    right: u128,
}

impl Node {
    pub fn new(value: u128) -> Node {
        let mut i: u32 = 0;
        let mut curr_val = value;
        while i < 26 {
            if curr_val == 0 {
                curr_val = 1;
                i += 1;
                continue;
            }
            let val_str = value.to_string();
            if val_str.len() % 2 != 0 {
                // case odd
                curr_val *= 2024;
                i += 1;
                continue;
            }
            let (val_1_str, val_2_str) = val_str.split_at(val_str.len() / 2);
            let val_1: u128 = val_1_str.parse().unwrap();
            let val_2: u128 = val_2_str.parse().unwrap();
            i += 1;
            return Node {
                value: value,
                steps: i,
                left: val_1,
                right: val_2
            }
        };
        // TODO: Probably buggy? We shouldn't use left/right values when steps is 25
        Node {
            value: value,
            steps: 26,
            left: 0,
            right: 0,
        }
    }
}

pub fn compute_score(value: u128, graph: &mut HashMap<u128, Node>, steps: u32) -> u64 {
    let node = graph.entry(value).or_insert(Node::new(value));
    let total = node.steps + steps;
    if total == 25 {
        return 2;
    } else if total > 25 {
        return 1;
    } else {
        let left = node.left;
        let right = node.right;
        return compute_score(left, graph, total) + compute_score(right, graph, steps)
    }
}

pub fn part_one(input: &str) -> Option<u64> {
    let mut stones: Vec<u32> = input.split(" ").map(|num| {
        num.parse().unwrap()
    }).collect();
    
    // I mean, obviously this is exponential increase.
    // But we're going to see certain numbers again.
    // In particular, we can iterate over one number at a time.
    // We should keep a mapping of number to vector.
    // Each element of the vector is the number of stones for that number after `i` blinks (1-indexed).
    // We should also store the last iteration for that number.
    // But each number is like 25,000 stones long at the end.
    // Can we store this information more efficiently?
    // Yes. We can store the two digits it BECOMES.
    // So if X becomes Y Z on the third step, then the value of X on the fourth step is the sum of Y and Z after 1 step.
    
    // We can think of this as a graph, and then a flood fill of that graph for 25 steps.
    // Simpler because it's a binary directed graph.

    // A Node has a value, number of steps at that node, and possibly 2 children.
    let mut total: u64 = 0;
    let mut graph: HashMap<u128, Node> = HashMap::new();
    for num in stones {
        total += compute_score(num as u128, &mut graph, 0);
    }

    Some(total)
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
        assert_eq!(result, Some(55312));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
