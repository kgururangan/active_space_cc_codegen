from math import factorial

from indices import fix_t3_indices, type_of_index
from term import Term, BinaryExpression
from utilities import check_include_term

# [TODO]: The equivalence handling in this module needs to be change
# I noticed that the equivalence is determined using the "bare" form of contraction indices
# passed in at the input (on the level of BinaryExpression). As a result, you determine the
# equivalence case once before entering the loop that turns each line active/inactive. The
# way the logic works now is that it checks all possible equivalence cases among n contraction lines,
# starting from the weakest cases and toward the strongest ones. Thus, you want the equivalence
# at the end to correspond to the strongest equivalence case. One thing to fix is that we should
# make a generic routine that taken in a set of n indices and their spins and spits out the highest
# equivalence case.

# The "strength" of an equivalence case really refers to the number of equivalence permutations.
# If we have a set of N indices and split them into M partitions, with the rank of each partition being k_m, m = 1,...,M,
# then, the number of equivalent permutations is (k_1!) * (k_2!) * ... * (k_M!).
# Example:
# Suppose we have 5 indices and find that 3 are equivalent and the other 2 are equivalent. Generically, we'll call
# this partitioning (123)(45). Thus, the number of equivalent permutations is 3! * 2! = 12. In contrast, if the
# partition is (12)(34)(5), the number of equivalent permutations is 2! * 2! * 1! = 4. Thus (123)(45) is a stronger
# equivalence than (12)(34)(5).
# The order to check equivalences:
# 1) binary (12) (strength = 2)
# 2) pair binary (12)(34) (strength = 4)
# 3) ternary (123) (strength = 6)
# 4) triple binary (12)(34)(56) (strength = 8)
# 5) ternary + pair binary (123)(45) (strength = 12)
# 6) quad binary (12)(34)(56)(78) (strength = 16)
# 8) ternary + pair binary (123)(45)(67) (strength = 24)
# 9) quadruple (1234) (strength = 24)
# (*) Note that while (8) and (9) have the same strength, (8) needs 7 indices while (9) uses just 4 so they will never occur at the same time

def contract(expression, num_active):

    retained_contractions = []

    if len(expression.contracted) == 1:
        all_contractions = single_contraction(expression)
    elif len(expression.contracted) == 2:
        all_contractions = double_contraction(expression)
    elif len(expression.contracted) == 3:
        all_contractions = triple_contraction(expression)
    elif len(expression.contracted) == 4:
        all_contractions = quadruple_contraction(expression)
    elif len(expression.contracted) == 5:
        all_contractions = quintuple_contraction(expression)
    else:
        print('Invalid number of contraction indices > 5')
        return

    # retain only those expressions in which T (or R) is restricted to
    # the appropriate active space paritioning
    for expr in all_contractions:
        if len(expr.B.indices) == 6:
            if check_include_term(expr.B.indices, num_active):
                retained_contractions.append(expr)
        else:
            retained_contractions.append(expr)

    return retained_contractions

# [TODO]: Can collapse all contraction cases into one function using intertools.combinations. Just need to work it out..
def single_contraction(expression):

    list_of_expressions = []
    for ip, p in enumerate([x.lower() for x in expression.contracted] + [x.upper() for x in expression.contracted]):

        weight = 1.0

        arr1 = list(expression.A.indices)
        arr1[expression.A.contracted_indices[0]] = p

        arr2 = list(expression.B.indices)
        arr2[expression.B.contracted_indices[0]] = p

        if len(arr2) == 6:
            new_arr, sign_perm = fix_t3_indices(arr2, expression.B.spin)
            sign = expression.sign * sign_perm
        else:
            new_arr = arr2
            sign = expression.sign


        term1 = Term(expression.A.symbol,
                     expression.A.spin,
                     ''.join(arr1))

        term2 = Term(expression.B.symbol,
                     expression.B.spin,
                     ''.join(new_arr))

        #print(BinaryExpression(sign, expression.weight, term1, term2).to_string())
        list_of_expressions.append(BinaryExpression(sign, expression.weight, term1, term2))

    return list_of_expressions

def double_contraction(expression):

    typ1 = type_of_index(expression.contracted[0])
    typ2 = type_of_index(expression.contracted[1])
    spin1 = expression.spin_of_contracted[0]
    spin2 = expression.spin_of_contracted[1]

    equivalence = ''
    if [typ1, spin1] == [typ2, spin2]:
        equivalence = '12'

    list_of_expressions = []
    for ip, p in enumerate([x.lower() for x in expression.contracted[0]] + [x.upper() for x in expression.contracted[0]]):
        for iq, q in enumerate([x.lower() for x in expression.contracted[1]] + [x.upper() for x in expression.contracted[1]]):

            weight = 1.0
            sign = expression.sign

            if equivalence == '12':
                if ip < iq: continue

            typ1 = type_of_index(p)
            typ2 = type_of_index(q)
            if [typ1, spin1] == [typ2, spin2]:
                weight = 0.5

            arr1 = list(expression.A.indices)
            arr1[expression.A.contracted_indices[0]] = p
            arr1[expression.A.contracted_indices[1]] = q

            arr2 = list(expression.B.indices)
            arr2[expression.B.contracted_indices[0]] = p
            arr2[expression.B.contracted_indices[1]] = q

            new_arr, sign_perm = fix_t3_indices(arr2, expression.B.spin)
            sign = expression.sign * sign_perm

            term1 = Term(expression.A.symbol,
                         expression.A.spin,
                         ''.join(arr1))

            term2 = Term(expression.B.symbol,
                         expression.B.spin,
                         ''.join(new_arr))

            list_of_expressions.append(BinaryExpression(sign, weight, term1, term2))

    return list_of_expressions

def triple_contraction(expression):

    typ1 = type_of_index(expression.contracted[0])
    typ2 = type_of_index(expression.contracted[1])
    typ3 = type_of_index(expression.contracted[2])
    spin1 = expression.spin_of_contracted[0]
    spin2 = expression.spin_of_contracted[1]
    spin3 = expression.spin_of_contracted[2]

    equivalence = ''
    if [typ1, spin1] == [typ2, spin2]:
        equivalence = '12'
    if [typ1, spin1] == [typ3, spin3]:
        equivalence = '13'
    if [typ2, spin2] == [typ3, spin3]:
        equivalence = '23'

    if [typ1, spin1] == [typ2, spin2] == [typ3, spin3]:
        equivalence = '123'

    list_of_expressions = []
    for ip, p in enumerate([x.lower() for x in expression.contracted[0]] + [x.upper() for x in expression.contracted[0]]):
        for iq, q in enumerate([x.lower() for x in expression.contracted[1]] + [x.upper() for x in expression.contracted[1]]):
            for ir, r in enumerate([x.lower() for x in expression.contracted[2]] + [x.upper() for x in expression.contracted[2]]):

                weight = 1.0

                typ1 = type_of_index(p)
                typ2 = type_of_index(q)
                typ3 = type_of_index(r)

                if equivalence == '12':
                    if ip < iq: continue
                if equivalence == '13':
                    if ip < ir: continue
                if equivalence == '23':
                    if iq < ir: continue

                if equivalence == '123':
                    if ip < iq or ip < ir or iq < ir: continue

                if [typ1, spin1] == [typ2, spin2] or \
                        [typ1, spin1] == [typ3, spin3] or \
                        [typ2, spin2] == [typ3, spin3]:
                    weight = 0.5

                arr1 = list(expression.A.indices)
                arr1[expression.A.contracted_indices[0]] = p
                arr1[expression.A.contracted_indices[1]] = q
                arr1[expression.A.contracted_indices[2]] = r

                arr2 = list(expression.B.indices)
                arr2[expression.B.contracted_indices[0]] = p
                arr2[expression.B.contracted_indices[1]] = q
                arr2[expression.B.contracted_indices[2]] = r

                new_arr, sign_perm = fix_t3_indices(arr2, expression.B.spin)
                sign = expression.sign * sign_perm

                term1 = Term(expression.A.symbol,
                             expression.A.spin,
                             ''.join(arr1))

                term2 = Term(expression.B.symbol,
                             expression.B.spin,
                             ''.join(new_arr))

                list_of_expressions.append(BinaryExpression(sign, weight, term1, term2))

    return list_of_expressions

def quadruple_contraction(expression):

    typ1 = type_of_index(expression.contracted[0])
    typ2 = type_of_index(expression.contracted[1])
    typ3 = type_of_index(expression.contracted[2])
    typ4 = type_of_index(expression.contracted[3])
    spin1 = expression.spin_of_contracted[0]
    spin2 = expression.spin_of_contracted[1]
    spin3 = expression.spin_of_contracted[2]
    spin4 = expression.spin_of_contracted[3]

    equivalence = ''
    if [typ1, spin1] == [typ2, spin2]:
        equivalence = '12'
    if [typ1, spin1] == [typ3, spin3]:
        equivalence = '13'
    if [typ1, spin1] == [typ4, spin4]:
        equivalence = '14'
    if [typ2, spin2] == [typ3, spin3]:
        equivalence = '23'
    if [typ2, spin2] == [typ4, spin4]:
        equivalence = '24'
    if [typ3, spin3] == [typ4, spin4]:
        equivalence = '34'

    if [typ1, spin1] == [typ2, spin2] and [typ3, spin3] == [typ4, spin4]:
        equivalence = '12,34'
    if [typ1, spin1] == [typ3, spin3] and [typ2, spin2] == [typ4, spin4]:
        equivalence = '13,24'
    if [typ1, spin1] == [typ4, spin4] and [typ2, spin2] == [typ3, spin3]:
        equivalence = '14,23'

    if [typ1, spin1] == [typ2, spin2] == [typ3, spin3]:
        equivalence = '123'
    if [typ1, spin1] == [typ2, spin2] == [typ4, spin4]:
        equivalence = '124'
    if [typ1, spin1] == [typ3, spin3] == [typ4, spin4]:
        equivalence = '134'
    if [typ2, spin2] == [typ3, spin3] == [typ4, spin4]:
        equivalence = '234'

    if [typ1, spin1] == [typ2, spin2] == [typ3, spin3] == [typ4, spin4]:
        equivalence = '1234'

    list_of_expressions = []
    for idp, p in enumerate([x.lower() for x in expression.contracted[0]] + [x.upper() for x in expression.contracted[0]]):
        for idq, q in enumerate([x.lower() for x in expression.contracted[1]] + [x.upper() for x in expression.contracted[1]]):
            for idr, r in enumerate([x.lower() for x in expression.contracted[2]] + [x.upper() for x in expression.contracted[2]]):
                for ids, s in enumerate([x.lower() for x in expression.contracted[3]] + [x.upper() for x in expression.contracted[3]]):

                    typ1 = type_of_index(p) + spin1
                    typ2 = type_of_index(q) + spin2
                    typ3 = type_of_index(r) + spin3
                    typ4 = type_of_index(s) + spin4

                    if equivalence == '12':
                        if idp < idq: continue
                    if equivalence == '13':
                        if idp < idr: continue
                    if equivalence == '14':
                        if idp < ids: continue
                    if equivalence == '23':
                        if idq < idr: continue
                    if equivalence == '24':
                        if idq < ids: continue
                    if equivalence == '34':
                        if idr < ids: continue

                    if equivalence == '12,34':
                        if idp < idq or idr < ids: continue
                    if equivalence == '13,24':
                        if idp < idr or idq < ids: continue
                    if equivalence == '14,23':
                        if idp < ids or idq < idr: continue

                    if equivalence == '123':
                        if idp < idq or idp < idr or idq < idr: continue
                    if equivalence == '124':
                        if idp < idq or idp < ids or idq < ids: continue
                    if equivalence == '134':
                        if idp < idr or idp < idq or idr < ids: continue
                    if equivalence == '234':
                        if idq < idr or idq < ids or idr < ids: continue

                    if equivalence == '1234':
                        if idp < idq or idp < idr or idp < ids or idq < idr or idq < ids or idr < ids: continue

                    npart = count_equivalent_partitions([typ1, typ2, typ3, typ4])
                    weight = 1.0
                    for n in npart:
                        weight /= factorial(n)
                    # if [typ1, spin1] == [typ2, spin2]:
                    #     weight *= 0.5
                    # if [typ1, spin1] == [typ3, spin3]:
                    #     weight *= 0.5
                    # if [typ2, spin2] == [typ3, spin3]:
                    #     weight *= 0.5
                    # if [typ1, spin1] == [typ4, spin4]:
                    #     weight *= 0.5
                    # if [typ2, spin2] == [typ4, spin4]:
                    #     weight *= 0.5
                    # if [typ3, spin3] == [typ4, spin4]:
                    #     weight *= 0.5

                    arr1 = list(expression.A.indices)
                    arr1[expression.A.contracted_indices[0]] = p
                    arr1[expression.A.contracted_indices[1]] = q
                    arr1[expression.A.contracted_indices[2]] = r
                    arr1[expression.A.contracted_indices[3]] = s

                    arr2 = list(expression.B.indices)
                    arr2[expression.B.contracted_indices[0]] = p
                    arr2[expression.B.contracted_indices[1]] = q
                    arr2[expression.B.contracted_indices[2]] = r
                    arr2[expression.B.contracted_indices[3]] = s

                    new_arr, sign_perm = fix_t3_indices(arr2, expression.B.spin)
                    sign = expression.sign * sign_perm

                    term1 = Term(expression.A.symbol,
                                 expression.A.spin,
                                 ''.join(arr1))

                    term2 = Term(expression.B.symbol,
                                 expression.B.spin,
                                 ''.join(new_arr))

                    list_of_expressions.append(BinaryExpression(sign, weight, term1, term2))

    return list_of_expressions

def quintuple_contraction(expression):

    typ1 = type_of_index(expression.contracted[0])
    typ2 = type_of_index(expression.contracted[1])
    typ3 = type_of_index(expression.contracted[2])
    typ4 = type_of_index(expression.contracted[3])
    typ5 = type_of_index(expression.contracted[4])
    spin1 = expression.spin_of_contracted[0]
    spin2 = expression.spin_of_contracted[1]
    spin3 = expression.spin_of_contracted[2]
    spin4 = expression.spin_of_contracted[3]
    spin5 = expression.spin_of_contracted[4]

    #print(expression.contracted)

    equivalence = ''
    if [typ1, spin1] == [typ2, spin2]:
        equivalence = '12'
    if [typ1, spin1] == [typ3, spin3]:
        equivalence = '13'
    if [typ1, spin1] == [typ4, spin4]:
        equivalence = '14'
    if [typ1, spin1] == [typ5, spin5]:
        equivalence = '15'
    if [typ2, spin2] == [typ3, spin3]:
        equivalence = '23'
    if [typ2, spin2] == [typ4, spin4]:
        equivalence = '24'
    if [typ2, spin2] == [typ5, spin5]:
        equivalence = '25'
    if [typ3, spin3] == [typ4, spin4]:
        equivalence = '34'
    if [typ3, spin3] == [typ5, spin5]:
        equivalence = '35'
    if [typ4, spin4] == [typ5, spin5]:
        equivalence = '45'

    if [typ1, spin1] == [typ2, spin2] and [typ3, spin3] == [typ4, spin4]:
        equivalence = '12,34'
    if [typ1, spin1] == [typ2, spin2] and [typ3, spin3] == [typ5, spin5]:
        equivalence = '12,35'
    if [typ1, spin1] == [typ2, spin2] and [typ4, spin4] == [typ5, spin5]:
        equivalence = '12,45'
    if [typ1, spin1] == [typ3, spin3] and [typ2, spin2] == [typ4, spin4]:
        equivalence = '13,24'
    if [typ1, spin1] == [typ3, spin3] and [typ2, spin2] == [typ5, spin5]:
        equivalence = '13,25'
    if [typ1, spin1] == [typ3, spin3] and [typ4, spin4] == [typ5, spin5]:
        equivalence = '13,45'
    if [typ1, spin1] == [typ4, spin4] and [typ2, spin2] == [typ3, spin3]:
        equivalence = '14,23'
    if [typ1, spin1] == [typ4, spin4] and [typ2, spin2] == [typ5, spin5]:
        equivalence = '14,25'
    if [typ1, spin1] == [typ4, spin4] and [typ3, spin3] == [typ5, spin5]:
        equivalence = '14,35'
    if [typ1, spin1] == [typ5, spin5] and [typ2, spin2] == [typ3, spin3]:
        equivalence = '15,23'
    if [typ1, spin1] == [typ5, spin5] and [typ2, spin2] == [typ4, spin4]:
        equivalence = '15,24'
    if [typ1, spin1] == [typ5, spin5] and [typ3, spin3] == [typ4, spin4]:
        equivalence = '15,34'
    if [typ2, spin2] == [typ3, spin3] and [typ4, spin4] == [typ5, spin5]:
        equivalence = '23,45'
    if [typ2, spin2] == [typ4, spin4] and [typ3, spin3] == [typ5, spin5]:
        equivalence = '24,35'
    if [typ2, spin2] == [typ5, spin5] and [typ3, spin3] == [typ4, spin4]:
        equivalence = '25,34'

    # threefold equivalences
    if [typ1, spin1] == [typ2, spin2] == [typ3, spin3]:
        equivalence='123'
    if [typ1, spin1] == [typ2, spin2] == [typ4, spin4]:
        equivalence='124'
    if [typ1, spin1] == [typ2, spin2] == [typ5, spin5]:
        equivalence='125'
    if [typ1, spin1] == [typ3, spin3] == [typ4, spin4]:
        equivalence='134'
    if [typ1, spin1] == [typ3, spin3] == [typ5, spin5]:
        equivalence='135'
    if [typ1, spin1] == [typ4, spin4] == [typ5, spin5]:
        equivalence='145'
    if [typ2, spin2] == [typ3, spin3] == [typ4, spin4]:
        equivalence='234'
    if [typ2, spin2] == [typ3, spin3] == [typ5, spin5]:
        equivalence='235'
    if [typ2, spin2] == [typ4, spin4] == [typ5, spin5]:
        equivalence='245'
    if [typ3, spin3] == [typ4, spin4] == [typ5, spin5]:
        equivalence='345'

    # threefold + twofold equivalence
    if [typ1, spin1] == [typ2, spin2] == [typ3, spin3] and [typ4, spin4] == [typ5, spin5]:
        equivalence='123,45'
    if [typ1, spin1] == [typ2, spin2] == [typ4, spin4] and [typ3, spin3] == [typ5, spin5]:
        equivalence='124,35'
    if [typ1, spin1] == [typ2, spin2] == [typ5, spin5] and [typ3, spin3] == [typ4, spin4]:
        equivalence='125,34'
    if [typ1, spin1] == [typ3, spin3] == [typ4, spin4] and [typ2, spin2] == [typ5, spin5]:
        equivalence='134,25'
    if [typ1, spin1] == [typ3, spin3] == [typ5, spin5] and [typ2, spin2] == [typ4, spin4]:
        equivalence='135,24'
    if [typ1, spin1] == [typ4, spin4] == [typ5, spin5] and [typ2, spin2] == [typ3, spin3]:
        equivalence='145,23'
    if [typ2, spin2] == [typ3, spin3] == [typ4, spin4] and [typ1, spin1] == [typ5, spin5]:
        equivalence='234,15'
    if [typ2, spin2] == [typ3, spin3] == [typ5, spin5] and [typ1, spin1] == [typ4, spin4]:
        equivalence='235,14'
    if [typ2, spin2] == [typ4, spin4] == [typ5, spin5] and [typ1, spin1] == [typ3, spin3]:
        equivalence='245,13'
    if [typ3, spin3] == [typ4, spin4] == [typ5, spin5] and [typ1, spin1] == [typ2, spin2]:
        equivalence='345,12'

    # fourfold equivalence

    # fivefold equivalence

    #print(equivalence)

    list_of_expressions = []
    for idp, p in enumerate([x.lower() for x in expression.contracted[0]] + [x.upper() for x in expression.contracted[0]]):
        for idq, q in enumerate([x.lower() for x in expression.contracted[1]] + [x.upper() for x in expression.contracted[1]]):
            for idr, r in enumerate([x.lower() for x in expression.contracted[2]] + [x.upper() for x in expression.contracted[2]]):
                for ids, s in enumerate([x.lower() for x in expression.contracted[3]] + [x.upper() for x in expression.contracted[3]]):
                    for idt, t in enumerate([x.lower() for x in expression.contracted[4]] + [x.upper() for x in expression.contracted[4]]):

                        typ1 = type_of_index(p) + spin1
                        typ2 = type_of_index(q) + spin2
                        typ3 = type_of_index(r) + spin3
                        typ4 = type_of_index(s) + spin4
                        typ5 = type_of_index(t) + spin5

                        if equivalence == '12':
                            if idp < idq: continue
                        if equivalence == '13':
                            if idp < idr: continue
                        if equivalence == '14':
                            if idp < ids: continue
                        if equivalence == '15':
                            if idp < idt: continue
                        if equivalence == '23':
                            if idq < idr: continue
                        if equivalence == '24':
                            if idq < ids: continue
                        if equivalence == '25':
                            if idq < idt: continue
                        if equivalence == '34':
                            if idr < ids: continue
                        if equivalence == '35':
                            if idr < idt: continue
                        if equivalence == '45':
                            if ids < idt: continue

                        if equivalence == '12,34':
                            if idp < idq or idr < ids: continue
                        if equivalence == '12,35':
                            if idp < idq or idr < idt: continue
                        if equivalence == '12,45':
                            if idp < idq or ids < idt: continue
                        if equivalence == '13,24':
                            if idp < idr or idq < ids: continue
                        if equivalence == '13,25':
                            if idp < idr or idq < idt: continue
                        if equivalence == '13,45':
                            if idp < idr or ids < idt: continue
                        if equivalence == '14,23':
                            if idp < ids or idq < idr: continue
                        if equivalence == '14,25':
                            if idp < ids or idq < idt: continue
                        if equivalence == '14,35':
                            if idp < ids or idr < idt: continue
                        if equivalence == '15,23':
                            if idp < idt or idq < idr: continue
                        if equivalence == '15,24':
                            if idp < idt or idq < ids: continue
                        if equivalence == '15,34':
                            if idp < idt or idr < ids: continue
                        if equivalence == '23,45':
                            if idq < idr or ids < idt: continue
                        if equivalence == '24,35':
                            if idq < ids or idr < idt: continue
                        if equivalence == '25,34':
                            if idq < idt or idr < ids: continue

                        if equivalence == '123':
                            if idp < idq or idp < idr or idq < idr: continue
                        if equivalence == '124':
                            if idp < idq or idp < ids or idq < ids: continue
                        if equivalence == '125':
                            if idp < idq or idp < idt or idq < idt: continue
                        if equivalence == '134':
                            if idp < idr or idp < ids or idr < ids: continue
                        if equivalence == '135':
                            if idp < idr or idp < idt or idr < idt: continue
                        if equivalence == '145':
                            if idp < ids or idp < idt or ids < idt: continue
                        if equivalence == '234':
                            if idq < idr or idq < ids or idr < ids: continue
                        if equivalence == '235':
                            if idq < idr or idq < idt or idr < idt: continue
                        if equivalence == '245':
                            if idq < ids or idq < idt or ids < idt: continue
                        if equivalence == '345':
                            if idr < ids or idr < idt or ids < idt: continue

                        if equivalence == '123,45':
                            if idp < idq or idp < idr or idq < idr or ids < idt: continue
                        if equivalence == '124,35':
                            if idp < idq or idp < ids or idq < ids or idr < idt: continue
                        if equivalence == '125,34':
                            if idp < idq or idp < idt or idq < idt or idr < ids: continue
                        if equivalence == '134,25':
                            if idp < idr or idp < ids or idr < ids or idq < idt: continue
                        if equivalence == '135,24':
                            if idp < idr or idp < idt or idr < idt or idq < ids: continue
                        if equivalence == '145,23':
                            if idp < ids or idp < idt or ids < idt or idq < idr: continue
                        if equivalence == '234,15':
                            if idq < idr or idq < ids or idr < ids or idp < idt: continue
                        if equivalence == '235,14':
                            if idq < idr or idq < idt or idr < idt or idp < ids: continue
                        if equivalence == '245,13':
                            if idq < ids or idq < idt or ids < idt or idp < idr: continue
                        if equivalence == '345,12':
                            if idr < ids or idr < idt or ids < idt or idp < idq: continue

                        npart = count_equivalent_partitions([typ1, typ2, typ3, typ4, typ5])
                        weight = 1.0
                        for n in npart:
                            weight /= factorial(n)

                        arr1 = list(expression.A.indices)
                        arr1[expression.A.contracted_indices[0]] = p
                        arr1[expression.A.contracted_indices[1]] = q
                        arr1[expression.A.contracted_indices[2]] = r
                        arr1[expression.A.contracted_indices[3]] = s
                        arr1[expression.A.contracted_indices[4]] = t

                        arr2 = list(expression.B.indices)
                        arr2[expression.B.contracted_indices[0]] = p
                        arr2[expression.B.contracted_indices[1]] = q
                        arr2[expression.B.contracted_indices[2]] = r
                        arr2[expression.B.contracted_indices[3]] = s
                        arr2[expression.B.contracted_indices[4]] = t

                        new_arr, sign_perm = fix_t3_indices(arr2, expression.B.spin)
                        sign = expression.sign * sign_perm

                        term1 = Term(expression.A.symbol,
                                     expression.A.spin,
                                     ''.join(arr1))

                        term2 = Term(expression.B.symbol,
                                     expression.B.spin,
                                     ''.join(new_arr))

                        list_of_expressions.append(BinaryExpression(sign, weight, term1, term2))

    return list_of_expressions


def count_equivalent_partitions(lst):

    temp = [lst.count(x) for x in lst]

    partition_count = [0] * len(lst)

    cnt = 0
    for i, t in enumerate(temp):
        cnt += t
        if cnt > len(lst):
            break
        else:
            partition_count[i] = t

    return partition_count