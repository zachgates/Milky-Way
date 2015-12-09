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

def _all(vals, typ):
    for i in vals:
        if not _is(i, typ):
            return False
    return True
    
def _any(vals, typ):
    for i in vals:
        if _is(i, typ):
            return True
    return False

def _of(vals, typs):
    retval = [any(_is(i, j) for j in typs) for i in vals]
    return all(retval)


# Primes


def _isprime(n):
    i = n - 1
    while i > 1:
        if n % i == 0:
            return False
        i -= 1
    return True

def _nprimes(n):
    retval = []
    i = 2
    while len(retval) < n:
        if _isprime(i):
            retval.append(i)
        i += 1
    return retval
