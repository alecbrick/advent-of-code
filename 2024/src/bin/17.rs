advent_of_code::solution!(17);

pub fn get_combo_value(registers: &Vec<u32>, combo: u32) -> u32 {
    if combo <= 3 {
        return combo;
    }
    return registers[(combo - 4) as usize];
}

pub fn adv(registers: &Vec<u32>, operand: u32) -> u32 {
    let num = registers[0];
    let combo_value = get_combo_value(registers, operand);
    let denom: u32 = (2 as u32).pow(combo_value);
    num / denom
}

pub fn part_one(_input: &str) -> Option<String> {
    let mut i = 0;
    let mut output: Vec<u32> = Vec::new();
    let mut registers: Vec<u32> = vec![47792830, 0, 0];
    let program: Vec<u32> = vec![2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0];
    while i < program.len() {
        let inst = program[i];
        let operand: u32 = program[i + 1];
        let mut jumped = false;
        match inst {
            0 => {
                registers[0] = adv(&registers, operand);
            },
            1 => {
                registers[1] = registers[1] ^ operand;
            },
            2 => {
                let combo_value = get_combo_value(&registers, operand);
                registers[1] = combo_value & 7;
            },
            3 => {
                if registers[0] != 0 {
                    i = operand as usize;
                    jumped = true;
                }
            },
            4 => {
                registers[1] = registers[1] ^ registers[2]
            },
            5 => {
                let combo_value = get_combo_value(&registers, operand);
                output.push(combo_value & 7);
            },
            6 => {
                registers[1] = adv(&registers, operand);
            },
            7 => {
                registers[2] = adv(&registers, operand);
            },
            _ => panic!("Unknown instruction")
        }
        if !jumped {
            i += 2;
        }
    }

    Some(output.into_iter().map(|num| num.to_string()).collect::<Vec<String>>().join(","))
}

/*
The program:
2 4     B = A % 8       Grab the last 3 bits of A into B
1 5     B = B ^ 5       Invert bits 1 and 3
7 5     C = A / 2^B     C = A / 2^B (Shift A right by B, put it in C)
1 6     B = B ^ 6       Invert bits 1 and 2 of B
4 3     B = B ^ C       XOR B with C (effectively, just the last 3 bits of C, which is A shifted)
5 5     PRINT B % 8     output THIS value
0 3     A = A / 8       shift A right by 3 and work on those bits next
3 0     JNZ 0           start over
*/

/*
So what do we do here?
We need to reconstruct the original A. So we need to work backwards.
For example, the last value printed is 0.
That means the last B is 0.
That means the last C equals the last B (up to the last 3 digits).
So, for each number, we have 8 possible pairs for B and C.
In fact, when we start, we only have 4 possible options for C (shift 0-3).
*/
pub fn part_two(_input: &str) -> Option<u128> {
    let mut program: Vec<u32> = vec![2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0];
    let mut possible_as: Vec<u128> = vec![0];
    
    program.reverse();
    for val in program {
        let mut new_possible_as: Vec<u128> = Vec::new();
        for c in 0..8 {
            // b_2 is the shift value which gets us C
            let b_2 = (val ^ c) ^ 6;
            // b_1 is the current 3 digits of A
            let b_1 = b_2 ^ 5;
            for possible_a in &possible_as {
                let a = possible_a * 8 + (b_1 as u128);
                if ((a >> b_2) & 7) as u32 == c {
                    new_possible_as.push(a);
                }
            }
        }
        possible_as = new_possible_as;
    }

    possible_as.iter().min().copied()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one("");
        println!("{:?}", result);
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        println!("{:?}", result);
    }
}
