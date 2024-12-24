use std::collections::{HashMap, HashSet};

advent_of_code::solution!(23);

pub fn part_one(input: &str) -> Option<u32> {
    let pairs: Vec<(&str, &str)> =input.trim().split("\n").map(|edge| {
        edge.split_once("-").unwrap()
    }).collect();

    let mut adj_list: HashMap<&str, HashSet<&str>> = HashMap::new();
    let mut ret = 0;
    for (c1, c2) in pairs {
        let empty_set = HashSet::new();
        let c1_list = adj_list.get(c1).unwrap_or(&empty_set);
        let c2_list = adj_list.get(c2).unwrap_or(&empty_set);
        let inter = c1_list.intersection(c2_list);
        for c3 in inter {
            if c1.starts_with("t") || c2.starts_with("t") || c3.starts_with("t") {
                ret += 1;
            }
        }
        adj_list.entry(c1).and_modify(|entry| {entry.insert(c2);}).or_insert_with(HashSet::new).insert(c2);
        adj_list.entry(c2).and_modify(|entry| {entry.insert(c1);}).or_insert_with(HashSet::new).insert(c1);
    }
    Some(ret)
}

pub fn part_two(input: &str) -> Option<u32> {
    let pairs: Vec<(&str, &str)> =input.trim().split("\n").map(|edge| {
        edge.split_once("-").unwrap()
    }).collect();

    let mut adj_list: HashMap<&str, HashSet<&str>> = HashMap::new();
    for (c1, c2) in pairs.iter() {
        adj_list.entry(c1).and_modify(|entry| {entry.insert(c2);}).or_insert_with(HashSet::new).insert(c2);
        adj_list.entry(c2).and_modify(|entry| {entry.insert(c1);}).or_insert_with(HashSet::new).insert(c1);
    }

    let mut the_list: HashSet<Vec<&str>> = pairs.iter().map(|pair_vec| {
        let mut set = Vec::new();
        set.push(pair_vec.0);
        set.push(pair_vec.1);
        set.sort();
        set
    }).collect();

    while !the_list.is_empty() {
        println!("Next iter. List is length {:?}", the_list.len());
        let mut next_list = HashSet::new();
        for set in the_list.iter() {
            let vec_as_set: HashSet<&str> = set.iter().cloned().collect();
            for (c1, vertices) in adj_list.iter() {
                if vertices.is_superset(&vec_as_set) {
                    let mut new_set = set.clone();
                    new_set.push(c1);
                    new_set.sort();
                    next_list.insert(new_set);
                }
            }
        }
        if next_list.is_empty() {
            let this_list_vec: Vec<Vec<&str>> = the_list.into_iter().collect();
            let lan_party = this_list_vec[0].clone();
            let result = lan_party.join(",");
            println!("{}", result);
            return None;
        }
        the_list = next_list;
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
