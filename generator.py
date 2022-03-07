from diagramperms import generate_active_permutations
from weights import get_permutation_weight
from parser import parse_expression
from contraction import binary_active_contraction
from indices import check_include_term, convert_char_to_ov, get_slicestr_t3


def write_HBarT3_contractions(expr_list, out_proj, out_proj_spin, nact_scheme=1, print_term=False):

    num_expr = len(expr_list)
    D = [None] * num_expr

    if out_proj_spin == 'A':
        weight0 = 36.0
        residual_term = 'dT.aaa.'
    if out_proj_spin == 'B':
        weight0 = 4.0
        residual_term = 'dT.aab.'
    if out_proj_spin == 'C':
        weight0 = 4.0
        residual_term = 'dT.abb.'
    if out_proj_spin == 'D':
        weight0 = 36.0
        residual_term = 'dT.bbb.'

    for inm, op in enumerate(out_proj):
        if op.upper() == op:
            if inm < 3:
                residual_term += 'V'
            else:
                residual_term += 'O'
        if op.upper() != op:
            if inm < 3:
                residual_term += 'v'
            else:
                residual_term += 'o'

    nterms = 0
    for i, expr in enumerate(expr_list):

        expr_perm_list = generate_active_permutations(expr, out_proj_spin)

        for expr1 in expr_perm_list:

            contr_chars, spin_contr, obj1, obj2, sign_orig = parse_expression(expr1)

            D = binary_active_contraction(contr_chars, spin_contr, obj1, obj2, sign_orig)

            # filter out those terms that have fewer than nact_scheme active indices in either particle or hole
            D2 = []
            for idx, d in enumerate(D):

                s = d.split(',')
                s2 = s[2].split('(')
                term2 = s2[0]
                contr2 = s2[1][:-1]

                include_term = check_include_term(contr2, nact_scheme)
                if include_term:
                    D2.append(d)

            term_print_list = []
            for idx, d in enumerate(D2):

                s = d.split(',')

                sign = s[0][0]
                weight = s[0][1:]
                if weight == '': weight = '1.0'

                s1 = s[1].split('(')
                term1 = s1[0]
                contr1 = s1[1][:-1]

                if term1 == 'h1A' or term1 == 'h1a':
                    term1 = 'H.a'
                    double_spin_string = 'aa'
                if term1 == 'h1B' or term1 == 'h1b':
                    term1 = 'H.b'
                    double_spin_string = 'bb'
                if term1 == 'h2A' or term1 == 'h2a':
                    term1 = 'H.aa'
                    double_spin_string = 'aaaa'
                if term1 == 'h2B' or term1 == 'h2b':
                    term1 = 'H.ab'
                    double_spin_string = 'abab'
                if term1 == 'h2C' or term1 == 'h2c':
                    term1 = 'H.bb'
                    double_spin_string = 'bbbb'

                slicestr = ''
                actslicestr = ''
                for ind, c in enumerate(contr1):
                    o_or_v = convert_char_to_ov(c)
                    slicestr += o_or_v
                    if c.upper() == c:
                        if o_or_v == 'o':
                            c1 = 'O'
                        if o_or_v == 'v':
                            c1 = 'V'
                    if c.upper() != c:
                        if o_or_v == 'o':
                            c1 = 'o'
                        if o_or_v == 'v':
                            c1 = 'v'

                    actslicestr += c1 + double_spin_string[ind] + ','

                s2 = s[2].split('(')
                term2 = s2[0]
                contr2 = s2[1][:-1]

                if term2 == 'T3A' or term2 == 't3A' or term2 == 't3a':
                    term2 = 'T.aaa'
                if term2 == 'T3B' or term2 == 't3B' or term2 == 't3b':
                    term2 = 'T.aab'
                if term2 == 'T3C' or term2 == 't3C' or term2 == 't3c':
                    term2 = 'T.abb'
                if term2 == 'T3D' or term2 == 't3D' or term2 == 't3d':
                    term2 = 'T.bbb'

                slicestr_t3 = get_slicestr_t3(contr2)

                term_print_list.append(
                    {'sign': sign,
                     'weight': weight,
                     'contr1': contr1,
                     'contr2': contr2,
                     'out_proj': out_proj,
                     'term1': term1,
                     'slicestr': slicestr,
                     'actslicestr': actslicestr[:-1],
                     'term2': term2,
                     'slicestr_t3': slicestr_t3}
                )

            # find the permutation weight using last contr1 and contr2
            perm_weight = get_permutation_weight(contr1, contr2, out_proj_spin)

            # print the term
            print(residual_term + ' += (' + str(perm_weight) + '/' + str(weight0) + ') * (')

            for t in term_print_list:
                print('        ' + t['sign'] + t['weight'] + '*' + 'np.einsum(' + "'" + t['contr1'] + ',' + t[
                    'contr2'] + '->' + t['out_proj'] + "'" + ', ' \
                      + t['term1'] + "." + t['slicestr'] + "[" + t['actslicestr'] + "]" + ', ' + t['term2'] + "." + t[
                          'slicestr_t3'] + ', ' + 'optimize=True)')

            print(')')

            nterms += 1

    return D2, nterms