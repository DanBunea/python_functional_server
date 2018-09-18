

def compose2(f, g):
    # def run(x):
        #res = f(x)
        # print f.__name__, res
        # return g(f(x))
    return lambda x: g(f(x))
    # return run

#compose n functions
def compose(*functions):
    return reduce(compose2, functions)


def compose_list(functions):
    return reduce(compose2, functions)
