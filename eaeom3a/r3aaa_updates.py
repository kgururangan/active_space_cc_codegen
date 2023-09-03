from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):
    projection = args.projection

    residual_term = 'x3a'

    g = Generator(projection, 'aaa', 1, output_quantity=residual_term)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('H', 'a', 'mJ'), Term('R', 'aaa', 'ABCmK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'a', 'Be'), Term('R', 'aaa', 'AeCJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'ABef'), Term('R', 'aaa', 'efCJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnJK'), Term('R', 'aaa', 'ABCmn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'CmKe'), Term('R', 'aaa', 'ABeJm')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'CmKe'), Term('R', 'aab', 'ABeJm')),
    ]
    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds R3_aaa EA-EOMCCSDt update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'AbcJK', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)

