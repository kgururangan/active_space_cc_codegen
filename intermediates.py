
from generator import write_HBarT3_contractions


if __name__ == "__main__":

    projection = 'AmIJ'
    out_proj_spin = 'A'

    weight0 = 1.0
    residual_term = 'VT3_'

    input_expr = ['+h2a(mnef),t3a(AefIJn)',
                  '+h2b(mnef),t3b(AefIJn)']

    print(input_expr)

    HBarT3_out, nterms = write_HBarT3_contractions(input_expr, projection, out_proj_spin, weight0, residual_term)
    print('# of terms = ', nterms)

    projection = 'ABIe'
    out_proj_spin = 'A'

    weight0 = 1.0
    residual_term = 'VT3_'

    input_expr = ['-h2a(mnef),t3a(ABfImn)',
                  '-h2b(mnef),t3b(ABfImn)']

    print(input_expr)

    HBarT3_out, nterms = write_HBarT3_contractions(input_expr, projection, out_proj_spin, weight0, residual_term)
    print('# of terms = ', nterms)