"""
Q1
Caleb Ooi
30521424
"""
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


def manualsearch(str, k):
    """
    k is the starting index

    """
    i = k
    while i < len(str) and str[i] == str[i-k]:
        i += 1
    return i-k


def z_algorithm(string, verbose=False):
    """
    complexity O(n)
    """
    n = len(string)
    l = 0
    r = 0
    z_values = [0]*n
    # store the length as the first value
    z_values[0] = n
    for k in range(1, n):
        # case 1
        if k > r:

            z = manualsearch(string, k)
            if z > 0:
                l = k
                r = k+z-1
        elif r >= k:
            # z box value on the prefix
            mirror = k-l
            z_mirror = z_values[mirror]

            current_zbox_max = r - k + 1
            if verbose:
                print(
                    f'current k={k}, mirror index={mirror}, mirror z box:{z_mirror}, current z box max: {current_zbox_max}')
            # z box value on the prefix is smaller than the current z box max, can just copy the value
            if z_mirror < current_zbox_max:
                z = z_mirror
            # z box value is the same as z box max(r), havent search after r need to manual search from r and add to z box
            elif z_mirror == current_zbox_max:
                additional_match = manualsearch(string, r)
                if verbose:
                    print(f'additional match:{additional_match}')
                if additional_match > 0:
                    z = z_mirror + additional_match-1
                else:
                    z = z_mirror
                l = k
                r = k+z - 1
            # z box value greater, stop at r
            elif z_mirror > current_zbox_max:
                z = r - k+1
        if verbose:
            print(f' current k={k} left value:{l}, right most:{r}')
        z_values[k] = z

    return z_values


def bad_char_pre(p, min_alpha="a", max_alpha="z", verbose=False):
    """
    Complexity O(M * n_char)
    bad_char_matrix[i] = latest occurence of char i in p[0,i)
    stores the index of the right most occurence of a character in the pattern that is less than i
    """
    n_char = ord(max_alpha) - ord(min_alpha) + 1
    bad_char_matrix = [[None] for _ in range(len(p))]
    # keep the latest to be reuse for new iteration
    latest_bad_char = [-1] * n_char
    bad_char_matrix[0] = latest_bad_char
    for i in range(1, len(p)):
        index = ord(p[i]) - ord(min_alpha)
        latest_bad_char[index] = i
        if verbose:
            print(latest_bad_char)
        bad_char_matrix[i] = latest_bad_char.copy()
    return bad_char_matrix


def good_suffix_table_pre(p, min_alpha="a", max_alpha="z", verbose=False):
    """
    find the right most of prefix with different preceding value
    start from the end of the pattern
    stores the end index of a string in that matches the suffix up to that point
    O(m)
    """
    # reversed to clculate right to left
    reversed_p = p[::-1]
    n_char = ord(max_alpha) - ord(min_alpha) + 1
    z_values_reversed = z_algorithm(reversed_p)
    if verbose:
        print(f'z suffix values{z_values_reversed} for {reversed_p}')

    z_values = z_values_reversed[::-1]
    if verbose:
        print(z_values)
    # add extra column at the end to include the last index
    good_suffix = [[-1] * n_char for _ in range(len(p)+1)]
    for i in range(len(p)-1):

        good_suf_val = len(p) - z_values[i]
        suffix_start_index = i - z_values[i] + 1
        if suffix_start_index > 0:
            # dont put any value if at its prefix, can use match prefix value to pre
            prev_char = ord(p[suffix_start_index-1]) - ord(min_alpha)
            good_suffix[good_suf_val][prev_char] = i
        if verbose:
            print(
                f'z value: {z_values[i]} at {i}, good suffix index is {good_suf_val}')

        if verbose:
            print(f'good suffix array{good_suffix[good_suf_val]}')

    return good_suffix


def matched_prefix_pre(p, min_alpha="a", max_alpha="z", verbose=False):
    """
    use z algorithm  z suffix go left to right , mp value fill right to left
    stores the length of the longest prefix that matches the suffix up to that point
    O(m)
    """
    mp = [0] * (len(p)+1)
    reversed_p = p[::-1]
    z_values_reversed = z_algorithm(reversed_p)[::-1]
    max_pre = 0
    for i in range(len(p)-1, -1, -1):
        start_index = len(p)-1 - i
        if verbose:
            print(
                f'start index {start_index} z value {z_values_reversed[start_index]}')
        max_pre = max(z_values_reversed[start_index], max_pre)
        mp[i] = max_pre
    return mp


def boyer_moore(string, pat, min_alpha=MIN_ALPHA, max_alpha=MAX_ALPHA, verbose=False):
    """
    Uses bad char matrix, good suffix matrix for strict good suffix and matched prefix for shift
    1. do all the pre processing O(m*no_char)
    2. scan right to left, if theres mismatched retrive the bad char index, good suffix index, if theres no gs using mp
        if thers match see if its in the skip region that is already covered when using gs or mp
    3. calculate the shift from current index to bad char index and gs index
    4. use the shift that is the largest
    5. if theres a match, shift by the longest prefix that not the pattern, if thats not found shift by 1

    Complexity O(n+m)

    """
    # pre processing
    if len(string) < len(pat) or len(pat) == 0:
        return []
    bad_char_table = bad_char_pre(pat, min_alpha, max_alpha)
    good_suffix_table = good_suffix_table_pre(pat, min_alpha, max_alpha)
    matched_prefix_table = matched_prefix_pre(pat, min_alpha, max_alpha)

    m = len(pat)
    s_i = m-1
    p_i = m-1

    skip_region_start = -1
    skip_region_end = -1
    # result
    matched_index = []

    if verbose:
        print(f"comparing {string[s_i-m+1:s_i+1]}")
    while s_i < len(string):
        if verbose:
            print(f'string index{s_i}')
        # check if the current char match, if matched then decrease the index and check if the index is in the skip region
        if string[s_i] == pat[p_i]:
            s_i -= 1
            p_i -= 1
            # check if checking the skip region of the pattern
            if p_i > 0 and p_i == skip_region_start:
                p_i = skip_region_end - 1
                s_i = s_i - (skip_region_start - skip_region_end)-1
                if verbose:
                    print(
                        f"skipped index {skip_region_start} to {skip_region_end}, old string index{s_i+skip_region_start+skip_region_end+1}, new string index{s_i}, new pattern index {p_i}")
                # reset skip_region
                skip_region_start = -1
                skip_region_end = -1

        else:
            mismatched_char = ord(string[s_i]) - ord(min_alpha)
            if verbose:
                print(f"mismatched index{s_i}, mismatched char {string[s_i]}")
            # bad char
            bad_char_val = bad_char_table[p_i][mismatched_char]
            # if not bad char found can shift the remaining pattern length otherwise calculate the shift from current index to the bad char index
            bad_char_shift = (m-p_i) if bad_char_val == - \
                1 else p_i - bad_char_val

            # check good suffix
            if (p_i == m-1):
                good_suffix_val = -1
                good_suffix_shift = 1
            else:

                good_suffix_val = good_suffix_table[p_i +
                                                    1][ord(string[s_i]) - ord(min_alpha)]
                # if no good suffix shift by 1
                good_suffix_shift = p_i - good_suffix_val-1 if good_suffix_val != -1 else 1
                skip_region_start = good_suffix_val
                gs_length = m-1 - p_i
                skip_region_end = good_suffix_val - gs_length

            # check matched prefix
            matched_prefix_val = matched_prefix_table[p_i+1]
            if good_suffix_val == -1:
                skip_region_start = matched_prefix_val - 1
                skip_region_end = 0
            # only use match prefix when theres no good suffix
            matched_prefix_shift = (
                m - matched_prefix_val) if matched_prefix_val != 0 and good_suffix_val == -1 else 1

            if verbose:
                print(
                    f"bad char val {bad_char_val}, good suffix val {good_suffix_val}, matched prefix val {matched_prefix_val}")
            if verbose:
                print(
                    f"bad char shift {bad_char_shift}, good suffix shift {good_suffix_shift}, matched prefix shift {matched_prefix_shift}")
            if verbose:
                print(f"skip region {skip_region_start} to {skip_region_end}")
            # reset
            s_i_top = s_i + (m-1-p_i)
            s_i = s_i_top + \
                max(bad_char_shift, good_suffix_shift, matched_prefix_shift)

            p_i = m-1
            if verbose:
                print(
                    f"new string postion {s_i}, comparing {string[s_i-m+1:s_i+1]}")

        # went through the whole pattern
        if p_i == -1:
            if verbose:
                print(f"found match at {s_i+1}")
            matched_index.append(s_i+1)
            next_matched = matched_prefix_table[1]
            # use the longest prefix thats not the whole pattern if not use 1
            next_shift = (
                m - next_matched) if next_matched != 0 else 1

            # reset the string index to end of current
            s_i = s_i + m
            s_i += next_shift
            # reset the pattern index to end
            p_i = m-1
            if verbose:
                print(
                    f"new string postion {s_i}, comparing {string[s_i-m+1:s_i+1]}")
    return matched_index, bad_char_table, good_suffix_table, matched_prefix_table


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
    matched_i, bad_char, good_suffix_tab, match_pre_tab = boyer_moore(
        s, p, verbose=args.verbose)
    matched_i_index_1 = [i+1 for i in matched_i]
    output = "output_stricterBM.txt"

    if args.verbose:
        print(f'output: {matched_i_index_1}')

    write_file(output, matched_i_index_1)
