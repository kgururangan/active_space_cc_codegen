from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection, get_label_from_projection

import argparse

def main(args):

    if args.spincase == 'aa':
        HR3_aa(args.projection)

    if args.spincase == 'ab':
        VT3_ab(args.projection)

    if args.spincase == 'bb':
        VT3_bb(args.projection)

def HR3_aa(projection):

    g = Generator(projection, 'aa', 1, full_asym_weight=1.0, output_label='X',
                  active_contract=True, active_obj_A=False, active_obj_B=True,
                  print_ph_slices_A=True, print_ph_slices_B=False)

    if projection.lower() == 'amij':
        expressions = [
                        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef', is_full=[True,False,False,False]), Term('R', 'aaa', 'AefIJn')),
                        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef', is_full=[True,False,False,False]), Term('R', 'aab', 'AefIJn')),
        ]

    if projection.lower() == 'abie':
        expressions = [
                        BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aaa', 'ABfImn')),
                        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'aab', 'ABfImn'))
        ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

def VT3_ab(projection):

    weight = 1.0
    residual_term = 'I2B_' + get_label_from_projection(projection)

    g = Generator(projection, 'ab', 1, full_asym_weight=weight, output_quantity=residual_term)

    if projection.lower() == 'amij': # vooo
        expressions = [
                       BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'nmfe'), Term('T', 'aab', 'AfeInJ')),
                       BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'nmfe'), Term('T', 'abb', 'AfeInJ'))
        ]
    if projection.lower() == 'mbij': # ovoo
        expressions = [
                       BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aab', 'efBInJ')),
                       BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'abb', 'efBInJ'))
        ]
    if projection.lower() == 'abej': # vvvo
        expressions = [
                       BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aab', 'AfBmnJ')),
                       BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'abb', 'AfBmnJ'))
        ]
    if projection.lower() == 'abie': # vvov
        expressions = [
                       BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'nmfe'), Term('T', 'aab', 'AfBInm')),
                       BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'nmfe'), Term('T', 'abb', 'AfBInm'))
        ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

def VT3_bb(projection):

    weight = 1.0
    residual_term = 'I2C_' + get_label_from_projection(projection)

    g = Generator(projection, 'bb', 1, full_asym_weight=weight, output_quantity=residual_term)

    if projection.lower() == 'amij':
        expressions = [
                        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'mnef', is_full=[True,False,False,False]), Term('T', 'bbb', 'AefIJn')),
                        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'nmfe', is_full=[True,False,False,False]), Term('T', 'abb', 'fAenIJ')),
        ]

    if projection.lower() == 'abie':
        expressions = [
                        BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'mnef'), Term('T', 'bbb', 'ABfImn')),
                        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'nmfe'), Term('T', 'abb', 'fABnIm'))
        ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds VT3 intermediates of the specified type.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., aa, ab, or bb.')
    parser.add_argument('projection',
                        help="String, for example 'AmIJ', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)