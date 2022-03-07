def parse_expression(expr):
    flag = False
    sign_orig = expr[0]

    if sign_orig not in ['+', '-']:
        sign_orig = '+'
        flag = True

    for idx, s in enumerate(expr):
        if s in ['h', 'v', 'f']:
            break
    else:
        print("Expression {} did not have a contraction tensor of 'H','V', or 'F'!".format(expr))

    if idx == 0 and sign_orig != '-':
        coef_orig = ''
    elif idx == 1 and sign_orig == '-':
        coef_orig = ''
    else:
        if not flag:
            coef_orig = expr[1:idx]
        else:
            coef_orig = expr[:idx]

    s = expr.split(',')
    num_terms = len(s)
    if num_terms != 2:
        print('Cannot handle non-binary contration!')
        return
    else:
        term1, term2 = s
        s1 = term1.split('(')
        s2 = term2.split('(')
        obj1 = {'sym': s1[0][1:], 'chars': s1[1][:-1], 'spin': s1[0][-1].upper(), 'contr_idx': [], 'uncontr_idx': []}
        obj2 = {'sym': s2[0], 'chars': s2[1][:-1], 'spin': s2[0][-1].upper(), 'contr_idx': [], 'uncontr_idx': []}

    uncontr_chars = list(set(obj1['chars']) ^ set(obj2['chars']))
    contr_chars = list(set(obj1['chars']) & set(obj2['chars']))
    spin_contr = [None] * len(contr_chars)

    # find the indical positions of each contraction index in the characters of obj1 and obj2
    for j, y in enumerate(contr_chars):
        for i, x in enumerate(obj1['chars']):
            if x == y:
                obj1['contr_idx'].append(i)
        for i, x in enumerate(obj2['chars']):
            if x == y:
                obj2['contr_idx'].append(i)

    # find the indical positions of each uncontracted index in the characters of obj1 and obj2
    for j, y in enumerate(uncontr_chars):
        for i, x in enumerate(obj1['chars']):
            if x == y:
                obj1['uncontr_idx'].append(i)
        for i, x in enumerate(obj2['chars']):
            if x == y:
                obj2['uncontr_idx'].append(i)

    # this is assuming we have H * T3 or H * R3, where H is at most 2-body
    # no support for 3-body contractions in object 1 (e.g., this would not fly
    # for left-CCSDt)
    # can easily bypass this by using 'p~' characters for beta indices on input
    for i, idx in enumerate(obj1['contr_idx']):
        if obj1['spin'] == 'A':
            spin_contr[i] = 'alpha'
        elif obj1['spin'] == 'B':
            if idx % 2 == 0:
                spin_contr[i] = 'alpha'
            else:
                spin_contr[i] = 'beta'
        elif obj1['spin'] == 'C':
            spin_contr[i] = 'beta'
        else:
            print('Object 1 spincase of {} not recognized or supported')

    return contr_chars, spin_contr, obj1, obj2, sign_orig