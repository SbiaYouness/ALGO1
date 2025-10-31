l1= [1,2,3,4,3,6,7,3,7,7]
max=l1[0]
for i in range(1,len(l1)):
    if max<l1[i]:
        max=l1[i]
print(max)
