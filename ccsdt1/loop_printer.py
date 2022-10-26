import argparse
from itertools import permutations
from actgen.utilities import signPermutation

def get_dims_from_projection(projection, spincase):
    dims = []
    act_or_inact = []
    double_spin_string = spincase * 2
    order = len(spincase)

    for i, p in enumerate(projection):
        if i < order:
            if p == '1':
                if double_spin_string[i] == 'a':
                    dims.append('nua_act')
                    act_or_inact.append('act')
                elif double_spin_string[i] == 'b':
                    dims.append('nub_act')
                    act_or_inact.append('act')
            elif p == '0':
                if double_spin_string[i] == 'a':
                    dims.append('nua_inact')
                    act_or_inact.append('inact')
                elif double_spin_string[i] == 'b':
                    dims.append('nub_inact')
                    act_or_inact.append('inact')
        else:
            if p == '1':
                if double_spin_string[i] == 'a':
                    dims.append('noa_act')
                    act_or_inact.append('act')
                elif double_spin_string[i] == 'b':
                    dims.append('nob_act')
                    act_or_inact.append('act')
            elif p == '0':
                if double_spin_string[i] == 'a':
                    dims.append('noa_inact')
                    act_or_inact.append('inact')
                elif double_spin_string[i] == 'b':
                    dims.append('nob_inact')
                    act_or_inact.append('inact')

    return dims, act_or_inact

def get_antisymmetrizer_combinations(projection, spincase):
    order = len(spincase)
    double_spin_string = spincase * 2

    if order == 3:
        idx = ['a', 'b', 'c', 'i', 'j', 'k']

    particles = projection[:order]
    holes = projection[order:]

    active_holes_alpha = [i for i, p in enumerate(holes) if p == '1' and double_spin_string[i] == 'a']
    inactive_holes_alpha = [i for i, p in enumerate(holes) if p == '0' and double_spin_string[i] == 'a']
    active_holes_beta = [i for i, p in enumerate(holes) if p == '1' and double_spin_string[i] == 'b']
    inactive_holes_beta = [i for i, p in enumerate(holes) if p == '0' and double_spin_string[i] == 'b']

    active_particles_alpha = [i for i, p in enumerate(particles) if p == '1' and double_spin_string[i] == 'a']
    inactive_particles_alpha = [i for i, p in enumerate(particles) if p == '0' and double_spin_string[i] == 'a']
    active_particles_beta = [i for i, p in enumerate(particles) if p == '1' and double_spin_string[i] == 'b']
    inactive_particles_beta = [i for i, p in enumerate(particles) if p == '0' and double_spin_string[i] == 'b']

    # get the starting indices
    # start_idx = [None] * 6
    # for

    # print(active_holes_alpha)
    # print(inactive_holes_alpha)
    # print(active_holes_beta)
    # print(inactive_holes_beta)
    # print(active_particles_alpha)
    # print(inactive_particles_alpha)
    # print(active_particles_beta)
    # print(inactive_particles_beta)

    perms = {'indices' : [], 'sign' : []}

    for c1 in list(permutations(active_particles_alpha, len(active_particles_alpha))):
        for c2 in list(permutations(inactive_particles_alpha, len(inactive_particles_alpha))):
            for c3 in list(permutations(active_particles_beta, len(active_particles_beta))):
                for c4 in permutations(inactive_particles_beta, len(inactive_particles_beta)):
                    for c5 in permutations(active_holes_alpha, len(active_holes_alpha)):
                        for c6 in permutations(inactive_holes_alpha, len(inactive_holes_alpha)):
                            for c7 in permutations(active_holes_beta, len(active_holes_beta)):
                                for c8 in permutations(inactive_holes_beta, len(inactive_holes_beta)):

                                    sign = (
                                            signPermutation(c1) * signPermutation(c2) * signPermutation(c3) * signPermutation(c4)
                                            * signPermutation(c5) * signPermutation(c6) * signPermutation(c7) * signPermutation(c8)
                                    )
                                    particles = [idx[i] for i in c1] + [idx[i] for i in c2] + [idx[i] for i in c3] + [idx[i] for i in c4]
                                    holes = [idx[order + i] for i in c6] + [idx[order + i] for i in c5] + [idx[order + i] for i in c8] + [idx[order + i] for i in c7]
                                    indices = particles + holes

                                    perms['indices'].append(indices)
                                    perms['sign'].append(sign)
    return perms



def t3a_loop(projection):

    dims, act = get_dims_from_projection(projection, 'aaa')
    perms = get_antisymmetrizer_combinations(projection, 'aaa')

    print('subroutine update_t3a_{}(t3a, resid, X3A, &'.format(projection))
    print('                             fA_oo_act, fA_vv_act, fA_oo_inact, fA_vv_inact, &')
    print('                             shift, &')
    print('                             noa_act, nua_act, noa_inact, nua_inact)')
    print('')
    print('      integer, intent(in)  :: noa_act, nua_act, noa_inact, nua_inact')
    print('      real(8), intent(in)  :: fA_oo_act(1:noa_act, 1:noa_act), &')
    print('                              fA_vv_act(1:nua_act, 1:nua_act), &')
    print('                              fA_oo_inact(1:noa_inact, 1:noa_inact), &')
    print('                              fA_vv_inact(1:nua_inact, 1:nua_inact)')
    print('      real(8), intent(in)  :: X3A(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t3a(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: t3a(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom, val')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print('                        denom = fA_oo_{}(i,i) + fA_oo_{}(j,j) + fA_oo_{}(k,k)&'.format(act[3], act[4], act[5]))
    print('                               -fA_vv_{}(a,a) - fA_vv_{}(b,b) - fA_vv_{}(c,c)'.format(act[0], act[1], act[2]))
    print('')
    print('                        val = X3A(a, b, c, i, j, k)/(denom - shift)')
    print('')
    print('                        t3a(a, b, c, i, j, k) = t3a(a, b, c, i, j, k) + val')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t3a({}, {}, {}, {}, {}, {}) = {}t3a(a, b, c, i, j, k)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_t3a_{}'.format(projection))


def t3b_loop(projection):

    dims, act = get_dims_from_projection(projection, 'aab')
    perms = get_antisymmetrizer_combinations(projection, 'aab')

    print('subroutine update_t3b_{}(t3b, resid, X3B, &'.format(projection))
    print('                             fA_oo_act, fA_vv_act, fA_oo_inact, fA_vv_inact, &')
    print('                             fB_oo_act, fB_vv_act, fB_oo_inact, fB_vv_inact, &')
    print('                             shift, &')
    print('                             noa_act, nua_act, noa_inact, nua_inact, &')
    print('                             nob_act, nub_act, nob_inact, nub_inact)')
    print('')
    print('      integer, intent(in)  :: noa_act, nua_act, noa_inact, nua_inact')
    print('      integer, intent(in)  :: nob_act, nub_act, nob_inact, nub_inact')
    print('      real(8), intent(in)  :: fA_oo_act(1:noa_act, 1:noa_act), &')
    print('                              fA_vv_act(1:nua_act, 1:nua_act), &')
    print('                              fA_oo_inact(1:noa_inact, 1:noa_inact), &')
    print('                              fA_vv_inact(1:nua_inact, 1:nua_inact), &')
    print('                              fB_oo_act(1:nob_act, 1:nob_act), &')
    print('                              fB_vv_act(1:nub_act, 1:nub_act), &')
    print('                              fB_oo_inact(1:nob_inact, 1:nob_inact), &')
    print('                              fB_vv_inact(1:nub_inact, 1:nub_inact)')
    print('      real(8), intent(in)  :: X3B(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t3b(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: t3b(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom, val')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print('                        denom = fA_oo_{}(i,i) + fA_oo_{}(j,j) + fB_oo_{}(k,k)&'.format(act[3], act[4], act[5]))
    print('                               -fA_vv_{}(a,a) - fA_vv_{}(b,b) - fB_vv_{}(c,c)'.format(act[0], act[1], act[2]))
    print('')
    print('                        val = X3B(a, b, c, i, j, k)/(denom - shift)')
    print('')
    print('                        t3b(a, b, c, i, j, k) = t3b(a, b, c, i, j, k) + val')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t3b({}, {}, {}, {}, {}, {}) = {}t3b(a, b, c, i, j, k)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_t3b_{}'.format(projection))

def t3c_loop(projection):

    dims, act = get_dims_from_projection(projection, 'abb')
    perms = get_antisymmetrizer_combinations(projection, 'abb')

    print('subroutine update_t3c_{}(t3c, resid, X3C, &'.format(projection))
    print('                             fA_oo_act, fA_vv_act, fA_oo_inact, fA_vv_inact, &')
    print('                             fB_oo_act, fB_vv_act, fB_oo_inact, fB_vv_inact, &')
    print('                             shift, &')
    print('                             noa_act, nua_act, noa_inact, nua_inact, &')
    print('                             nob_act, nub_act, nob_inact, nub_inact)')
    print('')
    print('      integer, intent(in)  :: noa_act, nua_act, noa_inact, nua_inact')
    print('      integer, intent(in)  :: nob_act, nub_act, nob_inact, nub_inact')
    print('      real(8), intent(in)  :: fA_oo_act(1:noa_act, 1:noa_act), &')
    print('                              fA_vv_act(1:nua_act, 1:nua_act), &')
    print('                              fA_oo_inact(1:noa_inact, 1:noa_inact), &')
    print('                              fA_vv_inact(1:nua_inact, 1:nua_inact), &')
    print('                              fB_oo_act(1:nob_act, 1:nob_act), &')
    print('                              fB_vv_act(1:nub_act, 1:nub_act), &')
    print('                              fB_oo_inact(1:nob_inact, 1:nob_inact), &')
    print('                              fB_vv_inact(1:nub_inact, 1:nub_inact)')
    print('      real(8), intent(in)  :: X3C(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t3c(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: t3c(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom, val')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print(
        '                        denom = fA_oo_{}(i,i) + fB_oo_{}(j,j) + fB_oo_{}(k,k)&'.format(act[3], act[4], act[5]))
    print(
        '                               -fA_vv_{}(a,a) - fB_vv_{}(b,b) - fB_vv_{}(c,c)'.format(act[0], act[1], act[2]))
    print('')
    print('                        val = X3C(a, b, c, i, j, k)/(denom - shift)')
    print('')
    print('                        t3c(a, b, c, i, j, k) = t3c(a, b, c, i, j, k) + val')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t3c({}, {}, {}, {}, {}, {}) = {}t3c(a, b, c, i, j, k)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_t3c_{}'.format(projection))

def t3d_loop(projection):

    dims, act = get_dims_from_projection(projection, 'bbb')
    perms = get_antisymmetrizer_combinations(projection, 'bbb')

    print('subroutine update_t3d_{}(t3d, resid, X3D, &'.format(projection))
    print('                             fB_oo_act, fB_vv_act, fB_oo_inact, fB_vv_inact, &')
    print('                             shift, &')
    print('                             nob_act, nub_act, nob_inact, nub_inact)')
    print('')
    print('      integer, intent(in)  :: nob_act, nub_act, nob_inact, nub_inact')
    print('      real(8), intent(in)  :: fB_oo_act(1:nob_act, 1:nob_act), &')
    print('                              fB_vv_act(1:nub_act, 1:nub_act), &')
    print('                              fB_oo_inact(1:nob_inact, 1:nob_inact), &')
    print('                              fB_vv_inact(1:nub_inact, 1:nub_inact)')
    print('      real(8), intent(in)  :: X3D(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t3d(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: t3d(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom, val')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print('                        denom = fB_oo_{}(i,i) + fB_oo_{}(j,j) + fB_oo_{}(k,k)&'.format(act[3], act[4],
                                                                                                  act[5]))
    print('                               -fB_vv_{}(a,a) - fB_vv_{}(b,b) - fB_vv_{}(c,c)'.format(act[0], act[1],
                                                                                                 act[2]))
    print('')
    print('                        val = X3D(a, b, c, i, j, k)/(denom - shift)')
    print('')
    print('                        t3d(a, b, c, i, j, k) = t3d(a, b, c, i, j, k) + val')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t3d({}, {}, {}, {}, {}, {}) = {}t3d(a, b, c, i, j, k)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], sign_string))
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_t3d_{}'.format(projection))


def main(args):

    if args.spincase == 'aaa':
        t3a_loop(args.projection)

    if args.spincase == 'aab':
        t3b_loop(args.projection)

    if args.spincase == 'abb':
        t3c_loop(args.projection)

    if args.spincase == 'bbb':
        t3d_loop(args.projection)

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Builds CCSDt T3 update loop for different spincases and projections.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., aaa, aab, abb, or bbb')
    parser.add_argument('projection',
                        help="String, for example '110111', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)
