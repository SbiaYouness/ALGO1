l1= [1,2,3,4,3,6,7,3,7,7]
temp=len(l1)-1
for i in range(0,temp):
    temp=len(l1)-1
    for j in range(i+1,temp+1):
        if l1[i] == l1[j]:
            l1.pop(i)
            break
print(l1)