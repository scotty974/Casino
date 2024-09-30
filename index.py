# IMPORTS #
from supabase import create_client, Client

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

    def get_solde(self):
        return self.money

    def set_solde(self, new_money):
        self.money = new_money

    def get_pseudo(self):
        return self.pseudo

    def get_level(self):
        return self.level

    def set_level(self, new_level:int):
        self.level = new_level

    def update(self):
        # MAJ user dans la BDD
        response = supabase.table('User').update({'pseudo':self.get_pseudo(),'level':self.get_level()}).eq('id',self.__id).execute()

    def __str__(self):
        # methode pour le print
        return "id : " + str(self.__id) + " : " + self.get_pseudo() + " is at level " + str(self.get_level())

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

# Main program #

user = User(input(("\nPseudo : ")))
print(user)
