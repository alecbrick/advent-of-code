use num::integer::Integer;
use regex::Regex;

advent_of_code::solution!(13);

pub fn part_one(input: &str) -> Option<u32> {
    let re = Regex::new(r"\d+").unwrap();
    let nums: Vec<Vec<u32>> = input.trim().split("\n\n").map(|config| {
        re.find_iter(config).map(|m| {
            m.as_str().parse().unwrap()
        }).collect()
    }).collect();

    let mut total = 0;

    for config in nums {
        let (ax, ay) = (config[0], config[1]);
        let (bx, by) = (config[2], config[3]);
        let (x_dest, y_dest) = (config[4], config[5]);

        let (mut curr_x, mut curr_y);
        let mut solutions: Vec<(u32, u32)> = Vec::new();
        for a in 0..100 {
            curr_x = ax * a;
            curr_y = ay * a;
            for b in 0..100 {
                if curr_x == x_dest && curr_y == y_dest {
                    solutions.push((a, b));
                }
                curr_x += bx;
                curr_y += by;
            }
        }
        if solutions.len() == 0 {
            continue;
        }
        let prices: Vec<u32> = solutions.iter().map(|(a, b)| { a * 3 + b }).collect();
        total += prices.iter().min().unwrap_or(&0);
    }
    Some(total)
}

pub fn find_best_solution(a: i128, b: i128, c: i128) -> Option<i128> {
    // had to get Claude to help me out with this one, this is some advanced stuff
    let egcd = a.extended_gcd(&b);

    // c must be divisible by GCD
    if c % egcd.gcd != 0 {
        return None
    }

    let (a, b, c) = (a / egcd.gcd, b / egcd.gcd, c / egcd.gcd);
    let x0 = egcd.x * c;
    let y0 = egcd.y * c;
    
    // First positive value
    let k = -x0 / b + if x0 % b != 0 { 1 } else { 0 };
    let x = x0 + k * b;
    let y = y0 - k * a;
    let left_result = if x >= 0 && y >= 0 {
        Some(3 * x + y)
    } else { 
        None 
    };

    // Last positive value
    let k = y0 / a;  // integer division rounds toward zero
    let x = x0 + k * b;
    let y = y0 - k * a;
    let right_result = if x >= 0 && y >= 0 {
        Some(3 * x + y)
    } else {
        None
    };

    match (left_result, right_result) {
        (Some(l), Some(r)) => Some(l.min(r)),
        (Some(l), None) => Some(l),
        (None, Some(r)) => Some(r),
        (None, None) => None
    }
}

pub fn part_two(input: &str) -> Option<u128> {
    let re = Regex::new(r"\d+").unwrap();
    let nums: Vec<Vec<i128>> = input.trim().split("\n\n").map(|config| {
        re.find_iter(config).map(|m| {
            m.as_str().parse().unwrap()
        }).collect()
    }).collect();

    let mut total = 0;

    for config in nums {
        // system of equations: A*ax + B*bx = x_dest || A * ay + B * by = y_dest
        let (ax, ay) = (config[0], config[1]);
        let (bx, by) = (config[2], config[3]);
        let (x_dest, y_dest) = (config[4] + 10000000000000, config[5] + 10000000000000);

        let det = ax * by - bx * ay;
        if det != 0 {
            // one solution
            let x_num = x_dest * by - y_dest * bx as i128;
            let y_num = ax * y_dest - ay * x_dest as i128;
            if x_num % det == 0 && y_num % det == 0 {
                let x =  x_num / det;
                let y: i128 = y_num / det;
                // solution must be positive
                if x >= 0 && y >= 0 {
                    total += 3 * x + y;
                }
            }
        } else if ax * y_dest != ay * x_dest {
            // parallel lines - no solution
            continue;
        } else {
            // infinite solutions (lines are colinear)
            // find the point (x, y) on this line that minimizes (3x + y)
            // that's either the x intercept or y intercept
            // but it needs to be the first INTEGER that's closest to either of these

            // update: this case literally never even happened lmao
            if let Some(best_solution) = find_best_solution(ax, bx, x_dest) {
                total += best_solution;
            }
        }
    }
    Some(total as u128)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(480));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
