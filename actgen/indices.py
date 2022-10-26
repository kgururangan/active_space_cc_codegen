from actgen.utilities import argsort, signPermutation

index_classification = {
            'fixed holes' : ['i', 'j', 'k', 'l'],
            'fixed particles' : ['a', 'b', 'c', 'd'],
            'free holes' : ['m', 'n', 'o'],
            'free particles' : ['e', 'f', 'g'],
}

def is_active(char):
    if len(char) > 1:
        char1 = char[0]
    else:
        char1 = char
    if char1.isupper():
        return True
    else:
        return False

def is_free_index(char):
    if len(char) > 1:
        char1 = char[0]
    else:
        char1 = char
    if char1 in ['m', 'n', 'o', 'M', 'N', 'O', 'e', 'f', 'g', 'E', 'F', 'G']:
        return True
    else:
        return False

def particle_or_hole(char):
    if len(char) > 1:
        char1 = char[0]
    else:
        char1 = char
    if char1 in ['m', 'n', 'o', 'i', 'j', 'k', 'l', 'M', 'N', 'O', 'I', 'J', 'K', 'L']:
        return 'hole'
    if char1 in ['e', 'f', 'g', 'a', 'b', 'c', 'd', 'E', 'F', 'G', 'A', 'B', 'C', 'D']:
        return 'particle'

def convert_char_to_ov(char):
    if particle_or_hole(char) == 'hole':
        return 'o'
    if particle_or_hole(char) == 'particle':
        return 'v'
    return -1

def type_of_index(char):
    if len(char) > 1:
        char1 = char[0]
    else:
        char1 = char
    if is_active(char1) and particle_or_hole(char1) == 'hole':
        return 'active_hole'
    if is_active(char1) and particle_or_hole(char1) == 'particle':
        return 'active_particle'
    if not is_active(char1) and particle_or_hole(char1) == 'hole':
        return 'inactive_hole'
    if not is_active(char1) and particle_or_hole(char1) == 'particle':
        return 'inactive_particle'


def fix_particle_index(idx):
    act_idx = [0] * len(idx)
    for i, ind in enumerate(idx):
        if is_active(ind): act_idx[i] = 1
    perm = argsort(act_idx)
    return list(reversed(perm))


def fix_hole_index(idx, order):
    act_idx = [0] * len(idx)
    for i, ind in enumerate(idx):
        if is_active(ind): act_idx[i] = 1
    perm = argsort(act_idx)
    return [x + order for x in perm]


def fix_t3_indices(arr, spin):
    sign = 1.0

    perm = list(range(6))
    if spin in ['aaa']:
        particles = arr[:3]
        holes = arr[3:]
        perm[:3] = fix_particle_index(particles)
        perm[3:] = fix_hole_index(holes, 3)
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation(perm[:3]) * signPermutation([x - 3 for x in perm[3:]])

    perm = list(range(6))
    if spin in ['aab']:
        particles = arr[:2]
        holes = arr[3:5]
        perm[:2] = fix_particle_index(particles)
        perm[3:5] = fix_hole_index(holes, 3)
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation(perm[:2]) * signPermutation([x - 3 for x in perm[3:5]])

    perm = list(range(6))
    if spin in ['abb']:
        particles = arr[1:3]
        holes = arr[4:]
        perm[1:3] = [x + 1 for x in fix_particle_index(particles)]
        perm[4:] = [x + 1 for x in fix_hole_index(holes, 3)]
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation([x - 1 for x in perm[1:3]]) * signPermutation([x - 4 for x in perm[4:]])

    perm = list(range(6))
    if spin in ['bbb']:
        particles = arr[:3]
        holes = arr[3:]
        perm[:3] = fix_particle_index(particles)
        perm[3:] = fix_hole_index(holes, 3)
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation(perm[:3]) * signPermutation([x - 3 for x in perm[3:]])

    return new_arr, sign


def get_slicestr_t3(contr):
    slicestr = [None] * 6
    for idx, c in enumerate(contr):
        typeOfIndex = type_of_index(c)
        if typeOfIndex == 'active_hole':
            slicestr[idx] = 'O'
        if typeOfIndex == 'inactive_hole':
            slicestr[idx] = 'o'
        if typeOfIndex == 'active_particle':
            slicestr[idx] = 'V'
        if typeOfIndex == 'inactive_particle':
            slicestr[idx] = 'v'
    slicestrjoined = ''.join(slicestr)
    return slicestrjoined

def fix_t4_indices(arr, spin):
    sign = 1.0

    perm = list(range(8))
    if spin in ['aaaa', 'bbbb']:
        particles = arr[:4]
        holes = arr[4:]
        perm[:4] = fix_particle_index(particles)
        perm[4:] = fix_hole_index(holes, 4)
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation(perm[:4]) * signPermutation([x - 4 for x in perm[4:]])

    perm = list(range(8))
    if spin in ['aaab']:
        particles = arr[:3]
        holes = arr[4:7]
        perm[:3] = fix_particle_index(particles)
        perm[4:7] = fix_hole_index(holes, 4)
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation(perm[:3]) * signPermutation([x - 4 for x in perm[4:7]])

    perm = list(range(8))
    if spin in ['aabb']:
        particles = arr[1:3]
        holes = arr[4:]
        perm[1:3] = [x + 1 for x in fix_particle_index(particles)]
        perm[4:] = [x + 1 for x in fix_hole_index(holes)]
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation([x - 1 for x in perm[1:3]]) * signPermutation([x - 4 for x in perm[4:]])

    return new_arr, sign

def get_slicestr_t4(contr):
    slicestr = [None] * 8
    for idx, c in enumerate(contr):
        typeOfIndex = type_of_index(c)
        if typeOfIndex == 'active_hole':
            slicestr[idx] = 'O'
        if typeOfIndex == 'inactive_hole':
            slicestr[idx] = 'o'
        if typeOfIndex == 'active_particle':
            slicestr[idx] = 'V'
        if typeOfIndex == 'inactive_particle':
            slicestr[idx] = 'v'
    slicestrjoined = ''.join(slicestr)
    return slicestrjoined