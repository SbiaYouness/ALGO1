import tkinter as tk
import random
from time import time
import threading

# Configuration du jeu
GRID_SIZE = 19
CELL_SIZE = 30
MSEMMEN_COUNT = 30  # Nombre de msemmen à collecter
LBEN_COUNT = 15     # Bouteilles de lben
GARO_COUNT = 4      # Power-ups (garo)
ENEMY_COUNT = 3     # Ennemis

class Robot:
    def __init__(self, nom, x=0, y=0, direction="N"):
        self.nom = nom
        self.x = x
        self.y = y
        self.direction = direction
        self.moves = 0
        self.score = 0
        self.msemmen_collected = 0
        self.lben_collected = 0
        self.garo_active = 0  # Temps restant de power-up
        self.lives = 3
        self.game_over = False
        self.victory = False

    def move(self, dx, dy):
        """Déplace le robot dans la direction donnée"""
        new_x = max(-GRID_SIZE // 2, min(self.x + dx, GRID_SIZE // 2))
        new_y = max(-GRID_SIZE // 2, min(self.y + dy, GRID_SIZE // 2))
        
        if new_x != self.x or new_y != self.y:
            self.x = new_x
            self.y = new_y
            self.moves += 1
            return True
        return False

    def position(self):
        return f"({self.x:+3d}, {self.y:+3d})"


class Enemy:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.scared = False
        self.home_x = x
        self.home_y = y
        
    def move(self, robot_pos):
        if random.random() < 0.6:  # 60% chance de bouger
            dx, dy = 0, 0
            
            # Si effrayé, fuir le robot
            if self.scared:
                if self.x < robot_pos[0]:
                    dx = -1
                elif self.x > robot_pos[0]:
                    dx = 1
                if self.y < robot_pos[1]:
                    dy = -1
                elif self.y > robot_pos[1]:
                    dy = 1
            else:
                # Sinon, poursuivre le robot
                if self.x < robot_pos[0]:
                    dx = 1
                elif self.x > robot_pos[0]:
                    dx = -1
                if self.y < robot_pos[1]:
                    dy = 1
                elif self.y > robot_pos[1]:
                    dy = -1
            
            # Bouger
            new_x = max(-GRID_SIZE // 2, min(self.x + dx, GRID_SIZE // 2))
            new_y = max(-GRID_SIZE // 2, min(self.y + dy, GRID_SIZE // 2))
            self.x = new_x
            self.y = new_y
    
    def respawn(self):
        """Réapparaître à la position d'origine"""
        self.x = self.home_x
        self.y = self.home_y


class Game:
    def __init__(self):
        self.robot = None
        self.enemies = []
        self.msemmen = set()  # Positions des msemmen
        self.lben = set()     # Positions du lben
        self.garo = set()     # Positions du garo (power-ups)
        self.start_time = time()
        self.paused = False
        
    def init_game(self, robot_name):
        centre = GRID_SIZE // 2
        self.robot = Robot(robot_name, 0, 0, "N")
        
        # Créer les ennemis avec couleurs
        enemy_colors = ["red", "cyan", "magenta"]
        enemy_positions = [(5, 5), (-5, 5), (0, 7)]
        
        for i in range(ENEMY_COUNT):
            x, y = enemy_positions[i]
            self.enemies.append(Enemy(x, y, enemy_colors[i]))
        
        # Placer les items aléatoirement
        positions_taken = {(0, 0)}  # Position de départ du robot
        for enemy in self.enemies:
            positions_taken.add((enemy.x, enemy.y))
        
        # Msemmen
        while len(self.msemmen) < MSEMMEN_COUNT:
            x = random.randint(-centre + 2, centre - 2)
            y = random.randint(-centre + 2, centre - 2)
            if (x, y) not in positions_taken:
                self.msemmen.add((x, y))
                positions_taken.add((x, y))
        
        # Lben
        while len(self.lben) < LBEN_COUNT:
            x = random.randint(-centre + 2, centre - 2)
            y = random.randint(-centre + 2, centre - 2)
            if (x, y) not in positions_taken:
                self.lben.add((x, y))
                positions_taken.add((x, y))
        
        # Garo (power-ups)
        while len(self.garo) < GARO_COUNT:
            x = random.randint(-centre + 2, centre - 2)
            y = random.randint(-centre + 2, centre - 2)
            if (x, y) not in positions_taken:
                self.garo.add((x, y))
                positions_taken.add((x, y))
    
    def check_collisions(self):
        pos = (self.robot.x, self.robot.y)
        
        # Collecter msemmen
        if pos in self.msemmen:
            self.msemmen.remove(pos)
            self.robot.msemmen_collected += 1
            self.robot.score += 10
            if self.robot.msemmen_collected >= MSEMMEN_COUNT:
                self.robot.victory = True
            return "🥞 Miam! Msemmen délicieux! +10 pts"
        
        # Collecter harira (power-up)
        if pos in self.harira:
            self.harira.remove(pos)
            self.robot.harira_active = 10  # 10 mouvements de protection
            self.robot.score += 50
            for enemy in self.enemies:
                enemy.scared = True
            return "🍲 HARIRA! Les djinns ont peur! +50 pts"
        
        # Collision avec ennemis
        for enemy in self.enemies:
            if enemy.x == self.robot.x and enemy.y == self.robot.y:
                if self.robot.harira_active > 0:
                    # Manger l'ennemi!
                    self.robot.score += 200
                    enemy.x = random.randint(-GRID_SIZE // 2, GRID_SIZE // 2)
                    enemy.y = random.randint(-GRID_SIZE // 2, GRID_SIZE // 2)
                    return f"💪 {enemy.name} vaincu! +200 pts"
                else:
                    # Perdre une vie
                    self.robot.lives -= 1
                    if self.robot.lives <= 0:
                        self.robot.game_over = True
                        return "💀 GAME OVER! Les djinns t'ont eu!"
                    else:
                        self.robot.x = 0
                        self.robot.y = 0
                        return f"😵 Aïe! Vie perdue! Il reste {self.robot.lives} vies"
        
        return ""
    
    def update_enemies(self):
        current_time = time()
        if current_time - self.last_move_time > 0.5:  # Ennemis bougent toutes les 0.5s
            for enemy in self.enemies:
                enemy.move((self.robot.x, self.robot.y))
            self.last_move_time = current_time
            
            # Décrémenter le temps de power-up
            if self.robot.harira_active > 0:
                self.robot.harira_active -= 1
                if self.robot.harira_active == 0:
                    for enemy in self.enemies:
                        enemy.scared = False


class GameDisplay:
    def __init__(self, taille=GRID_SIZE):
        self.taille = taille
        self.centre = taille // 2
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_game(self, game, message=""):
        self.clear_screen()
        robot = game.robot
        
        # En-tête stylisé marocain
        print("╔" + "═" * 78 + "╗")
        print("║" + f"🕌  ROBOT FI DERB - La Quête des Msemmen de {robot.nom.upper()}  🕌".center(78) + "║")
        print("╠" + "═" * 78 + "╣")
        
        # Stats
        vies = "❤️ " * robot.lives + "🖤" * (3 - robot.lives)
        harira_bar = "🔥" * min(robot.harira_active, 10) if robot.harira_active > 0 else ""
        print("║ " + f"Score: {robot.score}  |  {vies}  |  Msemmen: {robot.msemmen_collected}/{MSEMMEN_COUNT}  |  {harira_bar}".ljust(76) + " ║")
        print("╠" + "═" * 78 + "╣")
        
        # Grille de jeu
        for y in range(self.taille - 1, -1, -1):
            ligne = "║ "
            for x in range(self.taille):
                pos_x = x - self.centre
                pos_y = y - self.centre
                pos = (pos_x, pos_y)
                
                # Vérifier si c'est le robot
                if pos_x == robot.x and pos_y == robot.y:
                    if robot.harira_active > 0:
                        ligne += "🤩"  # Robot surpuissant
                    else:
                        symboles = {"N": "🔼", "E": "▶️", "S": "🔽", "O": "◀️"}
                        ligne += symboles.get(robot.direction, "🤖")
                # Vérifier les ennemis
                elif any(e.x == pos_x and e.y == pos_y for e in game.enemies):
                    enemy = next(e for e in game.enemies if e.x == pos_x and e.y == pos_y)
                    if enemy.scared:
                        ligne += "😱"  # Ennemi effrayé
                    else:
                        ligne += enemy.color
                # Vérifier les items
                elif pos in game.harira:
                    ligne += "🍲"  # Harira
                elif pos in game.msemmen:
                    ligne += "🥞"  # Msemmen
                # Murs et décorations
                elif (abs(pos_x) == self.centre or abs(pos_y) == self.centre):
                    ligne += "🧱"
                elif pos_x == 0 and pos_y == 0:
                    ligne += "🏠"  # Maison de départ
                else:
                    ligne += "··"
            
            print(ligne + " ║")
        
        # Séparateur
        print("╠" + "═" * 78 + "╣")
        
        # Temps de jeu
        temps = int(time() - game.start_time)
        print("║ " + f"{robot.position()}  |  Temps: {temps}s".ljust(76) + " ║")
        
        # Message d'action
        if message:
            print("║ " + f">>> {message}".ljust(76) + " ║")
        
        # Info sur les ennemis
        enemy_status = " | ".join([f"{e.name[:10]}: {'😱' if e.scared else '👹'}" for e in game.enemies])
        print("║ " + enemy_status.ljust(76) + " ║")
        
        # Séparateur
        print("╠" + "═" * 78 + "╣")
        
        # Commandes
        print("║ 🎮 COMMANDES: ↑↓←→ ou WASD pour bouger  |  ESPACE: pause  |  Q: quitter".ljust(79) + "║")
        print("╚" + "═" * 78 + "╝")
    
    def show_story_intro(self):
        self.clear_screen()
        print("╔" + "═" * 78 + "╗")
        print("║" + "🕌  ROBOT FI DERB - La Légende des Msemmen Perdus  🕌".center(78) + "║")
        print("╠" + "═" * 78 + "╣")
        print("║" + " " * 78 + "║")
        print("║" + "  Il était une fois dans les ruelles mystiques de Marrakech...".ljust(78) + "║")
        print("║" + " " * 78 + "║")
        print("║" + "  Un robot courageux doit récupérer tous les msemmen sacrés".ljust(78) + "║")
        print("║" + "  dispersés dans le labyrinthe du vieux derb.".ljust(78) + "║")
        print("║" + " " * 78 + "║")
        print("║" + "  Mais attention! Trois djinns gardent les trésors:".ljust(78) + "║")
        print("║" + "    👻 Aicha Kandisha - La dame de la rivière".ljust(78) + "║")
        print("║" + "    😈 Bouya Omar - Le djinn du sanctuaire".ljust(78) + "║")
        print("║" + "    👹 Lalla Mira - L'esprit de la médina".ljust(78) + "║")
        print("║" + " " * 78 + "║")
        print("║" + "  🥞 Collecte tous les msemmen pour gagner!".ljust(78) + "║")
        print("║" + "  🍲 La harira te donne le pouvoir de vaincre les djinns!".ljust(78) + "║")
        print("║" + "  ❤️  Tu as 3 vies. Utilise-les sagement!".ljust(78) + "║")
        print("║" + " " * 78 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║" + "  Que la baraka soit avec toi! 🤲".center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        print()
    
    def show_game_over(self, game, victory=False):
        self.clear_screen()
        robot = game.robot
        print("╔" + "═" * 78 + "╗")
        if victory:
            print("║" + "🎉🎉🎉  MABROUK! TU AS GAGNÉ!  🎉🎉🎉".center(78) + "║")
            print("╠" + "═" * 78 + "╣")
            print("║" + " " * 78 + "║")
            print("║" + f"  Tous les msemmen ont été récupérés!".center(78) + "║")
            print("║" + f"  Les djinns se sont enfuis de la médina!".center(78) + "║")
        else:
            print("║" + "💀  GAME OVER - Les Djinns Ont Gagné  💀".center(78) + "║")
            print("╠" + "═" * 78 + "╣")
            print("║" + " " * 78 + "║")
            print("║" + f"  Le robot {robot.nom} a été vaincu...".center(78) + "║")
            print("║" + "  Mais n'abandonne pas! Réessaie encore!".center(78) + "║")
        
        temps = int(time() - game.start_time)
        print("║" + " " * 78 + "║")
        print("║" + f"  📊 STATISTIQUES FINALES 📊".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("║" + f"    Score Final: {robot.score}".ljust(78) + "║")
        print("║" + f"    Msemmen Collectés: {robot.msemmen_collected}/{MSEMMEN_COUNT}".ljust(78) + "║")
        print("║" + f"    Temps de Jeu: {temps} secondes".ljust(78) + "║")
        print("║" + f"    Mouvements: {robot.moves}".ljust(78) + "║")
        print("║" + " " * 78 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║" + "  Merci d'avoir joué à Robot Fi Derb! 🕌".center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        print()


def jouer():
    display = GameDisplay()
    game = Game()
    
    # Écran d'histoire
    display.show_story_intro()
    nom = input("  Quel est le nom de ton robot héroïque? ").strip()
    if not nom:
        nom = "Robo"
    
    # Initialiser le jeu
    game.init_game(nom)
    message = f"🚀 Que l'aventure commence, {nom}!"
    
    display.draw_game(game, message)
    sleep(1)
    
    while True:
        # Mettre à jour les ennemis
        game.update_enemies()
        
        if msvcrt.kbhit():
            touche = msvcrt.getch()
            message = ""
            
            # Gérer les touches spéciales (flèches)
            if touche == b'\xe0' or touche == b'\x00':
                touche = msvcrt.getch()
                if touche == b'H':  # Flèche haut
                    game.robot.avancer()
                    message = game.check_collisions()
                elif touche == b'K':  # Flèche gauche
                    game.robot.tourner_gauche()
                    message = "↺ Tournée à gauche!"
                elif touche == b'M':  # Flèche droite
                    game.robot.tourner_droite()
                    message = "↻ Tournée à droite!"
                elif touche == b'P':  # Flèche bas
                    game.robot.reculer()
                    message = game.check_collisions()
                else:
                    continue
            else:
                try:
                    commande = touche.decode('utf-8').lower()
                except:
                    continue
                
                if commande == 'w':
                    game.robot.avancer()
                    message = game.check_collisions()
                elif commande == 'a':
                    game.robot.tourner_gauche()
                    message = "↺ Tournée à gauche!"
                elif commande == 'd':
                    game.robot.tourner_droite()
                    message = "↻ Tournée à droite!"
                elif commande == 's':
                    game.robot.reculer()
                    message = game.check_collisions()
                elif commande == ' ':
                    message = "⏸ Pause... Les djinns continuent de bouger!"
                    sleep(0.5)
                elif commande == 'q':
                    display.clear_screen()
                    print("\n👋 Abandon de la quête... Les djinns dansent de joie!\n")
                    break
                else:
                    continue
            
            # Vérifier victoire ou défaite
            if game.robot.victory:
                display.draw_game(game, "🎉 TOUS LES MSEMMEN COLLECTÉS!")
                sleep(2)
                display.show_game_over(game, victory=True)
                break
            elif game.robot.game_over:
                display.draw_game(game, "💀 TOUTES LES VIES PERDUES!")
                sleep(2)
                display.show_game_over(game, victory=False)
                break
            
            display.draw_game(game, message)
        
        # Petit délai pour réduire l'utilisation CPU
        sleep(0.05)


if __name__ == "__main__":
    try:
        jouer()
    except KeyboardInterrupt:
        print("\n\n👋 Jeu interrompu. Bessaha ou raha!\n")
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")
