l1= [1,2,3,4,3,6,7,3,7,7]
count=0
for i in range(1,len(l1)):
    if l1[i]%3==0:
        count+=1
print(count)