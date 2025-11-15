from pathlib import Path
from save import save_game, load_game

savef = Path(__file__).parent / "game.json"

game_data = load_game(savef)

if not game_data: #empty dictionary returned
    nom = input("Entrez votre nom: ")
    game_data = {
        "nom": nom,
        "pv": 100,
        "inventaire": []
    }
    print(f"Bienvenue {nom}!")
else:
    print(f"Bienvenue {game_data['nom']}!")

while True:
    print(f"\n{game_data['nom']} | PV: {game_data['pv']} | Inventaire: {game_data['inventaire']}")
    print("1. Attaquer")
    print("2. Fouiller")
    print("3. Se reposer")
    print("4. Sauvegarder et quitter")
    
    choix = input("Choix: ").strip()
    
    if choix == "1":
        degats = 10
        game_data['pv'] -= degats
        print(f"You attack and lose {degats} HP!")
        if game_data['pv'] <= 0:
            print("You died! Game Over.")
            game_data['pv'] = 100
            game_data['inventaire'] = []
    
    elif choix == "2":
        objets = ["Sword", "Potion", "Shield", "Diamond"]
        from random import choice
        objet = choice(objets)
        game_data['inventaire'].append(objet)
        print(f"You found: {objet}")
    
    elif choix == "3":
        soin = 20
        game_data['pv'] += soin
        if game_data['pv'] > 100:
            game_data['pv'] = 100
        print(f"You rest and recover {soin} HP!")
    
    elif choix == "4":
        save_game(game_data, savef)
        print("game saved successfully!")
        break
    
    else:
        print("1 or 2 or 3 or 4 only!")