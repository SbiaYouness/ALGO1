file=open("./file.txt",'r')
# print(file.readlines())
print(file.read())

with open("./file.txt",'w') as file2:
    for i in range(11):
        file2.write(f"5 x {i} = {i*5}\n")