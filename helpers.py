import random

def generate_cookie_value():
    """
    Voici un exemple de la fonction generate cookie value

    >>> len(generate_cookie_value())
    128
    """
    return str("".join(random.choice("0123456789ABCDEFadcdef@&!") for i in range(128)))

def somme (a, b): 
    """
    Voici un exemple de la fonction somme

    >>> somme(10,20)
    30
    """
    return int(a) + int(b)