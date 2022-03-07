from generator import write_HBarT3_contractions
from utilities import change_term_to_projection

def main(projection):

    out_proj_spin = 'A'
    weight0 = 36.0
    residual_term = 'dT.aaa'

    all_active_expr = ['-h1A(mI),t3A(ABCmJK)',
                       '+h1A(Ae),t3a(eBCIJK)',
                       '+h2A(mnIJ),t3a(ABCmnK)',
                       '+h2A(ABef),t3a(efCIJK)',
                       '+h2A(AmIe),t3a(eBCmJK)',
                       '+h2B(AmIe),t3b(BCeJKm)']

    input_expr = []

    for expr in all_active_expr:

        s = expr.split(',')
        s1 = s[0].split('(')
        s2 = s[1].split('(')

        contr1 = s1[1][0:-1]
        contr2 = s2[1][0:-1]

        term = [s1[0], '(', change_term_to_projection(contr1, projection), '),', s2[0], '(', change_term_to_projection(contr2, projection), ')']

        input_expr.append(''.join(term))

    print(input_expr)

    HBarT3_out, nterms = write_HBarT3_contractions(input_expr, projection, out_proj_spin, weight0, residual_term)
    print('# of terms = ', nterms)


if __name__ == "__main__":

    projection = 'AbcIJK'

    main(projection)