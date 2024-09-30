import math
def define_gain(level):
    # demande ma mise
    nb_mise = int(input("Entrez votre mise : "))
    while nb_mise == 0 :
        nb_mise = int(input("Entrez une valeur supérieur à 0 : "))
    gain = round(math.exp(level)*nb_mise, 2)
    return gain




print(define_gain(1))