import random
def random_number(level):
        if level == 1:
            nb_try = 3
            random_nb = random.randrange(1,10)
            return {"nb_try" : nb_try, "nb_random" : random_nb}
        elif level == 2:
            nb_try = 5
            random_nb = random.randrange(1,20)
            return {"nb_try" :nb_try,"nb_random" : random_nb}
        elif level ==3:
            nb_try = 7
            random_nb = random.randrange(1,30)
            return {"nb_try" :nb_try, "nb_random" :random_nb}
