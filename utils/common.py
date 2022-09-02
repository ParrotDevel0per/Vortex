import random
from string import ascii_lowercase, digits

def randStr(length = 32):
    s = ''.join(random.choice(ascii_lowercase + digits) for _ in range(length))
    return s