import random
import argparse


def repeated_squaring(n, e, m, verbose=False):
    binary_rep = bin(e)[2:]
    if verbose:
        print(f'binary_rep: {binary_rep}')
    current = n % m
    result = 1
    rever_bin_rep = binary_rep[::-1]

    for i in range(1, len(rever_bin_rep)):
        current = (current * current) % m
        bit = rever_bin_rep[i]
        if verbose:
            print(f'bit{bit}: {current} * {result} = {current * result}')

        if bit == '1':
            result = (current * result) % m
    return result


def miller_rabin(n, k=64, verbose=False):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    if verbose:
        print(f'{n-1} = 2^{s} * {t}')
    for iter in range(k):
        if verbose:
            print(f'iteration {iter + 1}')
        a = random.randint(2, n - 2)
        if verbose:
            print(f'selected initial a = {a}')
        x = repeated_squaring(a, n-1, n)
        if verbose:
            print(f'{a}^{t} mod {n} = {x}')
        # fermat's little theorem
        if x != 1:
            return False

        prev_x = x
        for i in range(1, s):
            x = repeated_squaring(x, 2, n)
            if verbose:
                print(f'a^(2^{i}* t) mod n = {x}')
            if x == 1 and (prev_x != 1 and prev_x != n - 1):
                return False
            prev_x = x

    return True


def gen_prime(n, k=64):
    while True:
        p = random.getrandbits(n)
        if miller_rabin(p, k):
            return p


def karatsuba_multiplication(a, b, verbose=False):
    # base case single digit multiplication
    if a < 10 and b < 10:
        return a*b
    num_digits = max(len(str(a)), len(str(b)))
    m = num_digits//2

    u1 = a // 10**m
    u0 = a % 10**m
    v1 = b // 10**m
    v0 = b % 10**m

    if verbose:
        print(f'u1: {u1}, u0: {u0}, v1: {v1}, v0: {v0}')

    z0 = karatsuba_multiplication(u0, v0)
    z1 = karatsuba_multiplication(u0, v1)
    z2 = karatsuba_multiplication(u1, v0)
    z3 = karatsuba_multiplication(u1, v1)

    if verbose:
        print(f'z0: {z0}, z1: {z1}, z2: {z2}, z3: {z3}')
    return z3*10**(2*m) + (z1+z2)*10**m + z0


def n_bit_prime_multiplication(n):
    p = gen_prime(n)
    q = gen_prime(n)
    return (p, q), karatsuba_multiplication(p, q)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    args = parser.parse_args()
    n = args.n
    (p, q), result = n_bit_prime_multiplication(n)
    with open('output_ptimesq.txt', 'w') as f:
        f.write(f'#p (in base 10)\n{p}\n')
        f.write(f'#q (in base 10)\n{q}\n')
        f.write(f'p*q (in base 10)\n{result}')
