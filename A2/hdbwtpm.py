import graphviz
import argparse

MIN_CHAR = '$'
MAX_CHAR = '~'


def countingSort(input: str, minChar='$', maxChar='~'):
    """ 
    input: bwt string
    output: sorted bwt string(sa), rank of each character in sa, count of each character in sa
    O(input)
    """
    minCharIndex = ord(minChar)
    maxCharIndex = ord(maxChar)
    alphabetSize = maxCharIndex-minCharIndex+1
    count = alphabetSize*[0]
    for char in input:
        count[ord(char)-minCharIndex] += 1
    rank = [0]*alphabetSize
    sum = 0
    for i in range(alphabetSize):
        sum += count[i]
        if count[i] != 0:
            rank[i] = sum

    sortedInput = len(input)*[None]
    for char in input:
        index = ord(char)-minCharIndex
        rank[index] -= 1
        sortedInput[rank[index]] = char

    return sortedInput, rank, count


def occurenceCountTable(input: str, minChar='$', maxChar='~'):
    """
    input: bwt string
    output: occurence count of each character in bwt at each index
    O(input)
    """
    alphabetSize = ord(maxChar)-ord(minChar)+1
    occurenceCount = alphabetSize*[0]
    occurenceCountTable = []
    for char in input:
        index = ord(char)-ord(minChar)
        occurenceCount[index] += 1
        occurenceCountTable.append(occurenceCount.copy())
    return occurenceCountTable


def returnFoundRange(char, OCCTable, rank, sp, ep, minChar='$', maxChar='~', verbose=False):
    """ 
    input: char the character searching for 
    input: OCCTable occurence count table
    input: rank rank of each character in sorted bwt
    input: current sp 
    input: current ep
    output: new range where the char is found 
    """
    charIndex = ord(char)-ord(minChar)
    if verbose:
        print(
            f'char: {char}, rank {rank[charIndex]}, occurance count {OCCTable[sp-1][charIndex]}')
    sp = rank[charIndex]+OCCTable[sp -
                                  1][charIndex] if sp != 0 else rank[charIndex]
    ep = rank[charIndex]+OCCTable[ep][charIndex]-1
    return sp, ep


def exactPatternMatching(bwt: str, pattern: str):
    # convert to sorted suffix array by reverse the index of bwt
    sortedBwt, rank, count = countingSort(bwt)
    occurenceCount = occurenceCountTable(bwt)

    # pattern matching
    sp = 0
    ep = len(bwt)-1
    patternIndex = len(pattern)-1
    while sp <= ep and patternIndex:
        char = pattern[patternIndex]
        sp, ep = returnFoundRange(
            char, occurenceCount, rank, sp, ep, verbose=True)
        patternIndex -= 1

    return ep-sp+1 if patternIndex == -1 else 0


def hammingDistancePatternMatching(bwt: str, pattern: str, d: int, minChar="$", maxChar='~', verbose=False):
    # pre processing bwt
    sortedBwt, rank, count = countingSort(
        bwt, minChar=minChar, maxChar=maxChar)
    occurenceCount = occurenceCountTable(bwt, minChar=minChar, maxChar=maxChar)
    unique_chars = set(bwt) - {'$'}  # Only consider characters present in BWT
    dMismatch = d
    dMismatchs = [0] * (d+1)

    def hdpmaux(sp, ep, patternIndex, d):
        if verbose:
            print(f'sp {sp}, ep {ep}, patternIndex {patternIndex}, d {d}')
        if sp > ep:
            if verbose:
                print(f'pattern not found')
            return 0

        if d < 0:
            if verbose:
                print(f'too many mismatch')
            return 0
        if patternIndex < 0:
            # iterate all the pattern, found a match
            if verbose:
                print(f'{ep-sp+1}pattern found with {dMismatch -d} mismatch  d {d}')

            dMismatchs[dMismatch - d] += ep-sp+1
            return ep-sp+1
        for char in unique_chars:  # Iterate only over characters present in BWT
            newsp, newep = returnFoundRange(
                char, occurenceCount, rank, sp, ep, minChar=minChar, maxChar=maxChar, verbose=verbose)
            if verbose:
                print(f'char {char}, sp {newsp}, ep {newep}')
            # continue the search with each unique char in the string,only reduce d if char is not the same as pattern
            hdpmaux(newsp, newep, patternIndex-1, d -
                    (pattern[patternIndex] != char))
        return dMismatchs
    return hdpmaux(0, len(bwt)-1, len(pattern)-1, d)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bwtFile', type=str, help='Path to the input file.')
    parser.add_argument('patternFile', type=str,
                        help='Path to the output file.')
    parser.add_argument(
        'maxD', type=int, help='Maximum number of hamming distance mismatches.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity.')
    args = parser.parse_args()
    bwtFile = args.bwtFile
    patternFile = args.patternFile
    maxD = args.maxD
    verbose = args.verbose
    outputFile = "output_hdbwtpm.txt"
    bwt, pattern = None, None
    with open(bwtFile, 'r') as f:
        bwt = f.readline().strip()
    with open(patternFile, 'r') as f:
        pattern = f.readline().strip()
    if verbose:
        print(f'bwt{bwt}, pattern{pattern}, maxD{maxD}')
    countArray = hammingDistancePatternMatching(
        bwt, pattern, maxD, verbose, minChar=MIN_CHAR, maxChar=MAX_CHAR)
    if verbose:
        print(f'count_array{countArray}')
    output = ["f"]

    with open(outputFile, 'w') as f:
        for d, count in enumerate(countArray):
            f.write(f'd = {d}, nMatches ={count}\n')
