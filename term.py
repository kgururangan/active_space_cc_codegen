from indices import type_of_index
from utilities import unique_objects, sign_to_str

class BinaryExpression:

    def __init__(self, sign, weight, term_1, term_2):

        self.sign = sign
        self.weight = weight
        self.A = term_1
        self.B = term_2

        self.uncontracted = list(set(self.A.indices) ^ set(self.B.indices))
        self.contracted = list(set(self.A.indices) & set(self.B.indices))

        # find the indical positions of each contraction index in the characters of obj1 and obj2
        temp_A = []
        temp_B = []
        for j, y in enumerate(self.contracted):
            for i, x in enumerate(self.A.indices):
                if x == y:
                    temp_A.append(i)
            for i, x in enumerate(self.B.indices):
                if x == y:
                    temp_B.append(i)
        setattr(self.A, 'contracted_indices', temp_A)
        setattr(self.B, 'contracted_indices', temp_B)

        self.spin_of_contracted = [self.A.spin_of_index(i) for i in self.A.contracted_indices]

    def to_string(self):
        return ''.join([sign_to_str(self.sign), str(self.weight), ',', self.A.to_index_string(), ',', self.B.to_index_string()])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Term:

    def __init__(self, symbol, spin, indices, is_full = None):

        self.symbol = symbol.upper()
        self.order = len(spin)
        self.spin = spin
        self.indices = indices

        if is_full is None:
            self.is_full = [False] * len(indices)
        else:
            self.is_full = is_full

        self.get_slices()
        self.contracted_indices = None

    def get_slices(self):
        self.act_spin_slices = []
        self.ph_slices = []
        self.act_ph_slices = []
        for i, char in enumerate(self.indices):
            index_type = type_of_index(char)
            spin_index = self.spin_of_index(i)
            if index_type == 'active_hole':
                self.ph_slices.append('o')
                self.act_ph_slices.append('O')
                if self.is_full[i]:
                    self.act_spin_slices.append(':')
                else:
                    self.act_spin_slices.append(''.join(['O', spin_index]))
            if index_type == 'inactive_hole':
                self.ph_slices.append('o')
                self.act_ph_slices.append('o')
                if self.is_full[i]:
                    self.act_spin_slices.append(':')
                else:
                    self.act_spin_slices.append(''.join(['o', spin_index]))
            if index_type == 'active_particle':
                self.ph_slices.append('v')
                self.act_ph_slices.append('V')
                if self.is_full[i]:
                    self.act_spin_slices.append(':')
                else:
                    self.act_spin_slices.append(''.join(['V', spin_index]))
            if index_type == 'inactive_particle':
                self.ph_slices.append('v')
                self.act_ph_slices.append('v')
                if self.is_full[i]:
                    self.act_spin_slices.append(':')
                else:
                    self.act_spin_slices.append(''.join(['v', spin_index]))

    def spin_of_index(self, i):
        double_spin_string = self.spin * 2
        return double_spin_string[i]

    def to_index_string(self):
        return ''.join([self.symbol, '.', self.spin, '(', self.indices, ')'])

    def to_sliced_string(self, active_object=True):
        if not active_object:
            slices = ''
            for sl in self.act_spin_slices:
                slices += str(sl) + ',' + ' '
            return ''.join([self.symbol, '.', self.spin, '.', ''.join(self.ph_slices), '[', slices[:-2], ']'])
        else:
            return ''.join([self.symbol, '.', self.spin, '.', ''.join(self.act_ph_slices)])

    def __eq__(self, other) :
        return self.__dict__ == other.__dict__

if __name__ == "__main__":

    t = Term('T', 'aab', 'Abfijn')
    print(t.to_string(active_object=True))

    h = Term('H', 'bb', 'cnKf')
    print(h.to_string(active_object=False))

    h2 = Term('H', 'bb', 'cnKf')
    print(h.to_string(active_object=False))

    expr = BinaryExpression(1.0, 1.0, h, t)
    print(expr.A.contracted_indices)
    print(expr.B.contracted_indices)
