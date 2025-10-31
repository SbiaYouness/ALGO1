from datetime import date

class Employe:
    def __init__(self,id,nom, prenom, date_naissance, date_embauche, salaire):
        self.id=id
        self.nom=nom
        self.prenom=prenom
        self.date_naissance=date_naissance
        self.date_embauche=date_embauche
        self.salaire=salaire

    def getAge(self):
        current_year = date.today().year
        naissance_year = int(self.date_naissance.split('/')[2])
        return current_year - naissance_year

    def getAnciennete(self):
        current_year = date.today().year
        embauche_year = int(self.date_embauche.split('/')[2])
        # embauche_year = self.date_embauche.year
        return current_year - embauche_year
    
    def mod_anciennete(self, nv_date):
        current_year = date.today().year
        embauche_year = int(self.date_embauche.split('/')[2])
        # embauche_year = self.date_embauche.year
        return current_year - embauche_year

emp1 = Employe(4342,"nom", "prenom", "11/06/2005", "16/08/2024", 342223)
print(emp1.getAge(), "Years old")
print(emp1.getAnciennete(), "Years of working")

mnths=date.today().month-int(emp1.date_embauche.split('/')[1])
days=date.today().day-int(emp1.date_embauche.split('/')[0])
jour_recru=mnths*30+emp1.getAnciennete()*365+days

print(jour_recru, "days on the job")