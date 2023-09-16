"""
Q2
Caleb Ooi
30521424
"""
# Need to pip install bitarray module
from bitarray import bitarray
import argparse
MIN_ALPHA = chr(33)
MAX_ALPHA = chr(126)


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


def bitarray_pre(pat, min_alpha="a", max_alpha="z"):
    """
    complexity: O(m*no_char)
    """
    no_char = ord(max_alpha) - ord(min_alpha) + 1
    bitarray_matrix = [bitarray(0) for _ in range(no_char)]
    # try to compare all the possible charcter in the alphabet with the pattern
    for character in range(no_char):
        matches = [chr(character + ord(min_alpha)) != char for char in pat]
        bitarray_matrix[character] = bitarray(matches)
    return bitarray_matrix


def bitwisepm(string, pat, min_alpha=MIN_ALPHA, max_alpha=MAX_ALPHA, verbose=False):
    """
    m is pattern, n is string
    Complexity: O(n+m)
    the intial bit vector is O(m)
    """
    if len(string) < len(pat) or len(pat) == 0:
        return []
    matched_index = []
    m = len(pat)
    bit_matrix = bitarray_pre(pat[::-1], min_alpha, max_alpha)
    # initial bitvector
    bit_vector = bitarray('0' * m)

    # calculate the bit vector0 by using pre process and shifting by 1 and or all of them
    for i in range(m-1, -1, -1):
        char_index = ord(string[i]) - ord(min_alpha)
        bit_vector |= bit_matrix[char_index] << (m-1-i)

    # if the most significant bit is 0, then it is a match
    if bit_vector[0] == 0:
        matched_index.append(0)
    if verbose:
        print(f'bit vector 0 {bit_vector}')

    # calculate the bit vector for the rest of the string using delta rule, don need to calculate if the suffix is shorter
    for i in range(1, len(string)-len(pat)+1):
        if verbose:
            print(f'string comparing {string[i:i+len(pat)]}')
        char_index = ord(string[i+m-1]) - ord(min_alpha)
        bit_vector = (bit_vector << 1) | (bit_matrix[char_index])
        if verbose:
            print(f'bit vector {i} {bit_vector}')
        if bit_vector[0] == 0:
            matched_index.append(i)
    return matched_index


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path1', type=str, help='Path to the first file.')
    parser.add_argument('path2', type=str, help='Path to the second file.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity.')
    args = parser.parse_args()
    filename1 = args.path1
    filename2 = args.path2

    s = read_file(filename1)
    p = read_file(filename2)
    print(p)
    matched_i = bitwisepm(s, p, MIN_ALPHA, MAX_ALPHA, verbose=args.verbose)
    matched_i_index1 = [i+1 for i in matched_i]
    output = "output_bitwisepm.txt"
    if args.verbose:
        print(f'output: {matched_i_index1}')
    write_file(output, matched_i_index1)
