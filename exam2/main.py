import datetime
import os
from pathlib import Path

dir=Path(__file__).parent


#Partie 1

class Evenement:   
    def __init__(self, titre:str, date:datetime.date, description:str = None)-> None:       
        self.titre = titre       
        self.date = date       
        self.description = description

        if not self.titre:
            raise ValueError("Le titre de ne peut pas etre vide")
        if self.date.year < 1970:
            raise ValueError("La date ne peut pas etre < 1970")
        
    def __str__(self)-> str:
        return f"{self.titre} ({self.date})"
    
    def est_passe(self) -> bool:
        return self.date < datetime.date.today()

#Partie 2

class Agenda:
    def __init__(self) -> None:
        self.evenements = []
    
    def ajouter_evenement(self, evenement: Evenement) -> None:
        for e in self.evenements:
            if e.titre == evenement.titre and e.date == evenement.date:
                raise ValueError("Un evenement avec le meme titre et la meme date existe deja")
        self.evenements.append(evenement)

    def rechercher(self, date=None, mot_cle=None) -> list[Evenement]:
        resultats = []

        for evenement in self.evenements:
            if date and evenement.date == date:
                resultats.append(evenement)
            elif mot_cle and (mot_cle.lower() in evenement.titre.lower() or (evenement.description and mot_cle.lower() in evenement.description.lower())):
                resultats.append(evenement)
        return resultats

    def supprimer(self, titre:str, date:datetime.date) -> None:
        for evenement in self.evenements:   
            if evenement.titre == titre and evenement.date == date:
                self.evenements.remove(evenement)
                return
        raise KeyError("Evenement non trouve pour suppression")

#Partie 3

    def statistiques(self) -> dict:
        stats = {
            "total": len(self.evenements),
            "passes": sum(1 for e in self.evenements if e.est_passe()),
            "futurs": sum(1 for e in self.evenements if not e.est_passe()),
            "par_annee":{
                year: sum(1 for e in self.evenements if e.date.year == year)
                for year in set(e.date.year for e in self.evenements) #set to avoid duplicate years 
            }
        }
        return stats

#Partie 4

    def exporter(self, chemin:str) -> None:
        if not os.access(os.path.dirname(chemin), os.W_OK):
            print("Permission refusee")
            return
        if not os.path.exists(os.path.dirname(chemin)):
            print("Le chemin est invalide")
            return

        with open(chemin, 'w') as f:
            for evenement in self.evenements: 
                line = f"{evenement.titre};{evenement.date.isoformat()};{evenement.description or ''}\n"
                f.write(line)

    def importer(self, chemin:str) -> None:
        if not os.path.exists(chemin):
            print("Le fichier n'existe pas")
            return
        if not os.access(chemin, os.R_OK):
            print("Permission refusee")
            return

        with open(chemin, 'r') as f:
            for line in f:
                parts = line.strip().split(';')

                if len(parts) < 2:
                    continue
                titre = parts[0]

                try:
                    date = datetime.date.fromisoformat(parts[1])
                except ValueError:
                    continue

                description = parts[2] if len(parts) > 2 else None

                evenement = Evenement(titre, date, description)
                self.ajouter_evenement(evenement)

#Partie 5

def charger_plage(agenda:Agenda, date_debut:datetime.date, date_fin:datetime.date) -> list[Evenement]:
    if date_debut > date_fin:
        raise ValueError("La date debut superieure a la date fin")

    resultats = []
    for i in range((date_fin - date_debut).days + 1):
        date_courante = date_debut + datetime.timedelta(days=i)
        rech=agenda.rechercher(date=date_courante)
        resultats.extend(rech)
    return resultats

#Partie 6

class EvenementRecurrent(Evenement):
    def __init__(self, titre:str, date:datetime.date, frequence:str, occurrences:int, description:str = None)-> None:
        super().__init__(titre, date, description)
        self.frequence = frequence  #en jours
        self.occurrences = occurrences #nombre d'occurrences

        if self.frequence not in ["quotidien", "hebdo", "mensuel"]:
            raise ValueError("Utilisez 'quotidien', 'hebdo' , 'mensuel'")
        if self.occurrences < 1:
            raise ValueError("Le nombre d'occurrences doit etre >= 1")
        
    def generer_occurrences(self) -> list[Evenement]: 
        evenements = []
        d = None

        if self.frequence == "quotidien":
            d = datetime.timedelta(days=1)
        elif self.frequence == "hebdo":
            d = datetime.timedelta(weeks=1)
        elif self.frequence == "mensuel":
            d = None  #handled separately

        current_date = self.date
        for _ in range(self.occurrences):
            evenements.append(Evenement(self.titre, current_date, self.description)) #en premier lieu date de l'evenement
            if self.frequence == "mensuel":
                month = (current_date.month % 12) + 1 #en cycle de 1 a 12
                year = current_date.year + (current_date.month // 12) #incremente seulement si le mois est 12
                day = min(current_date.day, (datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)).day) #garde le meme jour ou le dernier jour du mois
                current_date = datetime.date(year, month, day)
            else:
                current_date += d
        return evenements
    
#TESTs

e1 = Evenement("Anniversaire", datetime.date(2023, 5, 20), "Fete d'anniversaire")
e2 = Evenement("Reunion", datetime.date(2023, 6, 15), "Reunion de travail")
agenda = Agenda()
agenda.ajouter_evenement(e1)
agenda.ajouter_evenement(e2)

for evt in agenda.rechercher(mot_cle="Reunion"):
    print(evt)

stats = agenda.statistiques()
print(stats)

agenda.exporter(dir/"agenda.txt")

agenda2 = Agenda()
agenda2.importer(dir/"agenda.txt")

for evt in agenda2.evenements:
    print(evt)

agenda2.supprimer("Anniversaire", datetime.date(2023, 5, 20))
for evt in agenda2.evenements:
    print(evt)

Eventocc = EvenementRecurrent("Cours de yoga", datetime.date(2023, 7, 1), "hebdo", 4, "Session hebdo de yoga")
occurrences = Eventocc.generer_occurrences()

for evt in occurrences:
    print(evt)
