from typing import Any


def sig(obj: Any):
    from inspect import signature, Parameter
    params = []

    star = '_star_'
    for pn, cp in vars(obj.__class__).items():
        # property name , class property
        kw_only = True if pn==star else False # expected only once
        
        if isinstance(cp, property): # props will be taken as args
            if kw_only:
                if pn.startswith(star):
                    k = Parameter.VAR_KEYWORD
                else:
                    k = Parameter.KEYWORD_ONLY
            else:
                if pn.startswith(star):
                    k = Parameter.VAR_POSITIONAL
                else:
                    k = Parameter.POSITIONAL_OR_KEYWORD

            r = getattr(obj, pn)
            d = Parameter.empty if (r == ...) else r
            a = signature(cp.fget).return_annotation
            arg = Parameter(pn, k, default=d, annotation=a)
            params.append(arg)

    sig = Signature(params)
    return sig


from inspect import Signature
def redefine(f: callable, sig: Signature):
    f.__signature__ = sig
    return f

def decorator(obj):
    def f(_f):
        return redefine(_f, sig(obj))
    return f
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Something is happening after the function is called.")
        return result
    return wrapper



def test(): 
    class Obj:
        @property
        def p(self) -> int: return ...  #
        _star_ = ''
        @property
        def z(self): return 'z'
        @property
        def a(self): return 'a'
    
    @decorator(Obj())
    def f(x, y): ...
    return f

    _ = Obj()
    _ = sig(_)
    return _


def _test():
    import inspect
    def my_function(a, b=10, *, c, **kwargs):
        pass
    sig = inspect.signature(my_function)
    for name, param in sig.parameters.items():
        print(f"Parameter '{name}': Kind = {param.kind}, Default = {param.default if param.default is not inspect.Parameter.empty else 'No Default'}")
    # Output:
    # Parameter 'a': Kind = POSITIONAL_OR_KEYWORD, Default = No Default
    # Parameter 'b': Kind = POSITIONAL_OR_KEYWORD, Default = 10
    # Parameter 'c': Kind = KEYWORD_ONLY, Default = No Default
    # Parameter 'kwargs': Kind = VAR_KEYWORD, Default = No Default
