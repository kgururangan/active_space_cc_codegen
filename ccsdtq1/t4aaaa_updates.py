from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):
    projection = args.projection

    g = Generator(projection, "aaaa", 1)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term("H", "a", "mI"), Term("T", "aaaa", "ABCDmJKL")),     # (l/ijk) = 4
        BinaryExpression(+1.0, 1.0, Term("H", "a", "Ae"), Term("T", "aaaa", "eBCDIJKL")),     # (d/abc) = 4
        BinaryExpression(+1.0, 1.0, Term("H", "aa", "mnIJ"), Term("T", "aaaa", "ABCDmnKL")),  # (kl/ij) = 6
        BinaryExpression(+1.0, 1.0, Term("H", "aa", "ABef"), Term("T", "aaaa", "efCDIJKL")),  # (cd/ab) = 6
        BinaryExpression(+1.0, 1.0, Term("H", "aa", "AmIe"), Term("T", "aaaa", "eBCDmJKL")),  # (d/abc)(l/ijk) = 16
        BinaryExpression(+1.0, 1.0, Term("H", "ab", "AmIe"), Term("T", "aaab", "BCDeJKLm")),  # (d/abc)(l/ijk) = 16
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

    print("=========================================================================")

    g = Generator(projection, "aaaa", 1, active_obj_A=False, active_obj_B=False, print_vo_slices_A=True, print_vo_slices_B=False)

    expressions_2 = [
        BinaryExpression(1.0, 1.0, Term("I", "aaa", "BCDJef"), Term("T", "aaa", "AefIKL"))    # (j/ikl)(a/bcd) = 16
    ]

    for expression in expressions_2:


        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds T4_aaaa CCSDTq update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'ABcdIJKl', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)