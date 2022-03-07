# term_print_list = []
# for idx, c in enumerate(retained_contractions):
#
#     s = c.split(',')
#
#     sign = s[0][0]
#     weight = s[0][1:]
#     if weight == '': weight = '1.0'
#
#     s1 = s[1].split('(')
#     term1 = s1[0]
#     contr1 = s1[1][:-1]
#
#     slicestr = ''
#     actslicestr = ''
#     double_spin_string = spincase * 2
#     for ind, char in enumerate(contr1):
#
#         o_or_v = convert_char_to_ov(char)
#         slicestr += o_or_v
#
#         # check if string on term1 corresponds to a free index (line extending to right)
#         # also present in the output string. If so, can simply use entire occ/unocc manifold.
#         if char in ['e', 'f', 'm', 'n', 'E', 'F', 'M', 'N'] and c in projection:
#             actslicestr += ':,'
#         else:
#             if char.upper() == char:
#                 if o_or_v == 'o':
#                     char_label = 'O'
#                 if o_or_v == 'v':
#                     char_label = 'V'
#             if char.upper() != char:
#                 if o_or_v == 'o':
#                     char_label = 'o'
#                 if o_or_v == 'v':
#                     char_label = 'v'
#
#             actslicestr += char_label + double_spin_string[ind] + ','
#
#     s2 = s[2].split('(')
#     term2 = s2[0]
#     contr2 = s2[1][:-1]
#
#     slicestr_t3 = get_slicestr_t3(contr2)
#
#     term_print_list.append(
#         {'sign': sign,
#          'weight': weight,
#          'contr1': contr1,
#          'contr2': contr2,
#          'projection': projection,
#          'term1': term1,
#          'slicestr': slicestr,
#          'actslicestr': actslicestr[:-1],
#          'term2': term2,
#          'slicestr_t3': slicestr_t3}
#     )
#
# # find the permutation weight using last contr1 and contr2
# perm_weight = get_permutation_weight(contr1, contr2, spincase)
#
# # print the term
# print(residual_term + ' += (' + str(perm_weight) + '/' + str(weight0) + ') * (')
#
# for t in term_print_list:
#     code_string = str('        ' + t['sign'] + t['weight'] + '*' + 'np.einsum(' + "'" + t['contr1'] + ',' + t[
#         'contr2'] + '->' + t['projection'] + "'" + ', ' \
#           + t['term1'] + "." + t['slicestr'] + "[" + t['actslicestr'] + "]" + ', ' + t['term2'] + "." + t[
#               'slicestr_t3'] + ', ' + 'optimize=True)')
#
#
#     print('        ' + t['sign'] + t['weight'] + '*' + 'np.einsum(' + "'" + t['contr1'] + ',' + t[
#         'contr2'] + '->' + t['projection'] + "'" + ', ' \
#           + t['term1'] + "." + t['slicestr'] + "[" + t['actslicestr'] + "]" + ', ' + t['term2'] + "." + t[
#               'slicestr_t3'] + ', ' + 'optimize=True)')
#
# print(')')
#
# nterms += 1