import pyxel

WINDOW_WIDTH = 252
WINDOW_HEIGHT = 216
MAP_HEIGHT = 160

PLAYER_START_MONEY = 200  
PLAYER_START_LIVES = 20   

BLOON_HPS = [1, 2, 3, 4]  
BLOON_SPEEDS = [1.0, 1.5, 2.0, 2.5]  

TOWER_RANGES = [60, 85, 110]
TOWER_DAMAGES = [2, 3, 4]     
TOWER_COOLDOWN = 50           

BULLET_SPEED = 6  
COLLISION_THRESHOLD = 5
TOWER_COSTS = [60, 90, 120]
MAX_HORDES = 10

class Game:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Pokemon TD")
        pyxel.mouse(True)
        self._load_assets()
        self._init_sounds()
        self.reset()
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def _init_sounds(self):
        pyxel.sound(0).set(
            notes='C3 E3 G3 C4 G3 E3 R C3 E3 G3',
            tones='T',
            volumes='4',
            effects='N',
            speed=50
        )
        pyxel.sound(1).set(
            notes='C3E3G3',
            tones='S',
            volumes='4',
            effects='F',
            speed=20
        )
        pyxel.sound(2).set(
            notes='E3G3B3',
            tones='T',
            volumes='4',
            effects='F',
            speed=18
        )
        pyxel.sound(3).set(
            notes='G3B3D4',
            tones='P',
            volumes='4',
            effects='N',
            speed=15
        )
        pyxel.sound(4).set(
            notes='C2',
            tones='N',
            volumes='3',
            effects='F',
            speed=30
        )
        pyxel.sound(5).set(
            notes='C4E4G4',
            tones='S',
            volumes='4',
            effects='N',
            speed=10
        )
        pyxel.sound(6).set(
            notes='C3G2C2',
            tones='T',
            volumes='4',
            effects='F',
            speed=8
        )
        pyxel.music(0).set([0], [], [], [])

    def _load_assets(self):
        pyxel.image(0).load(0, 0, "mapa.png")
        for i, img in enumerate(["blastoise.png", "venusaur.png", "charizard.png"]):
            pyxel.image(1).load(i * 32, 0, img)
        for i, img in enumerate(["rattata.png", "raticate.png", "articuno.png", "mew.png"]):
            pyxel.image(2).load(i * 16, 0, img)

    def reset(self):
        self.money = PLAYER_START_MONEY
        self.lives = PLAYER_START_LIVES
        self.bloons = []
        self.towers = []
        self.bullets = []
        self.selected = None
        self.path = [(251, 75), (159, 75), (159, 107), (89, 107),
                     (89, 39), (40, 39), (40, 95), (0, 95)]
        self.timer = 0
        self.horde = 1
        self.remaining = 5 + self.horde * 2
        self.level = 0
        self.game_over = False
        self.paused = False

    def spawn_bloon(self):
        if self.horde <= 3:
            bloon_type = 0
        elif self.horde <= 6:
            bloon_type = 1 if pyxel.rndi(0, 1) else 0
        elif self.horde <= 9:
            bloon_type = pyxel.rndi(0, 2)
        else:
            bloon_type = pyxel.rndi(0, 3)

        self.bloons.append({
            "x": self.path[0][0],
            "y": self.path[0][1],
            "hp": BLOON_HPS[bloon_type],
            "speed": BLOON_SPEEDS[bloon_type],
            "idx": 0,
            "type": bloon_type
        })

    def update_bloons(self):
        for b in self.bloons[:]:
            next_idx = b["idx"] + 1
            if next_idx >= len(self.path):
                self.bloons.remove(b)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                continue

            tx, ty = self.path[next_idx]
            dx = tx - b["x"]
            dy = ty - b["y"]
            dist = (dx**2 + dy**2) ** 0.5

            if dist <= b["speed"]:
                b["x"], b["y"] = tx, ty
                b["idx"] += 1
            else:
                b["x"] += b["speed"] * dx / dist
                b["y"] += b["speed"] * dy / dist

    def update_towers(self):
        for t in self.towers:
            if "cd" not in t:
                t["cd"] = 0
            if t["cd"] > 0:
                t["cd"] -= 1
                continue

            target = None
            for b in self.bloons:
                dx = b["x"] - t["x"]
                dy = b["y"] - t["y"]
                if (dx**2 + dy**2)**0.5 <= TOWER_RANGES[t["type"]]:
                    target = b
                    break

            if target:
                self.shoot(t, target)

    def update_game(self):
        if self.remaining > 0:
            self.timer += 1
            if self.timer > 25: 
                self.spawn_bloon()
                self.remaining -= 1
                self.timer = 0
        elif not self.bloons:
            if self.horde < MAX_HORDES:
                pyxel.play(1, 5)
                self.horde += 1
                self.remaining = 5 + self.horde * 2
                self.level = min(self.horde // 3, 3)
            else:
                pyxel.play(1, 6)
                self.game_over = True

        self.update_bloons()
        self.update_towers()
        self.update_bullets()

    def shoot(self, tower, target):
        pyxel.play(1, tower["type"] + 1)

        dx = target["x"] - tower["x"]
        dy = target["y"] - tower["y"]
        dist = (dx**2 + dy**2)**0.5

        if dist == 0:
            return

        next_idx = target["idx"] + 1
        if next_idx < len(self.path):
            tx, ty = self.path[next_idx]
            pred_dx = tx - target["x"]
            pred_dy = ty - target["y"]
            pred_dist = (pred_dx**2 + pred_dy**2)**0.5

            if pred_dist > 0:
                time_to_hit = dist / BULLET_SPEED
                dx = (target["x"] + (pred_dx/pred_dist) * target["speed"] * time_to_hit) - tower["x"]
                dy = (target["y"] + (pred_dy/pred_dist) * target["speed"] * time_to_hit) - tower["y"]

        angles = {0: [-15, 0, 15], 1: [-10, 10], 2: [0]}[tower["type"]]
        for ang in angles:
            rad = ang * 3.14159 / 180
            ndx = dx * pyxel.cos(rad) - dy * pyxel.sin(rad)
            ndy = dx * pyxel.sin(rad) + dy * pyxel.cos(rad)

            norm = (ndx**2 + ndy**2)**0.5
            if norm > 0:
                self.bullets.append({
                    "x": tower["x"],
                    "y": tower["y"],
                    "dx": BULLET_SPEED * (ndx / norm),
                    "dy": BULLET_SPEED * (ndy / norm),
                    "dmg": TOWER_DAMAGES[tower["type"]],
                    "color": [12, 3, 8][tower["type"]]
                })

        tower["cd"] = TOWER_COOLDOWN

    def update_bullets(self):
        for b in self.bullets[:]:
            b["x"] += b["dx"]
            b["y"] += b["dy"]

            if (b["x"] < 0 or b["x"] > WINDOW_WIDTH or 
                b["y"] < 0 or b["y"] > MAP_HEIGHT):
                self.bullets.remove(b)
                continue

            for bloon in self.bloons:
                if (abs(b["x"] - bloon["x"]) < COLLISION_THRESHOLD and 
                    abs(b["y"] - bloon["y"]) < COLLISION_THRESHOLD):
                    pyxel.play(2, 4)
                    bloon["hp"] -= b["dmg"]
                    if bloon["hp"] <= 0:
                        self.bloons.remove(bloon)
                        self.money += 10
                    self.bullets.remove(b)
                    break

    def update(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.paused = not self.paused
            if self.paused:
                pyxel.stop()
            else:
                pyxel.playm(0, loop=True)

        if self.game_over or self.paused:
            return

        self.update_game()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if pyxel.mouse_y > MAP_HEIGHT:
                x = pyxel.mouse_x
                if 10 <= x < 40: self.selected = 0
                elif 50 <= x < 80: self.selected = 1
                elif 90 <= x < 120: self.selected = 2
                elif 130 <= x < 160: self.selected = None
            elif (self.selected is not None and 
                  self.money >= TOWER_COSTS[self.selected]):
                self.towers.append({
                    "x": pyxel.mouse_x,
                    "y": pyxel.mouse_y,
                    "type": self.selected
                })
                self.money -= TOWER_COSTS[self.selected]
                self.selected = None

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 0, 0, WINDOW_WIDTH, MAP_HEIGHT)

        for b in self.bloons:
            pyxel.blt(b["x"]-8, b["y"]-8, 2, b["type"]*16, 0, 16, 16, 0)
        for t in self.towers:
            pyxel.blt(t["x"]-16, t["y"]-16, 1, t["type"]*32, 0, 32, 32, 0)
        for b in self.bullets:
            pyxel.pset(int(b["x"]), int(b["y"]), b["color"])

        pyxel.rect(0, MAP_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT-MAP_HEIGHT, 1)

        shop_items = [
            {"x": 10, "img_x": 0},
            {"x": 50, "img_x": 32},
            {"x": 90, "img_x": 64}
        ]

        for i, item in enumerate(shop_items):
            pyxel.rectb(item["x"], MAP_HEIGHT+2, 30, 30, 7)
            pyxel.blt(item["x"]-1, MAP_HEIGHT+4, 1, item["img_x"], 0, 32, 32, 0)
            pyxel.text(item["x"]+2, MAP_HEIGHT+35, f"${TOWER_COSTS[i]}", 7)

        pyxel.rectb(130, MAP_HEIGHT+2, 30, 16, 7)
        pyxel.text(135, MAP_HEIGHT+6, "Cancel", 7)

        pyxel.text(WINDOW_WIDTH-60, 5, f"Money: {self.money}", 7)
        pyxel.text(WINDOW_WIDTH-60, 15, f"Lives: {self.lives}", 8)
        pyxel.text(WINDOW_WIDTH-60, 25, f"Horde: {self.horde}/{MAX_HORDES}", 9)

        if self.selected is not None:
            pyxel.blt(pyxel.mouse_x-16, pyxel.mouse_y-16, 
                      1, self.selected*32, 0, 32, 32, 0)

        if self.game_over:
            pyxel.cls(0)
            pyxel.text(WINDOW_WIDTH//2-20, WINDOW_HEIGHT//2, 
                       "GAME OVER", pyxel.frame_count%16)
            pyxel.text(WINDOW_WIDTH//2-40, WINDOW_HEIGHT//2+10,
                       f"Hordes: {self.horde}", 7)
        elif self.paused:
            pyxel.text(WINDOW_WIDTH//2-20, WINDOW_HEIGHT//2-10, "PAUSED", 8)
Game()