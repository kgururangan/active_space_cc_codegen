from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):

    if args.spincase == 'aaa':
        moments_aaa(args.projection)

    if args.spincase == 'aab':
        moments_aab(args.projection)

    if args.spincase == 'abb':
        moments_abb(args.projection)

    if args.spincase == 'bbb':
        moments_bbb(args.projection)

def moments_aaa(projection):

    g = Generator(projection, 'aaa', 0,
                  active_contract=False,
                  active_obj_A=False, active_obj_B=False,
                  print_ph_slices_A=True, print_ph_slices_B=False)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'AmIJ'), Term('T', 'aa', 'BCmK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'ABIe'), Term('T', 'aa', 'eCJK')),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

def moments_aab(projection):

    g = Generator(projection, 'aab', 0,
                  active_contract=False,
                  active_obj_A=False, active_obj_B=False,
                  print_ph_slices_A=True, print_ph_slices_B=False)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'BCeK', is_full=[False,False,True,False]), Term('T', 'aa', 'AeIJ', is_full=[False,True,False,False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mCJK', is_full=[True,False,False,False]), Term('T', 'aa', 'ABIm', is_full=[False,False,False,True])),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'ACIe', is_full=[False,False,False,True]), Term('T', 'ab', 'BeJK', is_full=[False,True,False,False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'AmIK', is_full=[False,True,False,False]), Term('T', 'ab', 'BCJm', is_full=[False,False,False,True])),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'ABIe', is_full=[False,False,False,True]), Term('T', 'ab', 'eCJK', is_full=[True,False,False,False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'AmIJ', is_full=[False,True,False,False]), Term('T', 'ab', 'BCmK', is_full=[False,False,True,False])),
    ]

    for expression in expressions:
        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

def moments_abb(projection):

    g = Generator(projection, 'abb', 0,
                  active_contract=False,
                  active_obj_A=False, active_obj_B=False,
                  print_ph_slices_A=True, print_ph_slices_B=False)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'ABIe', is_full=[False, False, False, True]),
                         Term('T', 'bb', 'eCJK', is_full=[True,False,False,False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'AmIJ', is_full=[False, True, False, False]),
                         Term('T', 'bb', 'BCmK', is_full=[False, False, True, False])),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'CBKe', is_full=[False, False, False, True]),
                         Term('T', 'ab', 'AeIJ', is_full=[False, True, False, False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'CmKJ', is_full=[False, True, False, False]),
                         Term('T', 'ab', 'ABIm', is_full=[False, False, False, True])),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'ABeJ', is_full=[False, False, True, False]),
                         Term('T', 'ab', 'eCIK', is_full=[True, False, False, False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mBIJ', is_full=[True, False, False, False]),
                         Term('T', 'ab', 'ACmK', is_full=[False, False, True, False])),
    ]

    for expression in expressions:
        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


def moments_bbb(projection):

    g = Generator(projection, 'bbb', 0,
                  active_contract=False,
                  active_obj_A=False, active_obj_B=False,
                  print_ph_slices_A=True, print_ph_slices_B=False)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'AmIJ', is_full=[False, True, False, False]),
                         Term('T', 'bb', 'BCmK', is_full=[False, False, True, False])),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'ABIe', is_full=[False, False, False, True]),
                         Term('T', 'bb', 'eCJK', is_full=[True, False, False, False])),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds <ijkabc| H(2) * T2 | 0 > moment-like projections of the specified type.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., aaa, aab, abb, or bbb.')
    parser.add_argument('projection',
                        help="String, for example 'ABcIJK', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)