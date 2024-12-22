pub mod template;

// Use this file to add helper functions and additional modules.
pub mod utils;

pub fn pos_out_of_bounds(pos: (i32, i32), height: i32, width: i32) -> bool {
    pos.0 < 0 || pos.1 < 0 || pos.0 >= height || pos.1 >= width
}

pub fn turn_left(dir: (i32, i32)) -> (i32, i32) {
    match dir {
        (1, 0) => (0, 1),
        (0, 1) => (-1, 0),
        (-1, 0) => (0, -1),
        (0, -1) => (1, 0),
        _ => panic!("bad dir")
    }
}

pub fn turn_right(dir: (i32, i32)) -> (i32, i32) {
    match dir {
        (1, 0) => (0, -1),
        (0, 1) => (1, 0),
        (-1, 0) => (0, 1),
        (0, -1) => (-1, 0),
        _ => panic!("bad dir")
    }
}