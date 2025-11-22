import os
from datetime import datetime
import string


with open("audit_arborescence.txt","w",encoding="utf-8") as f:
    for root,dirs,files in os.walk("archives"):
        for nom_fichier in files:
            chemin=os.path.join(root,nom_fichier)
            chemin_abs=os.path.abspath(chemin)
            taille_ko=os.path.getsize(chemin)//1024
            date_modif=datetime.fromtimestamp(os.path.getmtime(chemin)).strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Chemin: {chemin_abs}\nTaille: {taille_ko} Ko\nDernière modification: {date_modif}\n\n")

#2

if not os.path.exists("cleaned"):
    os.makedirs("cleaned")


def nettoyer_texte(text):
    cleanedtext=''.join(char.lower() for char in text if char in string.ascii_letters+" \n")
    lignes=cleanedtext.splitlines()
    lignes_nettoyees=[]
    for ligne in lignes:
        ligne=" ".join(word.strip() for word in ligne.split())
        if ligne:
            lignes_nettoyees.append(ligne)
    return lignes_nettoyees


with open("rapport_textes.txt","w",encoding="utf-8") as f_rapport:
    for root,dirs,files in os.walk("archives"):
        for nom_fichier in files:
            if nom_fichier.lower().endswith(".txt"):
                chemin=os.path.join(root,nom_fichier)
                with open(chemin,"r",encoding="utf-8",errors="ignore") as fin:
                    text=fin.read()
                lignes_nettoyees=nettoyer_texte(text)
                nom_clean="cleaned_"+nom_fichier
                chemin_clean=os.path.join("cleaned",nom_clean)
                with open(chemin_clean,"w",encoding="utf-8") as fout:
                    for l in lignes_nettoyees:
                        fout.write(l+"\n")
                nb_lignes=len(lignes_nettoyees)
                nb_mots=sum(len(l.split()) for l in lignes_nettoyees)
                max_longueur=max((len(l) for l in lignes_nettoyees),default=0)
                f_rapport.write(f"{nom_fichier} : lignes={nb_lignes}, mots={nb_mots}, max_longueur={max_longueur}\n")

# 3
with open("archives/grimoire.txt","r",encoding="utf-8",errors="ignore") as fin:
    lignes=[l.strip().lower() for l in fin if l.strip()]
    mots=[mot for ligne in lignes for mot in ligne.split()]

freq={}
for mot in mots:
    if mot in freq:
        freq[mot]+=1
    else:
        freq[mot]=1

top50=sorted(freq.items(), key=lambda x:x[1], reverse=True)[:50]

nb_lignes=len(lignes)
mot_lignes={}
for ligne in lignes:
    for mot in set(ligne.split()):
        if mot in mot_lignes:
            mot_lignes[mot]+=1
        else:
            mot_lignes[mot]=1
seuil=int(0.7*nb_lignes)
mots_70=[mot for mot,nb in mot_lignes.items() if nb>=seuil]

mots_1=[mot for mot,nb in freq.items() if nb==1]

palindromes=[mot for mot in freq if len(mot)>1 and mot==mot[::-1]]

with open("analyse_grimoire.txt","w",encoding="utf-8") as f:
    f.write("Frequence de chaque mot:\n")
    for mot,nb in sorted(freq.items(), key=lambda x:x[1], reverse=True):
        f.write(f"{mot}: {nb}\n")
    f.write("\nTop 50 mots les plus frequents:\n")
    for mot,nb in top50:
        f.write(f"{mot}: {nb}\n")
    f.write("\nMots presents dans au moins 70% des lignes:\n")
    for mot in mots_70:
        f.write(f"{mot}\n")
    f.write("\nMots n'apparaissant qu'une seule fois:\n")
    for mot in mots_1:
        f.write(f"{mot}\n")
    f.write("\nMots palindromes:\n")
    for mot in palindromes:
        f.write(f"{mot}\n")