# TODO: from/to should follow inheritance even when defined outside of the class

from collections import defaultdict
import inspect

_g_classmap = defaultdict(dict)

class CastError(Exception):
    def __str__(self):
        return "%s: %s >> %s" % (self[0], self[1], self[2])


def bfs(initial, expand):
    open_q = collections.deque(list(initial))
    visited = set(open_q)
    while open_q:
        node = open_q.popleft()
        yield node
        for next_node in expand(node):
            if next_node not in visited:
                visited.add(next_node)
                open_q.append(next_node)



def _add_cast_function(orig, target, f):
    if target in _g_classmap[orig]:
        raise ValueError("Duplicate function", orig, target)
    _g_classmap[orig][target] = f


def _get_cast_elements(cls_module, cls, attr):
    direction, other_cls_name = attr.split('__', 1)
    assert direction in ('from', 'to')
    try:
        other_cls = getattr(cls_module, other_cls_name)
    except AttributeError:
        other_cls = __builtins__[other_cls_name]

    if direction == 'to':
        orig, target = cls, other_cls
        f = getattr(cls, attr)
    else:
        orig, target = other_cls, cls
        # g = getattr(cls, attr).__func__   # Python 2.7
        g = getattr(cls, attr)
        def f(self, cls):
            return g(cls, self)
        f.__name__ = g.__name__

    return orig, target, f

def _cast(instance, orig_cls, target_cls):
    try:
        return _g_classmap[orig_cls][target_cls](instance, target_cls)
    except KeyError:
        breadcrumbs = {}
        def expand(n):
            for k in _g_classmap[n]:
                if k not in breadcrumbs:
                    breadcrumbs[k] = n
                yield k
        for x in bfs([orig_cls], expand):
            if x == target_cls:
                break
        else:
            raise CastError("Couldn't find a cast path", orig_cls, target_cls)

        x = target_cls
        path = []
        while x != orig_cls:
            path.append(x)
            x = breadcrumbs[x]
        path.reverse()

        prev = orig_cls
        inst = instance
        for n in path:
            inst = _g_classmap[prev][n](inst, n)
            prev = n
        return inst

def cast_instance(instance, target_cls):
    "Attempt to cast an instance to the target class"
    # Not using type() because it requires inheritance from object
    return _cast(instance, instance.__class__, target_cls)


def typecast_decor(cls):
    "Class decorator to activate typecast magic. For full functionality, use Typecast metaclass"
    cls_module = inspect.getmodule(cls)
    for attr in dir(cls):
        if attr.startswith(('from__', 'to__')):
            orig, target, f = _get_cast_elements(cls_module, cls, attr)

            _add_cast_function(orig, target, f)
            # TODO remove original functions?

    cls.__rshift__ = cast_instance
    cls.__rlshift__ = cast_instance
    return cls

class Typecast(type):
    "Metaclass to activate typecast magic on class"
    def __init__(cls, name, bases, nmspc):
        super(Typecast, cls).__init__(name, bases, nmspc) 

        typecast_decor(cls)

    # classmethods
    def __lshift__(cls, inst):
        return cast_instance(inst, cls)
    __rrshift__ = __lshift__


def _match_annotations_decor(f, match):
    names = list(f.__code__.co_varnames)
    annotations = f.__annotations__
    indices = [(names.index(n), a) for n,a in annotations.items()]
    def _inner(*args, **kwargs):
        args = list(args)
        for i, ann in indices:
            if i >= len(args):
                break
            args[i] = _autocast_match(args[i], ann)

        for name, val in kwargs.items():
            if name in annotations:
                kwargs[name] = _autocast_match(val, annotations[name])

        return f(*args, **kwargs)

    return _inner

# def _verify_match(inst, type_):
#     assert isinstance(inst, type_), "Expected type: '%s'. Instead got '%s'" % (type_, inst.__class__)

def _autocast_match(inst, type_):
    if isinstance(inst, type_):
        return inst
    else:
        return cast_instance(inst, type_)


def autocast(f):
    return _match_annotations_decor(f, _autocast_match)

# def verify_types(f):
#     return _match_annotations_decor(f, _verify_match)


