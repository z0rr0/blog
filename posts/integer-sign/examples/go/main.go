package main

import "fmt"

func main() {
	var (
		signed   int8
		unsigned uint8
	)

	fmt.Println("+---------------------------------------------------------------+")
	fmt.Println("|              Compare signed and unsigned numbers              |")
	fmt.Println("+-----+----------+----------+-----+-----------+-----------+-----+")
	fmt.Println("| #   | unsigned |   bin    | hex |   signed  |    bin    | hex |")
	fmt.Println("|-----|----------|----------|-----|-----------|-----------|-----|")

	for i := 0; i < 260; i++ {
		signed = int8(i)
		unsigned = uint8(i)

		fmt.Printf("| %-3[1]d | %-8[2]d | %-8[2]b | %-3[2]x | %-9[3]b | %-9[3]b | %-3[3]x |\n", i, unsigned, signed)
	}

	fmt.Println("+-----+----------+----------+-----+-----------+-----------+-----+")
}
