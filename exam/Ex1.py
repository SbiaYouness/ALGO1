import random

#1
list22=[1,5,5,9,18,17,6,5,89,4,222,5,1,566,9,84,5,874,2,325,87,495,1,74]

def unique(lst:list)->list:
    listunique=[]
    for nbr in lst:
        if nbr not in listunique:
            listunique.append(nbr)
    return listunique

print(unique(list22))

#2
tuplenbr= tuple(list22)
somme= sum(tuplenbr)
minimum= min(tuplenbr)
maxnbmum= max(tuplenbr)
moyenne= somme/len(tuplenbr)

print(f"La somme: {somme}, le min: {minimum}, le max: {maxnbmum}, la moyenne: {moyenne}")

#3

list3= []
for _ in range(len(list22)):
    list3.append(random.randint(0, 1000))

if len(list22)!=len(list3):
    raise ValueError("Les listes doivent avoir la meme longueur")
sumlist=[]
for i in range(len(list22)):
    sumlist.append(list22[i]+list3[i])

print("la somme de chaque element des deux listes: ", sumlist)

#4
res=[]
tmp=list22.copy() #pour ne pas pointer sur la meme list, on veut creer une nouvelle copie
for _ in range(5):
    maxnb=max(tmp)
    res.append(maxnb)
    tmp.remove(maxnb)

print("Top 5 nombres: ", res)

#5
croissantes=[list22[i] for i in range(1,len(list22)) if list22[i]>list22[i-1]]
print("nouvelle liste strictement croissante: \n", croissantes)

#6
count=0
for i in range(1,len(list22)):
    if list22[i]>list22[i-1]:
        count+=1
        if count>=2:
            print("contient sub list triee:")
            break
    else:
        count=0
else:
    print("ne contient pas de sub list triee:")

#7
i=0
while i<len(list22)/2:
    if list22[i]!=list22[-(i+1)]:
        print("n'est pas palindrome:")
        break
    i+=1
    if i==(len(list22)/2)-1:
        print("est un palindrome:")

