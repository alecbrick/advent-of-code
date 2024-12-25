advent_of_code::solution!(25);

pub fn part_one(input: &str) -> Option<u32> {
    let lock_keys: Vec<&str> = input.trim().split("\n\n").collect();
    let mut locks = Vec::new();
    let mut keys = Vec::new();

    for lk in lock_keys {
        let lk_vec: Vec<Vec<char>> = lk.split("\n").map(|row| row.chars().collect()).collect();
        let key = lk_vec[0][0] == '#';
        
        let mut counts = vec![0; lk_vec[0].len()];
        for i in 0..lk_vec.len() {
            for j in 0..lk_vec[0].len() {
                if lk_vec[i][j] == '#' {
                    counts[j] += 1;
                }
            }
        }
        if key {
            keys.push(counts);
        } else {
            locks.push(counts);
        }
    }

    let mut total = 0;
    for l in locks {
        for k in keys.iter() {
            let mut found = true;
            for i in 0..l.len() {
                if l[i] + k[i] > 7 {
                    found = false;
                } 
            }
            if found {
                total += 1;
            }
        }
    }

    Some(total)
}

pub fn part_two(_: &str) -> Option<u32> {
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
