def calculer_factorielle(number):
    if number==0:
        return 1
    return number*calculer_factorielle(number-1)
