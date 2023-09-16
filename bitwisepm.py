# Need to pip install bitarray module
from bitarray import bitarray
from bitarray.util import ba2int
from util import read_file, write_file
import argparse
MIN_ALPHA = chr(33)
MAX_ALPHA = chr(126)


def bitarray_pre(pat, min_alpha="a", max_alpha="z"):
    """
    complexity: O(m*no_char)
    """
    no_char = ord(max_alpha) - ord(min_alpha) + 1
    bitarray_matrix = [bitarray(0) for _ in range(no_char)]
    for character in range(no_char):
        matches = [chr(character + ord(min_alpha)) != char for char in pat]
        bitarray_matrix[character] = bitarray(matches)
    return bitarray_matrix


def bitwisepm(string, pat, min_alpha="a", max_alpha="z", verbose=False):
    """
    Complexity: O(n+m)

    """
    if len(string) < len(pat):
        return []
    matched_index = []
    alpha_range = ord(max_alpha) - ord(min_alpha) + 1
    m = len(pat)
    bit_matrix = bitarray_pre(pat[::-1], min_alpha, max_alpha)
    if verbose:
        print(f'bit matrix {bit_matrix}')
    bit_vector = bitarray('0' * m)

    # calculate the bit vector0 by using pre process and shifting by 1 and or all of them
    for i in range(m-1, -1, -1):
        char_index = ord(string[i]) - ord(min_alpha)
        bit_vector |= bit_matrix[char_index] << (m-1-i)

    if bit_vector[0] == 0:
        matched_index.append(0)
    if verbose:
        print(f'bit vector 0 {bit_vector}')

    for i in range(1, len(string)-len(pat)+1):
        if verbose:
            print(f'string comparing {string[i:i+len(pat)]}')
        char_index = ord(string[i+m-1]) - ord(min_alpha)
        bit_vector = (bit_vector << 1) | (bit_matrix[char_index])
        if verbose:
            print(f'bit vector {i} {bit_vector}')
        if bit_vector[0] == 0:
            matched_index.append(i)
    return matched_index, bit_matrix


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
