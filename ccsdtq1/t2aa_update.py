from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):
    projection = args.projection

    g = Generator(projection, "aa", 1)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term("H", "aa", "mnef"), Term("T", "aaaa", "ABefIJmn")),
        BinaryExpression(+1.0, 1.0, Term("H", "ab", "mnef"), Term("T", "aaab", "ABefIJmn")),
        BinaryExpression(+1.0, 1.0, Term("H", "bb", "mnef"), Term("T", "aabb", "ABefIJmn")),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds T2_aa CCSDTq update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'AbiJ', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)