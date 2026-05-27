def parse (program : str):
    """
    Recursively creates the ast for our program.

    If we find an opening parenthesis (paren), we treat the next symbol as an
    element in our tree, and go to the next symbol. Once we find the closing
    paren, we then return the list.

    >>> parse ("(begin (define r 10) (* pi (* r r)))")
    []
    [[[]]]

    """
    def rec_parse (current_tree, program):

        current_word = ""
        for letter_index in range(len(program)):
            current_letter = program[letter_index]
            # TODO Note that this doesn't actually catch any syntax mistakes, it
            # only works on the happy case. We need more than this.
            # Note that it also doesn't really work lol.
            if program [letter_index]== '(':
                # This will add an extra list layer that we don't want
                print (current_tree);
                current_tree.append([parse(program[letter_index + 1:])])
            elif program [letter_index] == ')':
                current_tree.append(current_word)
                print (current_tree);
                return current_tree
            elif program [letter_index] == ' ':
                current_tree.append(current_word)
                current_word = ""
            else:
                current_word = current_word + current_letter
                return current_tree

    return rec_parse([], program)
