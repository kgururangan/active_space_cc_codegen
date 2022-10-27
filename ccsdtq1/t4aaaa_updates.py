from actgen.term import Term, BinaryExpression
from actgen.generator import Generator

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

    g.kernel(expressions, projection, print_term=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds T4_aaaa CCSDTq update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'ABcdIJKl', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)