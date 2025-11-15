import tkinter as tk
from tkinter import messagebox
import random
from time import time

# Configuration du jeu
GRID_SIZE = 19
CELL_SIZE = 35
MSEMMEN_COUNT = 25
LBEN_COUNT = 4
ENEMY_COUNT = 3

class Robot:
    def __init__(self, nom, x=0, y=0, direction="N"):
        self.nom = nom
        self.x = x
        self.y = y
        self.direction = direction
        self.score = 0
        self.msemmen_collected = 0
        self.lben_active = 0
        self.lives = 3
        self.game_over = False
        self.victory = False

    def avancer(self):
        match self.direction:
            case "N":
                self.y = min(self.y + 1, GRID_SIZE // 2)
            case "E":
                self.x = min(self.x + 1, GRID_SIZE // 2)
            case "O":
                self.x = max(self.x - 1, -GRID_SIZE // 2)
            case "S":
                self.y = max(self.y - 1, -GRID_SIZE // 2)

    def reculer(self):
        match self.direction:
            case "N":
                self.y = max(self.y - 1, -GRID_SIZE // 2)
            case "E":
                self.x = max(self.x - 1, -GRID_SIZE // 2)
            case "O":
                self.x = min(self.x + 1, GRID_SIZE // 2)
            case "S":
                self.y = min(self.y + 1, GRID_SIZE // 2)

    def tourner_gauche(self):
        match self.direction:
            case "N":
                self.direction = "O"
            case "E":
                self.direction = "N"
            case "O":
                self.direction = "S"
            case "S":
                self.direction = "E"

    def tourner_droite(self):
        match self.direction:
            case "N":
                self.direction = "E"
            case "E":
                self.direction = "S"
            case "O":
                self.direction = "N"
            case "S":
                self.direction = "O"


class Enemy:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(["N", "S", "E", "O"])
        self.scared = False
        
    def move(self, robot_pos):
        if random.random() < 0.7:
            choices = []
            if self.scared:
                if self.x < robot_pos[0]:
                    choices.append("O")
                elif self.x > robot_pos[0]:
                    choices.append("E")
                if self.y < robot_pos[1]:
                    choices.append("S")
                elif self.y > robot_pos[1]:
                    choices.append("N")
            else:
                if self.x < robot_pos[0]:
                    choices.append("E")
                elif self.x > robot_pos[0]:
                    choices.append("O")
                if self.y < robot_pos[1]:
                    choices.append("N")
                elif self.y > robot_pos[1]:
                    choices.append("S")
            
            if choices:
                self.direction = random.choice(choices)
            else:
                self.direction = random.choice(["N", "S", "E", "O"])
        
        match self.direction:
            case "N":
                self.y = min(self.y + 1, GRID_SIZE // 2)
            case "S":
                self.y = max(self.y - 1, -GRID_SIZE // 2)
            case "E":
                self.x = min(self.x + 1, GRID_SIZE // 2)
            case "O":
                self.x = max(self.x - 1, -GRID_SIZE // 2)


class Game:
    def __init__(self, canvas, status_label):
        self.canvas = canvas
        self.status_label = status_label
        self.robot = None
        self.enemies = []
        self.msemmen = set()
        self.lben = set()
        self.garo = set()  # Obstacles
        self.start_time = time()
        self.last_move_time = time()
        self.running = False
        
    def init_game(self, robot_name):
        centre = GRID_SIZE // 2
        self.robot = Robot(robot_name, 0, 0, "N")
        
        # Créer les ennemis
        enemy_positions = [(5, 5, "#FF0000"), (-5, 5, "#FF69B4"), (0, 7, "#00CED1")]
        for x, y, color in enemy_positions[:ENEMY_COUNT]:
            self.enemies.append(Enemy(x, y, color))
        
        # Positions occupées
        positions_taken = {(0, 0)}
        for enemy in self.enemies:
            positions_taken.add((enemy.x, enemy.y))
        
        # Placer les garo (obstacles)
        garo_count = 15
        while len(self.garo) < garo_count:
            x = random.randint(-centre + 2, centre - 2)
            y = random.randint(-centre + 2, centre - 2)
            if (x, y) not in positions_taken and abs(x) + abs(y) > 3:
                self.garo.add((x, y))
                positions_taken.add((x, y))
        
        # Placer les msemmen
        while len(self.msemmen) < MSEMMEN_COUNT:
            x = random.randint(-centre + 1, centre - 1)
            y = random.randint(-centre + 1, centre - 1)
            if (x, y) not in positions_taken and (x, y) not in self.garo:
                self.msemmen.add((x, y))
                positions_taken.add((x, y))
        
        # Placer les lben (power-ups)
        while len(self.lben) < LBEN_COUNT:
            x = random.randint(-centre + 1, centre - 1)
            y = random.randint(-centre + 1, centre - 1)
            if (x, y) not in positions_taken and (x, y) not in self.garo:
                self.lben.add((x, y))
                positions_taken.add((x, y))
        
        self.running = True
        self.draw()
        self.update_status()
    
    def check_collisions(self):
        pos = (self.robot.x, self.robot.y)
        message = ""
        
        # Vérifier collision avec obstacles
        if pos in self.garo:
            # Revenir à la position précédente
            match self.robot.direction:
                case "N":
                    self.robot.y -= 1
                case "S":
                    self.robot.y += 1
                case "E":
                    self.robot.x -= 1
                case "O":
                    self.robot.x += 1
            return "🧱 Obstacle! Impossible de passer!"
        
        # Collecter msemmen
        if pos in self.msemmen:
            self.msemmen.remove(pos)
            self.robot.msemmen_collected += 1
            self.robot.score += 10
            if self.robot.msemmen_collected >= MSEMMEN_COUNT:
                self.robot.victory = True
            message = "🥞 Msemmen! +10 pts"
        
        # Collecter lben (power-up)
        if pos in self.lben:
            self.lben.remove(pos)
            self.robot.lben_active = 15
            self.robot.score += 50
            for enemy in self.enemies:
                enemy.scared = True
            message = "🥛 LBEN! Les fantômes ont peur! +50 pts"
        
        # Collision avec ennemis
        for enemy in self.enemies:
            if enemy.x == self.robot.x and enemy.y == self.robot.y:
                if self.robot.lben_active > 0:
                    self.robot.score += 200
                    enemy.x = random.randint(-GRID_SIZE // 2, GRID_SIZE // 2)
                    enemy.y = random.randint(-GRID_SIZE // 2, GRID_SIZE // 2)
                    message = "💪 Fantôme vaincu! +200 pts"
                else:
                    self.robot.lives -= 1
                    if self.robot.lives <= 0:
                        self.robot.game_over = True
                    else:
                        self.robot.x = 0
                        self.robot.y = 0
                        message = f"😵 Vie perdue! {self.robot.lives} restantes"
        
        return message
    
    def update_enemies(self):
        current_time = time()
        if current_time - self.last_move_time > 0.4:
            for enemy in self.enemies:
                old_pos = (enemy.x, enemy.y)
                enemy.move((self.robot.x, self.robot.y))
                # Vérifier collision avec obstacles
                if (enemy.x, enemy.y) in self.garo:
                    enemy.x, enemy.y = old_pos
            self.last_move_time = current_time
            
            if self.robot.lben_active > 0:
                self.robot.lben_active -= 1
                if self.robot.lben_active == 0:
                    for enemy in self.enemies:
                        enemy.scared = False
    
    def grid_to_canvas(self, x, y):
        """Convertir coordonnées de grille en coordonnées canvas"""
        canvas_x = (x + GRID_SIZE // 2) * CELL_SIZE + CELL_SIZE // 2
        canvas_y = (GRID_SIZE // 2 - y) * CELL_SIZE + CELL_SIZE // 2
        return canvas_x, canvas_y
    
    def draw(self):
        self.canvas.delete("all")
        
        # Fond avec motif
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = "#1E1E1E" if (i + j) % 2 == 0 else "#252525"
                self.canvas.create_rectangle(
                    i * CELL_SIZE, j * CELL_SIZE,
                    (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                    fill=color, outline=""
                )
        
        # Dessiner les lignes de grille plus subtiles
        for i in range(GRID_SIZE + 1):
            x = i * CELL_SIZE
            self.canvas.create_line(x, 0, x, GRID_SIZE * CELL_SIZE, fill="#3A3A3A", width=1)
            self.canvas.create_line(0, x, GRID_SIZE * CELL_SIZE, x, fill="#3A3A3A", width=1)
        # Dessiner les ennemis avec détails améliorés
        for enemy in self.enemies:
            cx, cy = self.grid_to_canvas(enemy.x, enemy.y)
            color = "#4169E1" if enemy.scared else enemy.color
            
            # Ombre fantôme
            self.canvas.create_oval(
                cx - 10, cy - 8, cx + 10, cy + 15,
                fill="#000000", outline="", stipple="gray50"
            )
            
            # Corps fantôme
            self.canvas.create_oval(
                cx - 13, cy - 13, cx + 13, cy + 13,
                fill=color, outline="black", width=2
            )
            
            # Yeux
            eye_color = "white" if not enemy.scared else "yellow"
            pupil_color = "black" if not enemy.scared else "white"
            
            # Oeil gauche
            self.canvas.create_oval(cx - 7, cy - 5, cx - 1, cy + 1, fill=eye_color, outline="black")
            self.canvas.create_oval(cx - 6, cy - 3, cx - 3, cy, fill=pupil_color)
            
            # Oeil droit
            self.canvas.create_oval(cx + 1, cy - 5, cx + 7, cy + 1, fill=eye_color, outline="black")
            self.canvas.create_oval(cx + 3, cy - 3, cx + 6, cy, fill=pupil_color)
            
            # Bouche
            if enemy.scared:
                # Bouche effrayée
                self.canvas.create_arc(
                    cx - 5, cy + 2, cx + 5, cy + 8,
                    start=180, extent=180, fill="black", outline="black"
                )
            else:
                # Bouche menaçante
                self.canvas.create_arc(
                    cx - 5, cy + 2, cx + 5, cy + 8,
                    start=0, extent=180, fill="black", outline="black"
                )
        
        for gx, gy in self.garo:
            cx, cy = self.grid_to_canvas(gx, gy)
            self.canvas.create_rectangle(
                cx - CELL_SIZE // 2 + 2, cy - CELL_SIZE // 2 + 2,
                cx + CELL_SIZE // 2 - 2, cy + CELL_SIZE // 2 - 2,
                fill="#8B4513", outline="#654321", width=2
            )
        
        # Dessiner les msemmen avec animation
        for mx, my in self.msemmen:
            cx, cy = self.grid_to_canvas(mx, my)
            # Halo doré
            self.canvas.create_oval(
                cx - 8, cy - 8, cx + 8, cy + 8,
                fill="#FFA500", outline="", stipple="gray25"
            )
            # Msemmen
            self.canvas.create_oval(
                cx - 5, cy - 5, cx + 5, cy + 5,
                fill="#FFD700", outline="#FF8C00", width=2
            )
            # Point brillant
            self.canvas.create_oval(
                cx - 2, cy - 2, cx, cy,
                fill="#FFFF00", outline=""
            )
        
        # Dessiner les lben (plus gros et animé)
        for lx, ly in self.lben:
            cx, cy = self.grid_to_canvas(lx, ly)
            # Aura de power-up
            self.canvas.create_oval(
                cx - 14, cy - 14, cx + 14, cy + 14,
                outline="#87CEEB", width=2, dash=(2, 2)
            )
            # Lben
            self.canvas.create_oval(
                cx - 10, cy - 10, cx + 10, cy + 10,
                fill="#FFFFFF", outline="#4682B4", width=3
            )
            # Reflet
            self.canvas.create_oval(
                cx - 6, cy - 6, cx - 2, cy - 2,
                fill="#E0FFFF", outline=""
            )
            # Texte L
            self.canvas.create_text(
                cx, cy + 1,
                text="L", font=("Arial", 10, "bold"),
                fill="#4682B4"
            )
        
        # Dessiner les ennemis
        for enemy in self.enemies:
            cx, cy = self.grid_to_canvas(enemy.x, enemy.y)
            color = "#4169E1" if enemy.scared else enemy.color
            self.canvas.create_oval(
                cx - 12, cy - 12, cx + 12, cy + 12,
                fill=color, outline="black", width=2
            )
            # Yeux
            eye_color = "white" if not enemy.scared else "black"
            self.canvas.create_oval(cx - 6, cy - 4, cx - 2, cy + 0, fill=eye_color)
            self.canvas.create_oval(cx + 2, cy - 4, cx + 6, cy + 0, fill=eye_color)
        
        # Dessiner le robot
        if self.robot:
            cx, cy = self.grid_to_canvas(self.robot.x, self.robot.y)
            
            # Ombre
            self.canvas.create_oval(
                cx - 12, cy - 10, cx + 12, cy + 14,
                fill="#000000", outline="", stipple="gray50"
            )
            
            # Corps du robot avec effet brillant
            robot_color = "#FFD700" if self.robot.lben_active > 0 else "#00FF00"
            self.canvas.create_oval(
                cx - 15, cy - 15, cx + 15, cy + 15,
                fill=robot_color, outline="#004400", width=3
            )
            
            # Effet brillant
            self.canvas.create_oval(
                cx - 9, cy - 9, cx - 3, cy - 3,
                fill="#FFFFFF", outline="", stipple="gray50"
            )
            
            # Direction avec flèche plus grande et visible
            if self.robot.direction == "N":
                points = [cx, cy - 12, cx - 8, cy + 2, cx + 8, cy + 2]
            elif self.robot.direction == "S":
                points = [cx, cy + 12, cx - 8, cy - 2, cx + 8, cy - 2]
            elif self.robot.direction == "E":
                points = [cx + 12, cy, cx - 2, cy - 8, cx - 2, cy + 8]
            else:  # O
                points = [cx - 12, cy, cx + 2, cy - 8, cx + 2, cy + 8]
            
            self.canvas.create_polygon(points, fill="#FF0000", outline="#8B0000", width=2)
            
            # Trail/traînée si power-up actif
            if self.robot.lben_active > 0:
                self.canvas.create_oval(
                    cx - 20, cy - 20, cx + 20, cy + 20,
                    outline="#FFD700", width=2, dash=(4, 4)
                )
    
    def update_status(self):
        if self.robot:
            vies = "❤️" * self.robot.lives + "🖤" * (3 - self.robot.lives)
            power = f" | 🔥LBEN: {self.robot.lben_active}s" if self.robot.lben_active > 0 else ""
            temps = int(time() - self.start_time)
            pause_text = " ⏸PAUSE" if not self.running else ""
            status = f"Score: {self.robot.score} | {vies} | Msemmen: {self.robot.msemmen_collected}/{MSEMMEN_COUNT} | Temps: {temps}s{power}{pause_text}"
            self.status_label.config(text=status)


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🕌 ROBOT FI DERB - La Quête des Msemmen")
        self.root.resizable(False, False)
        
        # Titre
        title_frame = tk.Frame(root, bg="#2C3E50", pady=10)
        title_frame.pack(fill=tk.X)
        
        title = tk.Label(
            title_frame,
            text="🕌 ROBOT FI DERB - La Quête des Msemmen 🕌",
            font=("Arial", 20, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title.pack()
        
        # Canvas pour le jeu
        self.canvas = tk.Canvas(
            root,
            width=GRID_SIZE * CELL_SIZE,
            height=GRID_SIZE * CELL_SIZE,
            bg="#1A1A1A",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Barre de statut
        status_frame = tk.Frame(root, bg="#34495E", pady=8)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="Score: 0 | ❤️❤️❤️ | Msemmen: 0/25 | Temps: 0s",
            font=("Arial", 12, "bold"),
            bg="#34495E",
            fg="#ECF0F1"
        )
        self.status_label.pack()
        
        # Instructions
        info_frame = tk.Frame(root, bg="#95A5A6", pady=5)
        info_frame.pack(fill=tk.X)
        
        info = tk.Label(
            info_frame,
            text="🎮 Flèches/WASD: Bouger | ESPACE: Pause | R: Restart | 🥞 Msemmen: +10pts | 🥛 Lben: Power-up",
            font=("Arial", 10),
            bg="#95A5A6",
            fg="#2C3E50"
        )
        info.pack()
        
        self.game = Game(self.canvas, self.status_label)
        
        # Dialogue de démarrage
        self.show_intro()
        
        # Bindings
        self.root.bind("<Key>", self.on_key_press)
        
        # Boucle de jeu
        self.game_loop()
    
    def show_intro(self):
        intro = """🕌 BIENVENUE DANS ROBOT FI DERB! 🕌

Il était une fois dans les ruelles mystiques de Marrakech...

Ta mission: Collecter tous les msemmen sacrés! 🥞

Attention aux fantômes qui gardent le trésor!
Utilise le lben 🥛 pour les vaincre!
Évite les garo (obstacles) 🧱

Que la baraka soit avec toi! 🤲"""
        
        messagebox.showinfo("Histoire", intro)
        nom = tk.simpledialog.askstring("Nom du Robot", "Quel est le nom de ton robot héroïque?", parent=self.root)
        if not nom:
            nom = "Robo"
        self.game.init_game(nom)
    
    def on_key_press(self, event):
        if not self.game.running or self.game.robot.game_over or self.game.robot.victory:
            return
        
        key = event.keysym.lower()
        message = ""
        
        # Mouvement direct et intuitif
        if key in ['up', 'w']:
            self.game.robot.direction = "N"
            self.game.robot.avancer()
            message = self.game.check_collisions()
        elif key in ['down', 's']:
            self.game.robot.direction = "S"
            self.game.robot.avancer()
            message = self.game.check_collisions()
        elif key in ['left', 'a']:
            self.game.robot.direction = "O"
            self.game.robot.avancer()
            message = self.game.check_collisions()
        elif key in ['right', 'd']:
            self.game.robot.direction = "E"
            self.game.robot.avancer()
            message = self.game.check_collisions()
        elif key == 'space':
            # Pause/unpause
            self.game.running = not self.game.running
            return
        elif key == 'r':
            # Restart rapide
            self.game = Game(self.canvas, self.status_label)
            nom = self.game.robot.nom if self.game.robot else "Robo"
            self.game.init_game(nom)
            return
        
        self.game.draw()
        self.game.update_status()
        
        if self.game.robot.victory:
            self.game.running = False
            self.show_end_screen(True)
        elif self.game.robot.game_over:
            self.game.running = False
            self.show_end_screen(False)
    
    def game_loop(self):
        if self.game.running and not self.game.robot.game_over and not self.game.robot.victory:
            self.game.update_enemies()
            message = self.game.check_collisions()
            self.game.draw()
            self.game.update_status()
            
            if self.game.robot.victory:
                self.game.running = False
                self.show_end_screen(True)
            elif self.game.robot.game_over:
                self.game.running = False
                self.show_end_screen(False)
        
        self.root.after(100, self.game_loop)
    
    def show_end_screen(self, victory):
        temps = int(time() - self.game.start_time)
        
        if victory:
            message = f"""🎉🎉🎉 MABROUK! TU AS GAGNÉ! 🎉🎉🎉

Tous les msemmen ont été récupérés!
Les fantômes se sont enfuis de la médina!

📊 STATISTIQUES FINALES:
Score Final: {self.game.robot.score}
Msemmen Collectés: {self.game.robot.msemmen_collected}/{MSEMMEN_COUNT}
Temps de Jeu: {temps} secondes

Bessaha ou raha! 🤲"""
        else:
            message = f"""💀 GAME OVER 💀

Le robot a été vaincu...
Mais n'abandonne pas! Réessaie encore!

📊 STATISTIQUES FINALES:
Score Final: {self.game.robot.score}
Msemmen Collectés: {self.game.robot.msemmen_collected}/{MSEMMEN_COUNT}
Temps de Jeu: {temps} secondes"""
        
        result = messagebox.askyesno("Fin du Jeu", message + "\n\nVeux-tu rejouer?")
        if result:
            self.game = Game(self.canvas, self.status_label)
            self.show_intro()
        else:
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    
    # Importer simpledialog pour le nom
    import tkinter.simpledialog
    
    game_gui = GameGUI(root)
    root.mainloop()
