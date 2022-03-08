from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection

import argparse

def main(args):
    projection = args.projection

    g = Generator(projection, 'aaa', 1)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('H', 'a', 'mI'), Term('T', 'aaa', 'ABCmJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'a', 'Ae'), Term('T', 'aaa', 'eBCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnIJ'), Term('T', 'aaa', 'ABCmnK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'ABef'), Term('T', 'aaa', 'efCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'AmIe'), Term('T', 'aaa', 'eBCmJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'AmIe'), Term('T', 'aab', 'BCeJKm'))
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds T3_aaa CCSDt update for specified projection.")
    parser.add_argument('projection', help="String, for example 'AbcIJK', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)