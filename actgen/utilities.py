
def argsort(seq):
    # http://stackoverflow.com/questions/3071415/...
    # efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)

def signPermutation(p):
    n = len(p)

    ###
    # ADDED THIS FOR LOOP PRINTER MODULE.
    # THIS WAS NOT USED WHEN GENERATING THE UPDATES!
    if n == 0: return 1.0
    if 0 not in p:
        p = [x - min(p) for x in p]
    ###

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

def check_include_term(contr, nact_scheme, order):
    num_act_hole = 0
    num_act_particle = 0
    for idx, c in enumerate(contr):
        if c.isupper():
            if idx < order:
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
        if c.lower() in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            if c.upper() == c:
                label += 'V'
            elif c.lower() == c:
                label += 'v'
        if c.lower() in ['i', 'j', 'k', 'l', 'm', 'n', 'o']:
            if c.upper() == c:
                label += 'O'
            elif c.lower() == c:
                label += 'o'
    return label

def numbers_to_active_string(num_string, order):

    if order == 3:
        string = 'ABCIJK'
    elif order == 4:
        string = 'ABCDIJKL'

    new_string = ''
    for i, s in enumerate(string):
        if num_string[i] == '1':
            new_string += s.upper()
        if num_string[i] == '0':
            new_string += s.lower()
    return new_string
