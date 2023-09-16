def manualsearch(str, k):
    i = k
    while i < len(str) and str[i] == str[i-k]:
        i += 1
    return i-k


def z_algorithm(string, verbose=False):
    n = len(string)
    l = 0
    r = 0
    z_values = [0]*n
    z_values[0] = n
    for k in range(1, n):
        # case 1
        if k > r:
            z = manualsearch(string, k)
            if z > 0:
                l = k
                r = k+z-1
        elif r >= k:
            mirror = k-l
            z_mirror = z_values[mirror]

            current_zbox_max = r - k + 1
            if verbose:
                print(
                    f'current k={k}, mirror index={mirror}, mirror z box:{z_mirror}, current z box max: {current_zbox_max}')

            if z_mirror < current_zbox_max:
                z = z_mirror
            elif z_mirror == current_zbox_max:
                additional_match = manualsearch(string, r)
                if verbose:
                    print(f'additional match:{additional_match}')
                if additional_match > 0:
                    z = z_mirror + additional_match-1
                z = z_mirror
                l = k
                r = k+z - 1
            elif z_mirror > current_zbox_max:
                z = r - k+1
        if verbose:
            print(f' current k={k} left value:{l}, right most:{r}')
        z_values[k] = z

    return z_values



def bad_char_pre(p, verbose=False):
    """
    Complexity O(M * n_char)
    bad_char_matrix[i] = latest occurence of char i in p[0,i)
    """
    n_char = 26
    bad_char_matrix = [[None] for _ in range(len(p))]
    latest_bad_char = [-1] * n_char
    for i in range(1, len(p)):
        index = ord(p[i]) - ord('a')
        latest_bad_char[index] = i
        if verbose:
            print(latest_bad_char)
        bad_char_matrix[i] = latest_bad_char.copy()
    return bad_char_matrix


def good_suffix_pre(p, verbose=False):
    """
    find the right most of prefix with different preceding value
    start from the end of the pattern
    """
    reversed_p = p[::-1]

    z_values_reversed = z_algorithm(reversed_p)
    if verbose:
        print(f'z suffix values{z_values_reversed} for {reversed_p}')
    z_values = z_values_reversed[::-1]
    if verbose:
        print(z_values)
    good_suffix = [-1] * (len(p)+1)
    for i in range(len(p)-1):
        good_suf_val = len(p) - z_values[i]
        if verbose:
            print(
                f'z value: {z_values[i]}, good suffix index is {good_suf_val}')
        good_suffix[good_suf_val] = i
        if verbose:
            print(f'good suffix array{good_suffix}')
    return good_suffix


def matched_prefix_pre(p, verbose=False):
    """
    use z algorithm  z suffix go left to right , mp value fill right to left

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


def boyer_moore(str, pat, verbose=False):
    """
    preprocessing time complexity: O(pattern)
    Complexity: O(n + m)
    bad_char = matrix of [length(str)][char]
    good_suffix = [length(str)+1]
    matched_prefix = [length(str)+1]
    """
    bad_char = bad_char_pre(pat)
    if verbose:
        print(bad_char, len(bad_char))
    good_suffix = good_suffix_pre(pat)
    if verbose:
        print(f'good suffix array{good_suffix}', len(good_suffix))
    matched_prefix = matched_prefix_pre(pat)
    if verbose:
        print(f'matched prefix array {matched_prefix}', len(matched_prefix))
    m = len(pat)
    s_i = len(pat)-1
    p_i = len(pat)-1
    skip_region_start = 0
    skip_region_end = 0
    matched_index = []
    while s_i < len(str):
        bad_char_shift = 1
        good_suffix_shift = 1
        if verbose:
            print(f'current string index: {s_i}, current pattern index: {p_i}')
        if str[s_i] == pat[p_i]:
            # check skip region
            # to do only skip if its not bad char
            s_i -= 1
            p_i -= 1
            if p_i == skip_region_start:
                p_i = skip_region_end-1
                s_i -= (skip_region_start - skip_region_end+1)
                skip_region_start = 0
                skip_region_end = 0
        else:
            skip_region_start = 0
            skip_region_end = 0
            # missmatch
            if verbose:
                print(f'mismatched char: {str[s_i], pat[p_i]} at index {s_i}')

            mismatched_char = ord(str[s_i]) - ord('a')
            bad_char_index = bad_char[p_i][mismatched_char]
            if bad_char_index == -1:
                bad_char_shift = m-p_i
            else:
                bad_char_shift = p_i - bad_char_index

            if verbose:
                print(f'bad char shift: {bad_char_shift}')

            # good suffix. select the index where it matches
            good_suffix_index = good_suffix[p_i+1]
            # no good suffix
            if (good_suffix_index > 0 and p_i < m-1):
                good_suffix_shift = m-1 - good_suffix_index
                skip_region_start = good_suffix_index
                skip_region_end = good_suffix_index - (m - 2 - p_i)
                if verbose:
                    print(
                        f'pattern index: {p_i}good suffix shift: {good_suffix_shift}, good suffix length: {m-1 -p_i} skip region: {skip_region_start} to {skip_region_end}')

            elif (p_i < m-1):
                good_suffix_shift = m-1 - matched_prefix[p_i+1]+1
                skip_region_start = matched_prefix[p_i]
                skip_region_end = 0
                if verbose:
                    print(
                        f'pattern index: {p_i} matched prefix: {matched_prefix[p_i]}, skip region {skip_region_start} to {skip_region_end}')
            if verbose:
                print(
                    f'bad char shift: {bad_char_shift} good suffix shift: {good_suffix_shift}')

            distance_to_shift = max(bad_char_shift, good_suffix_shift)

            # move s_i
            s_i += (m-1-p_i) + distance_to_shift
            # reset p_i to the end of string
            p_i = m-1

            if verbose:
                print(
                    f'shift by {distance_to_shift}, new index: {s_i} compare with {str[s_i-m+1:s_i+1]}')

        if p_i == -1:
            # fully matched
            matched_index.append(s_i+1)
            prev_matched_end = s_i + m
            p_i = len(pat)-1
            s_i += matched_prefix[1] + m
            if s_i == prev_matched_end:
                s_i += m-1
    return matched_index
