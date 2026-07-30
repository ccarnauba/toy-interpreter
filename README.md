# Toy interpreter

I wanted to learn more about programming languages, so I started working on a
toy lisp interpreter. I have heard about Norvig's famous Lispy, and I
deliberately avoided reading it for this implementation. This toy interpreter
currently supports:

- lambda functions
- if-else statements
- variable definitions
- basic arithmetic operation
- begin
- quote

Notably, we're missing:
- lists
- any kind of garbage collection
- user-friendly error messages
- no tail calls

One fun thing about lisp in python I realized is that we can define most
functions outside of our "eval" function, and we can extend our global scope
quite easily!

I hope to extend this interpreter to include other cool features! In particular,
I'm curious about how languages get optimized, and how they manage to return
instructive and clear errors. I'll likely add more after reading something on
programming languages.

## How to run
This interpreter offers both a REPL and a file input mode. For the REPL call `$
python interpreter.py`, and for the file input, `$ python interpreter.py <my_file>`.
