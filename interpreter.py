import operator

def tokenize (program : str) -> list[str]:
    """
    Tokenizes our program on spaces.

    >>> tokenize ("(begin (define r 10) (* pi (* r r)))")
    ['(', 'begin', '(', 'define', 'r', '10', ')', '(', '*', 'pi', '(', '*', 'r', 'r', ')', ')', ')']
    >>> tokenize ("(define r 10)")
    ['(', 'define', 'r', '10', ')']
    >>> tokenize ("(begin (define r 10))")
    ['(', 'begin', '(', 'define', 'r', '10', ')', ')']
    """

    # Start by first splitting program in tokenizable way. We'll tokenize on
    # spaces, and since spaces aren't required around parens, lets add them
    sanitized_program = program.replace('(', ' ( ').replace(')', ' ) ')

    # Splitting on spaces doesn't make
    return [char for char in sanitized_program.split(' ') if char]

def token_to_number_or_string (token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token

def parse (program : str):
    """
    recursively creates the ast for our program.

    if we find an opening parenthesis (paren), we treat the next symbol as an
    element in our tree, and go to the next symbol. once we find the closing
    paren, we then return the list.

    >>> parse("0")
    [0]
    >>> parse ("10")
    [10]
    >>> parse ("(begin (define r 10) (* pi (* r r)))")
    [['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]]
    >>> parse ("(begin (define r 10))")
    [['begin', ['define', 'r', 10]]]
    >>> parse ("(define r 10)")
    [['define', 'r', 10]]
    >>> parse ("(define r 10) (define d 20)")
    [['define', 'r', 10], ['define', 'd', 20]]
    """
    def rec_parse(local_tree: list, tokenized_program : list[str]):
        # todo think of a way to handle degenerate programs:
        # 1. what if we have a program without parens?
        # 2. what about a program with unmatched parens?
        while tokenized_program:
            token = token_to_number_or_string(tokenized_program.pop(0))

            # if we're entering a new function, we create a new tree.
            if token == '(':
                program_after_paren = rec_parse([], tokenized_program)
                # append the new function to our tree
                local_tree.append(program_after_paren)

            # if we reach the end of the program, we're done with this tree
            elif token == ')':
                return local_tree
            else:
                local_tree.append(token)


        return local_tree

    return rec_parse([], tokenize(program))

class Env():
    def __init__(self, parent=None):
        self.parent = parent
        self.env = {}

        def find(self, var):
            if var in self.env:
                return self.env[var]
            elif var in self.parent:
                return self.parent[var]
            else:
                raise ValueError


def create_starter_env():
    env = Env()
    env.env.update({'+': operator.add, '-': operator.sub})

global_env = create_starter_env


# TODO: Add let expressions.
def my_eval(exp : list, env=global_env):
    '''
    Now, given an expression from the ast of our program, evaluates the expression.
    >>
    >>> my_eval (parse("(define r 10)")[0])
    >>> my_eval (parse("(* r r)")[0])
    >>> my_eval (parse("(+ 2 3)")[0])
    '''
    if isinstance(exp, str):
        return env.find(str)

    elif isinstance(exp, (int, float)):
        return exp

    # If we have a symbol, we return the symbol.
    elif exp[0] == 'quote':
        return exp[1]

    # If our expression is of type "define name <exp>"
    elif exp[0] == 'define':
        env[exp[1]] = my_eval(exp[2], env)

    # If our expression is of type if cond then consequent else alternate
    elif exp[0] == 'if':
        if my_eval(exp[1], env):
            return my_eval(exp[2], env)
        else:
            return my_eval(exp[3], env)

    # If we have a lambda expression
    elif exp[0] == 'lambda':
        return

    else:
