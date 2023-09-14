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

	fmt.Println("+---------------------------------------------------------------------------------+")
	fmt.Println("|                    Compare signed and unsigned numbers                          |")
	fmt.Println("+-----+----------+----------+-----+--------+-----------+-----+--------------------+")
	fmt.Println("| #   | unsigned |   bin    | hex | signed |    bin    | hex | signed as unsigned |")
	fmt.Println("|-----|----------|----------|-----|--------|-----------|-----|--------------------|")

	for i := 0; i < 260; i++ {
		signed = int8(i)
		unsigned = uint8(i)
		signedAsUnsigned := s2u(signed)

		fmt.Printf("| %-3[1]d | %-8[2]d | %-8[2]b | %-3[2]x | %-6[3]d | %-9[3]b | %-3[3]x | %-18[4]b |\n", i, unsigned, signed, signedAsUnsigned)
	}

	fmt.Println("+-----+----------+----------+-----+--------+-----------+-----+--------------------+")
}
