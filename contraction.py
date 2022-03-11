from indices import fix_t3_indices, type_of_index
from term import Term, BinaryExpression
from utilities import check_include_term

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
    else:
        print('Invalid number of contraction indices > 4')
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
        equivalence = '1234'
    if [typ1, spin1] == [typ3, spin3] and [typ2, spin2] == [typ4, spin4]:
        equivalence = '1324'
    if [typ1, spin1] == [typ4, spin4] and [typ2, spin2] == [typ3, spin3]:
        equivalence = '1423'

    list_of_expressions = []
    for idp, p in enumerate([x.lower() for x in expression.contracted[0]] + [x.upper() for x in expression.contracted[0]]):
        for idq, q in enumerate([x.lower() for x in expression.contracted[1]] + [x.upper() for x in expression.contracted[1]]):
            for idr, r in enumerate([x.lower() for x in expression.contracted[2]] + [x.upper() for x in expression.contracted[2]]):
                for ids, s in enumerate([x.lower() for x in expression.contracted[3]] + [x.upper() for x in expression.contracted[3]]):

                    weight = 1.0

                    typ1 = type_of_index(p)
                    typ2 = type_of_index(q)
                    typ3 = type_of_index(r)
                    typ4 = type_of_index(s)

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
                    if equivalence == '1234':
                        if idp < idq or idr < ids: continue
                    if equivalence == '1324':
                        if idp < idr or idq < ids: continue
                    if equivalence == '1423':
                        if idp < ids or idq < idr: continue

                    if [typ1, spin1] == [typ2, spin2]:
                        weight *= 0.5
                    if [typ1, spin1] == [typ3, spin3]:
                        weight *= 0.5
                    if [typ2, spin2] == [typ3, spin3]:
                        weight *= 0.5
                    if [typ1, spin1] == [typ4, spin4]:
                        weight *= 0.5
                    if [typ2, spin2] == [typ4, spin4]:
                        weight *= 0.5
                    if [typ3, spin3] == [typ4, spin4]:
                        weight *= 0.5

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