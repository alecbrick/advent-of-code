use std::collections::HashMap;

advent_of_code::solution!(11);

pub fn compute_total(input: &str, n: u32) -> u128 {
    let mut stones = input.split(" ").fold(HashMap::new(), |mut acc, num| {
        let n: u128 = num.parse().unwrap();
        let _ = *acc.entry(n).and_modify(|n| *n += 1).or_insert(1);
        acc
    });
    println!("Stones: {:?}", stones);
    
    for _ in 0..n {
        let mut new_stones: HashMap<u128, u128> = HashMap::new();
        for (stone_ref, count_ref) in stones.iter() {
            let stone = *stone_ref;
            let count = *count_ref;
            if stone == 0 {
                new_stones.entry(1).and_modify(|n| *n += count).or_insert(count);
            } else {
                let val_str = stone.to_string();
                if val_str.len() % 2 != 0 {
                    let next_key = stone * 2024;
                    new_stones.entry(next_key).and_modify(|n| *n += count).or_insert(count);
                } else {
                    let (val_1_str, val_2_str) = val_str.split_at(val_str.len() / 2);
                    let val_1: u128 = val_1_str.parse().unwrap();
                    let val_2: u128 = val_2_str.parse().unwrap();
                    new_stones.entry(val_1).and_modify(|n| *n += count).or_insert(count);
                    new_stones.entry(val_2).and_modify(|n| *n += count).or_insert(count);
                }
            } 
        }
        stones = new_stones;
    }

    return stones.iter().fold(0, |acc, (_, value)| {acc + value})
}

pub fn part_one(input: &str) -> Option<u128> {
    Some(compute_total(input, 25))
}

pub fn part_two(input: &str) -> Option<u128> {
    Some(compute_total(input, 75))
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
