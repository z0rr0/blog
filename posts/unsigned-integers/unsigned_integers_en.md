# Unsigned Integers in Programming #blog

This post is an English translation of my original article, first published at [z0rr0.blog/unsigned-integers](https://z0rr0.blog/unsigned-integers).

## Why Do We Need Them?

This is a short discussion about unsigned integers in programming.
From a mathematical point of view, they may look a bit strange - why do we even need such “truncated” numbers?

Nevertheless, there are solid reasons for their existence. Here are the main ones:

1. **Extending the available numeric range using the same number of bits.** You can store more values if negative numbers are not required. For example, an 8-bit signed integer can store values from −128 to 127, while an unsigned type can store values from 0 to 255.
2. **Additional control over business logic.** Sometimes application requirements explicitly forbid negative values (for example, quantity of goods, customer age, file size, etc.). Using unsigned types helps to clearly express these constraints and prevents errors related to improper use of negative numbers.
3. **Performance optimizations.** On some CPU architectures, operations on unsigned numbers may be faster than on signed ones. Additionally, this serves as a hint for the compiler or interpreter that certain optimizations are possible.

## How Do They Work?

Let’s write a few small examples to clearly see how unsigned integers behave.

Here is an example in Go. The program iterates over values from 0 to 259 and prints their representation as signed and unsigned numbers, along with their binary and hexadecimal forms.

```go
package main

import (
	"fmt"
	"unsafe"
)

func s2u(s int8) uint8 {
	return *(*uint8)(unsafe.Pointer(&s))
}

func main() {
	var (
		signed   int8
		unsigned uint8
	)

	size := unsafe.Sizeof(signed)
	fmt.Printf("Size of int8 and uint8: %d byte(s)\n\n", size)

	println("+---------------------------------------------------------------------------------+")
	println("|                    Compare signed and unsigned numbers                          |")
	println("+-----+----------+----------+-----+--------+-----------+-----+--------------------+")
	println("| #   | unsigned |   bin    | hex | signed |    bin    | hex | signed as unsigned |")
	println("|-----|----------|----------|-----|--------|-----------|-----|--------------------|")

	for i := range 260 {
		signed = int8(i)
		unsigned = uint8(i)
		signedAsUnsigned := s2u(signed)

		fmt.Printf("| %-3[1]d | %-8[2]d | %-8[2]b | %-3[2]x | %-6[3]d | %-9[3]b | %-3[3]x | %-18[4]b |\n", i, unsigned, signed, signedAsUnsigned)
	}

	println("+-----+----------+----------+-----+--------+-----------+-----+--------------------+")
}
```

The output looks like this (heavily truncated for readability, with `...` inserted):

```
Size of int8 and uint8: 1 byte(s)

+---------------------------------------------------------------------------------+
|                    Compare signed and unsigned numbers                          |
+-----+----------+----------+-----+--------+-----------+-----+--------------------+
| #   | unsigned |   bin    | hex | signed |    bin    | hex | signed as unsigned |
|-----|----------|----------|-----|--------|-----------|-----|--------------------|
| 0   | 0        | 0        | 0   | 0      | 0         | 0   | 0                  |
| 1   | 1        | 1        | 1   | 1      | 1         | 1   | 1                  |
| 2   | 2        | 10       | 2   | 2      | 10        | 2   | 10                 |
...
| 126 | 126      | 1111110  | 7e  | 126    | 1111110   | 7e  | 1111110            |
| 127 | 127      | 1111111  | 7f  | 127    | 1111111   | 7f  | 1111111            |
| 128 | 128      | 10000000 | 80  | -128   | -10000000 | -80 | 10000000           |
| 129 | 129      | 10000001 | 81  | -127   | -1111111  | -7f | 10000001           |
| 130 | 130      | 10000010 | 82  | -126   | -1111110  | -7e | 10000010           |
...
| 254 | 254      | 11111110 | fe  | -2     | -10       | -2  | 11111110           |
| 255 | 255      | 11111111 | ff  | -1     | -1        | -1  | 11111111           |
| 256 | 0        | 0        | 0   | 0      | 0         | 0   | 0                  |
| 257 | 1        | 1        | 1   | 1      | 1         | 1   | 1                  |
| 258 | 2        | 10       | 2   | 2      | 10        | 2   | 10                 |
| 259 | 3        | 11       | 3   | 3      | 11        | 3   | 11                 |
+-----+----------+----------+-----+--------+-----------+-----+--------------------+
```

And here is a similar example in Rust:

```rust
fn main() {
    let size = std::mem::size_of::<u8>();
    println!("Size of i8 and u8: {} byte(s)\n", size);

    println!("+---------------------------------------------------------------------------------+");
    println!("|                    Compare signed and unsigned numbers                          |");
    println!("+-----+----------+----------+-----+--------+-----------+-----+--------------------+");
    println!("| #   | unsigned |   bin    | hex | signed |    bin    | hex | signed as unsigned |");
    println!("|-----|----------|----------|-----|--------|-----------|-----|--------------------|");

    for number in 0..260 {
        // cast 32 bit integer to 8 bit one
        let unsigned: u8 = number as u8; // unsigned integer 8 bit
        let signed: i8 = unsigned as i8; // signed integer 8 bit
        let s2u: u8 = signed as u8; // cast signed to unsigned

        println!(
            "| {0:<3} | {1:<8} | {1:<8b} | {1:<3x} | {2:<6} | {2:<9b} | {2:<3x} | {3:<18b} |",
            number, unsigned, signed, s2u,
        );
    }

    println!("+-----+----------+----------+-----+--------+-----------+-----+--------------------+");
}
```

The output is very similar, but with a few differences:

* In Rust, negative numbers are printed without a minus sign in binary and hexadecimal representations.
* In Go, the same values are printed using two’s complement with a leading minus sign.

It is important to understand that this is only a difference in representation. In memory, both languages store exactly the same data, and Rust also uses two’s complement internally.

```
Size of i8 and u8: 1 byte(s)

+---------------------------------------------------------------------------------+
|                    Compare signed and unsigned numbers                          |
+-----+----------+----------+-----+--------+-----------+-----+--------------------+
| #   | unsigned |   bin    | hex | signed |    bin    | hex | signed as unsigned |
|-----|----------|----------|-----|--------|-----------|-----|--------------------|
| 0   | 0        | 0        | 0   | 0      | 0         | 0   | 0                  |
| 1   | 1        | 1        | 1   | 1      | 1         | 1   | 1                  |
| 2   | 2        | 10       | 2   | 2      | 10        | 2   | 10                 |
...
| 126 | 126      | 1111110  | 7e  | 126    | 1111110   | 7e  | 1111110            |
| 127 | 127      | 1111111  | 7f  | 127    | 1111111   | 7f  | 1111111            |
| 128 | 128      | 10000000 | 80  | -128   | 10000000  | 80  | 10000000           |
| 129 | 129      | 10000001 | 81  | -127   | 10000001  | 81  | 10000001           |
| 130 | 130      | 10000010 | 82  | -126   | 10000010  | 82  | 10000010           |
...
| 254 | 254      | 11111110 | fe  | -2     | 11111110  | fe  | 11111110           |
| 255 | 255      | 11111111 | ff  | -1     | 11111111  | ff  | 11111111           |
| 256 | 0        | 0        | 0   | 0      | 0         | 0   | 0                  |
| 257 | 1        | 1        | 1   | 1      | 1         | 1   | 1                  |
| 258 | 2        | 10       | 2   | 2      | 10        | 2   | 10                 |
| 259 | 3        | 11       | 3   | 3      | 11        | 3   | 11                 |
+-----+----------+----------+-----+--------+-----------+-----+--------------------+
```

**A Short Digression on Two’s Complement.** In a very simplified form, the algorithm for obtaining two’s complement (using `-2` as an example) can be described as follows:

* As shown in the Rust output, the binary representation of `-2` is `11111110`.
* The most significant bit (the leftmost one) represents the sign: `0` for positive, `1` for negative.
* If the most significant bit is `0`, the two’s complement representation is identical to the direct binary representation.
* Otherwise, to obtain the two’s complement of a negative number, invert all bits except the most significant one, resulting in `10000001`, and then add `1`, producing `10000010`. The first bit is interpreted as the sign, and the remaining bits (`0000010`) represent the value `2`. The final result is `-2`.

Looking at the outputs above, two natural questions arise:

1. How can the same binary representation be interpreted differently by the computer?
2. How do we correctly convert signed values to unsigned ones and vice versa?

For the first question, the answer is simple: there is no difference in memory. During compilation or interpretation, the analyzer tracks which type is used at each point. Depending on that type, the same sequence of bits is interpreted differently. Type information effectively lives in the program’s “metadata”, not in the data itself.

Consider this Go program `program.go`:

```go
package main

func signedLess(a, b int8) bool {
	return a < b
}

func unsignedLess(a, b uint8) bool {
	return a < b
}

func main() {
	var (
		signedA   int8  = -1
		signedB   int8  = 2
		unsignedA uint8 = 255
		unsignedB uint8 = 2
	)

	println(signedLess(signedA, signedB))
	println(unsignedLess(unsignedA, unsignedB))
}
```

If we inspect its ARM64 assembly output:

```sh
# GOARCH=arm64
go tool compile -S program.go
```

```
main.signedLess STEXT size=32 args=0x8 locals=0x0 funcid=0x0 align=0x0 leaf
  0x0000 00000 (program.go:3)       TEXT    main.signedLess(SB), LEAF|NOFRAME|ABIInternal, $0-8
  0x0000 00000 (program.go:3)       FUNCDATA        $0, gclocals·g5+hNtRBP6YXNjfog7aZjQ==(SB)
  0x0000 00000 (program.go:3)       FUNCDATA        $1, gclocals·g5+hNtRBP6YXNjfog7aZjQ==(SB)
  0x0000 00000 (program.go:3)       FUNCDATA        $5, main.signedLess.arginfo1(SB)
  0x0000 00000 (program.go:3)       FUNCDATA        $6, main.signedLess.argliveinfo(SB)
  0x0000 00000 (program.go:3)       PCDATA  $3, $1
  0x0000 00000 (program.go:4)       MOVB    R0, R2
  0x0004 00004 (program.go:4)       MOVB    R1, R1
  0x0008 00008 (program.go:4)       CMPW    R2, R1
  0x000c 00012 (program.go:4)       CSET    GT, R0
  0x0010 00016 (program.go:4)       RET     (R30)
  0x0000 02 1c 40 93 21 1c 40 93 3f 00 02 6b e0 d7 9f 9a  ..@.!.@.?..k....
  0x0010 c0 03 5f d6 00 00 00 00 00 00 00 00 00 00 00 00  .._.............
main.unsignedLess STEXT size=32 args=0x8 locals=0x0 funcid=0x0 align=0x0 leaf
  0x0000 00000 (program.go:7)       TEXT    main.unsignedLess(SB), LEAF|NOFRAME|ABIInternal, $0-8
  0x0000 00000 (program.go:7)       FUNCDATA        $0, gclocals·g5+hNtRBP6YXNjfog7aZjQ==(SB)
  0x0000 00000 (program.go:7)       FUNCDATA        $1, gclocals·g5+hNtRBP6YXNjfog7aZjQ==(SB)
  0x0000 00000 (program.go:7)       FUNCDATA        $5, main.unsignedLess.arginfo1(SB)
  0x0000 00000 (program.go:7)       FUNCDATA        $6, main.unsignedLess.argliveinfo(SB)
  0x0000 00000 (program.go:7)       PCDATA  $3, $1
  0x0000 00000 (program.go:8)       MOVBU   R0, R2
  0x0004 00004 (program.go:8)       MOVBU   R1, R1
  0x0008 00008 (program.go:8)       CMPW    R2, R1
  0x000c 00012 (program.go:8)       CSET    HI, R0
  0x0010 00016 (program.go:8)       RET     (R30)
  0x0000 02 1c 40 d3 21 1c 40 d3 3f 00 02 6b e0 97 9f 9a  ..@.!.@.?..k....
  0x0010 c0 03 5f d6 00 00 00 00 00 00 00 00 00 00 00 00  .._.............
```

As shown above, even though `signedA` and `unsignedA` are stored identically in memory, the load instructions (`MOVB` vs `MOVBU`) and the condition codes used to produce the result (`CSET GT` vs `CSET HI`) are different. This is because the compiler knows which type is used in each function and emits machine code appropriate for operating on that type. The `CMPW R2, R1` instruction sets condition flags based on the most significant bit, which may be interpreted as a sign bit or as part of the magnitude depending on the comparison that follows. The comparison itself is selected based on the type: `GT` (greater than) is used for signed comparisons, while `HI` (higher) is used for unsigned comparisons.

Some languages are strict about signedness. Go and Rust do not allow implicit conversions between signed and unsigned integers, which is why the examples used `unsafe.Pointer` in Go and `as` casts in Rust.

```go
var unsigned uint8 = -1
// cannot use -1 (untyped int constant) as uint8 value in assignment (overflows)
```

Even in Go, mistakes are possible. For example, this code produces an infinite loop:

```go
package main

func main() {
	var i uint

	// ...
	for i = 5; i >= 0; i-- {
		println(i)
	}
}
```

This is why the  [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html#Integer_Types) and the designers of Java were historically skeptical about using unsigned integers for arithmetic, recommending them mainly for bit masks.

In C and C++, implicit conversions are allowed and often happen without warnings:

```c++
uint8_t unsigned_number = -1; // implicit conversion, value becomes 255
```

A classic example is comparing signed and unsigned values, such as `if (-1 > unsigned_number)`, which may unexpectedly evaluate to `true`.

Java historically had no unsigned primitives (except `char`, which is 16-bit), as the language designers considered them too error-prone.

Python goes even further: it has a single `int` type with arbitrary precision. When interpreting raw bytes, you must explicitly specify whether the value is signed or unsigned:

```python
number = b"\xff"
unsigned = int.from_bytes(number, byteorder="big", signed=False) # 255
signed = int.from_bytes(number, byteorder="big", signed=True)  # -1
```

Now let us move on to the second question: how to correctly convert a signed integer to an unsigned one and vice versa. In modern programming languages, this is typically done using two’s complement representation, which we discussed earlier — for example, the value `254` (binary `11111110`) is interpreted as `-2`. In fact, no inverse algorithm is required here: we simply reinterpret the same sequence of bits, treating the most significant bit as part of the value rather than as an explicit `- / +` sign.

Another way to reason about two’s complement is the following:

1. If the number is non-negative, the signed and unsigned representations are identical.
2. If the number is negative, the most significant bit is `1`, and the value can be computed as `254 − 256 = −2`, where `256` is `2^8`, i.e. the maximum representable value for an 8-bit number plus one.

## Can We Look at Another Example?

I would like to share a few examples where incorrect handling of unsigned integers has led to bugs.

Consider a ClickHouse table:

```sql
CREATE TABLE test
(
    timestamp DateTime,
    sign      Int8 DEFAULT 1,
    value     UInt8,
    comment   String
) ENGINE = MergeTree() ORDER BY timestamp;
```

This table stores append-only events. Logical deletions are represented by `sign = -1`, while `value` is stored as `UInt8`.

Now we aggregate by day using a materialized view:

```sql
CREATE MATERIALIZED VIEW mv_test
(
    `day`   Date,
    `total` UInt64
)
ENGINE = SummingMergeTree() ORDER BY day
AS
SELECT toStartOfDay(timestamp) AS day,
       sum(value * sign)       AS total
FROM test
GROUP BY day;
```

We choose the `UInt64` type for `total` because we expect it to store the sum of `UInt8` value events; rollbacks should evaluate to `0` and therefore not affect the final result.

```sql
INSERT INTO test
VALUES ('2026-01-01 00:00:01', 1, 1, 'number 1'),
       ('2026-01-01 00:00:02', 1, 2, 'number 2'),
       ('2026-01-01 00:00:06', 1, 255, 'number 255, max unsigned 8-bit');

SELECT * FROM mv_test ORDER BY day FORMAT Vertical;

Row 1:
──────
day:   2026-01-01
total: 258
```

Everything appears to work correctly, but only while implicitly assuming that rollback timestamps always совпiding with the original events. Once this assumption is broken, either by mistake or by design — issues start to surface. For example, the "2nd event rollback" record falls on the day after the "2nd event":

```sql
INSERT INTO test
VALUES ('2026-01-02 23:59:55', 1, 1, '1st event'),
       ('2026-01-02 23:59:58', -1, 1, '1st event rollback'),
       ('2026-01-02 23:59:59', 1, 1, '2nd event'),
       ('2026-01-03 00:00:02', -1, 1, '2nd event rollback');

SELECT * FROM mv_test ORDER BY day FORMAT Vertical;

Row 1:
──────
day:   2026-01-01
total: 258

Row 2:
──────
day:   2026-01-02
total: 1

Row 3:
──────
day:   2026-01-03
total: 18446744073709551615
```

However, a query equivalent to the materialized view `mv_test` produces a different result:

```sql
SELECT toStartOfDay(timestamp) AS day,
       sum(value * sign)       AS total
FROM test
GROUP BY day
ORDER BY day
FORMAT Vertical;

Row 1:
──────
day:   2026-01-01 00:00:00
total: 258

Row 2:
──────
day:   2026-01-02 00:00:00
total: 1

Row 3:
──────
day:   2026-01-03 00:00:00
total: -1
```

The value `18446744073709551615` is the maximum representable value of `UInt64`, i.e. `2^64 − 1`, which corresponds to `-1` when interpreted as an unsigned number. At the same time, the second query returns the correct result of `-1`, because by default the database engine interprets `total` as a signed value.

We once encountered a very similar issue in a real production system and it involved money. At some point, the total amount of refunds for a single day unexpectedly exceeded the revenue accumulated over several years :)

However, since this is only a matter of how the result is interpreted, and the underlying bytes are physically identical, the fix can be straightforward. If the materialized view is based on a separate table, it is sufficient to change the column type using an `ALTER TABLE` operation. Otherwise, the materialized view must be recreated and fully repopulated.

## What Conclusions Can We Draw?

1. Unsigned integers play an important role in programming, enabling efficient memory usage and self-documenting constraints.
2. Signed and unsigned integers are merely different interpretations of the same bit patterns.
3. Choosing between them requires careful consideration of language rules, implicit conversions, and edge cases.

## What Else Is Worth Reading?

1. [Wikipedia - Unsigned integer](https://en.wikipedia.org/wiki/Unsigned_integer)
2. [Wikipedia - Two's complement](https://en.wikipedia.org/wiki/Two%27s_complement)
3. Blog posts by [Julia Evans](https://jvns.ca)
  - [Unsigned Integers in C and C++](https://jvns.ca/blog/2017/03/21/unsigned-integers-in-c-and-cpp/)
  - [integer overflow/underflow](https://jvns.ca/blog/2023/01/18/examples-of-problems-with-integers/#example-2-integer-overflow-underflow)
  - [how do computers represent negative integers?](https://jvns.ca/blog/2023/01/18/examples-of-problems-with-integers/#aside-how-do-computers-represent-negative-integers)
  - [security problems because of integer overflow](https://jvns.ca/blog/2023/01/18/examples-of-problems-with-integers/#example-5-security-problems-because-of-integer-overflow)
  - [compilers removing integer overflow checks](https://jvns.ca/blog/2023/01/18/examples-of-problems-with-integers/#example-8-compilers-removing-integer-overflow-checks)
