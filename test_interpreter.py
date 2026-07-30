import interpreter
import pytest

fib = \
    """
    (define fib
      (lambda (x)
        (if (< x 0)
         0
         (if (= x 1)
             1
             (+ (fib (- x 2))
             (fib (- x 1)))))))
    """
double_lambda = "(lambda (n) (lambda (x) (+ n x)))"

def test_parser():
    fib_ast = ['define', 'fib',
               ['lambda', ['x'],
                ['if', ['<', 'x', 0],
                 0,
                 ['if',
                  ['=', 'x', 1],
                  1,
                  ['+',
                   ['fib', ['-', 'x', 2]],
                   ['fib', ['-', 'x', 1]]]]]]]

    assert interpreter.parse(fib) == [fib_ast]
    assert interpreter.parse(f"{fib} (fib 5)") == [fib_ast, ['fib', 5]]

def test_eval():
    inner_scope_overrides_outer =\
    """
    (define x 10)

    (define a
      (lambda (x)
        (+ x x)))

    (a 2)

    x
    """

    function_call_with_wrong_arg_length =\
    """
    (define add
    (lambda (x a)
    (+ x a)))

    (add 3 2 4)
    """

    # Evaluation can't happen if we have more arguments than params.
    with pytest.raises(AssertionError):
        interpreter.my_eval(interpreter.parse(function_call_with_wrong_arg_length))

    # Test that inner scope takes precedence over outer scope
    assert interpreter.my_eval(interpreter.parse(inner_scope_overrides_outer)) == 10

    # Test to show double lambdas work
    assert interpreter.my_eval(interpreter.parse(f"(({double_lambda} 5) 3)")) == 8

    # Numbers eval to numbers
    assert interpreter.my_eval(interpreter.parse("2")) == 2

    # Addition works
    assert interpreter.my_eval(interpreter.parse("(+ 1 2)")) == 3

    # Recursion works!
    assert interpreter.my_eval(interpreter.parse(f"{fib} (fib 5)")) == 5
