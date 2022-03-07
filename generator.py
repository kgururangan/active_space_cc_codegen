from diagramperms import generate_active_permutations
from weights import get_permutation_weight
from parser import parse_expression
from contraction import binary_active_contraction
from indices import check_include_term, convert_char_to_ov, get_slicestr_t3, type_of_index, is_free_index


def active_space_generator(list_of_expressions, projection, spincase, weight0, residual_term, nact_scheme=1):

    all_expressions = []
    for i, expr in enumerate(list_of_expressions):
        # for each expression, generate all unique active-space diagram permutations
        all_expressions.append(generate_active_permutations(expr, spincase))

    # get the container label for the output quantity (e.g., residual)
    residual_term = get_residual_label(projection, residual_term)

    active_space_contractions = []
    # loop over the provided expressions
    nterm = 0
    for expr in all_expressions:
        # loop over unique active-space diagrams
        for expr_perm in expr:

            # get all possible active-space contractions by splitting the contraction lines into active/inactive
            all_contractions = binary_active_contraction(contr_chars, spin_contr, obj1, obj2, sign_orig)

            # filter out those terms that have fewer than nact_scheme active indices in either particle or hole
            retained_contractions = []
            for c in enumerate(all_contractions):
                # get the indices describing the T3 operator
                s = c.split(',')
                s2 = s[2].split('(')
                term2 = s2[0]
                contr2 = s2[1][:-1]
                # based on the number of active/inactive labels, decide whether
                # this T3 block belongs to the active-space CC calculation
                include_term = check_include_term(contr2, nact_scheme)
                if include_term:
                    retained_contractions.append(c)
            active_space_contractions.append(retained_contractions)

            # find the permutation weight using last contr1 and contr2
            perm_weight = get_permutation_weight(contr1, contr2, spincase)


    return active_space_contractions, residual_term

def get_residual_label(projection, residual_term):

    for inm, op in enumerate(projection):
        if type_of_index(op) == 'active_hole':
            residual_term += 'O'
        if type_of_index(op) == 'active_particle':
            residual_term += 'V'
        if type_of_index(op) == 'inactive_hole':
            residual_term += 'o'
        if type_of_index(op) == 'inactive_particle':
            residual_term += 'v'

    return residual_term