#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
from inspect import signature
# from functools import update_wrapper
from functools import wraps


def disable():
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    return


def decorator(func):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''

    @wraps(func)
    def wrapper():
        __doc__ = func.__doc__
        return func

    return wrapper


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""
    functions = collections.defaultdict(int)

    @wraps(func)
    def wrapper(*args, **kwargs):
        functions[func.__name__] += 1
        print('Function {} calls {} counts'.format(func.__name__, str(functions[func.__name__])))
        original_func = func(*args, **kwargs)
        return original_func

    return wrapper


ARGS, KWARGS, RESULT = (0, 1, 2)


def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    functions = collections.defaultdict(list)

    @wraps(func)
    def wrapper(*args, **kwargs):
        values = functions.get(func.__name__)
        if values:
            for val in values:
                if (val[ARGS] == args) and (val[KWARGS] == kwargs):
                    print('Exist result for function {}'.format(func.__name__))
                    return val[RESULT]

        if kwargs:
            result = func(*args, **kwargs)
        elif args:
            result = func(*args)
        else:
            result = func()

        cache = functions[func.__name__]
        cache.append([args, kwargs, result])
        functions[func.__name__] = cache
        return result

    return wrapper


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''
    @wraps(func)
    def wrapper(*args):
        result = False
        args_count = len(args)
        func_parameters_count = len(signature(func).parameters)

        if args_count > func_parameters_count:
            window = len(args)

            # Get first parametrs
            parm = args[window - func_parameters_count:window:]
            result = func(*parm)
            for i in range(window - func_parameters_count, 0, -1):
                parm = args[i - 1:i:]
                result = func(*parm, result)

        elif args_count == func_parameters_count:
            result = func(*args)

        elif args_count < func_parameters_count:
            result = args[0]

        return result
    return wrapper


def trace(func):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''

    @wraps(func)
    def wrapper(*args):

        return func

    return wrapper


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    # print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    # print("bar was called", bar.calls, "times")

    print(fib.__doc__)
    fib(3)
    # print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
