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

    # The tricky part is dealing with essentially the moments of CCSDT on quadruples, i.e.,
    # < ijklabcd | H(3) | 0 > = < ijklabcd | H(2) + [H(2), T3] + 1/2 [[H(2), T3], T3] | 0 >
    #
    # The most expensive term of this expansion comes from the diagram in (H(2)*T3**2)_C
    # x1 = -1.0 * np.einsum("Dmfe,BCJm->BCDJef", H.aa.voov[Va, :, :, :], T.aa[Va, Va, Oa, :], optimize=True)
    # x1 -= np.transpose(x1, (2, 1, 0, 3, 4, 5)) + np.transpose(x1, (0, 2, 1, 3, 4, 5))
    # dT.aaaa.VVVVOOOO += (16.0 / 576.0) * (
    #         -0.5 * np.einsum('BCDJef,AfeIKL->ABCDIJKL',  x1[:, :, :, :, va, va], T.aaa[Va, va, va, Oa, Oa, Oa], optimize=True)
    #         + 1.0 * np.einsum('BCDJeF,FAeIKL->ABCDIJKL', x1[:, :, :, :, va, Va], T.aaa[Va, Va, va, Oa, Oa, Oa], optimize=True)
    #         - 0.5 * np.einsum('BCDJEF,FEAIKL->ABCDIJKL', x1[:, :, :, :, Va, Va], T.aaa[Va, Va, Va, Oa, Oa, Oa], optimize=True)
    # )

    # g = Generator("BCDJef", 'aaa', 0,
    #               active_contract=False,
    #               active_obj_A=False, active_obj_B=False,
    #               print_ph_slices_A=True, print_ph_slices_B=False)
    #
    # expressions_2 = [
    #     BinaryExpression(-1.0, 1.0, Term("H", "aa", "Dmfe", is_full=[False,True,False,False]),
    #                                 Term("T", "aa", "BCJm", is_full=[False,False,False,True]))    # (j/ikl)(a/bcd) = 16
    # ]
    #
    # for expression in expressions_2:
    #
    #
    #     expression.A.indices = change_term_to_projection(expression.A.indices, projection)
    #     expression.B.indices = change_term_to_projection(expression.B.indices, projection)
    #
    #     g.generate(expression)
    #
    # g.print_expression()


    g = Generator(projection, "aaaa", 0, active_obj_A=False, active_obj_B=False, print_vo_slices_A=True, print_vo_slices_B=False)

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