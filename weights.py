
def get_permutation_weight(contr1, contr2, spincase):

    # find the permutation weight using last contr1 and contr2
    dict_1 = get_counting_dict(contr1, spincase)
    dict_2 = get_counting_dict(contr2, spincase)

    perm_weight = 1.0
    for key in dict_1.keys():
        val1 = dict_1[key]
        val2 = dict_2[key]

        if val1 == 1 and val2 == 2 or val2 == 1 and val1 == 2:
            perm_weight *= 3.0
        elif val1 == 1 and val2 == 1:
            perm_weight *= 2.0

    return perm_weight

def get_counting_dict(contr, spincase):
    if spincase in ['aaa', 'aa', 'a']:
        return {'num_virt_alpha': contr.count('a') + contr.count('b') + contr.count('c'),
                'num_core_alpha': contr.count('i') + contr.count('j') + contr.count('k'),
                'num_act_hole_alpha': contr.count('I') + contr.count('J') + contr.count('K'),
                'num_act_particle_alpha': contr.count('A') + contr.count('B') + contr.count('C'),
                'num_virt_beta': 0,
                'num_core_beta': 0,
                'num_act_hole_beta': 0,
                'num_act_particle_beta': 0
                }
    if spincase in ['aab']:
        return {'num_virt_alpha': contr.count('a') + contr.count('b'),
                'num_core_alpha': contr.count('i') + contr.count('j'),
                'num_act_hole_alpha': contr.count('I') + contr.count('J'),
                'num_act_particle_alpha': contr.count('A') + contr.count('B'),
                'num_virt_beta': contr.count('c'),
                'num_core_beta': contr.count('k'),
                'num_act_hole_beta': contr.count('K'),
                'num_act_particle_beta': contr.count('C')
                }
    if spincase in ['abb', 'ab']:
        return {'num_virt_alpha': contr.count('a'),
                'num_core_alpha': contr.count('i'),
                'num_act_hole_alpha': contr.count('I'),
                'num_act_particle_alpha': contr.count('A'),
                'num_virt_beta': contr.count('b') + contr.count('c'),
                'num_core_beta': contr.count('j') + contr.count('k'),
                'num_act_hole_beta': contr.count('J') + contr.count('K'),
                'num_act_particle_beta': contr.count('B') + contr.count('C')
                }
    if spincase in ['bbb', 'bb', 'b']:
        return {'num_virt_beta': contr.count('a') + contr.count('b') + contr.count('c'),
                'num_core_beta': contr.count('i') + contr.count('j') + contr.count('k'),
                'num_act_hole_beta': contr.count('I') + contr.count('J') + contr.count('K'),
                'num_act_particle_beta': contr.count('A') + contr.count('B') + contr.count('C'),
                'num_virt_alpha': 0,
                'num_core_alpha': 0,
                'num_act_hole_alpha': 0,
                'num_act_particle_alpha': 0
                }
