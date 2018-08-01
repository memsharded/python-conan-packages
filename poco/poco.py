import sys
import lib.pypoco as pypoco

def random_float():
    r = pypoco.Random()
    return r.nextFloat()

print random_float()
