from utilities import change_term_to_projection
from generator import write_HBarT3_contractions

def write_vt3a_intermediate(projection):

    weight0 = 1.0
    out_proj_spin = 'A'
    residual_term = 'I2' + out_proj_spin + '_'

    if projection.lower() == 'amij':
        all_active_expr = ['+h2a(mnef),t3a(AefIJn)',
                           '+h2b(mnef),t3b(AefIJn)']
    if projection.lower() == 'abie':
        all_active_expr = ['-h2a(mnef),t3a(ABfImn)',
                           '-h2b(mnef),t3b(ABfImn)']
    input_expr = []

    for expr in all_active_expr:
        s = expr.split(',')
        s1 = s[0].split('(')
        s2 = s[1].split('(')

        contr1 = s1[1][0:-1]
        contr2 = s2[1][0:-1]

        term = [s1[0], '(', change_term_to_projection(contr1, projection), '),', s2[0], '(',
                change_term_to_projection(contr2, projection), ')']

        input_expr.append(''.join(term))

    print(input_expr)

    HBarT3_out, nterms = write_HBarT3_contractions(input_expr, projection, out_proj_spin, weight0, residual_term)
    print('# of terms = ', nterms)

def write_vt3b_intermediate(projection):

    weight0 = 1.0
    out_proj_spin = 'B'
    residual_term = 'I2' + out_proj_spin + '_'

    if projection.lower() == 'amij': # vooo
        all_active_expr = ['+h2b(nmfe),t3b(AfeInJ)',
                           '+h2c(nmfe),t3c(AfeInJ)']
    if projection.lower() == 'mbij': # ovoo
        all_active_expr = ['+h2a(mnef),t3b(efBInJ)',
                           '+h2b(mnef),t3c(efBInJ)']
    if projection.lower() == 'abej': # vvvo
        all_active_expr = ['-h2a(mnef),t3b(AfBmnJ)',
                           '-h2b(mnef),t3c(AfBmnJ)']
    if projection.lower() == 'abie': # vvov
        all_active_expr = ['-h2b(nmfe),t3b(AfBImn)',
                           '-h2c(nmfe),t3c(AfBImn)']

    input_expr = []

    for expr in all_active_expr:
        s = expr.split(',')
        s1 = s[0].split('(')
        s2 = s[1].split('(')

        contr1 = s1[1][0:-1]
        contr2 = s2[1][0:-1]

        term = [s1[0], '(', change_term_to_projection(contr1, projection), '),', s2[0], '(',
                change_term_to_projection(contr2, projection), ')']

        input_expr.append(''.join(term))

    print(input_expr)

    HBarT3_out, nterms = write_HBarT3_contractions(input_expr, projection, out_proj_spin, weight0, residual_term)
    print('# of terms = ', nterms)


if __name__ == "__main__":

    projection = 'AmIJ'

    #write_vt3a_intermediate(projection)

    write_vt3b_intermediate('Abej')

