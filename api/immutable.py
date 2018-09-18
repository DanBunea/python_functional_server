import functools
import collections

Immutable = collections.namedtuple('Immutable',"data errors")

#Immutability
def to_namedtuple(dictionary):
    NT = collections.namedtuple('Immutable', dictionary.keys())
    gen_dict = NT(**dictionary)
    return gen_dict

def from_namedtuple(tup):
    d = dict()
    for f in tup._fields:
        d[f] = getattr(tup,f)
    return d

def deep_freeze(dictionary):
    assert dictionary!=None
    assert isinstance(dictionary, dict)
    return to_namedtuple(dictionary)


def pi_change(path, val, obj):
    assert path!=None
    assert obj!=None
    # assert "Immutable" in str(type(obj))

    if hasattr(obj, path):
        dic = dict()
        dic[path]=val
        return obj._replace(**dic)
    else:
        obj_dict = from_namedtuple(obj)
        obj_dict[path]=val
        return to_namedtuple(obj_dict)


def change(key="data", val=None):
    def inner_change(state):
        return pi_change(key, val, state)
    return inner_change


def pi_value(path,obj):
    assert path!=None,"pi_value. path cannot be None"
    assert obj!=None,"pi_value. object cannot be None"
    assert "Immutable" in str(type(obj)), "pi_value expected Immutable but was" +  str(type(obj))
    assert hasattr(obj,path),"pi_value. Expected object to have"+str(path)

    return getattr(obj, path)


def curry(*args, **create_time_kwds):
    func = args[0]
    create_time_args = args[1:]
    def curried_function(*call_time_args, **call_time_kwds):
        args = create_time_args + call_time_args
        kwds = create_time_kwds.copy()
        kwds.update(call_time_kwds)
        return func(*args, **kwds)
    return curried_function


def value(key="data"):
    return curry(pi_value, key)
