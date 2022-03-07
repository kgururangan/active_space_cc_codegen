from diagramperms import generate_active_permutations
from weights import get_permutation_weight
from contraction import contract
#from indices import check_include_term, convert_char_to_ov, get_slicestr_t3, type_of_index, is_free_index


def active_space_generator(expression, projection, spincase, weight0, num_active=1):


    # generate all unique active-space diagram permutations
    unique_expressions = generate_active_permutations(expression, spincase)
    nterm = len(unique_expressions)

    # # get the container label for the output quantity (e.g., residual)
    # residual_label = get_residual_label(projection, residual_label)

    # loop over unique active-space diagrams
    active_space_contractions = []
    for expr in unique_expressions:
        # get all possible active-space contractions by splitting the contraction lines into active/inactive
        all_contractions.append(contract(expr, num_active))

    # find the permutation weight using last contr1 and contr2
    perm_weight = get_permutation_weight(contr1, contr2, spincase)


    return active_space_contractions

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
