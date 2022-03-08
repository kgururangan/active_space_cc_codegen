from term import Term, BinaryExpression
from generator import Generator
from utilities import change_term_to_projection, get_label_from_projection

def vt3a_intermediate(projection):

    weight = 1.0
    residual_term = 'I2A_' + get_label_from_projection(projection)

    g = Generator(projection, 'aa', 1, full_asym_weight=weight, output_quantity=residual_term)

    if projection.lower() == 'amij':
        expressions = [
                        BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef', is_full=[True,False,False,False]), Term('T', 'aaa', 'AefIJn')),
                        BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef', is_full=[True,False,False,False]), Term('T', 'aab', 'AefIJn')),
        ]

    if projection.lower() == 'abie':
        expressions = [
                        BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aaa', 'ABfImn')),
                        BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'aab', 'ABfImn'))
        ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()

def vt3b_intermediate(projection):

    weight = 1.0
    residual_term = 'I2B_' + get_label_from_projection(projection)

    g = Generator(projection, 'ab', 1, full_asym_weight=weight, output_quantity=residual_term)

    if projection.lower() == 'amij': # vooo
        expressions = [
                       BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'nmfe'), Term('T', 'aab', 'AfeInJ')),
                       BinaryExpression(+1.0, 1.0, Term('H', 'bb', 'nmfe'), Term('T', 'abb', 'AfeInJ'))
        ]
    if projection.lower() == 'mbij': # ovoo
        expressions = [
                       BinaryExpression(+1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aab', 'efBInJ')),
                       BinaryExpression(+1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'abb', 'efBInJ'))
        ]
    if projection.lower() == 'abej': # vvvo
        expressions = [
                       BinaryExpression(-1.0, 1.0, Term('H', 'aa', 'mnef'), Term('T', 'aab', 'AfBmnJ')),
                       BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'mnef'), Term('T', 'abb', 'AfBmnJ'))
        ]
    if projection.lower() == 'abie': # vvov
        expressions = [
                       BinaryExpression(-1.0, 1.0, Term('H', 'ab', 'nmfe'), Term('T', 'aab', 'AfBImn')),
                       BinaryExpression(-1.0, 1.0, Term('H', 'bb', 'nmfe'), Term('T', 'abb', 'AfBImn'))
        ]

    for expression in expressions:

        expression.A.indices = change_term_to_projection(expression.A.indices, projection)
        expression.B.indices = change_term_to_projection(expression.B.indices, projection)

        g.generate(expression)

    g.print_expression()



if __name__ == "__main__":

    projection = 'AmiJ'

    vt3a_intermediate(projection)

    #vt3b_intermediate(projection)


