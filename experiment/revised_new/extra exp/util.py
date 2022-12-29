import numpy as np
from copy import deepcopy
import gmpy2
import random


# map into Zn ring space
def space_mapping(value, plain_space):
    """
    Map the value into a defined domain. (modulo reduction)
    we define that Z(N) is a integer domain where [-N/2, N/2]
    :param value: input value
    :param public_key_N: N of the public key. 
    :return value: mapped value
    """
    value %= plain_space
    if value*2 > plain_space:
        value -= plain_space
    return value




# pseudorandom function with seed, label
def PRF(seed, label, PRrange):
    random.seed(seed + label)
    #return random.randrange(self.max_int*2) - self.max_int
    return random.randrange(PRrange) - PRrange//2
