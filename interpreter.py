import operator
import sys

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

    return [char for char in sanitized_program.split() if char]

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
    >>> parse ("(begin (define r 10) (* pi (* r r)))")
    [['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]]
    >>> parse ("(begin (define r 10))")
    [['begin', ['define', 'r', 10]]]
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
    def __init__(self, initial_env=None, parent=None):
        self.parent = parent
        self.bindings = initial_env if initial_env else {}

    def find(self, var):
        """Inner environments shadow outer envs. As such, we return the
        value assigned in the inner most env
         """
        if var in self.bindings:
            return self.bindings[var]
        elif self.parent:
            return self.parent.find(var)
        else:
            error = NameError(f"unbound variable: {var}")
            raise error

    def define(self, name, value):
        self.bindings[name] = value

class Procedure():
    def __init__(self, params, body, parent_env):
        '''
        A function has parameters, the body of the function itself, and a
        parent env. We have to store the parent env, since the body of the function
        creates a different scope, and we don't want to clobber the parent scope.
        '''
        self.params = params
        self.body = body
        self.parent_env = parent_env

    def __call__(self, *args):
        """
        To run a procedure, we need the arguments -- which we'll compare
        against the params of the function. If the lengths are different,
        return an error, otherwise, create a new Env with the args assigned to
        the params, and evaluate the body of the function with that env.
        """
        assert len(args) == len(self.params), \
            f"Number of arguments does not match the number of parameters: args:{len(args)}, params:{len(self.params)}"
        initial_env = dict(zip(self.params, args))
        function_scope = Env(initial_env, parent = self.parent_env)
        return my_eval_exp(self.body, function_scope)

def create_starter_env():
    # TODO: Add more to our starter env.
    return \
        Env(initial_env =
            {'+': operator.add, '-': operator.sub,
             '*': operator.mul, '/': operator.truediv,
             '=': operator.eq, '>': operator.gt,
             '<': operator.lt
             })

global_env = create_starter_env()


def my_eval_exp(exp: list, env: Env = global_env):
    '''
    Now, given an expression from the ast of our program, evaluates the expression.
    >>> my_eval_exp (parse("(quote (+ 1 2))")[0])
    ['+', 1, 2]
    >>> my_eval_exp (parse("2")[0])
    2
    >>> my_eval_exp (parse("(define a 10)")[0])
    >>> my_eval_exp(parse("(+ a a)")[0])
    20
    >>> my_eval_exp (parse ("((lambda (x) (+ x x)) 5)")[0])
    10
    >>> my_eval_exp(parse("(begin (define r 10) (* r r))")[0])
    100
    '''
    if isinstance(exp, str):
        return env.find(exp)

    elif isinstance(exp, (int, float)):
        return exp

    elif exp[0] == 'begin':
        return my_eval(exp[1:], env)

    # If we have a symbol, we return the symbol.
    elif exp[0] == 'quote':
        return exp[1]

    # If our expression is of type "define name <exp>"
    elif exp[0] == 'define':
        env.define(exp[1], my_eval_exp(exp[2], env))

    # If our expression is of type if cond then consequent else alternate
    elif exp[0] == 'if':
        if my_eval_exp(exp[1], env):
            return my_eval_exp(exp[2], env)
        else:
            return my_eval_exp(exp[3], env)

    # If we have (lambda (x) <exp>), we want to create a new procedure. Note
    # that we have to write a separate construction to represent a lambda since
    # these can be stored in a variable
    elif exp[0] == 'lambda':
        params = exp[1]
        body = exp[2]
        return Procedure(params, body, env)

    # If its none of our keywords, it must be a procedure application. We try
    # to eval the procedure application. If it doesn't exist, raise, otherwise,
    # we run it, with the evaluated results of the args
    else:
        maybe_proc = my_eval_exp(exp[0], env)
        args = [my_eval_exp(arg, env) for arg in exp[1:]]
        return maybe_proc(*args)

def my_eval (program : list, env = global_env):
    '''
    Runs my_eval_proc on every expression in our program.

    >>> my_eval(parse("(define r 10)(* r r)"))
    100
    '''
    last_result = None
    for exp in program:
        last_result = my_eval_exp(exp, env)

    return last_result


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print(f"Incorrect use of interpreter. Either pass in a file to run the program, or no arguments to enter REPL mode.")
        exit(1)
    elif(len(sys.argv) == 2):
        with open(sys.argv[1]) as program_file:
            program = program_file.read()
            my_eval(parse(program))
    else:
        while(True):
            try:
                expression = input("> ")

            except EOFError:
                exit(0)

            try:
                parsed_exp = parse(expression)

            except Exception as err:
                print(f"Invalid expression. Error: {err}")
                continue

            try:
                evaluated_exp = my_eval(parsed_exp)
            except Exception as e:
                print(f"Error: {e}")
                continue

            if evaluated_exp is not None:
                print(evaluated_exp)
