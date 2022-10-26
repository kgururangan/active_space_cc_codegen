from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):
    projection = args.projection

    g = Generator(projection, 'bbb', 1)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('H', 'b', 'mI'), Term('T', 'bbb', 'ABCmJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'b', 'Ae'), Term('T', 'bbb', 'eBCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'mnIJ'), Term('T', 'bbb', 'ABCmnK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'ABef'), Term('T', 'bbb', 'efCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'AmIe'), Term('T', 'bbb', 'eBCmJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mAeI'), Term('T', 'abb', 'eBCmJK'))
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds T3_bbb CCSDt update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'AbcIJK', specifying the desired outward line projection.")
    #parser.add_argument('--n', '-number', type=str, help='Numerical representation of active/inactive indices defining projection, e.g., 111011.')
    args = parser.parse_args()

    main(args)