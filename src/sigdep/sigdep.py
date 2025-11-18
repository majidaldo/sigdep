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
    name = f.__name__
    fs = f"def {name}{sig}:\n"
    body = get_function_body(f)
    body = (' '*4+l for l in body.split('\n'))
    body = '\n'.join(body)
    fs = (fs
        + ((' '*4+'"'*3+f.__doc__+'"'*3+'\n') if f.__doc__ else '')
        + body)
    fl = {}
    exec(fs, locals=fl)
    return fl[name]


def my_function(arg1, arg2):
    """This is a docstring."""
    x = arg1 + arg2
    y = x * 2
    return y

def get_function_body(func):
    import inspect
    source_lines = inspect.getsource(func).splitlines()
    
    # Find the start of the function body (after the 'def' line and potential docstring)
    start_index = 0
    for i, line in enumerate(source_lines):
        if line.strip().startswith("def "):
            start_index = i
            break
    
    # If a docstring exists, find its end
    if func.__doc__:
        docstring_lines = func.__doc__.splitlines()
        docstring_end_line_content = docstring_lines[-1] if docstring_lines else ""
        
        for i in range(start_index + 1, len(source_lines)):
            if docstring_end_line_content in source_lines[i] and source_lines[i].strip().endswith('"""'):
                start_index = i
                break
    
    # The body starts after the definition line and optional docstring
    body_lines = source_lines[start_index + 1:]
    
    # Dedent the body to remove the function's indentation level
    if body_lines:
        first_line_indentation = len(body_lines[0]) - len(body_lines[0].lstrip())
        dedented_body = [line[first_line_indentation:] for line in body_lines]
        return "\n".join(dedented_body)
    else:
        return ""



def decorator(obj):
    def f(_f):
        return redefine(_f, sig(obj))
    return f



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
    def f(x, y):
        """sdfsdf
        """
        x, y
        x,y
        def inner():
            jj
        ...
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
