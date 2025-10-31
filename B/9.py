mydict= {"nom":"Aissam",
         "age":36,
         "sexe":"M"}
print(mydict.keys())
print(mydict.values())

count=0
for keys in mydict.keys():
    if keys == "adresse":
        print(mydict[keys])
        count=1
if count==0:
    print("Non Dispo")

for keys,values in mydict.values():
    print(values)