import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    #Sigdep

    ## Why?
    To programmatically encode relationships between function arguments.
    Other benefits follow from treating parameters as object properties such as documentation.
    ## How?
    Use objects for encoding relationships between arguments.
    Use a decorator to dynamically create a function.
    """)
    return


@app.cell
def _():
    from sigdep import paramize, var_property
    help(paramize)
    return paramize, var_property


@app.cell
def _(paramize, var_property):
    class Params:
        @property
        def p(self) -> int: return ...  # '...' to in
        _star_ = ''
        @property
        def z(self) -> str: return 'z'
        @property
        def a(self): return 'a'
        @var_property
        def k(self): return ...

    class Params1:
        @var_property
        def l(self): return ...#[]
    
    @paramize(Params1())
    def f1():
        """f1"""
        return

    @paramize(Params())
    def f():
        """sdfsdf"""
        return

    #from inspect import signature as sig
    #sig(f).parameters['p'].kind
    (f1,f)#(3)
    return


if __name__ == "__main__":
    app.run()
