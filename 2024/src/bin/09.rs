advent_of_code::solution!(9);

pub fn input_to_disk(input: &str) -> Vec<i32> {
    let mut ret: Vec<i32> = Vec::new();
    let mut id = 0;
    for c in input.chars() {
        let c_digit = c.to_digit(10).unwrap() as usize;
        let id_val = if id % 2 == 1 { -1 } else { id / 2 };
        for i in 0..c_digit {
            ret.push(id_val);
        }
        id += 1;
    }
    ret
}

pub fn part_one(input: &str) -> Option<u64> {
    let mut disk = input_to_disk(input.trim());

    let mut front_pointer = 0;
    let mut back_pointer = disk.len() - 1;

    while front_pointer < back_pointer {
        if disk[front_pointer] == -1 {
            while back_pointer > 0 && disk[back_pointer] == -1 {
                back_pointer -= 1;
            }
            if back_pointer < front_pointer {
                break;
            }
            disk[front_pointer] = disk[back_pointer];
            disk[back_pointer] = -1;
        }
        front_pointer += 1;
    }
    println!("{:?}", disk);


    let mut checksum: u64 = 0;
    for i in 0..disk.len() {
        let c = disk[i];
        if c == -1 {
            break;
        }
        checksum += (c as u64) * (i as u64);
    }

    Some(checksum)
}

pub fn input_to_disk_2(input: &str) -> Vec<(i32, usize)> {
    let mut ret: Vec<(i32, usize)> = Vec::new();
    let mut id = 0;
    for c in input.chars() {
        let c_digit = c.to_digit(10).unwrap() as usize;
        let id_val = if id % 2 == 1 { -1 } else { id / 2 };
        ret.push((id_val, c_digit));
        id += 1;
    }
    ret
}

pub fn part_two(input: &str) -> Option<u64> {
    let mut disk = input_to_disk_2(input.trim());

    let mut back_pointer = disk.len() - 1;
    while back_pointer > 0 {
        // don't care if the back pointer points to nothing
        if disk[back_pointer].0 == -1 {
            back_pointer -= 1;
            continue;
        }
        let segment_length = disk[back_pointer].1;
        let front_pointer = 0;
        let found = false;
        while front_pointer < back_pointer {
            if disk[front_pointer].0 == -1 && disk[front_pointer].1 <= segment_length {
                found = true;
                break;
            }
            front_pointer += 1;
        }
        if found {
            // move back pointer into front pointer
        }
        let front_pointer = 0;
        if disk[front_pointer].0 == -1 {
            while back_pointer > 0 && disk[back_pointer] == -1 {
                back_pointer -= 1;
            }
            if back_pointer < front_pointer {
                break;
            }
            disk[front_pointer] = disk[back_pointer];
            disk[back_pointer] = -1;
        }
        front_pointer += 1;
    }
    println!("{:?}", disk);


    let mut checksum: u64 = 0;
    for i in 0..disk.len() {
        let c = disk[i];
        if c == -1 {
            break;
        }
        checksum += (c as u64) * (i as u64);
    }

    Some(checksum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(1928));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
