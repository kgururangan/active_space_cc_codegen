from utilities import string_replacer, unique_objects
from term import Term, BinaryExpression

def generate_active_permutations(reference_expression, projection_spincase, verbose=False):
    from itertools import combinations

    expression_permutations = []

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

        return contr1, contr2, -1.0 * sign

    def _get_products(list1, list2):

        if len(list1) > 0 and len(list2) > 0:
            return [[1], [list1[0], list2[0]]]
        else:
            return [[1]]

    dict_1 = get_swapping_dict(reference_expression.A.indices, projection_spincase)
    dict_2 = get_swapping_dict(reference_expression.B.indices, projection_spincase)

    for perm1 in _get_products(dict_1['act_hole_alpha'], dict_2['core_alpha']):
        for perm2 in _get_products(dict_1['core_alpha'], dict_2['act_hole_alpha']):
            for perm3 in _get_products(dict_1['act_particle_alpha'], dict_2['virt_alpha']):
                for perm4 in _get_products(dict_1['virt_alpha'], dict_2['act_particle_alpha']):
                    for perm5 in _get_products(dict_1['act_hole_beta'], dict_2['core_beta']):
                        for perm6 in _get_products(dict_1['core_beta'], dict_2['act_hole_beta']):
                            for perm7 in _get_products(dict_1['act_particle_beta'], dict_2['virt_beta']):
                                for perm8 in _get_products(dict_1['virt_beta'], dict_2['act_particle_beta']):
                                    contr1 = reference_expression.A.indices
                                    contr2 = reference_expression.B.indices
                                    sign = reference_expression.sign

                                    if verbose:
                                        print('\n')
                                        print('Original:',contr1, contr2, sign)
                                        print(perm1, perm2, perm3, perm4, perm5, perm6, perm7, perm8)
                                        print('-----------------------------------------')

                                    contr1, contr2, sign = _apply_swap(perm1, contr1, contr2, sign)
                                    if verbose:
                                        print(perm1, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm2, contr1, contr2, sign)
                                    if verbose:
                                        print(perm2, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm3, contr1, contr2, sign)
                                    if verbose:
                                        print(perm3, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm4, contr1, contr2, sign)
                                    if verbose:
                                        print(perm4, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm5, contr1, contr2, sign)
                                    if verbose:
                                        print(perm5, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm6, contr1, contr2, sign)
                                    if verbose:
                                        print(perm6, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm7, contr1, contr2, sign)
                                    if verbose:
                                        print(perm7, contr1, contr2, sign)

                                    contr1, contr2, sign = _apply_swap(perm8, contr1, contr2, sign)
                                    if verbose:
                                        print(perm8, contr1, contr2, sign)

                                    permuted_term_1 = Term(reference_expression.A.symbol,
                                                           reference_expression.A.spin,
                                                           contr1,
                                                           is_full=reference_expression.A.is_full)
                                    permuted_term_2 = Term(reference_expression.B.symbol,
                                                           reference_expression.B.spin,
                                                           contr2,
                                                           is_full=reference_expression.B.is_full)
                                    permuted_expression = BinaryExpression(sign,
                                                                           reference_expression.weight,
                                                                           permuted_term_1,
                                                                           permuted_term_2)

                                    expression_permutations.append(permuted_expression)

    return unique_objects(expression_permutations)


def get_swapping_dict(contr, spincase):
    if spincase in ['aaa', 'aa', 'a']:
        dict_out = {'virt_alpha': [x for x in ['a', 'b', 'c'] if x in contr],
                    'core_alpha': [x for x in ['i', 'j', 'k'] if x in contr],
                    'act_hole_alpha': [x for x in ['I', 'J', 'K'] if x in contr],
                    'act_particle_alpha': [x for x in ['A', 'B', 'C'] if x in contr],
                    'virt_beta': [],
                    'core_beta': [],
                    'act_hole_beta': [],
                    'act_particle_beta': []
                    }
    if spincase in ['aab']:
        dict_out = {'virt_alpha': [x for x in ['a', 'b'] if x in contr],
                    'core_alpha': [x for x in ['i', 'j'] if x in contr],
                    'act_hole_alpha': [x for x in ['I', 'J'] if x in contr],
                    'act_particle_alpha': [x for x in ['A', 'B'] if x in contr],
                    'virt_beta': [x for x in ['c'] if x in contr],
                    'core_beta': [x for x in ['k'] if x in contr],
                    'act_hole_beta': [x for x in ['K'] if x in contr],
                    'act_particle_beta': [x for x in ['C'] if x in contr]
                    }
    if spincase in ['abb', 'ab']:
        dict_out = {'virt_alpha': [x for x in ['a'] if x in contr],
                    'core_alpha': [x for x in ['i'] if x in contr],
                    'act_hole_alpha': [x for x in ['I'] if x in contr],
                    'act_particle_alpha': [x for x in ['A'] if x in contr],
                    'virt_beta': [x for x in ['b', 'c'] if x in contr],
                    'core_beta': [x for x in ['j', 'k'] if x in contr],
                    'act_hole_beta': [x for x in ['J', 'K'] if x in contr],
                    'act_particle_beta': [x for x in ['B', 'C'] if x in contr]
                    }
    if spincase in ['bbb', 'bb', 'b']:
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

