from generator import write_HBarT3_contractions
from utilities import change_term_to_projection

def main(projection):

    out_proj_spin = 'B'

    all_active_expr = ['-h1A(mI),t3b(ABCmJK)',
                       '-h1B(mK),t3b(ABCIJm)',
                       '+h1A(Ae),t3b(eBCIJK)',
                       '+h1B(Ce),t3b(ABeIJK)',
                       '+h2A(mnIJ),t3b(ABCmnK)',
                       '+h2B(mnJK),t3b(ABCImn)',
                       '+h2A(ABef),t3b(efCIJK)',
                       '+h2B(BCef),t3b(AefIJK)',
                       '+h2A(AmIe),t3b(eBCmJK)',
                       '+h2B(AmIe),t3c(BeCJmK)',
                       '+h2B(mCeK),t3a(eABmIJ)',
                       '+h2C(CmKe),t3b(ABeIJm)',
                       '-h2B(AmeK),t3b(eBCIJm)',
                       '-h2B(mCIe),t3b(ABemJK)']

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

    HBarT3_out, nterms = write_HBarT3_contractions(input_expr, projection, out_proj_spin, print_term=False)
    print('# of terms = ', nterms)


if __name__ == "__main__":

    projection = 'ABcIJK'

    main(projection)