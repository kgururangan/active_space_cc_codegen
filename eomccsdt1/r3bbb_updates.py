from actgen.term import Term, BinaryExpression
from actgen.generator import Generator
from actgen.utilities import change_term_to_projection

import argparse

def main(args):
    projection = args.projection

    residual_term = 'x3d'

    g = Generator(projection, 'bbb', 0,
                  active_contract=False,
                  output_quantity='x3d',
                  active_obj_A=False, active_obj_B=False,
                  print_ph_slices_A=True, print_ph_slices_B=False)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('X', 'bb', 'BmJI', is_full=[False, True, False, False]),
                         Term('T', 'bb', 'ACmK', is_full=[False, False, True, False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'BmJI', is_full=[False, True, False, False]),
                         Term('R', 'bb', 'ACmK', is_full=[False, False, True, False])),
        BinaryExpression(+1.0, 1.0, Term('X', 'bb', 'BAJe', is_full=[False, False, False, True]),
                         Term('T', 'bb', 'eCIK', is_full=[True, False, False, False])),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'BAJe', is_full=[False, False, False, True]),
                         Term('R', 'bb', 'eCIK', is_full=[True, False, False, False])),
    ]

    for expression in expressions:
        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

    g = Generator(projection, 'bbb', 1, output_quantity=residual_term)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('X', 'b', 'Be'), Term('T', 'bbb', 'AeCIJK')),
        BinaryExpression(-1.0, 1.0, Term('X', 'b', 'mJ'), Term('T', 'bbb', 'ABCImK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'bb', 'mnIJ'), Term('T', 'bbb', 'ABCmnK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'bb', 'ABef'), Term('T', 'bbb', 'efCIJK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'bb', 'BmJe'), Term('T', 'bbb', 'AeCimK')),
        BinaryExpression(+1.0, 1.0, Term('X', 'ab', 'mBeJ'), Term('T', 'abb', 'eCAmKI')),
        BinaryExpression(-1.0, 1.0, Term('H', 'b', 'mJ'), Term('R', 'bbb', 'ABCImK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'b', 'Be'), Term('R', 'bbb', 'AeCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'mnIJ'), Term('R', 'bbb', 'ABCmnK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'ABef'), Term('R', 'bbb', 'efCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'AmIe'), Term('R', 'bbb', 'eBCmJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mAeI'), Term('R', 'abb', 'eCBmKJ')),
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Builds R3_bbb EOMCCSDt update for specified projection.")
    parser.add_argument('projection', type=str, help="String, for example 'AbcIJK', specifying the desired outward line projection.")
    #parser.add_argument('--n', '-number', type=str, help='Numerical representation of active/inactive indices defining projection, e.g., 111011.')
    args = parser.parse_args()

    main(args)