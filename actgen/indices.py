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


def fix_t4_indices(arr, spin):
    sign = 1.0

    # a  b  c  d  i  j  k  l
    # 0  1  2  3  4  5  6  7

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
        particles_a = arr[:2]
        holes_a = arr[4:6]
        particles_b = arr[2:4]
        holes_b = arr[6:]
        perm[:2] = [x for x in fix_particle_index(particles_a)]
        perm[2:4] = [x + 2 for x in fix_particle_index(particles_b)]
        perm[4:6] = [x for x in fix_hole_index(holes_a, 4)]
        perm[6:]  = [x + 2 for x in fix_hole_index(holes_b, 4)]
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation(perm[1:2]) * signPermutation([x - 2 for x in perm[2:4]])\
                    * signPermutation([x - 4 for x in perm[4:6]]) * signPermutation([x - 6 for x in perm[6:]])

    perm = list(range(8))
    if spin in ['abbb']:
        particles = arr[1:4]
        holes = arr[5:]
        perm[1:4] = [x + 1 for x in fix_particle_index(particles)]
        perm[5:] = [x + 1 for x in fix_hole_index(holes, 4)]
        new_arr = [arr[i] for i in perm]
        sign = sign * signPermutation([x - 1 for x in perm[1:4]]) * signPermutation([x - 5 for x in perm[5:]])

    return new_arr, sign

if __name__ == "__main__":

    arr = "AbCdiJKl"

    new_arr, sign = fix_t4_indices(arr, 'aabb')

    print(arr)
    print(new_arr)
    print(sign)