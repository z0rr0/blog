def main() -> None:
    number = b"\xff"

    unsigned = int.from_bytes(number, byteorder="big", signed=False)
    signed = int.from_bytes(number, byteorder="big", signed=True)

    print(f"size of number {number=} in bytes:", len(number))  # 1
    print(f"{unsigned=}")  # 255
    print(f"{signed=}")  # -1


if __name__ == "__main__":
    main()
