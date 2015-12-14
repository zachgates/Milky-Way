import shorthand as sh


# Synced Lists


class Empty(object):
    pass


class ParallelLists(object):
    
    def __init__(self, *args):
        """Initialize lists with names in N"""
        self.lists = {i: [] for i in list(args)}
    
    def append(self, *args, **kwargs):
        """Push args to the list named kwargs['sl']"""
        K = kwargs['sl']
        for k, v in self.lists.items():
            for N in args:
                if k == K:
                    self.lists[k].append(N)
                else:
                    self.lists[k].append(Empty())

    def merge(self):
        """Merge lists into a single list"""
        merged = []
        for m in zip(*self.lists.values()):
            m = [n for n in m if not sh._is(n, Empty)]
            if len(m) == 1:
                merged.append(m[0])
            else:
                return []
        return merged
