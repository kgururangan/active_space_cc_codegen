
def argsort(seq):
    # http://stackoverflow.com/questions/3071415/...
    # efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)

def signPermutation(p):
    n = len(p)
    visited = [False] * n
    sign = 1.0
    for k in range(n):
        if not visited[k]:
            ct = k
            L = 0
            while not visited[ct]:
                L += 1
                visited[ct] = True
                ct = p[ct]
            if L % 2 == 0:
                sign *= -1.0
    return sign

def flip_sign(sign):
    if sign == '+':
        return '-'
    if sign == '-':
        return '+'

def string_replacer(s, newstring, index, nofail=False):
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")
    if index < 0:
        return newstring + s
    if index > len(s):
        return s + newstring
    return s[:index] + newstring + s[index+1:]

def change_term_to_projection(string, reference_string):

    string_out = string

    for s0 in reference_string:

        for i, s in enumerate(string):
            if s.lower() == s0 or s.upper() == s0:
                string_out = string_out[:i] + s0 + string_out[i+1:]

    return string_out