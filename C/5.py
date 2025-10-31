def som(*args, negative=True,**kwargs):
    sum=0
    for num in args: 
        if negative or num >=0:
            sum+=num
    
    print("paramtere keywords:")
    for key, value in kwargs.items():
        print(f" {key} = {value}")
    
    return sum

print(som(1,-2,3, negative=False, debug=True, mode="test"))
