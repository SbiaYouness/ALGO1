dict_etud={"1":("ali",[19,16]),"2":("karim",[14,15]),"3":("omar",[11,12]),"4":("alaa",[9,10]),"5":("ghali",[2,3])}

#Ajouter 
def ajouter(nom:str,notes:list)->None:
    dict_etud[str(len(dict_etud)+1)]=(nom,notes)

#modifier
def modifier(num:str,nom:str=None,notes:list=None)->None:
    if num in dict_etud:
        current_nom,current_notes=dict_etud[num]
        if nom is not None:
            current_nom=nom
        if notes is not None:
            current_notes=notes
        dict_etud[num]=(current_nom,current_notes)
    else:
        raise KeyError("Numero d'etudiant non trouve")
    
#Supprimer
def supprimer(num:str)->None:
    if num in dict_etud:
        del dict_etud[num]
    else:
        raise KeyError("Numero d'etudiant non trouve")

#moyenne    
def calculer_moyenne(num:str)->float:
    if num in dict_etud:
        _,notes=dict_etud[num]
        return sum(notes)/len(notes)
    else:
        raise KeyError("Numero d'etudiant non trouve")

# moyenne ≥ 14.
def etudiants_reussite(seuil:float=14.0)->dict:
    reussite={}
    for num,(nom,notes) in dict_etud.items():
        moyenne=sum(notes)/len(notes)
        if moyenne>=seuil:
            reussite[num]=(nom,notes)
    return reussite

# inversé 
def dictionnaire_inverse()->dict:
    inverse_dict={}
    for _,(nom,notes) in dict_etud.items():
        moyenne=round(sum(notes)/len(notes),2)
        if moyenne not in inverse_dict:
            inverse_dict[moyenne]=[]
        inverse_dict[moyenne].append(nom)
    return inverse_dict

# dupliquer
def detecter_duplique()->list:
    duplique=[]
    for _,(nom,notes) in dict_etud.items():
        if len(notes)!=len(set(notes)):
            duplique.append(nom)
    return duplique

def trier_etudiants(par:str="nom")->list:
    if par=="nom":
        return sorted(dict_etud.items(),key=lambda item:item[1][0])
    elif par=="moyenne":
        return sorted(dict_etud.items(),key=lambda item:sum(item[1][1])/len(item[1][1]),reverse=True)
    elif par=="nb_notes":
        return sorted(dict_etud.items(),key=lambda item:len(item[1][1]),reverse=True)
    else:
        raise ValueError("Critere de tri non supporte")

# progresse
def etudiants_progresse()->list:
    progresse=[]
    for _,(nom,notes) in dict_etud.items():
        if len(notes)>=4:
            moyenne_totale=sum(notes)/len(notes)
            moyenne_derniere=sum(notes[-2:])/2
            if moyenne_derniere>moyenne_totale:
                progresse.append(nom)
    return progresse

#Fusionner
def fusionner_dicts(dict1:dict,dict2:dict)->dict:
    fusionne=dict1.copy()
    for num,(nom,notes) in dict2.items():
        moyenne2=sum(notes)/len(notes)
        if num in fusionne:
            _,notes1=fusionne[num]
            moyenne1=sum(notes1)/len(notes1)
            if moyenne2>moyenne1:
                fusionne[num]=(nom,notes)
        else:
            fusionne[num]=(nom,notes)
    return fusionne

