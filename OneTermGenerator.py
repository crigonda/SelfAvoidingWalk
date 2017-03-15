"""Pseudo random congruential generator, using one term reccurence."""

DEF_MOD_VAL = 2147483647
DEF_MULT_VAL = 16807
DEF_SEED_VAL = 10

class OneTermGenerator(object):
    """ Prime modulus multiplicative linear congruential generator. """

    # Constructor
    def __init__(self, m=DEF_MOD_VAL, a=DEF_MULT_VAL, s=DEF_SEED_VAL):
        self.mod = m
        self.mult = a
        self.seed = s

    def changeModulo(self, m):
        """Changes the modulo."""
        valid = False
        try:
            m = int(m)
            # The modulo must be positive, and superior to the seed
            if m > 0 and m > self.seed:
                self.mod = m
                valid = True
        except ValueError:
            pass
        return valid

    def changeMultiplier(self, a):
        """Changes the multiplier."""
        valid = False
        try:
            a = int(a)
            # The multiplier must be positive and inferior to the modulo
            if a < self.mult and a > 0:
                self.mult = a
                valid = True
        except ValueError:
            pass
        return valid

    def changeSeed(self, s):
        """Changes the seed."""
        valid = False
        try:
            s = int(s)
            # The seed must be positive and inferior to the modulo
            if s < self.mod and s > 0:
                self.seed = s
                valid = True
        except ValueError:
            pass
        return valid

    def generate(self):
        """Generates a pseudo random number."""
        self.seed = self.mult * self.seed % self.mod
        return self.seed / self.mod
