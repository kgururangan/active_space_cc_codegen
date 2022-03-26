from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection

import argparse

def main(args):

    projection = args.projection

    #residual_term = 'dR.aaa.' + get_label_from_projection(projection)
    residual_term = 'x3c'

    g = Generator(projection, 'abb', 0,
                  active_contract=False,
                  output_quantity='x3c',
                  active_obj_A=False, active_obj_B=False,
                  print_ph_slices_A=True, print_ph_slices_B=False)

    expressions = [
        BinaryExpression(+1.0, 1.0, Term('X', 'ab', 'ABIe', is_full=[False, False, False, True]),
                         Term('T', 'bb', 'eCJK', is_full=[True,False,False,False])),
        BinaryExpression(-1.0, 1.0, Term('X', 'ab', 'AmIJ', is_full=[False, True, False, False]),
                         Term('T', 'bb', 'BCmK', is_full=[False, False, True, False])),
        BinaryExpression(+1.0, 1.0, Term('X', 'bb', 'CBKe', is_full=[False, False, False, True]),
                         Term('T', 'ab', 'AeIJ', is_full=[False, True, False, False])),
        BinaryExpression(-1.0, 1.0, Term('X', 'bb', 'CmKJ', is_full=[False, True, False, False]),
                         Term('T', 'ab', 'ABIm', is_full=[False, False, False, True])),
        BinaryExpression(+1.0, 1.0, Term('X', 'ab', 'ABeJ', is_full=[False, False, True, False]),
                         Term('T', 'ab', 'eCIK', is_full=[True, False, False, False])),
        BinaryExpression(-1.0, 1.0, Term('X', 'ab', 'mBIJ', is_full=[True, False, False, False]),
                         Term('T', 'ab', 'ACmK', is_full=[False, False, True, False])),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'ABIe', is_full=[False, False, False, True]),
                         Term('R', 'bb', 'eCJK', is_full=[True,False,False,False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'AmIJ', is_full=[False, True, False, False]),
                         Term('R', 'bb', 'BCmK', is_full=[False, False, True, False])),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'CBKe', is_full=[False, False, False, True]),
                         Term('R', 'ab', 'AeIJ', is_full=[False, True, False, False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'CmKJ', is_full=[False, True, False, False]),
                         Term('R', 'ab', 'ABIm', is_full=[False, False, False, True])),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'ABeJ', is_full=[False, False, True, False]),
                         Term('R', 'ab', 'eCIK', is_full=[True, False, False, False])),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mBIJ', is_full=[True, False, False, False]),
                         Term('R', 'ab', 'ACmK', is_full=[False, False, True, False])),
    ]


    for expression in expressions:
        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

    g = Generator(projection, 'abb', 1, output_quantity=residual_term)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('X', 'a', 'mI'), Term('T', 'abb', 'ABCmJK')),
        BinaryExpression(-1.0, 1.0, Term('X', 'b', 'mJ'), Term('T', 'abb', 'ABCImK')),
        BinaryExpression(1.0, 1.0, Term('X', 'a', 'Ae'), Term('T', 'abb', 'eBCIJK')),
        BinaryExpression(1.0, 1.0, Term('X', 'b', 'Be'), Term('T', 'abb', 'AeCIJK')),
        BinaryExpression(1.0, 1.0, Term('X', 'bb', 'mnJK'), Term('T', 'abb', 'ABCImn')),
        BinaryExpression(1.0, 1.0, Term('X', 'ab', 'mnIJ'), Term('T', 'abb', 'ABCmnK')),
        BinaryExpression(1.0, 1.0, Term('X', 'bb', 'BCef'), Term('T', 'abb', 'AefIJK')),
        BinaryExpression(1.0, 1.0, Term('X', 'ab', 'ABef'), Term('T', 'abb', "efCIJK")),
        BinaryExpression(1.0, 1.0, Term('X', 'aa', 'AmIe'), Term('T', 'abb', 'eBCmJK')),
        BinaryExpression(1.0, 1.0, Term('X', 'ab', 'AmIe'), Term('T', 'bbb', 'eBCmJK')),
        BinaryExpression(1.0, 1.0, Term('X', 'ab', 'mBeJ'), Term('T', 'aab', 'AeCImK')),
        BinaryExpression(1.0, 1.0, Term('X', 'bb', 'BmJe'), Term('T', 'abb', 'AeCImK')),
        BinaryExpression(-1.0, 1.0, Term('X', 'ab', 'mBIe'), Term('T', 'abb', 'AeCmJK')),
        BinaryExpression(-1.0, 1.0, Term('X', 'ab', 'AmeJ'), Term('T', 'abb', 'eBCImK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'a', 'mI'), Term('R', 'abb', 'ABCmJK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'b', 'mJ'), Term('R', 'abb', 'ABCImK')),
        BinaryExpression(1.0, 1.0, Term('H', 'a', 'Ae'), Term('R', 'abb', 'eBCIJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'b', 'Be'), Term('R', 'abb', 'AeCIJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'bb', 'mnJK'), Term('R', 'abb', 'ABCImn')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'mnIJ'), Term('R', 'abb', 'ABCmnK')),
        BinaryExpression(1.0, 1.0, Term('H', 'bb', 'BCef'), Term('R', 'abb', 'AefIJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'ABef'), Term('R', 'abb', "efCIJK")),
        BinaryExpression(1.0, 1.0, Term('H', 'aa', 'AmIe'), Term('R', 'abb', 'eBCmJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'AmIe'), Term('R', 'bbb', 'eBCmJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'mBeJ'), Term('R', 'aab', 'AeCImK')),
        BinaryExpression(1.0, 1.0, Term('H', 'bb', 'BmJe'), Term('R', 'abb', 'AeCImK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mBIe'), Term('R', 'abb', 'AeCmJK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'AmeJ'), Term('R', 'abb', 'eBCImK'))
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds R3_abb EOMCCSDt update for specified projection.")
    parser.add_argument('projection',
                        help="String, for example 'AbcIJK', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)