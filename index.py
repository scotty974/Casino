# IMPORTS #
from supabase import create_client, Client
import random
import math
import threading
from time import time
# API #
url: str = "https://frqopmgtjlnbdglpkjiu.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZycW9wbWd0amxuYmRnbHBraml1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc2OTExMTIsImV4cCI6MjA0MzI2NzExMn0.Ke--_ynpBjmgVRHNK-A5eMktpkQ6sQ135H7KMoyBTT0"
supabase: Client = create_client(url, key)

# FUNCTIONS #
def get_user_from_pseudo(pseudo:str):
    response = supabase.table('User').select('*').execute()
    for _user in response.data:
        if _user['pseudo'] == pseudo:
            print(f'user {pseudo} already exist in database')
            # user already exist
            pseudo = pseudo
            level = _user['level']
            __id = _user['id']
            money = _user['money']
            return __id, pseudo, money, level
    return None


def random_number(level):
    liste_a = [3,5,7]
    liste_b = [10,20,30]
    
    return liste_a[level-1], liste_b[level-1], random.randint(0,liste_b[level-1])

# CLASS #
class User:

    def __init__(self, pseudo:str):
        if _user := get_user_from_pseudo(pseudo):
            self.__id = _user[0]
            self.pseudo = _user[1]
            self.money = _user[2]
            self.level = _user[3]
        else:
            #user creation
            self.pseudo = pseudo
            self.level = 1
            print(f'Creation of user {pseudo} in database...')
            self.money = int(input('Saisissez le montant que vous souhaitez ajouter à votre compte : '))
            response = (supabase.table("User").insert({"pseudo":self.pseudo, 'money':self.money}).execute())
            self.__id = get_user_from_pseudo(self.pseudo)[0]

    def get_money(self):
        return self.money

    def set_money(self, new_money):
        self.money = new_money
        self.update()

    def get_pseudo(self):
        return self.pseudo

    def get_level(self):
        return self.level

    def set_level(self, new_level:int):
        self.level = new_level
        self.update()

    def get_id(self):
        return self.__id

    def update(self):
        # MAJ user dans la BDD
        response = supabase.table('User').update({'pseudo':self.get_pseudo(),'level':self.get_level(), 'money' : self.get_money()}).eq('id',self.__id).execute()


########################################
#table_User = {id:int,
#              pseudo:str,
#              level:int
#              money:float
#              }

#table_Historique = {user_id:int,
#                    nb_try:int,
#                    mise:int,
#                    level:int
#                    }
#
# Charger/créer un utilisateur
########################################

class Casino:

    def __init__(self,player:User):
        self.player = player
        self.current_level = None
        self.user_input = None

    def loose_gain(self,nb_mise):
        return self.player.set_money(self.player.get_money() - nb_mise)

    def define_gain(self):
        # demande ma mise
        nb_mise = int(input("Entrez votre mise : "))
        while nb_mise == 0 :
            nb_mise = int(input("Entrez une valeur supérieur à 0 : "))
        if self.player.get_money() < nb_mise :
            response = input("Vous n'avez pas assez d'argent ! Voulez vous rajouter de l'argent ? Y/N : ")
            if response == 'Y':
                new_money = int(input("Entrez la somme : "))
                self.player.set_money(self.player.get_money() + new_money)
            elif response == 'N' :
                nb_mise = int(input("Entrez une nouvelle mise : "))

        gain = round(math.exp(self.player.get_level())*nb_mise, 2)
        return gain, nb_mise

    def choose_level(self):

        print(f"Your current level is {self.player.get_level()}")
        self.current_level = None
        while self.current_level is None:
            level = int(input("Choisi ton level [1,2,3] : "))
            if level <= self.player.get_level():
                self.current_level = level
                break
            else:
                print("Le niveau choisi est trop élevé pas rapport au tien")

    def player_gain(self):

        gain, mise = self.define_gain()
        self.choose_level()
        nb_essais_max, borne_sup, nb_a_trouver = random_number(self.current_level)
        self.nb_essais = 0
        reussite = False

        while self.nb_essais < nb_essais_max:

            self.nb_essais +=1

            if self.get_input() == False:
                print("Bravo, vous avez perdu un essai.")
            else:
                if self.user_input > nb_a_trouver:
                    print("Trop grand ! ")
                elif self.user_input < nb_a_trouver:
                    print("Trop petit ! ")
                else :
                    print("Bingo {} ! Vous avez trouvé le bon numéro en {} coups  ! ".format(self.player.get_pseudo(),self.nb_essais))
                    print(gain)
                    new_gain = self.player.get_money() + gain
                    self.player.set_money(new_gain)
                    print("Votre solde est de : {} euros".format(new_gain))
                    new_level = self.player.get_level() + 1
                    if new_level <= 3:
                        self.player.set_level(new_level)
                    print("Vous êtes au niveau {}".format(self.player.get_level()))
                    reussite = True
                    break

        if not reussite:

            print("Dommage vous avez perdu ! Le nombre exact est : {}".format(nb_a_trouver))
            self.loose_gain(nb_mise=mise)
            print("Vous avez perdu : {} euros. ".format(mise))
            new_level = self.player.get_level() - 1
            if new_level > 1 :
                self.player.set_level(new_level)
            print("Vous êtes niveau : {}".format(self.player.get_level()))

        self.game_played(mise, reussite)

    def game_played(self,nb_mise, reussite):
        response = supabase.table('Historique').insert({'user_id':self.player.get_id(),'nb_try':self.nb_essais,'mise':nb_mise,'level':self.current_level, 'correct':reussite}).execute()

    def play(self):
        while True:
            self.player_gain()
            if input("Continuer à jouer ? Y/N : ") == "N":
                break
        print('Le Casino vous remercie, à Bientôt !')

    def stat(self):
        response = supabase.table('Historique').select('mise','level','correct','nb_try').eq('user_id',self.player.get_id()).execute()
        size = len(response.data)
        # utiliser panda içi
        somme_mise = 0
        nb_reussite = 0
        liste_levels = [0,0,0]
        highest_level = 0
        for hist in response.data:
            somme_mise += hist['mise']
            liste_levels[hist['level']-1] += 1
            if hist['level'] > highest_level:
                highest_level = hist['level']
            if hist['correct'] == True:
                nb_reussite += 1
        fav_level = liste_levels.index(max(liste_levels))+1
        avg_mise = somme_mise/size
        winrate = nb_reussite/size
        print(f'\n# ACCOUNT STAT OF {self.player.get_id()}:{self.player.get_pseudo()} #\nCurrent Balance : {self.player.get_money()}$\nGame played : {size}\nFavorite Level : {fav_level}\nHighest Played Level : {highest_level}\nActual Level : {self.player.get_level()}\nAVG Mise : {round(avg_mise,2)}$\nWin Rate : {round(winrate*100,2)}%\n#')

    def get_input(self):
        self.user_input = None
        start = time()
        while self.user_input is None:
            try:
                print("Vous avez 10sec pour Selectionner une valeur entre 0 et {} : ".format(self.current_level*10))
                self.user_input = int(input())
                if (time()-start) > 10:
                    self.user_input = None
                    return False
                else :
                    return True
            except:
                print("Cette entrée n'est pas un entier. Veuillez réessayer (le compteur tourne)")
                self.user_input = None

        


# Main program #
if __name__ == "__main__":
    user = User(input("\nPseudo : "))
    Instance = Casino(player=user)
    if input('Play/Stat : ') == "Play":
        Instance.play()
    elif "Stat":
        Instance.stat()