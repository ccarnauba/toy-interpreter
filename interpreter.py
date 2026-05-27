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
    sanitized_program = ""
    for char in program:
        if char == '(':
            sanitized_program = sanitized_program + (' ( ')
        elif char == ')':
            sanitized_program = sanitized_program + (' ) ')
        else:
            sanitized_program = sanitized_program + char

    return [ char for char in sanitized_program.split(' ') if char ]

def parse (program : str):
    """
    Recursively creates the ast for our program.

    If we find an opening parenthesis (paren), we treat the next symbol as an
    element in our tree, and go to the next symbol. Once we find the closing
    paren, we then return the list.

    >>> parse ("(begin (define r 10) (* pi (* r r)))")
    ['begin', ['define', 'r', '10'], ['*', 'pi', ['*', 'r', 'r']]]
    >>> parse ("(begin (define r 10))")
    ['begin', ['define', 'r', '10']]
    >>> parse ("(define r 10)")
    ['define', 'r', '10']
    """
    def rec_parse(local_tree, tokenized_program : list[str]):
        if tokenized_program == []:
            return local_tree

        token = tokenized_program.pop(0)

        while token:
            if token == '(':
                program_after_paren = rec_parse([], tokenized_program)
                local_tree.append(program_after_paren)
            elif token == ')':
                return local_tree
            else:
                local_tree.append(token)

            if tokenized_program:
                token = tokenized_program.pop(0)
            else:
                token = None

        return local_tree

    return rec_parse([], tokenize(program))[0]
