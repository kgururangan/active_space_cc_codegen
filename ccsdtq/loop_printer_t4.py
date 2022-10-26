import argparse
from itertools import permutations
from actgen.utilities import signPermutation

def get_dims_from_projection(projection, spincase, use_full=False):
    dims = []
    act_or_inact = []
    double_spin_string = spincase * 2
    order = len(spincase)

    if use_full:
        for i, p in enumerate(projection):
            if i < order:
                if double_spin_string[i] == 'a':
                    dims.append('nua')
                elif double_spin_string[i] == 'b':
                    dims.append('nub')
            else:
                if double_spin_string[i] == 'a':
                    dims.append('noa')
                elif double_spin_string[i] == 'b':
                    dims.append('nob')

    else:
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
    if order == 4:
        idx = ['a', 'b', 'c', 'd', 'i', 'j', 'k', 'l']

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



def t4a_loop(projection='11111111'):

    dims, act = get_dims_from_projection(projection, 'aaaa', use_full=True)
    perms = get_antisymmetrizer_combinations(projection, 'aaaa')

    print('subroutine update_t4a(t4a, resid, X4A, &')
    print('                             fA_oo, fA_vv, &')
    print('                             shift, &')
    print('                             noa, nua)')
    print('')
    print('      integer, intent(in)  :: noa, nua')
    print('      real(8), intent(in)  :: fA_oo(1:noa, 1:noa), &')
    print('                              fA_vv(1:nua, 1:nua)')
    print('      real(8), intent(in)  :: X4A(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t4a(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      !f2py intent(in, out)  :: t4a(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('')
    print('      integer :: i, j, k, l, a, b, c, d')
    print('      real(8) :: denom, val')
    print('')
    print('   do i = 1 , {}'.format(dims[4]))
    print('      do j = 1 , {}'.format(dims[5]))
    print('         do k = 1 , {}'.format(dims[6]))
    print('            do l = 1 , {}'.format(dims[7]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('                        do d = 1 , {}'.format(dims[3]))
    print('')
    print('                        denom = fA_oo(i,i) + fA_oo(j,j) + fA_oo(k,k) + fA_oo(l,l)&')
    print('                               -fA_vv(a,a) - fA_vv(b,b) - fA_vv(c,c) - fA_vv(d,d)')
    print('')
    print('                        val = &')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = '+'
        print('                        {}X4A({}, {}, {}, {}, {}, {}, {}, {})&'
              .format(sign_string, idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7]))
    print('')
    print('                        t4a(a, b, c, d, i, j, k, l) = t4a(a, b, c, d, i, j, k, l) + val/(denom-shift)')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t4a({}, {}, {}, {}, {}, {}, {}, {}) = {}t4a(a, b, c, d, i, j, k, l)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    print('                        end do')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('   end do')
    print('')
    print('end subroutine update_t4a')

def t4b_loop(projection='11111111'):

    dims, act = get_dims_from_projection(projection, 'aaab', use_full=True)
    perms = get_antisymmetrizer_combinations(projection, 'aaab')

    print('subroutine update_t4b(t4b, resid, X4B, &')
    print('                             fA_oo, fA_vv, fB_oo, fB_vv, &')
    print('                             shift, &')
    print('                             noa, nua, nob, nub)')
    print('')
    print('      integer, intent(in)  :: noa, nua, nob, nub')
    print('      real(8), intent(in)  :: fA_oo(1:noa, 1:noa), &')
    print('                              fB_oo(1:nob, 1:nob), &')
    print('                              fA_vv(1:nua, 1:nua), &')
    print('                              fB_vv(1:nub, 1:nub)')
    print('      real(8), intent(in)  :: X4B(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t4b(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      !f2py intent(in, out)  :: t4b(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('')
    print('      integer :: i, j, k, l, a, b, c, d')
    print('      real(8) :: denom, val')
    print('')
    print('   do i = 1 , {}'.format(dims[4]))
    print('      do j = 1 , {}'.format(dims[5]))
    print('         do k = 1 , {}'.format(dims[6]))
    print('            do l = 1 , {}'.format(dims[7]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('                        do d = 1 , {}'.format(dims[3]))
    print('')
    print('                        denom = fA_oo(i,i) + fA_oo(j,j) + fA_oo(k,k) + fB_oo(l,l)&')
    print('                               -fA_vv(a,a) - fA_vv(b,b) - fA_vv(c,c) - fB_vv(d,d)')
    print('')
    print('                        val = &')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = '+'
        print('                        {}X4B({}, {}, {}, {}, {}, {}, {}, {})&'
              .format(sign_string, idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7]))
    print('')
    print('                        t4b(a, b, c, d, i, j, k, l) = t4b(a, b, c, d, i, j, k, l) + val/(denom-shift)')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t4b({}, {}, {}, {}, {}, {}, {}, {}) = {}t4b(a, b, c, d, i, j, k, l)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    print('                        end do')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('   end do')
    print('')
    print('end subroutine update_t4b')

def t4c_loop(projection='11111111'):

    dims, act = get_dims_from_projection(projection, 'aabb', use_full=True)
    perms = get_antisymmetrizer_combinations(projection, 'aabb')

    print('subroutine update_t4c(t4c, resid, X4C, &')
    print('                             fA_oo, fA_vv, fB_oo, fB_vv, &')
    print('                             shift, &')
    print('                             noa, nua, nob, nub)')
    print('')
    print('      integer, intent(in)  :: noa, nua, nob, nub')
    print('      real(8), intent(in)  :: fA_oo(1:noa, 1:noa), &')
    print('                              fB_oo(1:nob, 1:nob), &')
    print('                              fA_vv(1:nua, 1:nua), &')
    print('                              fB_vv(1:nub, 1:nub)')
    print('      real(8), intent(in)  :: X4C(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t4c(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      !f2py intent(in, out)  :: t4c(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('')
    print('      integer :: i, j, k, l, a, b, c, d')
    print('      real(8) :: denom, val')
    print('')
    print('   do i = 1 , {}'.format(dims[4]))
    print('      do j = 1 , {}'.format(dims[5]))
    print('         do k = 1 , {}'.format(dims[6]))
    print('            do l = 1 , {}'.format(dims[7]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('                        do d = 1 , {}'.format(dims[3]))
    print('')
    print('                        denom = fA_oo(i,i) + fA_oo(j,j) + fB_oo(k,k) + fB_oo(l,l)&')
    print('                               -fA_vv(a,a) - fA_vv(b,b) - fB_vv(c,c) - fB_vv(d,d)')
    print('')
    print('                        val = &')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = '+'
        print('                        {}X4C({}, {}, {}, {}, {}, {}, {}, {})&'
              .format(sign_string, idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7]))
    print('')
    print('                        t4c(a, b, c, d, i, j, k, l) = t4c(a, b, c, d, i, j, k, l) + val/(denom-shift)')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = '+'
        print('                        t4c({}, {}, {}, {}, {}, {}, {}, {}) = {}t4c(a, b, c, d, i, j, k, l)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    print('                        end do')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('   end do')
    print('')
    print('end subroutine update_t4c')

def t4d_loop(projection='11111111'):

    dims, act = get_dims_from_projection(projection, 'abbb', use_full=True)
    perms = get_antisymmetrizer_combinations(projection, 'abbb')

    print('subroutine update_t4d(t4d, resid, X4D, &')
    print('                             fA_oo, fA_vv, fB_oo, fB_vv, &')
    print('                             shift, &')
    print('                             noa, nua, nob, nub)')
    print('')
    print('      integer, intent(in)  :: noa, nua, nob, nub')
    print('      real(8), intent(in)  :: fA_oo(1:noa, 1:noa), &')
    print('                              fB_oo(1:nob, 1:nob), &')
    print('                              fA_vv(1:nua, 1:nua), &')
    print('                              fB_vv(1:nub, 1:nub)')
    print('      real(8), intent(in)  :: X4D(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t4d(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      !f2py intent(in, out)  :: t4d(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('')
    print('      integer :: i, j, k, l, a, b, c, d')
    print('      real(8) :: denom, val')
    print('')
    print('   do i = 1 , {}'.format(dims[4]))
    print('      do j = 1 , {}'.format(dims[5]))
    print('         do k = 1 , {}'.format(dims[6]))
    print('            do l = 1 , {}'.format(dims[7]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('                        do d = 1 , {}'.format(dims[3]))
    print('')
    print('                        denom = fA_oo(i,i) + fB_oo(j,j) + fB_oo(k,k) + fB_oo(l,l)&')
    print('                               -fA_vv(a,a) - fB_vv(b,b) - fB_vv(c,c) - fB_vv(d,d)')
    print('')
    print('                        val = &')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = '+'
        print('                        {}X4D({}, {}, {}, {}, {}, {}, {}, {})&'
              .format(sign_string, idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7]))
    print('')
    print('                        t4d(a, b, c, d, i, j, k, l) = t4d(a, b, c, d, i, j, k, l) + val/(denom-shift)')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t4d({}, {}, {}, {}, {}, {}, {}, {}) = {}t4d(a, b, c, d, i, j, k, l)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    print('                        end do')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('   end do')
    print('')
    print('end subroutine update_t4d')

def main(args):

    if args.spincase == 'aaaa':
        t4a_loop()
    if args.spincase == 'aaab':
        t4b_loop()
    if args.spincase == 'aabb':
        t4c_loop()
    if args.spincase == 'abbb':
        t4d_loop()
    if args.spincase == 'bbbb':
        t4e_loop()

def t4e_loop(projection='11111111'):

    dims, act = get_dims_from_projection(projection, 'bbbb', use_full=True)
    perms = get_antisymmetrizer_combinations(projection, 'bbbb')

    print('subroutine update_t4e(t4e, resid, X4E, &')
    print('                             fB_oo, fB_vv, &')
    print('                             shift, &')
    print('                             nob, nub)')
    print('')
    print('      integer, intent(in)  :: nob, nub')
    print('      real(8), intent(in)  :: fB_oo(1:nob, 1:nob), &')
    print('                              fB_vv(1:nub, 1:nub)')
    print('      real(8), intent(in)  :: X4E(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(in)  :: shift')
    print('')
    print('      real(8), intent(inout) :: t4e(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      !f2py intent(in, out)  :: t4e(0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1, 0:{}-1)'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('      real(8), intent(out)   :: resid(1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{}, 1:{})'
                                                        .format(dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6], dims[7]))
    print('')
    print('      integer :: i, j, k, l, a, b, c, d')
    print('      real(8) :: denom, val')
    print('')
    print('   do i = 1 , {}'.format(dims[4]))
    print('      do j = 1 , {}'.format(dims[5]))
    print('         do k = 1 , {}'.format(dims[6]))
    print('            do l = 1 , {}'.format(dims[7]))
    print('               do a = 1 , {}'.format(dims[0]))
    print('                  do b = 1 , {}'.format(dims[1]))
    print('                     do c = 1 , {}'.format(dims[2]))
    print('                        do d = 1 , {}'.format(dims[3]))
    print('')
    print('                        denom = fB_oo(i,i) + fB_oo(j,j) + fB_oo(k,k) + fB_oo(l,l)&')
    print('                               -fB_vv(a,a) - fB_vv(b,b) - fB_vv(c,c) - fB_vv(d,d)')
    print('')
    print('                        val = &')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = '+'
        print('                        {}X4E({}, {}, {}, {}, {}, {}, {}, {})&'
              .format(sign_string, idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7]))
    print('')
    print('                        t4e(a, b, c, d, i, j, k, l) = t4e(a, b, c, d, i, j, k, l) + val/(denom-shift)')
    for i in range(1, len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        t4e({}, {}, {}, {}, {}, {}, {}, {}) = {}t4e(a, b, c, d, i, j, k, l)'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    for i in range(len(perms['indices'])):
        idx = perms['indices'][i]
        if perms['sign'][i] == -1.0:
            sign_string = '-1.0 * '
        else:
            sign_string = ''
        print('                        resid({}, {}, {}, {}, {}, {}, {}, {}) = {}val'
              .format(idx[0], idx[1], idx[2], idx[3], idx[4], idx[5], idx[6], idx[7], sign_string))
    print('')
    print('                        end do')
    print('                     end do')
    print('                  end do')
    print('               end do')
    print('            end do')
    print('         end do')
    print('      end do')
    print('   end do')
    print('')
    print('end subroutine update_t4e')

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Builds the T4 full update loop for different spincases.")
    parser.add_argument('spincase', help='String specifying spincase, e.g., aaaa, aaab, aabb, abbb, or bbbb')
    args = parser.parse_args()

    main(args)
