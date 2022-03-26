from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection

import argparse

def main(args):

    if args.spincase == 'aa':
        t2_aa(args.projection)

    if args.spincase == 'ab':
        t2_ab(args.projection)

    if args.spincase == 'bb':
        t2_bb(args.projection)

def t2_aa(projection):

    g = Generator(projection, 'aa', 1, active_output_quantity=False, output_label='dR')

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('X', 'a', 'me'), Term('T', 'aaa', 'ABeIJm')),
        BinaryExpression(+1.0, 1.0, Term('X', 'b', 'me'), Term('T', 'aab', 'ABeIJm')),
        BinaryExpression(+1.0, 1.0, Term('H', 'a', 'me'), Term('R', 'aaa', 'ABeIJm')),
        BinaryExpression(+1.0, 1.0, Term('H', 'b', 'me'), Term('R', 'aab', 'ABeIJm')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mnIf'), Term('R', 'aab', 'ABfmJn')),
        BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'mnIf'), Term('R', 'aaa', 'ABfmJn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'Anef'), Term('R', 'aaa', 'eBfIJn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'Anef'), Term('R', 'aab', 'eBfIJn'))
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()



def t2_ab(projection):

    g = Generator(projection, 'ab', 1, active_output_quantity=False, output_label='dR')

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('X', 'a', 'me'), Term('T', 'aab', 'AeBImJ')),
        BinaryExpression(+1.0, 1.0, Term('X', 'b', 'me'), Term('T', 'abb', 'AeBImJ')),
        BinaryExpression(+1.0, 1.0, Term('H', 'a', 'me'), Term('R', 'aab', 'AeBImJ')),
        BinaryExpression(+1.0, 1.0, Term('H', 'b', 'me'), Term('R', 'abb', 'AeBImJ')),
        BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'mnIf'), Term('R', 'aab', 'AfBmnJ')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'nmfJ'), Term('R', 'aab', 'AfBInm')),
        BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'mnJf'), Term('R', 'abb', 'AfBInm')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mnIf'), Term('R', 'abb', 'AfBmnJ')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'Anef'), Term('R', 'aab', 'efBInJ')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'Anef'), Term('R', 'abb', 'efBInJ')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'nBfe'), Term('R', 'aab', 'AfeInJ')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'Bnef'), Term('R', 'abb', 'AfeInJ')),

    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()



def t2_bb(projection):

    g = Generator(projection, 'bb', 1, active_output_quantity=False, output_label='dR')

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('X', 'a', 'me'), Term('T', 'abb', 'eABmIJ')),
        BinaryExpression(+1.0, 1.0, Term('X', 'b', 'me'), Term('T', 'bbb', 'ABeIJm')),
        BinaryExpression(+1.0, 1.0, Term('H', 'a', 'me'), Term('R', 'abb', 'eABmIJ')),
        BinaryExpression(+1.0, 1.0, Term('H', 'b', 'me'), Term('R', 'bbb', 'ABeIJm')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'Anef'), Term('R', 'bbb', 'eBfIJn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'nAfe'), Term('R', 'abb', 'feBnIJ')),
        BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'mnIf'), Term('R', 'bbb', 'ABfmJn')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'nmfI'), Term('R', 'abb', 'fABnmJ'))
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds R2 EOMCCSDt update for specified projection and spincase.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., aa, ab, or bb.')
    parser.add_argument('projection',
                        help="String, for example 'AbIJ', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)