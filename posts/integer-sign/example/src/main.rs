fn main() {
    println!("+-----------------------------------------------------------+");
    println!("|            Compare signed and unsigned numbers            |");
    println!("+-----+----------+----------+-----+--------+----------+-----+");
    println!("| #   | unsigned |   bin    | hex | signed |   bin    | hex |");
    println!("|-----|----------|----------|-----|--------|----------|-----|");

    for number in 0..260 {
        // cast 32 bit integer to 8 bit one
        let unsigned: u8 = number as u8; // unsigned integer 8 bit
        let signed: i8 = unsigned as i8; // signed integer 8 bit

        println!(
            "| {0:<3} | {1:<8} | {1:<8b} | {1:<3x} | {2:<6} | {2:<8b} | {2:<3x} |",
            number, unsigned, signed,
        );
    }

    println!("+-----+----------+----------+-----+--------+----------+-----+");
}
