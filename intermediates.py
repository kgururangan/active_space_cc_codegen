from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection, get_label_from_projection

import argparse

def main(args):

    if args.spincase == 'aa':
        VT3_aa(args.projection)

    if args.spincase == 'ab':
        VT3_ab(args.projection)

    if args.spincase == 'bb':
        VT3_bb(args.projection)

def VT3_aa(projection):

    residual_term = 'I2A_' + get_label_from_projection(projection)

    g = Generator(projection, 'aa', 1, full_asym_weight=1.0, output_quantity=residual_term)

    if projection.lower() == 'amij':
        expressions = [
                        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aaa', 'AefIJn')),
                        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'aab', 'AefIJn')),
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
                       BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'nmfe'), Term('T', 'aab', 'AfBImn')),
                       BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'nmfe'), Term('T', 'abb', 'AfBImn'))
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