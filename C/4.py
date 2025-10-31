def som(*args, negative=True):
    sum=0
    for num in args: 
        if negative or num >=0:
            sum+=num
    return sum

print(som(2,5,6))