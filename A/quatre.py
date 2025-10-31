distance = int(input("entre la distance: "))

choix = input("votre distance est en km ou mille?")

if choix =="km":
    distance*=1.6
    print(f"apres la conversion en mille, la distance =", distance)
elif choix =="mille":
    distance/=1.6
    print(f"apres la conversion en km, la distance =", distance)

