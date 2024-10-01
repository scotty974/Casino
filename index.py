# IMPORTS #
from supabase import create_client, Client
import random
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
        self.nb_user = None
        print(f"Hello {self.player.get_pseudo()}, vous avez {self.player.get_money()}$, Très bien ! Installez vous SVP à la table de pari.")

    def loose_gain(self,mise):
        return self.player.set_money(self.player.get_money() - mise)

    def choose_level(self):

        print(f"{self.player.get_pseudo()}, vous êtes level {self.player.get_level()}")
        self.current_level = None
        while self.current_level is None:
            level = int(input("Choisissez votre level [1,2,3] : "))
            if level <= self.player.get_level():
                self.current_level = level
                break
            else:
                print("Le niveau choisi est trop élevé pas rapport au votre")

    def get_mise(self):
        mise = None
        print(f"Current balance : {self.player.get_money()}$")
        while mise is None:
            try : 
                mise = float(input("Pari de niveau {} selectionné, veuillez saisir une mise : ".format(self.current_level)))
                if mise <= self.player.get_money():
                    self.player.set_money(self.player.get_money()-mise)
                    return mise
                else:
                    difference = mise-self.player.get_money()
                    if input(f"Vous n'avez pas les fonds suffisants, souhaitez vous apporter la différence ({difference}$) ? Y/N : ") == "Y":
                        self.player.set_money(self.player.get_money()+difference)
                        self.player.set_money(self.player.get_money()-mise)
                        return mise
                    mise = None
            except :
                print("!format de la saisie incorrect!")
                mise = None


    def apply_gain(self, mise, nb_essais_max):
        if nb_essais_max < self.nb_coup:
            pass
        else:
            l3 = [2,1,0.5]
            l5 = [4]+l3+[0.25]
            l7 = [8]+l5+[0.125]
            if nb_essais_max == 3:
                money = l3[self.nb_coup-1]*mise
            elif nb_essais_max == 5:
                money = l5[self.nb_coup-1]*mise
            elif nb_essais_max == 7:
                money = l7[self.nb_coup-1]*mise
            self.player.set_money(self.player.get_money()+money)

    def partie(self):

        self.choose_level()
        mise = self.get_mise()
        nb_essais_max, borne_sup, nb_python = random_number(self.current_level)
        self.nb_coup = 0
        reussite = False

        while self.nb_coup < nb_essais_max:

            self.nb_coup +=1

            if self.get_input() == False:
                print("Bravo, vous avez perdu un essai.")
            else:
                if self.nb_user > nb_python:
                    print("Trop grand ! ")
                elif self.nb_user < nb_python:
                    print("Trop petit ! ")
                else :
                    print("Bingo {} ! Vous avez trouvé le bon numéro en {} coups  ! ".format(self.player.get_pseudo(),self.nb_coup))
                    self.apply_gain(mise, nb_essais_max)
                    print("Votre solde est de : {} euros".format(self.player.get_money()))
                    new_level = self.player.get_level() + 1
                    if new_level <= 3:
                        self.player.set_level(new_level)
                    print("Vous êtes au niveau {}".format(self.player.get_level()))
                    reussite = True
                    break

        if not reussite:
            self.nb_coup += 1
            print("Dommage vous avez perdu ! Le nombre exact est : {}".format(nb_python))
            self.apply_gain(mise, nb_essais_max)
            print("Vous avez perdu : {} euros. ".format(mise))
            new_level = self.player.get_level() - 1
            if new_level >= 1 :
                self.player.set_level(new_level)
            print("Vous êtes niveau : {}".format(self.player.get_level()))

        self.game_played(mise, reussite)

    def game_played(self, mise, reussite):
        response = supabase.table('Historique').insert({'user_id':self.player.get_id(),'nb_try':self.nb_coup,'mise':int(mise),'level':self.current_level, 'correct':reussite}).execute()

    def play(self):
        if (input("Avant de jouer, souhaitez vous consulter les règles du Casino ? Y/N : ")) == "Y":
            print("""Le jeu comporte 3 levels avec la possibilié que le joueur choissise son level (si ce n'est pas sa 1è fois dans le Casino).
	En d'autres termes, tout nouveau joueur doit passer par le 1è level. Suite à la 1è partie, il a le droit de choisir son level en lui rappelant / proposant le dernier niveau atteint\n.
	Lors de chaque niveau, Python tire un nombre : level 1 (entre 1 et 10),
	level2 (1 et 20), level3 (1 et 30). C'est à vous de deviner le nombre mystérieux avec 3 essais (en tout) lors du 1è 
	level, 5 au 2è level et 7 au 3è level. Chaque essai ne durera pas plus de 10 secondes. Au-delà, 
	vous perdez votre essai. Att : si vous perdez un level, vous rejouez le level précédent.
	Quand vous souhaitez quitter le jeu, un compteur de 10 secondes est mis en place. 
	En absence de validation de la décision, le jeu est terminé.
	Python fournit enfin les statistiques du jeu (voir ci-dessous).""")
        while True:
            self.partie()
            if input("Continuer à jouer ? Y/N : ") == "N":
                break
        if input("Consulter vos stats ? Y/N : ") == "Y":
            self.stat()
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
        self.nb_user = None
        start = time()
        while self.nb_user is None:
            try:
                print("Vous avez 10sec pour Selectionner une valeur entre 0 et {} : ".format(self.current_level*10))
                self.nb_user = int(input())
                if (time()-start) > 10:
                    self.nb_user = None
                    return False
                else :
                    return True
            except:
                print("Cette entrée n'est pas un entier. Veuillez réessayer (le compteur tourne)")
                self.nb_user = None

        


# Main program #
if __name__ == "__main__":
    user = User(input("Je suis Python. Quel est votre pseudo ? "))
    instance = Casino(player=user)
    instance.play()