from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

# Create a new full sorted integral object, so that it can store one- and two-body parts
# populate the active/inactive slices using explicit oa, ob, va, vb, Oa, Ob, Va, Vb slicing
# with the active-space defined intermediates of (l3*t3)_C and (L2*t3)_C. It is fortunate that
# the only required (L2*t3)_C intermediate is of the X.a.vo and X.b.vo variety, while (l3*t3)_C
# do not contribute anything of the vo type.
# Using this two-body integral as an intermediate, we can perform full contractions with Hbar to
# form the single and double projections. The triple projections do not engage any of these
# intermediates, so there is no need to worry about active indices on the outputs of these quantities.
# As a result, we should only have one function to update L1 and one to upate L2. We do not need to break
# up into the various active-space cases since the twobody object will be full.

def main(args):

    if args.type == 'L2t3':

        if args.spincase == 'a':
            L2T3_a_vo(args.projection)

        if args.spincase == 'b':
            L2T3_b_vo(args.projection)

    if args.type == 'l3t3':

        if args.spincase == 'a':
            if args.projection.lower() == 'im':
                L3T3_a_oo(args.projection)
            if args.projection.lower() == 'ea':
                L3T3_a_vv(args.projection)



# def L2T3_a_vo(projection):
#
#     g = Generator(projection, 'a', 1, full_asym_weight=1.0, active_output_quantity=True, output_label='dL',
#                                       active_contract = True, active_obj_A = False, active_obj_B = True,
#                                       print_ph_slices_A = True, print_ph_slices_B = False)
#     expressions = [
#         BinaryExpression(+1.0, 1.0, Term('L', 'aa', 'efmn'), Term('T', 'aaa', 'aefimn')),
#         BinaryExpression(+1.0, 1.0, Term('L', 'ab', 'efmn'), Term('T', 'aab', 'aefimn')),
#         BinaryExpression(+1.0, 1.0, Term('L', 'bb', 'efmn'), Term('T', 'abb', 'aefimn')),
#     ]
#
#     for expression in expressions:
#
#         expression.A.indices = change_term_to_projection(expression.A.indices, projection)
#         expression.B.indices = change_term_to_projection(expression.B.indices, projection)
#
#         g.generate(expression)
#
#     g.print_expression()
#
#     return
#
# def L2T3_b_vo(projection):
#
#     g = Generator(projection, 'b', 1, full_asym_weight=1.0, active_output_quantity=True, output_label='dL',
#                                       active_contract = True, active_obj_A = False, active_obj_B = True,
#                                       print_ph_slices_A = True, print_ph_slices_B = False)
#     expressions = [
#         BinaryExpression(+1.0, 1.0, Term('L', 'aa', 'efmn'), Term('T', 'aab', 'efAmnI')),
#         BinaryExpression(+1.0, 1.0, Term('L', 'ab', 'efmn'), Term('T', 'abb', 'efAmnI')),
#         BinaryExpression(+1.0, 1.0, Term('L', 'bb', 'efmn'), Term('T', 'bbb', 'efAmnI')),
#     ]
#
#     for expression in expressions:
#
#         expression.A.indices = change_term_to_projection(expression.A.indices, projection)
#         expression.B.indices = change_term_to_projection(expression.B.indices, projection)
#
#         g.generate(expression)
#
#     g.print_expression()
#
#     return


def L3T3_a_oo(projection):

    # oo
    g = Generator(projection, 'a', 1, full_asym_weight=1.0, active_output_quantity=False, output_label='X',
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

def L3T3_a_vv(projection):
    # vv
    g = Generator(projection, 'a', 1, full_asym_weight=1.0, active_output_quantity=True, output_label='dL',
                                      active_contract = True, active_obj_A = True, active_obj_B = True,
                                      print_ph_slices_A = False, print_ph_slices_B = False)
    expressions = [
        BinaryExpression(+1.0, 1.0, Term('L', 'aaa', 'Afgmno'), Term('T', 'aaa', 'efgmno')),
        BinaryExpression(+1.0, 1.0, Term('L', 'aab', 'Afgmno'), Term('T', 'aab', 'efgmno')),
        BinaryExpression(+1.0, 1.0, Term('L', 'abb', 'Afgmno'), Term('T', 'abb', 'efgmno')),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds LT-type active-space intermediates.")
    parser.add_argument('type',
                        help='Type of LT contraction. E.g, L2t3, l3t3, etc.')
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., a, b, aa, ab, bb.')
    parser.add_argument('projection',
                        help="String, for example 'AI', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)