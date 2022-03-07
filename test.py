from term import Term, BinaryExpression
from diagramperms import generate_active_permutations
from contraction import contract

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
    term_1 = Term('H', 'aa', 'mnef')
    term_2 = Term('T', 'aaa', 'efAmnI')
    expression = BinaryExpression(1.0, 1.0, term_1, term_2)



    new_expressions = generate_active_permutations(expression, 'aaa', verbose=False)

    y = contract(expression)


    for expr in y:
        print(expr.to_string())



if __name__ == "__main__":

    projection = 'AbcIJK'

    main(projection)