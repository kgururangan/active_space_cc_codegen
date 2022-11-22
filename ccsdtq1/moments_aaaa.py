from actgen.term import Term, BinaryExpression
from actgen.generator import Generator

import argparse


def main(args):

    projection = args.projection

    g = Generator(projection, "aaaa", 0,
                  active_contract=False,
                  active_obj_A=False, active_obj_B=False,
                  print_vo_slices_A=True, print_vo_slices_B=False)

    expressions = [
        # < ijklabcd | H(2) | 0 >
        # < ijklabcd | (H(2) * T3)_C + (H(2) * 1/2 T3**2)_C | 0 >
        BinaryExpression(1.0, 1.0, Term("H", "aa", "CDKe", is_full=[False,False,False,True]), Term("T", "aaa", "ABeIJL", is_full=[False,False,True,False,False,False])),
        BinaryExpression(-1.0, 1.0, Term("H", "aa", "CmKL", is_full=[False,True,False,False]), Term("T", "aaa", "ABDIJm", is_full=[False,False,False,False,False,True])),
        BinaryExpression(1.0, 1.0, Term("X", "aaa", "BmnJKL", is_full=[False,True,True,False,False,False]), Term("T", "aaa", "ACDImn", is_full=[False,False,False,False,True,True])),
        BinaryExpression(1.0, 1.0, Term("X", "aaa", "ABmIJL", is_full=[False,False,True,False,False,False]), Term("T", "aa", "CDKm", is_full=[False,False,False,True])),
        BinaryExpression(1.0, 1.0, Term("X", "aaa", "CDmKLe", is_full=[False,False,True,False,False,True]), Term("T", "aaa", "ABeIJm", is_full=[False,False,True,False,False,True])),
        BinaryExpression(1.0, 1.0, Term("X", "aab", "CDmKLe", is_full=[False,False,True,False,False,True]), Term("T", "aab", "ABeIJm", is_full=[False,False,True,False,False,True])),
    ]

    g.kernel(expressions, projection, print_term=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds moments of CCSDT equation projected on quadruples for the aaaa spincase.")
    parser.add_argument('projection', type=str, help="String, for example 'ABcdIJKl', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)