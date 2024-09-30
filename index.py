from supabase import create_client, Client

url: str = "https://frqopmgtjlnbdglpkjiu.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZycW9wbWd0amxuYmRnbHBraml1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc2OTExMTIsImV4cCI6MjA0MzI2NzExMn0.Ke--_ynpBjmgVRHNK-A5eMktpkQ6sQ135H7KMoyBTT0"
supabase: Client = create_client(url, key)

class User:

    def __init__(self, pseudo:str):
        response = supabase.table('User').select('*').execute()
        self.state = 0
        for _user in response.data:
            if _user['pseudo'] == pseudo:
                print(f'user {pseudo} already exist in database')
                #user already exist
                self.pseudo = pseudo
                self.level = _user['level']
                self.__id = _user['id']
                self.state = 1
                break
        if self.state == 0:
            #user creation
            print(f'creation of user {pseudo} in database')
            response = (supabase.table("User").insert({"pseudo": pseudo}).execute())

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
        return self.get_pseudo() + " is at level " + str(self.get_level())
#table_User = {id:int,
#              pseudo:str,
#              level:int
#              }

#table_Historique = {user_id:int,
#                    nb_try:int,
#                    mise:int,
#                    level:int
#                    }

# Charger/créer un utilisateur
user = User(input(("\nPseudo : ")))
