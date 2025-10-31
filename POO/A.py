msg="Bonjour Tout le Monde!"
print(len(msg))
print(msg[1:21])

msg=msg.upper()
msg=msg.lower()
print(msg)

list1=msg.split(" ")
# for i in range(len(msg)):
#     list1.append(msg[i]) 


list1 ?????

print(list1)

list2=[]
for char in list1[3]:
    list2.append(char)

list2[-1:]="2021"
print(list2)