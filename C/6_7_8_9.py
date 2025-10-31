l1 = [13, 10, 2, 5, 1, 9]
def select(a):
    if a<10:
        return True
    elif a>=10:
        return False

print(select(13))

def myfilter(l1):
    l2=[]
    for val in l1:
        l2.append(select(val))
    return l2

l3 = list(filter(lambda a: a < 10, l1))

print(myfilter(l1))
print(l3)
