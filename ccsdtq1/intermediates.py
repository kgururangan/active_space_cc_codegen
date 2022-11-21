from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection, get_label_from_projection

import argparse

def main(args):

    if args.spincase == 'aaa':
        VT4_aaa(args.projection)


def VT4_aaa(projection):


    # g = Generator(projection, 'aaa', 1, full_asym_weight=1.0, output_label='X',
    #               active_contract=True, active_obj_A=False, active_obj_B=True,
    #               print_ph_slices_A=True, print_ph_slices_B=False, active_output_quantity=False)

    g = Generator(projection, 'aaa', 1, full_asym_weight=1.0, output_label="X", active_output_quantity=False)

    if projection.lower() == 'abmijk':
        expressions = [
            BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef', is_full=[True,False,False,False]), Term('T', 'aaaa', 'ABefIJKn')),
            BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef', is_full=[True,False,False,False]), Term('T', 'aaab', 'ABefIJKn')),
        ]

    if projection.lower() == "abcije":
        expressions = [
            BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'mnef', is_full=[True,False,False,False]), Term('T', 'aaaa', 'ABCfIJmn')),
            BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mnef', is_full=[True,False,False,False]), Term('T', 'aaab', 'ABCfIJmn')),
        ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds the VT4 3-body intermediates of the specified type.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., aaa, aab, abb, or bbb.')
    parser.add_argument('projection',
                        help="String, for example 'ABmIJK' or 'ABCIJe', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)