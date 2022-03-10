from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection

import argparse

def main(args):

    projection = args.projection

    g = Generator(projection, 'aab', 1)

    expressions = [
        BinaryExpression(-1.0, 1.0, Term('H', 'a', 'mI'), Term('T', 'aab', 'ABCmJK')),
        BinaryExpression(-1.0, 1.0, Term('H', 'b', 'mK'), Term('T', 'aab', 'ABCIJm')),
        BinaryExpression(+1.0, 1.0, Term('H', 'a', 'Ae'), Term('T', 'aab', 'eBCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'b', 'Ce'), Term('T', 'aab', 'ABeIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnIJ'), Term('T', 'aab', 'ABCmnK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnJK'), Term('T', 'aab', 'ABCImn')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'ABef'), Term('T', 'aab', 'efCIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'BCef'), Term('T', 'aab', 'AefIJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'AmIe'), Term('T', 'aab', 'eBCmJK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'AmIe'), Term('T', 'abb', 'BeCJmK')),
        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mCeK'), Term('T', 'aaa', 'ABeIJm')),
        BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'CmKe'), Term('T', 'aab', 'ABeIJm')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'AmeK'), Term('T', 'aab', 'eBCIJm')),
        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mCIe'), Term('T', 'aab', 'ABemJK'))
    ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds T3_aab CCSDt update for specified projection.")
    parser.add_argument('projection',
                        help="String, for example 'AbcIJK', specifying the desired outward line projection.")
    args = parser.parse_args()

    main(args)