import random
def random_number(level):
    nb_try = 1
    for i in range(3):
        nb_try += 2
        random_nb = random.randrange(1, 10*(i+1))
        if i == level -1:
            return {'nb_try' : nb_try, 'random_nb' : random_nb}
        else : 
            print('Rentrez un niveau valide !')
        

print(random_number(1))