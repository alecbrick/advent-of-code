use std::{cmp::Ordering, collections::{HashMap, HashSet}};

advent_of_code::solution!(5);

fn parse_input(input: &str) -> (HashMap<u32, HashSet<u32>>, Vec<Vec<u32>>) {
    let (rule_str, lines_str) = input.split_once("\n\n").unwrap();

    let mut rules: HashMap<u32, HashSet<u32>> = HashMap::new();
    for line in rule_str.split("\n") {
        let (start_str, end_str) = line.split_once("|").unwrap();
        let start: u32 = start_str.parse().unwrap();
        let end: u32 = end_str.parse().unwrap();
        rules.entry(start).or_default().insert(end);
    }

    let lines: Vec<Vec<u32>> = lines_str.trim().split("\n").map(|line| {
        line.split(",").map(|elem| elem.parse().unwrap()).collect()
    }).collect();
    (rules, lines)

}

pub fn part_one(input: &str) -> Option<u32> {
    let (rules, lines) = parse_input(input);

    let mut total: u32 = 0;
    for line in lines {
        let mut found = true;
        for i in 0..line.len() - 1 {
            for j in i + 1..line.len() {
                if rules.contains_key(&line[j]) && rules[&line[j]].contains(&line[i]) {
                    found = false;
                    break;
                }
            }
            if !found {
                break;
            }
        }
        if found {
            total += line[(line.len() - 1) / 2]
        }
    }
    return Some(total)
}

pub fn part_two(input: &str) -> Option<u32> {
    let (rules, lines)= parse_input(input);

    let mut total: u32 = 0;
    for line in lines {
        let mut line_copy = line.clone();
        line_copy.sort_by(|a, b| {
            if a == b {
                Ordering::Equal
            } else if rules.contains_key(a) && rules[a].contains(b) {
                Ordering::Less
            } else {
                Ordering::Greater
            }
        });
        if line != line_copy {
            total += line_copy[(line.len() - 1) / 2]
        }
    }
    return Some(total)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(143));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
