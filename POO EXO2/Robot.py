class Robot:
    def __init__(self,nom,x=0,y=0,direction="N"):
        self.nom=nom
        self.x=x
        self.y=y
        self.direction=direction

    def avancer(self):
        # if self.direction=="N":
        #     self.y+=1
        # elif self.direction=="E":
        #     self.x+=1
        # elif self.direction=="O":
        #     self.x-=1
        # elif self.direction=="S":
        #     self.y-=1
        match self.direction:
            case "N":
                self.y+=1
            case "E":
                self.x+=1
            case "O":
                self.x-=1
            case "S":
                self.y-=1
            case _:
                print("Direction inconnue")

    def tourner_gauche(self):
        match self.direction:
            case "N":
                self.direction= "O"
            case "E":
                self.direction= "N"
            case "O":
                self.direction= "S"
            case "S":
                self.direction= "E"

    def tourner_droite(self):
        match self.direction:
            case "N":
                self.direction= "E"
            case "E":
                self.direction= "S"
            case "O":
                self.direction= "N"
            case "S":
                self.direction= "O"

    def position(self):
        return f"Robot {self.nom} en position (x={self.x},y={self.y}), direction {self.direction}"
    

R1= Robot("me")

R1.avancer()
print(R1.position())

R1.direction="O"
R1.avancer()
print(R1.position())

R1.direction="S"
R1.avancer()
print(R1.position())

R1.direction="E"
R1.avancer()
print(R1.position())

R1.tourner_droite()
R1.avancer()
R1.avancer()
R1.avancer()
print(R1.position())

R1.tourner_droite()
R1.avancer()
print(R1.position())
