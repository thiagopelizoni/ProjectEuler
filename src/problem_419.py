# Problem: https://projecteuler.net/problem=419
from itertools import groupby


def look_and_say(s):
    return ''.join(str(len(list(g))) + k for k, g in groupby(s))


def mat_mul(A, B, mod):
    r, m = len(A), len(B)
    c = len(B[0])
    res = [[0] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            for k in range(m):
                res[i][j] = (res[i][j] + A[i][k] * B[k][j]) % mod
    return res


def mat_pow(M, exp, mod):
    n = len(M)
    res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while exp > 0:
        if exp % 2 == 1:
            res = mat_mul(res, M, mod)
        M = mat_mul(M, M, mod)
        exp //= 2
    return res


def decompose(s, sorted_atoms):
    n = len(sorted_atoms)
    counts = [0] * n
    pos = 0
    while pos < len(s):
        found = False
        for atom in sorted_atoms:
            seq_len = len(atom['seq'])
            if pos + seq_len <= len(s) and s[pos:pos + seq_len] == atom['seq']:
                counts[atom['index']] += 1
                pos += seq_len
                found = True
                break
        if not found:
            return None
    return counts


def main():
    """
    Purpose
    -------
    Solves Project Euler problem 419 by computing the number of 1s, 2s, and 3s in the
    10^12-th term of the look and say sequence starting from 1, modulo 2^30.

    Method / Math Rationale
    -----------------------
    Uses John Conway's analysis of the look and say sequence, modeling it as
    independent atomic elements evolving via a transition matrix. Decomposes the
    sequence into atoms after a few iterations, then uses matrix exponentiation to
    advance the counts to the desired generation.

    Complexity
    ----------
    O(92^3 * log(10^12)) for matrix exponentiation, which is small.

    References
    ----------
    https://projecteuler.net/problem=419
    https://en.wikipedia.org/wiki/Look-and-say_sequence
    """
    mod = 1 << 30

    atoms_data = [
        (1, 'H', '22', ['H']),
        (2, 'He', '13112221133211322112211213322112', ['Hf', 'Pa', 'H', 'Ca', 'Li']),
        (3, 'Li', '312211322212221121123222112', ['He']),
        (4, 'Be', '111312211312113221133211322112211213322112', ['Ge', 'Ca', 'Li']),
        (5, 'B', '1321132122211322212221121123222112', ['Be']),
        (6, 'C', '3113112211322112211213322112', ['B']),
        (7, 'N', '111312212221121123222112', ['C']),
        (8, 'O', '132112211213322112', ['N']),
        (9, 'F', '31121123222112', ['O']),
        (10, 'Ne', '111213322112', ['F']),
        (11, 'Na', '123222112', ['Ne']),
        (12, 'Mg', '3113322112', ['Pm', 'Na']),
        (13, 'Al', '1113222112', ['Mg']),
        (14, 'Si', '1322112', ['Al']),
        (15, 'P', '311311222112', ['Ho', 'Si']),
        (16, 'S', '1113122112', ['P']),
        (17, 'Cl', '132112', ['S']),
        (18, 'Ar', '3112', ['Cl']),
        (19, 'K', '1112', ['Ar']),
        (20, 'Ca', '12', ['K']),
        (21, 'Sc', '3113112221133112', ['Ho', 'Pa', 'H', 'Ca', 'Co']),
        (22, 'Ti', '11131221131112', ['Sc']),
        (23, 'V', '13211312', ['Ti']),
        (24, 'Cr', '31132', ['V']),
        (25, 'Mn', '111311222112', ['Cr', 'Si']),
        (26, 'Fe', '13122112', ['Mn']),
        (27, 'Co', '32112', ['Fe']),
        (28, 'Ni', '11133112', ['Zn', 'Co']),
        (29, 'Cu', '131112', ['Ni']),
        (30, 'Zn', '312', ['Cu']),
        (31, 'Ga', '13221133122211332', ['Eu', 'Ca', 'Ac', 'H', 'Ca', 'Zn']),
        (32, 'Ge', '31131122211311122113222', ['Ho', 'Ga']),
        (33, 'As', '11131221131211322113322112', ['Ge', 'Na']),
        (34, 'Se', '13211321222113222112', ['As']),
        (35, 'Br', '3113112211322112', ['Se']),
        (36, 'Kr', '11131221222112', ['Br']),
        (37, 'Rb', '1321122112', ['Kr']),
        (38, 'Sr', '3112112', ['Rb']),
        (39, 'Y', '1112133', ['Sr', 'U']),
        (40, 'Zr', '12322211331222113112211', ['Y', 'H', 'Ca', 'Tc']),
        (41, 'Nb', '1113122113322113111221131221', ['Er', 'Zr']),
        (42, 'Mo', '13211322211312113211', ['Nb']),
        (43, 'Tc', '311322113212221', ['Mo']),
        (44, 'Ru', '132211331222113112211', ['Eu', 'Ca', 'Tc']),
        (45, 'Rh', '311311222113111221131221', ['Ho', 'Ru']),
        (46, 'Pd', '111312211312113211', ['Rh']),
        (47, 'Ag', '132113212221', ['Pd']),
        (48, 'Cd', '3113112211', ['Ag']),
        (49, 'In', '11131221', ['Cd']),
        (50, 'Sn', '13211', ['In']),
        (51, 'Sb', '3112221', ['Pm', 'Sn']),
        (52, 'Te', '1322113312211', ['Eu', 'Ca', 'Sb']),
        (53, 'I', '311311222113111221', ['Ho', 'Te']),
        (54, 'Xe', '11131221131211', ['I']),
        (55, 'Cs', '13211321', ['Xe']),
        (56, 'Ba', '311311', ['Cs']),
        (57, 'La', '11131', ['Ba']),
        (58, 'Ce', '1321133112', ['La', 'H', 'Ca', 'Co']),
        (59, 'Pr', '31131112', ['Ce']),
        (60, 'Nd', '111312', ['Pr']),
        (61, 'Pm', '132', ['Nd']),
        (62, 'Sm', '311332', ['Pm', 'Ca', 'Zn']),
        (63, 'Eu', '1113222', ['Sm']),
        (64, 'Gd', '13221133112', ['Eu', 'Ca', 'Co']),
        (65, 'Tb', '3113112221131112', ['Ho', 'Gd']),
        (66, 'Dy', '111312211312', ['Tb']),
        (67, 'Ho', '1321132', ['Dy']),
        (68, 'Er', '311311222', ['Ho', 'Pm']),
        (69, 'Tm', '11131221133112', ['Er', 'Ca', 'Co']),
        (70, 'Yb', '1321131112', ['Tm']),
        (71, 'Lu', '311312', ['Yb']),
        (72, 'Hf', '11132', ['Lu']),
        (73, 'Ta', '13112221133211322112211213322113', ['Hf', 'Pa', 'H', 'Ca', 'W']),
        (74, 'W', '312211322212221121123222113', ['Ta']),
        (75, 'Re', '111312211312113221133211322112211213322113', ['Ge', 'Ca', 'W']),
        (76, 'Os', '1321132122211322212221121123222113', ['Re']),
        (77, 'Ir', '3113112211322112211213322113', ['Os']),
        (78, 'Pt', '111312212221121123222113', ['Ir']),
        (79, 'Au', '132112211213322113', ['Pt']),
        (80, 'Hg', '31121123222113', ['Au']),
        (81, 'Tl', '111213322113', ['Hg']),
        (82, 'Pb', '123222113', ['Tl']),
        (83, 'Bi', '3113322113', ['Pm', 'Pb']),
        (84, 'Po', '1113222113', ['Bi']),
        (85, 'At', '1322113', ['Po']),
        (86, 'Rn', '311311222113', ['Ho', 'At']),
        (87, 'Fr', '1113122113', ['Rn']),
        (88, 'Ra', '132113', ['Fr']),
        (89, 'Ac', '3113', ['Ra']),
        (90, 'Th', '1113', ['Ac']),
        (91, 'Pa', '13', ['Th']),
        (92, 'U', '3', ['Pa'])
    ]

    atoms = [dict(index=id - 1, name=name, seq=seq, decays=decays) for id, name, seq, decays in atoms_data]
    name_to_index = {atom['name']: atom['index'] for atom in atoms}
    num_atoms = len(atoms)

    M = [[0 for _ in range(num_atoms)] for _ in range(num_atoms)]
    for atom in atoms:
        j = atom['index']
        for p_name in atom['decays']:
            i = name_to_index[p_name]
            M[i][j] += 1

    a = [atom['seq'].count('1') for atom in atoms]
    b = [atom['seq'].count('2') for atom in atoms]
    c = [atom['seq'].count('3') for atom in atoms]

    sorted_atoms = sorted(atoms, key=lambda x: len(x['seq']), reverse=True)

    s = '1'
    n = 1
    max_tries = 100
    v = None

    while n <= max_tries:
        temp_v = decompose(s, sorted_atoms)
        if temp_v is not None:
            v = temp_v
            break
        s = look_and_say(s)
        n += 1

    if v is None:
        raise ValueError("Did not decompose within max tries")

    target = 10**12
    remaining = target - n

    if remaining > 0:
        M_pow = mat_pow(M, remaining, mod)
        v = [sum(M_pow[i][j] * v[j] % mod for j in range(num_atoms)) % mod for i in range(num_atoms)]

    A = sum(v[i] * a[i] % mod for i in range(num_atoms)) % mod
    B = sum(v[i] * b[i] % mod for i in range(num_atoms)) % mod
    C = sum(v[i] * c[i] % mod for i in range(num_atoms)) % mod

    print(f"{A},{B},{C}")


if __name__ == "__main__":
    main()