import string

def nombremots(data):
    n=0
    list=data.split(" ")
    for mot in list:
        n+=1
    return n

def lengthmots(data):
    n=0
    sumlen=0
    list=data.split(" ")
    for mot in list:
        sumlen+=len(mot)
        n+=1
    return sumlen/n if n > 0 else 0

def longueurmoyen(data):
    mot=data.split(" ")
    longueur= [len(m) for m in mot]
    moy = sum(longueur)/len(longueur)
    occ = occmots(data)  
    occMax = max(occ.values())
    l = [k for k,v in occ.items() if v== occMax ] 
    return l,occMax, moy

def occmots(data):
    dict={}
    for mot in data.split(" "):
        mot=mot.strip(string.punctuation).lower()
        dict[mot]=dict.get(mot,0)+1
    return dict

def palindrome(data):
    return [mot for mot in data.split(" ") if mot.strip(string.punctuation).lower() == mot.strip(string.punctuation).lower()[::-1] and len(mot) > 1]

def nbrPhrase(data):
    # list3=data.replace(",",".")
    phrases = data.split(".")
    return len(phrases)

def lengthPhrase(data):
    dictP={}
    phrases = data.split(".")
    for phrase in phrases:
        dictP[phrase]=len(phrase)
    return dictP

def typePunc(data):
    punc=set()
    for char in data:
        if char in string.punctuation:
            punc.add(char)
    return punc

def stats_longueur(data):
    stats = {}
    for mot in data.split():
        mot = mot.strip(string.punctuation).lower()
        longueur = len(mot)
        if longueur > 0:
            stats[longueur] = stats.get(longueur, 0) + 1
    return stats

def topMots(data):
    occ = occmots(data)
    top_10 = sorted(occ.items(), key=lambda x: x[1], reverse=True)[:10] #trie par tuple[1]=>value
    return top_10

def phrasesLongues(data):
    phrases = [p.strip() for p in data.split(".") if p.strip()]
    phrases_triees = sorted(phrases, key=len, reverse=True)[:3]
    return phrases_triees

def diversite_vocabulaire(data):
    mots = [mot.strip(string.punctuation).lower() for mot in data.split() if mot.strip(string.punctuation)]
    mots_uniques = set(mots)
    total = len(mots)
    return len(mots_uniques), total, (len(mots_uniques) / total * 100) 

def patterns_repetitifs(data):
    mots = data.split()
    patterns = []
    for i in range(len(mots) - 1):
        mot1 = mots[i].strip(string.punctuation).lower()
        mot2 = mots[i + 1].strip(string.punctuation).lower()
        if mot1 == mot2 and mot1:
            patterns.append(mot1)
    return patterns

with open('TD init\data.txt', 'rt', encoding='utf-8') as fichier:
    data = fichier.read()

print("1. ANALYSE LEXICALE ===\n")

print("nombre de mots dans le texte est:",nombremots(data))
print("La longueur moyenne des mots est:",lengthmots(data))

clemax, nbrmax, moyenne=longueurmoyen(data)
print("Les mots les plus utilises sont {} occurence de {} fois, et la longueurs moyenne: {} ".format(clemax, nbrmax, moyenne))

print("Les mots palindromes sont:",palindrome(data))

print("Le nombre des phrases est:",nbrPhrase(data))

print("Le nombre des phrases est:",lengthPhrase(data))

print("Les type de ponctuation sont:",typePunc(data))

for k, v in sorted(stats_longueur(data).items()):
    print("les mots avec longueur= %d ont l'occurence: %d"%(k,v))

print("Top 10 des mots:")
listTpl = topMots(data)
for index, (mot, freq) in enumerate(listTpl, 1):
    print(f"  {index}. '{mot}': {freq} fois")

lstph=phrasesLongues(data)
print(f"Les phrases plus longues:{lstph[0]}\n{lstph[1]}\n{lstph[2]}")

unqmots, ttlmots, prctgmots = diversite_vocabulaire(data)

print(f"Nombre Mots uniques utilises:{unqmots}, en total il y en a:{ttlmots}, pourcentage de diversity={prctgmots:.2f}")

print("Les patterns repetitif")
for pttrn in patterns_repetitifs(data):
    print(pttrn,end="  ;  ")
