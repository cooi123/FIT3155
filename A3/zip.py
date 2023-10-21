from bitarray import bitarray
import heapq


def int_to_bitarray(n, length=0):
    return bitarray(bin(n)[2:].zfill(length))


def elias_omega_encoding(n: int, verbose=False) -> bitarray:
    def length_encoding(n, bitvalues=bitarray('')):
        if n == 1:
            return bitvalues
        else:

            bit_repr = int_to_bitarray(n-1)
            bit_repr[0] = 0
            if verbose:
                print(f"n={n}, bit_repr={bit_repr}")
            return length_encoding(len(bit_repr), bit_repr+bitvalues)
    bit_repr = int_to_bitarray(n)
    if verbose:
        print(f'val ={n}, bit_repr={bit_repr}')
    return length_encoding(len(bit_repr), bit_repr)


class Tree():
    def __init__(self, val, occurance, left, right):
        self.val = val
        self.occurance = occurance
        self.left = left
        self.right = right


def generate_tree(n, verbose=False):
    unique_char_occurance = {char: n.count(char) for char in n}
    queue = [(val, key, Tree(key, val, None, None))
             for key, val in unique_char_occurance.items()]
    heapq.heapify(queue)
    if verbose:
        print(f"occurance={queue}")

    while len(queue) > 1:
        left_chars, left_occurance, left_tree = heapq.heappop(queue)
        right_chars, right_occurance, right_tree = heapq.heappop(queue)

        heapq.heappush(queue, (left_chars+right_chars, left_occurance+right_occurance, Tree(
            left_chars+right_chars, left_occurance+right_occurance, left_tree, right_tree)))
    return queue[0][2]


def travese_tree(root, verbose=False):
    all_codes = {}

    def travese_tree_aux(root, code, verbose=False):
        if verbose:
            print(f"root={root}, code={code}")
        if root.left is None and root.right is None:
            all_codes[root.val] = bitarray(code)
        else:
            travese_tree_aux(root.left, code+'0')
            travese_tree_aux(root.right, code+'1')
    travese_tree_aux(root, '')
    return all_codes


def huffman_encoding(n, codes=None, verbose=False):
    if codes is None:
        tree = generate_tree(n, verbose)
        codes = travese_tree(tree, verbose)
    if verbose:
        print(f"codes={codes}")
    res = bitarray('')
    for char in n:
        res += codes[char]
    return res


def get_huffmann_code(n, verbose=False):
    tree = generate_tree(n, verbose)
    codes = travese_tree(tree, verbose)
    return codes


def ascii_8bit_encoding(n):
    res = bitarray('')
    for char in n:
        res += int_to_bitarray(ord(char), 8)
        print(int_to_bitarray(ord(char), 8))
    return res


def LZ77(data, W, L, codes=None, verbose=False):
    if codes is None:
        codes = get_huffmann_code(data, verbose)
    current_index = 0
    search_index = 0
    max_look_ahead_index = L
    res = []
    while current_index < len(data):
        search_index = max(0, current_index-W)
        temp_index = current_index

        max_look_ahead_index = min(current_index+L, len(data))
        search_window_start = search_index
        is_max = False
        max_len = 0

        if verbose:
            print(
                f"current index= {current_index} window={data[search_index:current_index]}, look_ahead={data[current_index:max_look_ahead_index]}")

        while search_index < current_index and current_index < max_look_ahead_index:
            # search for the longest match

            if data[current_index] == data[search_index]:
                search_index += 1
                current_index += 1
                if current_index - temp_index > max_len:
                    max_len = current_index - temp_index
                    if not is_max:

                        search_window_start = search_index-max_len
                        if verbose:
                            print(f'search index ={search_window_start}')
                        is_max = True
            else:
                # reset the current_index
                current_index = temp_index
                search_index += 1
                is_max = False

        if verbose:
            print(
                f"offset={(temp_index-search_window_start)}, len={max_len}, next={data[temp_index+ max_len]}")

        res.append(((temp_index-search_window_start),
                   max_len, data[temp_index + max_len]))
        current_index = temp_index + max_len+1

        encoding = bitarray('')
    for offset, length, next_char in res:

        encoding += elias_omega_encoding(offset+1)
        encoding += elias_omega_encoding(length+1)
        encoding += codes[next_char]
        print(
            f'<{offset},{length},{next_char}> encoded as {elias_omega_encoding(offset+1)+elias_omega_encoding(length+1)+codes[next_char]}')
    return encoding


def file_encoding(file_name, W, L, verbose=False):
    file_name_length = len(file_name)
    file_name_length_encoding = elias_omega_encoding(file_name_length+1)
    file_name_encoding = ascii_8bit_encoding(file_name)
    if verbose:
        print(
            f"file_name_length={file_name_length}, file_name_length_encoding={file_name_length_encoding}, file_name_encoding={file_name_encoding}")
    with open(file_name, 'r') as f:
        content = f.read()
    length_content = len(content)
    length_content_encoding = elias_omega_encoding(length_content+1)
    if verbose:
        print(
            f"length_content={length_content}, length_content_encoding={length_content_encoding}")
    huffman_code = get_huffmann_code(content)
    length_huffman_code = len(huffman_code)
    length_huffman_code_encoding = elias_omega_encoding(length_huffman_code+1)

    huffman_code_encoding = bitarray('')
    for char in sorted(huffman_code):
        occurance = huffman_code[char]
        huffman_code_encoding += ascii_8bit_encoding(char)
        huffman_code_encoding += elias_omega_encoding(len(occurance)+1)
        huffman_code_encoding += occurance
    if verbose:
        print(
            f"huffman_code={huffman_code}, huffman_code_encoding={huffman_code_encoding}")

    header_encoding = file_name_length_encoding + file_name_encoding + \
        length_content_encoding + length_huffman_code_encoding + huffman_code_encoding
    content_encoding = LZ77(content, W, L, huffman_code)
    file_encoding = header_encoding+content_encoding
    with open(file_name+".bin", 'wb') as f:
        for i in range(0, len(file_encoding), 8):
            print(file_encoding[i:i+8])
            f.write(bytes(file_encoding[i:i+8]))


if __name__ == "__main__":
    