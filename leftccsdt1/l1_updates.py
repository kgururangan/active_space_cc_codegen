from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):

    if args.spincase == 'a':
        t_a(args.projection)

    # if args.spincase == 'b':
    #     t_b(args.projection)

def t_a(projection):

    g = Generator(projection, 'a', 1, full_asym_weight=1.0, active_output_quantity=True, output_label='dL',
                                      active_contract = True, active_obj_A = True, active_obj_B = True,
                                      print_ph_slices_A = False, print_ph_slices_B = False)
    expressions = [
        BinaryExpression(+1.0, 1.0, Term('L', 'aaa', 'efgIno'), Term('T', 'aaa', 'efgmno')),
        BinaryExpression(+1.0, 1.0, Term('L', 'aab', 'efgIno'), Term('T', 'aab', 'efgmno')),
        BinaryExpression(+1.0, 1.0, Term('L', 'abb', 'efgIno'), Term('T', 'abb', 'efgmno')),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds L1 left-CCSDt update for specified projection and spincase.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., a or b.')
    parser.add_argument('projection',
                        help="String, for example 'AI', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)