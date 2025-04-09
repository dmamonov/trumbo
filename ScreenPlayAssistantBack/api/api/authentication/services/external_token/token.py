import random
import string

def random_token(length=4):
    return ''.join(random.choices(string.digits, k = length))
