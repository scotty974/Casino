import random
from mise import define_gain
def random_number(level):
    # valeur par défault
    nb_try = 1
    # création des levels
    for i in range(3):
        nb_try += 2
        random_nb = random.randrange(1, 10*(i+1))
        if i == level -1:
            return {'nb_try' : nb_try, 'random_nb' : random_nb}
        else : 
            print('Rentrez un niveau valide !')
        

def player_gain():
    gain = define_gain(1)
    level_data = random_number(1)
    nb_cout = 0
    while nb_cout < level_data['nb_try']:
        nb_cout +=1
        nb = int(input("Devine le nombre auquel je pense  : "))
        if nb > level_data["random_nb"]:
            print("Trop grand ! ")
        elif nb < level_data['random_nb']:
            print("Trop petit ! ")
        else : 
            print("Bingo ! Vous avez trouvé le bon numéro en {} coups  ! ".format(nb_cout))
            print("Votre gain est de : {} euros".format(gain))
            break
    else : 
        print("Dommage vous avez perdu ! Le nombre exact est : {}".format(level_data['random_nb']))
        
        
player_gain()
