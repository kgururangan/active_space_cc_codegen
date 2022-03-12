from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection

import argparse

def main(args):

    if args.spincase == 'a':
        t_a(args.projection)

    if args.spincase == 'b':
        t_b(args.projection)

def t_a(projection):

    g = Generator(projection, 'a', 1, active_output_quantity=False)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aaa', 'AefImn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'aab', 'AefImn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'mnef'), Term('T', 'abb', 'AefImn')),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


def t_b(projection):

    g = Generator(projection, 'b', 1, active_output_quantity=False)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'mnef'), Term('T', 'bbb', 'AefImn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aab', 'efAmnI')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'abb', 'efAmnI')),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds T1 CCSDt update for specified projection and spincase.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., a or b.')
    parser.add_argument('projection',
                        help="String, for example 'AI', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)