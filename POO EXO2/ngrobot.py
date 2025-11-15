import Robot
class NGRobot(Robot):
    def __init__(self,nom,x=0,y=0,direction="N", vitesse=1):
        super().__init__(nom,x,y,direction)
        self.vitesse=vitesse
    
    def avancer(self):
        for i in range(self.vitesse):
            super().avancer()

    def accelerer(self):
        self.vitesse+=1

    def ralentir(self):
        if self.vitesse > 1:
            self.vitesse-=1
        
R1= Robot("me")
print(R1.position())
R1.avancer()
R1.tourner_droite()
print(R1.position())
R2 = NGRobot("ngme")
print(R2.position())
R2.accelerer()
R2.avancer()
print(R2.position()) 