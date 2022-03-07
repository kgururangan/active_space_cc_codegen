from indices import fix_t3_indices, type_of_index

def binary_active_contraction(contr_chars, spin_contr, obj1, obj2, sign_orig):

    num_contr_inds = len(contr_chars)

    if num_contr_inds == 1:



    if num_contr_inds == 2:

        d1 = []
        ct = 0

        typ1 = type_of_index(contr_chars[0])
        typ2 = type_of_index(contr_chars[1])
        spin1 = spin_contr[0]
        spin2 = spin_contr[1]

        equivalence = ''
        if [typ1, spin1] == [typ2, spin2]:
            equivalence = '12'

        for ip, p in enumerate([contr_chars[0].lower(), contr_chars[0].upper()]):
            for iq, q in enumerate([contr_chars[1].lower(), contr_chars[1].upper()]):

                weight = ''

                if equivalence == '12':
                    if ip < iq: continue

                typ1 = type_of_index(p)
                typ2 = type_of_index(q)
                if [typ1, spin1] == [typ2, spin2]:
                    weight = '0.5'

                arr1 = list(obj1['chars'])
                arr1[obj1['contr_idx'][0]] = p
                arr1[obj1['contr_idx'][1]] = q
                arr2 = list(obj2['chars'])
                arr2[obj2['contr_idx'][0]] = p
                arr2[obj2['contr_idx'][1]] = q

                new_arr, sign2 = fix_t3_indices(arr2, obj2['spin'])
                if sign2 in ['', '+']:
                    sign = sign_orig
                else:
                    if sign_orig in ['', '+']:
                        sign = '-'
                    else:
                        sign = '+'

                coef = sign + weight
                term1 = obj1['symbol'] + '(' + ''.join(arr1) + ')'
                term2 = obj2['symbol'] + '(' + ''.join(new_arr) + ')'

                new_obj1 = {'symbol' : obj1['symbol']}

                d1.append(coef + ',' + term1 + ',' + term2)

                ct += 1

    if num_contr_inds == 3:

        d1 = []
        ct = 0

        typ1 = type_of_index(contr_chars[0])
        typ2 = type_of_index(contr_chars[1])
        typ3 = type_of_index(contr_chars[2])
        spin1 = spin_contr[0]
        spin2 = spin_contr[1]
        spin3 = spin_contr[2]

        equivalence = ''
        if [typ1, spin1] == [typ2, spin2]:
            equivalence = '12'
        if [typ1, spin2] == [typ3, spin3]:
            equivalence = '13'
        if [typ2, spin2] == [typ3, spin3]:
            equivalence = '23'

        for ip, p in enumerate([contr_chars[0].lower(), contr_chars[0].upper()]):
            for iq, q in enumerate([contr_chars[1].lower(), contr_chars[1].upper()]):
                for ir, r in enumerate([contr_chars[2].lower(), contr_chars[2].upper()]):

                    weight = ''

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
                        weight = '0.5'

                    arr1 = list(obj1['chars'])
                    arr1[obj1['contr_idx'][0]] = p
                    arr1[obj1['contr_idx'][1]] = q
                    arr1[obj1['contr_idx'][2]] = r

                    arr2 = list(obj2['chars'])
                    arr2[obj2['contr_idx'][0]] = p
                    arr2[obj2['contr_idx'][1]] = q
                    arr2[obj2['contr_idx'][2]] = r

                    new_arr, sign2 = fix_t3_indices(arr2, obj2['spin'])
                    if sign2 in ['', '+']:
                        sign = sign_orig
                    else:
                        if sign_orig in ['', '+']:
                            sign = '-'
                        else:
                            sign = '+'

                    signcoef = sign + weight
                    term1 = obj1['symbol'] + '(' + ''.join(arr1) + ')'
                    term2 = obj2['symbol'] + '(' + ''.join(new_arr) + ')'

                    d1.append(signcoef + ',' + term1 + ',' + term2)

                    ct += 1

    if num_contr_inds == 4:

        d1 = []
        ct = 0

        typ1 = type_of_index(contr_chars[0])
        typ2 = type_of_index(contr_chars[1])
        typ3 = type_of_index(contr_chars[2])
        typ4 = type_of_index(contr_chars[3])
        spin1 = spin_contr[0]
        spin2 = spin_contr[1]
        spin3 = spin_contr[2]
        spin4 = spin_contr[3]

        equivalence = ''
        if [typ1, spin1] == [typ2, spin2]:
            equivalence = '12'
        if [typ1, spin2] == [typ3, spin3]:
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

        for idp, p in enumerate([contr_chars[0].lower(), contr_chars[0].upper()]):
            for idq, q in enumerate([contr_chars[1].lower(), contr_chars[1].upper()]):
                for idr, r in enumerate([contr_chars[2].lower(), contr_chars[2].upper()]):
                    for ids, s in enumerate([contr_chars[3].lower(), contr_chars[3].upper()]):

                        weight = ''

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

                        weightnum = 1.0
                        if [typ1, spin1] == [typ2, spin2]:
                            weightnum *= 0.5
                        if [typ1, spin1] == [typ3, spin3]:
                            weightnum *= 0.5
                        if [typ2, spin2] == [typ3, spin3]:
                            weightnum *= 0.5
                        if [typ1, spin1] == [typ4, spin4]:
                            weightnum *= 0.5
                        if [typ2, spin2] == [typ4, spin4]:
                            weightnum *= 0.5
                        if [typ3, spin3] == [typ4, spin4]:
                            weightnum *= 0.5
                        if weightnum == 1.0:
                            weight = ''
                        else:
                            weight = str(weightnum)

                        arr1 = list(obj1['chars'])
                        arr1[obj1['contr_idx'][0]] = p
                        arr1[obj1['contr_idx'][1]] = q
                        arr1[obj1['contr_idx'][2]] = r
                        arr1[obj1['contr_idx'][3]] = s

                        arr2 = list(obj2['chars'])
                        arr2[obj2['contr_idx'][0]] = p
                        arr2[obj2['contr_idx'][1]] = q
                        arr2[obj2['contr_idx'][2]] = r
                        arr2[obj2['contr_idx'][3]] = s

                        new_arr, sign2 = fix_t3_indices(arr2, obj2['spin'])
                        if sign2 in ['', '+']:
                            sign = sign_orig
                        else:
                            if sign_orig in ['', '+']:
                                sign = '-'
                            else:
                                sign = '+'

                        coef = sign + weight
                        term1 = obj1['symbol'] + '(' + ''.join(arr1) + ')'
                        term2 = obj2['symbol'] + '(' + ''.join(new_arr) + ')'

                        d1.append(coef + ',' + term1 + ',' + term2)

                        ct += 1
    return d1

def single_contraction(expression):

    for ip, p in enumerate([expression.contracted.lower(), contr_chars[0].upper()]):

        weight = ''

        arr1 = list(obj1['chars'])
        arr1[obj1['contr_idx'][0]] = p
        arr2 = list(obj2['chars'])
        arr2[obj2['contr_idx'][0]] = p

        new_arr, sign2 = fix_t3_indices(arr2, obj2['spin'])
        if sign2 in ['', '+']:
            sign = sign_orig
        else:
            if sign_orig in ['', '+']:
                sign = '-'
            else:
                sign = '+'



        signcoef = sign + weight
        term1 = obj1['symbol'] + '(' + ''.join(arr1) + ')'
        term2 = obj2['symbol'] + '(' + ''.join(new_arr) + ')'

        d1.append(signcoef + ',' + term1 + ',' + term2)

