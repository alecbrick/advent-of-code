use std::collections::{HashMap, HashSet};

advent_of_code::solution!(22);

pub fn mix_prune(secret: u128, val: u128) -> u128 {
    (secret ^ val) % 16777216
}

pub fn next_secret_number(secret: u128) -> u128 {
    let x1 = mix_prune(secret, secret * 64);
    let x2 = mix_prune(x1, x1 / 32);
    mix_prune(x2, x2 * 2048)
}

pub fn part_one(input: &str) -> Option<u128> {
    let numbers: Vec<u128> = input.split("\n").map(|num| num.parse().unwrap()).collect();
    let mut total: u128 = 0;
    for num in numbers {
        let mut curr = num;
        for _ in 0..2000 {
            curr = next_secret_number(curr);
        }
        total += curr;
    }
    Some(total)
}

pub fn part_two(input: &str) -> Option<u32> {
    let numbers: Vec<u128> = input.split("\n").map(|num| num.parse().unwrap()).collect();
    let mut change_to_amount: HashMap<(i8, i8, i8, i8), u32> = HashMap::new();
    for num in numbers {
        let mut buyer_price: Vec<i8> = Vec::new();
        let mut change_set: HashSet<(i8, i8, i8, i8)> = HashSet::new();
        buyer_price.push((num % 10) as i8);
        let mut curr = num;
        for i in 1..2001 {
            curr = next_secret_number(curr);
            buyer_price.push((curr % 10) as i8);
            if i >= 4 {
                let (i0, i1, i2, i3, i4) = (buyer_price[i - 4], buyer_price[i - 3], buyer_price[i - 2], buyer_price[i - 1], buyer_price[i]);
                let changes = (i1 - i0, i2 - i1, i3 - i2, i4 - i3);
                if change_set.contains(&changes) {
                    continue;
                }
                if changes == (-2, 1, -1, 3) {
                    println!("Found changes! Prices are {:?}", (i0, i1, i2, i3, i4));
                }
                change_set.insert(changes);
                change_to_amount.entry(changes).and_modify(|n| *n += i4 as u32).or_insert(i4 as u32);
            }
        }
    }

    println!("amount of {:?} is {:?}", 1, change_to_amount[&(-2, 1, -1, 3)]);
    let mut max_change = (0, 0, 0, 0);
    let mut max_amount = 0;
    for (change, amount) in change_to_amount.into_iter() {
        if amount > max_amount {
            max_change = change;
            max_amount = amount;
        }
    }
    println!("max change is {:?}", max_change);
    Some(max_amount)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(37327623));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(23));
    }
}
