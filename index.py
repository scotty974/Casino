# IMPORTS #
from supabase import create_client, Client
import random
import math
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
        

    
    def __str__(self):
        # methode pour le print
        return "id : " + str(self.get_id()) + " : " + self.get_pseudo() + " is at level " + str(self.get_level())

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
        self.current_level = None
        while self.current_level is None:
            level = int(input("Choisi ton level"))
            if level <= self.player.get_level():
                self.current_level = level
                break
            else:
                print("Le niveau choisi est trop élevé pas rapport au tien")

    def player_gain(self):
        gain, nb_mise = self.define_gain()
        self.choose_level()
        level_data = random_number(self.current_level)
        nb_coups = 0
        while nb_coups < level_data['nb_try']:
            nb_coups +=1
            nb = int(input("Devine le nombre auquel je pense  : "))
            if nb > level_data["random_nb"]:
                print("Trop grand ! ")
            elif nb < level_data['random_nb']:
                print("Trop petit ! ")
            else :
                print("Bingo ! Vous avez trouvé le bon numéro en {} coups  ! ".format(nb_coups))
                print(gain)
                new_gain = self.player.get_money() + gain
                self.player.set_money(new_gain)
                print("Votre solde est de : {} euros".format(new_gain))
                new_level = self.player.get_level() + 1
                if new_level <= 3:
                    self.player.set_level(new_level)
                print("Vous êtes au niveau {}".format(new_level))
                break
        else :
            print("Dommage vous avez perdu ! Le nombre exact est : {}".format(level_data['random_nb']))
            self.loose_gain(nb_mise=nb_mise)
            print("Vous avez perdu : {} euros. ".format(nb_mise))
            new_level = self.player.get_level() - 1
            if new_level <= 1 :
                self.player.set_level(new_level)
            print("Vous êtes niveau : {}".format(new_level))
        self.game_played(nb_coups, nb_mise)

    def game_played(self,nb_coups,nb_mise):
        response = supabase.table('Historique').insert({'user_id':self.player.get_id(),'nb_try':nb_coups,'mise':nb_mise,'level':self.current_level}).execute()

    def play(self):
        self.player_gain()

# Main program #

user = User(input("\nPseudo : "))
print(user)
Instance = Casino(player=user)
Instance.play()