import random
def random_number(level):
    # valeur par défault
    nb_try = 3
    # création des levels
    for i in range(3):
        nb_try += 2
        random_nb = random.randrange(1, 10+10)
        if i == level -1:
            return {'nb_try' : nb_try, 'random_nb' : random_nb}
        else : 
            print('Rentrez un niveau valide !')
        
print(random_number(2))