from utilities import string_replacer, flip_sign

def generate_active_permutations(expr, out_proj_spin):
    from itertools import combinations

    expr_list = []

    sign0 = expr[0]
    s = expr.split(',')
    s1 = s[0].split('(')
    contr01 = s1[1][0:-1]
    s2 = s[1].split('(')
    contr02 = s2[1][0:-1]

    def _apply_swap(perm, contr1, contr2, sign):
        import re

        if perm == [1]:
            return contr1, contr2, sign

        p1 = perm[0]
        p2 = perm[1]

        result1 = [_.start() for _ in re.finditer(p1, contr1)]
        result2 = [_.start() for _ in re.finditer(p2, contr2)]
        for idx in result1:
            contr1 = string_replacer(contr1, p2, idx)
        for idx in result2:
            contr2 = string_replacer(contr2, p1, idx)

        return contr1, contr2, flip_sign(sign)

    def _get_products(list1, list2):

        if len(list1) > 0 and len(list2) > 0:
            return [[1], [list1[0], list2[0]]]
        else:
            return [[1]]

    dict_1 = get_swapping_dict(contr01, out_proj_spin)
    dict_2 = get_swapping_dict(contr02, out_proj_spin)

    for perm1 in _get_products(dict_1['act_hole_alpha'], dict_2['core_alpha']):
        for perm2 in _get_products(dict_1['core_alpha'], dict_2['act_hole_alpha']):
            for perm3 in _get_products(dict_1['act_particle_alpha'], dict_2['virt_alpha']):
                for perm4 in _get_products(dict_1['virt_alpha'], dict_2['act_particle_alpha']):
                    for perm5 in _get_products(dict_1['act_hole_beta'], dict_2['core_beta']):
                        for perm6 in _get_products(dict_1['core_beta'], dict_2['act_hole_beta']):
                            for perm7 in _get_products(dict_1['act_particle_beta'], dict_2['virt_beta']):
                                for perm8 in _get_products(dict_1['virt_beta'], dict_2['act_particle_beta']):
                                    contr1 = contr01
                                    contr2 = contr02
                                    sign = sign0

                                    # print('\n')
                                    # print('Original:',contr1, contr2, sign)
                                    # print(perm1, perm2, perm3, perm4, perm5, perm6, perm7, perm8)
                                    # print('-----------------------------------------')

                                    contr1, contr2, sign = _apply_swap(perm1, contr1, contr2, sign)
                                    # print(perm1, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm2, contr1, contr2, sign)
                                    # print(perm2, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm3, contr1, contr2, sign)
                                    # print(perm3, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm4, contr1, contr2, sign)
                                    # print(perm4, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm5, contr1, contr2, sign)
                                    # print(perm5, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm6, contr1, contr2, sign)
                                    # print(perm6, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm7, contr1, contr2, sign)
                                    # print(perm7, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm8, contr1, contr2, sign)
                                    # print(perm8, contr1, contr2, sign)

                                    s = expr.split(',')
                                    s1 = s[0].split('(')
                                    s2 = s[1].split('(')

                                    term = [sign, s1[0][1:], '(', contr1, '),', s2[0], '(', contr2, ')']

                                    expr_list.append(''.join(term))

    return list(set(expr_list))


def get_counting_dict(contr, spincase):
    if spincase == 'A':
        return {'num_virt_alpha': contr.count('a') + contr.count('b') + contr.count('c'),
                'num_core_alpha': contr.count('i') + contr.count('j') + contr.count('k'),
                'num_act_hole_alpha': contr.count('I') + contr.count('J') + contr.count('K'),
                'num_act_particle_alpha': contr.count('A') + contr.count('B') + contr.count('C'),
                'num_virt_beta': 0,
                'num_core_beta': 0,
                'num_act_hole_beta': 0,
                'num_act_particle_beta': 0
                }
    if spincase == 'B':
        return {'num_virt_alpha': contr.count('a') + contr.count('b'),
                'num_core_alpha': contr.count('i') + contr.count('j'),
                'num_act_hole_alpha': contr.count('I') + contr.count('J'),
                'num_act_particle_alpha': contr.count('A') + contr.count('B'),
                'num_virt_beta': contr.count('c'),
                'num_core_beta': contr.count('k'),
                'num_act_hole_beta': contr.count('K'),
                'num_act_particle_beta': contr.count('C')
                }
    if spincase == 'C':
        return {'num_virt_alpha': contr.count('a'),
                'num_core_alpha': contr.count('i'),
                'num_act_hole_alpha': contr.count('I'),
                'num_act_particle_alpha': contr.count('A'),
                'num_virt_beta': contr.count('b') + contr.count('c'),
                'num_core_beta': contr.count('j') + contr.count('k'),
                'num_act_hole_beta': contr.count('J') + contr.count('K'),
                'num_act_particle_beta': contr.count('B') + contr.count('C')
                }
    if spincase == 'D':
        return {'num_virt_beta': contr.count('a') + contr.count('b') + contr.count('c'),
                'num_core_beta': contr.count('i') + contr.count('j') + contr.count('k'),
                'num_act_hole_beta': contr.count('I') + contr.count('J') + contr.count('K'),
                'num_act_particle_beta': contr.count('A') + contr.count('B') + contr.count('C'),
                'num_virt_alpha': 0,
                'num_core_alpha': 0,
                'num_act_hole_alpha': 0,
                'num_act_particle_alpha': 0
                }


def get_swapping_dict(contr, spincase):
    if spincase == 'A':
        dict_out = {'virt_alpha': [x for x in ['a', 'b', 'c'] if x in contr],
                    'core_alpha': [x for x in ['i', 'j', 'k'] if x in contr],
                    'act_hole_alpha': [x for x in ['I', 'J', 'K'] if x in contr],
                    'act_particle_alpha': [x for x in ['A', 'B', 'C'] if x in contr],
                    'virt_beta': [],
                    'core_beta': [],
                    'act_hole_beta': [],
                    'act_particle_beta': []
                    }
    if spincase == 'B':
        dict_out = {'virt_alpha': [x for x in ['a', 'b'] if x in contr],
                    'core_alpha': [x for x in ['i', 'j'] if x in contr],
                    'act_hole_alpha': [x for x in ['I', 'J'] if x in contr],
                    'act_particle_alpha': [x for x in ['A', 'B'] if x in contr],
                    'virt_beta': [x for x in ['c'] if x in contr],
                    'core_beta': [x for x in ['k'] if x in contr],
                    'act_hole_beta': [x for x in ['K'] if x in contr],
                    'act_particle_beta': [x for x in ['C'] if x in contr]
                    }
    if spincase == 'C':
        dict_out = {'virt_alpha': [x for x in ['a'] if x in contr],
                    'core_alpha': [x for x in ['i'] if x in contr],
                    'act_hole_alpha': [x for x in ['I'] if x in contr],
                    'act_particle_alpha': [x for x in ['A'] if x in contr],
                    'virt_beta': [x for x in ['b', 'c'] if x in contr],
                    'core_beta': [x for x in ['j', 'k'] if x in contr],
                    'act_hole_beta': [x for x in ['J', 'K'] if x in contr],
                    'act_particle_beta': [x for x in ['B', 'C'] if x in contr]
                    }
    if spincase == 'D':
        dict_out = {'virt_beta': [x for x in ['a', 'b', 'c'] if x in contr],
                    'core_beta': [x for x in ['i', 'j', 'k'] if x in contr],
                    'act_hole_beta': [x for x in ['I', 'J', 'K'] if x in contr],
                    'act_particle_beta': [x for x in ['A', 'B', 'C'] if x in contr],
                    'virt_alpha': [],
                    'core_alpha': [],
                    'act_hole_alpha': [],
                    'act_particle_alpha': []
                    }

    # this part is done because you only need one swap between representative
    # indices of each type. Any additional swaps that can be generated are
    # related to the existing diagrams via antisymmetrizers.
    # E.g.,
    # if you have H(Amie)*t3a(eBCmJK), you only need the terms
    # +H(Amie)*t3a(eBCmJK) and A(JK)[-H(AmJe)*t3a(eBCmiK)].
    # There could also be -H(AmKe)*t3a(eBCmJi), but this is
    # part of the antisymmetrizer A(JK) applied to the second
    # diagram.
    for key in dict_out.keys():
        if len(dict_out[key]) > 1:
            dict_out[key] = [dict_out[key][0]]

    return dict_out