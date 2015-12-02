# Shorthand


def _is(val, typ):
    if isinstance(val, typ):
        return True
    return False

def _either(val1, val2, typ):
    if _is(val1, typ) or _is(val2, typ):
        return True
    return False

def _both(val1, val2, typ):
    if _is(val1, typ) and _is(val2, typ):
        return True
    return False

def _any(vals, typ):
    for i in vals:
        if not _is(i, typ):
            return False
    return True

def _of(vals, typs):
    retval = [any(_is(i, j) for j in typs) for i in vals]
    return all(retval)
