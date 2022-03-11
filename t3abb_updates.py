from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection

import argparse

def main(args):

    projection = args.projection

    g = Generator(projection, 'abb', 1)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('H', 'a', 'mI'), Term('T', 'abb', 'ABCmJK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'b', 'mJ'), Term('T', 'abb', 'ABCImK')),
        BinaryExpression(1.0, 1.0, Term('H', 'a', 'Ae'), Term('T', 'abb', 'eBCIJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'b', 'Be'), Term('T', 'abb', 'AeCIJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'bb', 'mnJK'), Term('T', 'abb', 'ABCImn')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'mnIJ'), Term('T', 'abb', 'ABCmnK')),
        BinaryExpression(1.0, 1.0, Term('H', 'bb', 'BCef'), Term('T', 'abb', 'AefIJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'ABef'), Term('T', 'abb', "efCIJK")),
        BinaryExpression(1.0, 1.0, Term('H', 'aa', 'AmIe'), Term('T', 'abb', 'eBCmJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'AmIe'), Term('T', 'bbb', 'eBCmJK')),
        BinaryExpression(1.0, 1.0, Term('H', 'ab', 'mBeJ'), Term('T', 'aab', 'AeCImK')),
        BinaryExpression(1.0, 1.0, Term('H', 'bb', 'BmJe'), Term('T', 'abb', 'AeCImK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mBIe'), Term('T', 'abb', 'AeCmJK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'AmeJ'), Term('T', 'abb', 'eBCImK'))
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds T3_abb CCSDt update for specified projection.")
    parser.add_argument('projection',
                        help="String, for example 'AbcIJK', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)