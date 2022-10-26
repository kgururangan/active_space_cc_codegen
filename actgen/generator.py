from actgen.diagramperms import generate_active_permutations
from actgen.weights import get_permutation_weight
from actgen.contraction import contract
from actgen.indices import type_of_index, index_classification
from actgen.utilities import sign_to_str
from math import factorial

class Generator:

    def __init__(self, projection, projection_spincase, num_active,
                 output_quantity=None, output_label='dT', full_asym_weight=None, active_contract=True,
                 active_obj_A=False, active_obj_B=True,
                 print_vo_slices_A=True, print_vo_slices_B=False,
                 print_ph_slices_A=True, print_ph_slices_B=True,
                 active_output_quantity=True):

        # overall projection (e.g., ABCIJK, ABcIJK, etc.)
        self.projection = projection
        # projection spincase (aaa, aab, abb, bbb, aa, ab, bb, a, b)
        self.projection_spincase = projection_spincase
        # number of active
        self.num_active = num_active
        self.active_contract = active_contract
        self.active_obj_A = active_obj_A
        self.active_obj_B = active_obj_B
        self.active_output_quantity=active_output_quantity
        self.use_vo_slicing_A = print_vo_slices_A
        self.use_vo_slicing_B = print_vo_slices_B
        self.use_ph_slicing_A = print_ph_slices_A
        self.use_ph_slicing_B = print_ph_slices_B
        self.contractions = []
        self.permutation_weights = []

        self.number_terms = 0

        if full_asym_weight is None:
            self.get_full_asym_weight()
        else:
            self.full_asym_weight = full_asym_weight

        if output_quantity is None:
            self.get_default_output_label(output_label)
        else:
            self.output_quantity = output_quantity

    def generate(self, expression):

        # generate all unique active-space diagram permutations
        unique_expressions = generate_active_permutations(expression, self.projection_spincase)

        # loop over uniquely permuted diagrams
        for expr in unique_expressions:

            #print(expr.to_string())    # uncomment to print the unique diagram terms

            if self.active_contract:
                # get all possible active-space contractions by splitting the contraction lines into active/inactive
                self.contractions.append(contract(expr, self.num_active))
            else:
                self.contractions.append([expr])
            self.permutation_weights.append(get_permutation_weight(expr, self.projection_spincase))

    def get_default_output_label(self, label):

        self.output_quantity = label+'.' + self.projection_spincase

        if self.active_output_quantity:
            self.output_quantity += '.'
            for inm, op in enumerate(self.projection):
                if type_of_index(op) == 'active_hole':
                    self.output_quantity += 'O'
                if type_of_index(op) == 'active_particle':
                    self.output_quantity += 'V'
                if type_of_index(op) == 'inactive_hole':
                    self.output_quantity += 'o'
                if type_of_index(op) == 'inactive_particle':
                    self.output_quantity += 'v'
        else:
            slices = []
            double_spin_string = self.projection_spincase * 2
            for inm, op in enumerate(self.projection):
                if type_of_index(op) == 'active_hole':
                    slices.append( ''.join( ['O', double_spin_string[inm]] ) )
                if type_of_index(op) == 'active_particle':
                    slices.append( ''.join( ['V', double_spin_string[inm]] ) )
                if type_of_index(op) == 'inactive_hole':
                    slices.append( ''.join( ['o', double_spin_string[inm]] ) )
                if type_of_index(op) == 'inactive_particle':
                    slices.append( ''.join( ['v', double_spin_string[inm]] ) )
            self.output_quantity += '[' + ', '.join(slices) + ']'



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
                  + expr.A.to_sliced_string(active_object=self.active_obj_A, use_vo_slices=self.use_vo_slicing_A, use_ph_slices=self.use_ph_slicing_A) + ', '
                  + expr.B.to_sliced_string(active_object=self.active_obj_B, use_vo_slices=self.use_vo_slicing_B, use_ph_slices=self.use_ph_slicing_B) + ', '
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
        self.full_asym_weight *= factorial(n_act)
        self.full_asym_weight *= factorial(n_inact)

        n_act = 0
        n_inact = 0
        for p in indices['a']['particles']:
            if p.upper() in self.projection:
                n_act += 1
            if p.lower() in self.projection:
                n_inact += 1
        self.full_asym_weight *= factorial(n_act)
        self.full_asym_weight *= factorial(n_inact)

        n_act = 0
        n_inact = 0
        for h in indices['b']['holes']:
            if h.upper() in self.projection:
                n_act += 1
            if h.lower() in self.projection:
                n_inact += 1
        self.full_asym_weight *= factorial(n_act)
        self.full_asym_weight *= factorial(n_inact)

        n_act = 0
        n_inact = 0
        for p in indices['b']['particles']:
            if p.upper() in self.projection:
                n_act += 1
            if p.lower() in self.projection:
                n_inact += 1
        self.full_asym_weight *= factorial(n_act)
        self.full_asym_weight *= factorial(n_inact)
