from collections import defaultdict
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol, tree_mode):
        if self.is_terminal(symbol): return  symbol
        else:
            expansion =  self.random_expansion(symbol)
            out = " ".join(self.gen(s, tree_mode) for s in expansion)
            if tree_mode:
                return "(" + symbol + " " + out + ")"
            return out


    def random_sent(self, k, tree_mode):
        out = ''
        for i in xrange(k):
            out += self.gen("ROOT", tree_mode) + '\n'
        return out[:-1]

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0:
                return r
        return r


if __name__ == '__main__':

    import sys

    args = sys.argv
    pcfg = PCFG.from_file(args[1])
    tree_mode = False

    k=1
    if '-n' in args:
        k = sys.argv[3]

    if '-t' in args:
        tree_mode = True

    output = pcfg.random_sent(int(k), tree_mode)


    print(output)