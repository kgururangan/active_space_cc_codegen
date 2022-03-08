
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

def sign_to_str(sign):
    if sign == 1.0:
        return '+'
    else:
        return '-'

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

def unique_objects(L):
    L_unique = []
    for i, obj_i in enumerate(L):
        flag = True
        for j in range(i):
            if L[j] == obj_i:
                flag = False
        if flag:
            L_unique.append(obj_i)
    return L_unique

def check_include_term(contr, nact_scheme):
    num_act_hole = 0
    num_act_particle = 0
    for idx, c in enumerate(contr):
        if c.isupper():
            if idx < 3:
                num_act_particle += 1
            else:
                num_act_hole += 1
    include_term = False
    if num_act_hole >= nact_scheme and num_act_particle >= nact_scheme:
        include_term = True
    return include_term

def get_label_from_projection(projection):
    label = ''
    order = len(projection)
    for i, c in enumerate(projection):
        if i < order:
            if c.upper() == c:
                label += 'V'
            elif c.lower() == c:
                label += 'v'
        else:
            if c.upper() == c:
                label += 'H'
            elif c.lower() == c:
                label += 'h'
    return label
