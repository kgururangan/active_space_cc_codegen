from term import Term, BinaryExpression
from diagramperms import generate_active_permutations
from contraction import contract
from generator import active_space_generator

def main(projection):
    #
    # out_proj_spin = 'A'
    # weight0 = 36.0
    # residual_term = 'dT.aaa.'
    #
    # all_active_expr = ['-h1A(mI),t3A(ABCmJK)',
    #                    '+h1A(Ae),t3a(eBCIJK)',
    #                    '+h2A(mnIJ),t3a(ABCmnK)',
    #                    '+h2A(ABef),t3a(efCIJK)',
    #                    '+h2A(AmIe),t3a(eBCmJK)',
    #                    '+h2B(AmIe),t3b(BCeJKm)']

    # -h1A(mI) * t3A(ABCmJK)
    # +h2A(Amie),t3a(ebcmJK)
    term_1 = Term('H', 'aa', 'Amie')
    term_2 = Term('T', 'aaa', 'ebcmJK')
    expression = BinaryExpression(1.0, 1.0, term_1, term_2)

    diagrams, perm_weights = active_space_generator(expression, 'aaa', num_active=1)

    for unique_diagram, perm_weight in zip(diagrams, perm_weights):
        print('------------')
        for expr in unique_diagram:
            print(perm_weight, expr.to_string())



if __name__ == "__main__":

    projection = 'AbcIJK'

    main(projection)