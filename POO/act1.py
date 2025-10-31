class Voiture :
    def __init__(self,code,marque,kilometrage):
        self.code=code
        self.marque=marque
        self.kilometrage=kilometrage
    
    def mod_kilo(self,newkilo):
        self.kilometrage+=newkilo
    
    def afficher(self):
        print(f"La voiture de code {self.code} et marque {self.marque} a le kilometrage {self.kilometrage}")

v1=Voiture(23,"dacia",343724)
v2=Voiture(24,"bmw",10002)
v3=Voiture(25,"audi",94256)
v1.afficher()
v2.mod_kilo(8)
v2.afficher()
