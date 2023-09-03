from actgen.term import Term, BinaryExpression
from actgen.generator import Generator

import argparse

# [TODO]:
# Additional functionality must be added to support active-space contractions between an intermediate
# and an active cluster operator, e.g., I_vvovvv * t3 -> abcdijkl, where the intermediate I is also
# constructed using active-space operators. We cannot assume that all required active-space slices
# of I will be constructed before the contraction because we do not generally know the indices on I
# beforehand. They will need to be generated together somehow...
# One option, particularly for CCSDtq, is to construct the (H(2) * T3)_C 3-body intermediates beforehand,
# storing the smallest-sized objet required for all contractions. For example, in the ABcdijKL projection,
# it looks like the expensive I_vvvovv intermediate only requires (Nu, nu, nu, no, nu, nu), where no/nu
# span the entire occupied/unoccupied space. Thus, this is a Nu * no * nu**4 object; it's not small, but perhaps
# on the order of T3 storage. Maybe this is acceptable, and it would allow us to use slicing of a full array
# for the next (I * T3)_C contraction, which projects onto the quadruples active-space projection.
#
# In reality, the CCSDTQ equations should be formualted as follows
# 1. update t1
# 2. build ccs hbar
# 3. update t2
# 4. build ccsd hbar
# 5. update t3
# 6. build ccsdt hbar
# 7. build 3-body intermediates for ccsdt moments
# 8. update t4,
# and the task of active-spacifying the CCSDT moments is about performing step 7 in an efficient manner

def main(args):

    projection = args.projection

    # The tricky part is dealing with essentially the moments of CCSDT on quadruples, i.e.,
    # < ijklabcd | H(3) | 0 > = < ijklabcd | H(2) + [H(2), T3] + 1/2 [[H(2), T3], T3] | 0 >
    #
    # The most expensive term of this expansion comes from the diagram in (H(2)*T3**2)_C
    # E.g., for the projection ABCDIJKL
    # x1 = -1.0 * np.einsum("Dmfe,BCJm->BCDJef", H.aa.voov[Va, :, :, :], T.aa[Va, Va, Oa, :], optimize=True)
    # x1 -= np.transpose(x1, (2, 1, 0, 3, 4, 5)) + np.transpose(x1, (0, 2, 1, 3, 4, 5))
    # dT.aaaa.VVVVOOOO += (16.0 / 576.0) * (
    #         -0.5 * np.einsum('BCDJef,AfeIKL->ABCDIJKL',  x1[:, :, :, :, va, va], T.aaa[Va, va, va, Oa, Oa, Oa], optimize=True)
    #         + 1.0 * np.einsum('BCDJeF,FAeIKL->ABCDIJKL', x1[:, :, :, :, va, Va], T.aaa[Va, Va, va, Oa, Oa, Oa], optimize=True)
    #         - 0.5 * np.einsum('BCDJEF,FEAIKL->ABCDIJKL', x1[:, :, :, :, Va, Va], T.aaa[Va, Va, Va, Oa, Oa, Oa], optimize=True)
    # )

    # for intproj in ["bcdjef", "Acdjef", "bcdLef", "AcdLef"]:
    #
    #     g = Generator(intproj, "aaa", 0,
    #                   active_contract=False,
    #                   active_obj_A=False, active_obj_B=False,
    #                   print_ph_slices_A=True, print_ph_slices_B=False)
    #
    #     expressions_2 = [
    #         BinaryExpression(-1.0, 1.0, Term("H", "aa", "Dmfe", is_full=[False,True,False,False]),
    #                                     Term("T", "aa", "BCJm", is_full=[False,False,False,True]))    # (j/ikl)(a/bcd) = 16
    #     ]
    #
    #     g.kernel(expressions_2, projection)

    g = Generator(projection, "aaaa", 0,
                  active_obj_A=False, active_obj_B=False,
                  print_vo_slices_A=True, print_vo_slices_B=False)

    expressions_2 = [
        BinaryExpression(1.0, 1.0, Term("H", "aa", "CDKe"), Term("T", "aaa", "ABeIJL")),
        BinaryExpression(-1.0, 1.0, Term("H", "aa", "CmKL"), Term("T", "aaa", "ABDIJm")),
        BinaryExpression(1.0, 1.0, Term("I", "aaa", "BmnJKL"), Term("T", "aaa", "ACDImn")),
        BinaryExpression(1.0, 1.0, Term("I", "aaa", "BCDJef"), Term("T", "aaa", "AefIKL")), # this is the expensive one...
        BinaryExpression(1.0, 1.0, Term("I", "aaa", "CDmKLe"), Term("T", "aaa", "ABeIJm")),
        BinaryExpression(1.0, 1.0, Term("I", "aab", "CDmKLe"), Term("T", "aab", "ABeIJm")),
    ]

    g.kernel(expressions_2, projection, print_term=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds moments of CCSDT equation projected on quadruples for the aaaa spincase.")
    parser.add_argument('projection', type=str, help="String, for example 'ABcdIJKl', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)