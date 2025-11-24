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
    ...to programmatically encode relationships between function arguments.
    ## How?
    Use objects for encoding relationships between arguments.
    Use a decorator to dynamically create a function.
    """)
    return


@app.cell
def _():
    from sigdep import paramize
    paramize
    return (paramize,)


@app.cell
def _(paramize):
    class Params:
        @property
        def p(self) -> int: return ...  # '...' to in
        _star_ = ''
        @property
        def z(self): return 'z'
        @property
        def a(self): return 'a'
        @property
        def k(self): return 'k'

    
    @paramize(Params())
    def f(*, x, y):
        """sdfsdf"""
        return

    #from inspect import signature as sig
    #sig(f).parameters['p'].kind
    f#(3)
    return


if __name__ == "__main__":
    app.run()
