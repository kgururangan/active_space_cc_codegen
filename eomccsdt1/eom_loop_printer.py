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



def r3a_loop(projection):

    dims, act = get_dims_from_projection(projection, 'aaa')
    perms = get_antisymmetrizer_combinations(projection, 'aaa')

    print('subroutine update_r3a_{}(r3a, omega, &'.format(projection))
    print('                             H1A_oo_act, H1A_vv_act, H1A_oo_inact, H1A_vv_inact, &')
    print('                             shift, &')
    print('                             noa_act, nua_act, noa_inact, nua_inact)')
    print('')
    print('      integer, intent(in)  :: noa_act, nua_act, noa_inact, nua_inact')
    print('      real(8), intent(in)  :: H1A_oo_act(1:noa_act, 1:noa_act), &')
    print('                              H1A_vv_act(1:nua_act, 1:nua_act), &')
    print('                              H1A_oo_inact(1:noa_inact, 1:noa_inact), &')
    print('                              H1A_vv_inact(1:nua_inact, 1:nua_inact)')
    print('      real(8), intent(in)  :: shift, omega')
    print('')
    print('      real(8), intent(inout) :: r3a(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: r3a(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print('                        denom = H1A_oo_{}(i,i) + H1A_oo_{}(j,j) + H1A_oo_{}(k,k)&'.format(act[3], act[4], act[5]))
    print('                               -H1A_vv_{}(a,a) - H1A_vv_{}(b,b) - H1A_vv_{}(c,c)'.format(act[0], act[1], act[2]))
    print('')
    print('')
    print('                        r3a(a, b, c, i, j, k) = r3a(a, b, c, i, j, k) /(omega + denom + shift)')
    print('')
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_r3a_{}'.format(projection))


def r3b_loop(projection):

    dims, act = get_dims_from_projection(projection, 'aab')
    perms = get_antisymmetrizer_combinations(projection, 'aab')

    print('subroutine update_r3b_{}(r3b, omega, &'.format(projection))
    print('                             H1A_oo_act, H1A_vv_act, H1A_oo_inact, H1A_vv_inact, &')
    print('                             H1B_oo_act, H1B_vv_act, H1B_oo_inact, H1B_vv_inact, &')
    print('                             shift, &')
    print('                             noa_act, nua_act, noa_inact, nua_inact, &')
    print('                             nob_act, nub_act, nob_inact, nub_inact)')
    print('')
    print('      integer, intent(in)  :: noa_act, nua_act, noa_inact, nua_inact')
    print('      integer, intent(in)  :: nob_act, nub_act, nob_inact, nub_inact')
    print('      real(8), intent(in)  :: H1A_oo_act(1:noa_act, 1:noa_act), &')
    print('                              H1A_vv_act(1:nua_act, 1:nua_act), &')
    print('                              H1A_oo_inact(1:noa_inact, 1:noa_inact), &')
    print('                              H1A_vv_inact(1:nua_inact, 1:nua_inact), &')
    print('                              H1B_oo_act(1:nob_act, 1:nob_act), &')
    print('                              H1B_vv_act(1:nub_act, 1:nub_act), &')
    print('                              H1B_oo_inact(1:nob_inact, 1:nob_inact), &')
    print('                              H1B_vv_inact(1:nub_inact, 1:nub_inact)')
    print('      real(8), intent(in)  :: shift, omega')
    print('')
    print('      real(8), intent(inout) :: r3b(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: r3b(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print('                        denom = H1A_oo_{}(i,i) + H1A_oo_{}(j,j) + H1B_oo_{}(k,k)&'.format(act[3], act[4], act[5]))
    print('                               -H1A_vv_{}(a,a) - H1A_vv_{}(b,b) - H1B_vv_{}(c,c)'.format(act[0], act[1], act[2]))
    print('')
    print('')
    print('                        r3b(a, b, c, i, j, k) = r3b(a, b, c, i, j, k)/(omega + denom + shift)')
    print('')
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_r3b_{}'.format(projection))

def r3c_loop(projection):

    dims, act = get_dims_from_projection(projection, 'abb')
    perms = get_antisymmetrizer_combinations(projection, 'abb')

    print('subroutine update_r3c_{}(r3c, omega, &'.format(projection))
    print('                             H1A_oo_act, H1A_vv_act, H1A_oo_inact, H1A_vv_inact, &')
    print('                             H1B_oo_act, H1B_vv_act, H1B_oo_inact, H1B_vv_inact, &')
    print('                             shift, &')
    print('                             noa_act, nua_act, noa_inact, nua_inact, &')
    print('                             nob_act, nub_act, nob_inact, nub_inact)')
    print('')
    print('      integer, intent(in)  :: noa_act, nua_act, noa_inact, nua_inact')
    print('      integer, intent(in)  :: nob_act, nub_act, nob_inact, nub_inact')
    print('      real(8), intent(in)  :: H1A_oo_act(1:noa_act, 1:noa_act), &')
    print('                              H1A_vv_act(1:nua_act, 1:nua_act), &')
    print('                              H1A_oo_inact(1:noa_inact, 1:noa_inact), &')
    print('                              H1A_vv_inact(1:nua_inact, 1:nua_inact), &')
    print('                              H1B_oo_act(1:nob_act, 1:nob_act), &')
    print('                              H1B_vv_act(1:nub_act, 1:nub_act), &')
    print('                              H1B_oo_inact(1:nob_inact, 1:nob_inact), &')
    print('                              H1B_vv_inact(1:nub_inact, 1:nub_inact)')
    print('      real(8), intent(in)  :: shift, omega')
    print('')
    print('      real(8), intent(inout) :: r3c(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: r3c(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print(
        '                        denom = H1A_oo_{}(i,i) + H1B_oo_{}(j,j) + H1B_oo_{}(k,k)&'.format(act[3], act[4], act[5]))
    print(
        '                               -H1A_vv_{}(a,a) - H1B_vv_{}(b,b) - H1B_vv_{}(c,c)'.format(act[0], act[1], act[2]))
    print('')
    print('')
    print('                        r3c(a, b, c, i, j, k) = r3c(a, b, c, i, j, k)/(omega + denom + shift)')
    print('')
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_r3c_{}'.format(projection))

def r3d_loop(projection):

    dims, act = get_dims_from_projection(projection, 'bbb')
    perms = get_antisymmetrizer_combinations(projection, 'bbb')

    print('subroutine update_r3d_{}(r3d, omega, &'.format(projection))
    print('                             H1B_oo_act, H1B_vv_act, H1B_oo_inact, H1B_vv_inact, &')
    print('                             shift, &')
    print('                             nob_act, nub_act, nob_inact, nub_inact)')
    print('')
    print('      integer, intent(in)  :: nob_act, nub_act, nob_inact, nub_inact')
    print('      real(8), intent(in)  :: H1B_oo_act(1:nob_act, 1:nob_act), &')
    print('                              H1B_vv_act(1:nub_act, 1:nub_act), &')
    print('                              H1B_oo_inact(1:nob_inact, 1:nob_inact), &')
    print('                              H1B_vv_inact(1:nub_inact, 1:nub_inact)')
    print('      real(8), intent(in)  :: shift, omega')
    print('')
    print('      real(8), intent(inout) :: r3d(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('      !f2py intent(in, out)  :: r3d(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
          .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5]))
    print('')
    print('      integer :: i, j, k, a, b, c')
    print('      real(8) :: denom')
    print('')
    print('      do i = 1 , {}'.format(dims[3]))
    print('         do j = 1 , {}'.format(dims[4]))
    print('            do k = 1 , {}'.format(dims[5]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('')
    print('                        denom = H1B_oo_{}(i,i) + H1B_oo_{}(j,j) + H1B_oo_{}(k,k)&'.format(act[3], act[4],
                                                                                                  act[5]))
    print('                               -H1B_vv_{}(a,a) - H1B_vv_{}(b,b) - H1B_vv_{}(c,c)'.format(act[0], act[1],
                                                                                                 act[2]))
    print('')
    print('')
    print('                        r3d(a, b, c, i, j, k) = r3d(a, b, c, i, j, k)/(omega + denom + shift)')
    print('')
    print('')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('')
    print('end subroutine update_r3d_{}'.format(projection))


def in_module_update_aaa(numeric_label):

    # numeric_label = ''
    # for i in projection:
    #     if i.upper() == i:
    #         numeric_label.join('1')
    #     else:
    #         numeric_label.join('0')

    projection = ''
    for i, c in enumerate(numeric_label):
        if i < 3:
            if c == '1':
                projection += 'V'
            else:
                projection += 'v'
        else:
            if c == '1':
                projection += 'O'
            else:
                projection += 'o'

    print('')
    print('def update(R, omega, H, system):')
    print('')
    print('    oa, Oa, va, Va, ob, Ob, vb, Vb = get_active_slices(system)')
    print('')
    print('    R.aaa.{} = eomcc_active_loops.eomcc_active_loops.update_r3a_{}('.format(projection, numeric_label))
    print('        R.aaa.{},'.format(projection))
    print('        omega,')
    print('        H.a.oo[Oa, Oa],')
    print('        H.a.vv[Va, Va],')
    print('        H.a.oo[oa, oa],')
    print('        H.a.vv[va, va],')
    print('        0.0,')
    print('    )')

    print('    return R')


def in_module_update_aab(numeric_label):

    # numeric_label = ''
    # for i in projection:
    #     if i.upper() == i:
    #         numeric_label.join('1')
    #     else:
    #         numeric_label.join('0')

    projection = ''
    for i, c in enumerate(numeric_label):
        if i < 3:
            if c == '1':
                projection += 'V'
            else:
                projection += 'v'
        else:
            if c == '1':
                projection += 'O'
            else:
                projection += 'o'

    print('')
    print('def update(R, omega, H, system):')
    print('')
    print('    oa, Oa, va, Va, ob, Ob, vb, Vb = get_active_slices(system)')
    print('')
    print('    R.aab.{} = eomcc_active_loops.eomcc_active_loops.update_r3b_{}('.format(projection, numeric_label))
    print('        R.aab.{},'.format(projection))
    print('        omega,')
    print('        H.a.oo[Oa, Oa],')
    print('        H.a.vv[Va, Va],')
    print('        H.a.oo[oa, oa],')
    print('        H.a.vv[va, va],')
    print('        H.b.oo[Ob, Ob],')
    print('        H.b.vv[Vb, Vb],')
    print('        H.b.oo[ob, ob],')
    print('        H.b.vv[vb, vb],')
    print('        0.0,')
    print('    )')

    print('    return R')

def in_module_update_abb(numeric_label):

    # numeric_label = ''
    # for i in projection:
    #     if i.upper() == i:
    #         numeric_label.join('1')
    #     else:
    #         numeric_label.join('0')

    projection = ''
    for i, c in enumerate(numeric_label):
        if i < 3:
            if c == '1':
                projection += 'V'
            else:
                projection += 'v'
        else:
            if c == '1':
                projection += 'O'
            else:
                projection += 'o'

    print('')
    print('def update(R, omega, H, system):')
    print('')
    print('    oa, Oa, va, Va, ob, Ob, vb, Vb = get_active_slices(system)')
    print('')
    print('    R.abb.{} = eomcc_active_loops.eomcc_active_loops.update_r3c_{}('.format(projection, numeric_label))
    print('        R.abb.{},'.format(projection))
    print('        omega,')
    print('        H.a.oo[Oa, Oa],')
    print('        H.a.vv[Va, Va],')
    print('        H.a.oo[oa, oa],')
    print('        H.a.vv[va, va],')
    print('        H.b.oo[Ob, Ob],')
    print('        H.b.vv[Vb, Vb],')
    print('        H.b.oo[ob, ob],')
    print('        H.b.vv[vb, vb],')
    print('        0.0,')
    print('    )')

    print('    return R')

def in_module_update_bbb(numeric_label):

    # numeric_label = ''
    # for i in projection:
    #     if i.upper() == i:
    #         numeric_label.join('1')
    #     else:
    #         numeric_label.join('0')

    projection = ''
    for i, c in enumerate(numeric_label):
        if i < 3:
            if c == '1':
                projection += 'V'
            else:
                projection += 'v'
        else:
            if c == '1':
                projection += 'O'
            else:
                projection += 'o'

    print('')
    print('def update(R, omega, H, system):')
    print('')
    print('    oa, Oa, va, Va, ob, Ob, vb, Vb = get_active_slices(system)')
    print('')
    print('    R.bbb.{} = eomcc_active_loops.eomcc_active_loops.update_r3d_{}('.format(projection, numeric_label))
    print('        R.bbb.{},'.format(projection))
    print('        omega,')
    print('        H.b.oo[Ob, Ob],')
    print('        H.b.vv[Vb, Vb],')
    print('        H.b.oo[ob, ob],')
    print('        H.b.vv[vb, vb],')
    print('        0.0,')
    print('    )')

    print('    return R')

def main(args):

    if args.spincase == 'aaa':
        r3a_loop(args.projection)
        in_module_update_aaa(args.projection)

    if args.spincase == 'aab':
        r3b_loop(args.projection)
        in_module_update_aab(args.projection)

    if args.spincase == 'abb':
        r3c_loop(args.projection)
        in_module_update_abb(args.projection)

    if args.spincase == 'bbb':
        r3d_loop(args.projection)
        in_module_update_bbb(args.projection)

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Builds EOMCCSDt R3 update loop for different spincases and projections.")
    parser.add_argument('spincase',
                        help='String specifying spincase, e.g., aaa, aab, abb, or bbb')
    parser.add_argument('projection',
                        help="String, for example '110111', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)