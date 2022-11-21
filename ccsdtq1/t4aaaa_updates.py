from actgen.term import Term, BinaryExpression
from actgen.generator import Generator

import argparse

def main(args):
    projection = args.projection

    g = Generator(projection, "aaaa", 1)

    expressions = [
        # < ijklabcd | (H(2) * T4)_C | 0 >
        BinaryExpression(-1.0, 1.0, Term("H", "a", "mI"), Term("T", "aaaa", "ABCDmJKL")),     # (l/ijk) = 4
        BinaryExpression(+1.0, 1.0, Term("H", "a", "Ae"), Term("T", "aaaa", "eBCDIJKL")),     # (d/abc) = 4
        BinaryExpression(+1.0, 1.0, Term("H", "aa", "mnIJ"), Term("T", "aaaa", "ABCDmnKL")),  # (kl/ij) = 6
        BinaryExpression(+1.0, 1.0, Term("H", "aa", "ABef"), Term("T", "aaaa", "efCDIJKL")),  # (cd/ab) = 6
        BinaryExpression(+1.0, 1.0, Term("H", "aa", "AmIe"), Term("T", "aaaa", "eBCDmJKL")),  # (d/abc)(l/ijk) = 16
        BinaryExpression(+1.0, 1.0, Term("H", "ab", "AmIe"), Term("T", "aaab", "BCDeJKLm")),  # (d/abc)(l/ijk) = 16
    ]

    g.kernel(expressions, projection, print_term=False)

    g = Generator(projection, "aaaa", 0,
                  active_contract=False,
                  active_obj_A=False, active_obj_B=False,
                  print_vo_slices_A=True, print_vo_slices_B=False)

    expressions = [
        # The tricky V*T4 intermediates, which are computed as full quantities
        BinaryExpression(1.0, 1.0, Term("VT4", "aaa", "BCDJKe", is_full=[False, False, False, False, False, True]),
                         Term("T", "aa", "AeIL", is_full=[False, True, False, False])),
        BinaryExpression(-1.0, 1.0, Term("VT4", "aaa", "BCmJKL", is_full=[False, False, True, False, False, False]),
                         Term("T", "aa", "ADIm", is_full=[False, False, False, True])),
    ]

    g.kernel(expressions, projection, print_term=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds T4_aaaa CCSDTq update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'ABcdIJKl', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)