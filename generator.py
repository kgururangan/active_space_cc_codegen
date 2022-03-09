from diagramperms import generate_active_permutations
from weights import get_permutation_weight
from contraction import contract
from indices import type_of_index, index_classification
from utilities import sign_to_str
from math import factorial

class Generator:

    def __init__(self, projection, projection_spincase, num_active, output_quantity=None, full_asym_weight=None):
        self.projection = projection
        self.projection_spincase = projection_spincase
        self.num_active = num_active
        self.contractions = []
        self.permutation_weights = []

        self.number_terms = 0

        if full_asym_weight is None:
            self.get_full_asym_weight()
        else:
            self.full_asym_weight = full_asym_weight

        if output_quantity is None:
            self.get_output_label()
        else:
            self.output_quantity = output_quantity

    def generate(self, expression):

        # generate all unique active-space diagram permutations
        unique_expressions = generate_active_permutations(expression, self.projection_spincase)

        # loop over uniquely permuted diagrams
        for expr in unique_expressions:
            # get all possible active-space contractions by splitting the contraction lines into active/inactive
            self.contractions.append(contract(expr, self.num_active))
            self.permutation_weights.append(get_permutation_weight(expr, self.projection_spincase))

    def get_output_label(self):

        self.output_quantity = 'dT.' + self.projection_spincase + '.'

        for inm, op in enumerate(self.projection):
            if type_of_index(op) == 'active_hole':
                self.output_quantity += 'O'
            if type_of_index(op) == 'active_particle':
                self.output_quantity += 'V'
            if type_of_index(op) == 'inactive_hole':
                self.output_quantity += 'o'
            if type_of_index(op) == 'inactive_particle':
                self.output_quantity += 'v'

    def print_expression(self):
        # for expressions, perm_weight in zip(self.contractions, self.permutation_weights):
        #     yield self.expression_to_string(expressions, perm_weight)
        self.number_terms = 0
        for expressions, perm_weight in zip(self.contractions, self.permutation_weights):
            self.expression_to_string(expressions, perm_weight)
            self.number_terms += 1
        print("# of terms = ", self.number_terms)


    def expression_to_string(self, expressions, weight):
        # print the term
        print(self.output_quantity + ' += (' + str(weight) + '/' + str(self.full_asym_weight) + ') * (')

        for expr in expressions:
            print('        ' + sign_to_str(expr.sign) + str(expr.weight) + '*'
                  + 'np.einsum(' + "'" + expr.A.indices + ',' +  expr.B.indices + '->' + self.projection + "'" + ', '
                  + expr.A.to_sliced_string(active_object=False) + ', '
                  + expr.B.to_sliced_string(active_object=True) + ', '
                  + 'optimize=True)')
        print(')')


    def get_full_asym_weight(self):
        self.full_asym_weight = 1.0
        particles = index_classification['fixed particles']
        holes = index_classification['fixed holes']

        indices = {'a' : {'holes' : [], 'particles' : []},
                   'b' : {'holes' : [], 'particles' : []}}
        double_spin_string = self.projection_spincase * 2
        for p in particles:
            idx = self.projection.rfind(p.lower())
            if idx == -1:
                idx = self.projection.rfind(p.upper())
            indices[double_spin_string[idx]]['particles'].append(p)
        for h in holes:
            idx = self.projection.rfind(h.lower())
            if idx == -1:
                idx = self.projection.rfind(h.upper())
            indices[double_spin_string[idx]]['holes'].append(h)

        n_act = 0
        n_inact = 0
        for h in indices['a']['holes']:
            if h.upper() in self.projection:
                n_act += 1
            if h.lower() in self.projection:
                n_inact += 1
        if n_act > 0: self.full_asym_weight *= factorial(n_act)
        if n_inact > 0: self.full_asym_weight *= factorial(n_inact)

        n_act = 0
        n_inact = 0
        for p in indices['a']['particles']:
            if p.upper() in self.projection:
                n_act += 1
            if p.lower() in self.projection:
                n_inact += 1
        if n_act > 0: self.full_asym_weight *= factorial(n_act)
        if n_inact > 0: self.full_asym_weight *= factorial(n_inact)

        n_act = 0
        n_inact = 0
        for h in indices['b']['holes']:
            if h.upper() in self.projection:
                n_act += 1
            if h.lower() in self.projection:
                n_inact += 1
        if n_act > 0: self.full_asym_weight *= factorial(n_act)
        if n_inact > 0: self.full_asym_weight *= factorial(n_inact)

        n_act = 0
        n_inact = 0
        for p in indices['b']['particles']:
            if p.upper() in self.projection:
                n_act += 1
            if p.lower() in self.projection:
                n_inact += 1
        if n_act > 0: self.full_asym_weight *= factorial(n_act)
        if n_inact > 0: self.full_asym_weight *= factorial(n_inact)
