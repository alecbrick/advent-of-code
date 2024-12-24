advent_of_code::solution!(7);

pub fn part_one(input: &str) -> Option<i64> {
    let mut total = 0;
    for line in input.split("\n") {
        let (result_str, operands) = line.split_once(": ")?;
        let result: i64 = result_str.parse::<i64>().unwrap();
        let mut result_set: Vec<i64> = Vec::new();
        for op_str in operands.split(" ") {
            let op: i64 = op_str.parse().unwrap();
            if result_set.len() == 0 {
                result_set.push(op);
            } else {
                let mut new_result_set: Vec<i64> = Vec::new();
                for x in result_set {
                    if x + op <= result {
                        new_result_set.push(x + op);
                    }
                    if x * op <= result {
                        new_result_set.push(x * op);
                    }
                }
                result_set = new_result_set;
            }
        }
        if result_set.contains(&result) {
            total += result;
        }
    };
    return Some(total)
}

pub fn part_two(input: &str) -> Option<i64> {
    let mut total = 0;
    for line in input.split("\n") {
        let (result_str, operands) = line.split_once(": ")?;
        let result: i64 = result_str.parse::<i64>().unwrap();
        let mut result_set: Vec<i64> = Vec::new();
        for op_str in operands.split(" ") {
            let op: i64 = op_str.parse().unwrap();
            if result_set.len() == 0 {
                result_set.push(op);
            } else {
                let mut new_result_set: Vec<i64> = Vec::new();
                for x in result_set {
                    if x + op <= result {
                        new_result_set.push(x + op);
                    }
                    if x * op <= result {
                        new_result_set.push(x * op);
                    }
                    let conc = x.to_string() + &op.to_string();
                    let conc_int = conc.parse().unwrap();
                    if conc_int <= result {
                        new_result_set.push(conc_int);
                    }
                }
                result_set = new_result_set;
            }
        }
        if result_set.contains(&result) {
            total += result;
        }
    };
    return Some(total)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(3749));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
