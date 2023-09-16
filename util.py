def read_file(file_path: str) -> str:
    f = open(file_path, "r")
    line = f.readlines()
    f.close()
    return line[0]


def write_file(file_path: str, content: [int]):
    f = open(file_path, "w")
    for val in content:
        f.write(str(val) + "\n")
    f.close()


if __name__ == "__main__":
    string = read_file("string.txt")
    pattern = read_file("pattern.txt")
    print(string, pattern)
    write_file("output.txt", [1, 2, 3, 4])
