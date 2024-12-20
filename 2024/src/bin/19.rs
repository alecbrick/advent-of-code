use std::{cmp::min, collections::{HashMap, HashSet}};

use regex::Regex;

advent_of_code::solution!(19);

pub fn part_one(input: &str) -> Option<u32> {
    let (patterns_str, designs_str) = input.trim().split_once("\n\n").unwrap();

    let patterns: Vec<&str> = patterns_str.split(", ").collect();
    let designs: Vec<&str> = designs_str.split("\n").collect();

    let regex_str = patterns.join("|");
    let re = Regex::new(format!("^({})+$", regex_str).as_str()).unwrap();
    
    let results: Vec<&str> = designs.into_iter().filter(|x| re.is_match(x)).collect();

    Some(results.len() as u32)
}



pub fn part_two(input: &str) -> Option<u64> {
    let (patterns_str, designs_str) = input.trim().split_once("\n\n").unwrap();

    let patterns: HashSet<&str> = patterns_str.split(", ").collect();
    println!("{:?}", patterns);
    let designs: Vec<&str> = designs_str.split("\n").collect();

    let mut sum = 0;
    let mut max_len = 0;
    let mut min_len = 100;

    for pattern in &patterns {
        if pattern.len() > max_len {
            max_len = pattern.len();
        }
        if pattern.len() < min_len {
            min_len = pattern.len();
        }
    }
    println!("Min, max: {} / {}", min_len, max_len);
    let mut pattern_to_count: HashMap<String, u64> = HashMap::new();

    fn find_designs(design: &str, pattern_to_count: &mut HashMap<String, u64>, min_len: usize, max_len: usize, patterns: &HashSet<&str>) -> u64 {
        if design.len() == 0 {
            return 1;
        }
        if design.len() < min_len {
            return 0;
        }
        if pattern_to_count.contains_key(design) {
            return *pattern_to_count.get(design).unwrap()
        }
        let mut total = 0;
        for i in min_len..min(design.len() + 1, max_len + 1) {
            let slice = &design[0..i];
            if patterns.contains(&slice) {
                total += find_designs(&design[i..design.len()], pattern_to_count, min_len, max_len, patterns)
            }
        }
        pattern_to_count.insert(design.to_string(), total);
        return total
    }

    for design in designs {
        let result = find_designs(design, &mut pattern_to_count, min_len as usize, max_len as usize, &patterns);
        println!("Result for {}: {}", design, result);
        sum += result
    }
    println!("{:?}", pattern_to_count);

    Some(sum as u64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(6));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(16));
    }
}
