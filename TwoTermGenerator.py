"""Pseudo random congruential generator, using two terms reccurence."""

DEF_MOD_VAL = 2147483647
DEF_MULTN2_VAL = 1583458089
DEF_MULTN1_VAL = 784588716
DEF_SEEDN2_VAL = 10
DEF_SEEDN1_VAL = 10

class TwoTermGenerator(object):
    """Linear recursive generator with two terms."""

    # Constructor
    def __init__(self, m=DEF_MOD_VAL, an_2=DEF_MULTN2_VAL, an_1=DEF_MULTN1_VAL,\
    s0=DEF_SEEDN2_VAL, s1=DEF_SEEDN1_VAL):
        self.mod = m
        self.an_2 = an_2
        self.an_1 = an_1
        self.sn_2 = s0
        self.sn_1 = s1

    def changeModulo(self, m):
        """Changes the modulo."""
        valid = False
        try:
            m = int(m)
            # The modulo must be positive, and superior to the seeds
            if m > 0 and m > self.sn_1 and m > self.sn_2:
                self.mod = m
                valid = True
        except ValueError:
            pass
        return valid

    def changeMultiplierN_2(self, an_2):
        """Changes the first multiplier."""
        valid = False
        try:
            an_2 = int(an_2)
            # The multiplier must be positive and inferior to the modulo
            if an_2 < self.mod and an_2 > 0:
                self.an_2 = an_2
                valid = True
        except ValueError:
            pass
        return valid

    def changeMultiplierN_1(self, an_1):
        """Changes the second multiplier."""
        valid = False
        try:
            an_1 = int(an_1)
            # The multiplier must be positive and inferior to the modulo
            if an_1 < self.mod and an_1 > 0:
                self.an_1 = an_1
                valid = True
        except ValueError:
            pass
        return valid

    def changeSeedn_2(self, sn_2):
        """Changes the second recurrence term."""
        valid = False
        try:
            sn_2 = int(sn_2)
            # The seed must be positive and inferior to the modulo
            if sn_2 < self.mod and sn_2 > 0:
                self.sn_2 = sn_2
                valid = True
        except ValueError:
            pass
        return valid

    def changeSeedn_1(self, sn_1):
        """Changes the first recurrence term."""
        valid = False
        try:
            sn_1 = int(sn_1)
            # The seed must be positive and inferior to the modulo
            if sn_1 < self.mod and sn_1 > 0:
                self.sn_1 = sn_1
                valid = True
        except ValueError:
            pass
        return valid

    def generate(self):
        """Generates a pseudo random number."""
        tempSn_1 = self.sn_1
        self.sn_1 = (self.an_2*self.sn_2 + self.an_1*self.sn_1) % self.mod
        self.sn_2 = tempSn_1
        return self.sn_1 / self.mod
