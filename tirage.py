import random
def random_number(level):
    nb_try = 0
    for i in range(3):
        nb_try += 2
        random_nb = random.randrange(1, 10+10)
        if i == level -1:
            print(nb_try, random_nb)
        

random_number(1)