from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):
    projection = args.projection

    #residual_term = 'dR.aaa.' + get_label_from_projection(projection)
    residual_term = 'x3a'

    g = Generator(projection, 'aaa', 1, output_quantity=residual_term)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('X', 'a', 'Be'), Term('T', 'aaa', 'AeCIJK')),
        BinaryExpression(-1.0, 1.0, Term('X', 'a', 'mJ'), Term('T', 'aaa', 'ABCImK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'aa', 'mnIJ'), Term('T', 'aaa', 'ABCmnK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'aa', 'ABef'), Term('T', 'aaa', 'efCIJK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'aa', 'BmJe'), Term('T', 'aaa', 'AeCimK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'ab', 'BmJe'), Term('T', 'aab', 'ACeIKm')),
        BinaryExpression(-1.0, 1.0, Term('H', 'a', 'mJ'), Term('R', 'aaa', 'ABCImK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'a', 'Be'), Term('R', 'aaa', 'AeCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnIJ'), Term('R', 'aaa', 'ABCmnK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'ABef'), Term('R', 'aaa', 'efCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'AmIe'), Term('R', 'aaa', 'eBCmJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'AmIe'), Term('R', 'aab', 'BCeJKm')),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds R3_aaa EOMCCSDt update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'AbcIJK', specifying the desired outward line projection.")
    #parser.add_argument('--n', '-number', type=str, help='Numerical representation of active/inactive indices defining projection, e.g., 111011.')
    args = parser.parse_args()

    main(args)

