import tkinter as tk
import random

# Game settings
WIDTH = 600
HEIGHT = 400
PLAYER_SPEED = 10
BULLET_SPEED = -10
ENEMY_SPEED = 2
ENEMY_DROP = 20
ENEMY_ROWS = 3
ENEMY_COLS = 5

class SpaceInvaders:
    def __init__(self, master):
        self.master = master
        master.title("Space Invaders")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.score = 0
        self.game_over = False
        self.player = self.canvas.create_rectangle(0,0,40,20, fill="white")
        self.canvas.move(self.player, WIDTH//2 - 20, HEIGHT - 30)
        self.bullets = []
        self.enemies = []
        self.enemy_direction = 1
        self.create_enemies()
        self.score_text = self.canvas.create_text(10,10, anchor="nw", fill="white", text=f"Score: {self.score}")
        master.bind("<Left>", lambda e: self.move_player(-PLAYER_SPEED))
        master.bind("<Right>", lambda e: self.move_player(PLAYER_SPEED))
        master.bind("<space>", lambda e: self.shoot())
        self.update()

    def move_player(self, dx):
        if self.game_over:
            return
        self.canvas.move(self.player, dx, 0)
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if x1 < 0:
            self.canvas.move(self.player, -x1, 0)
        elif x2 > WIDTH:
            self.canvas.move(self.player, WIDTH - x2, 0)

    def shoot(self):
        if self.game_over:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        bullet = self.canvas.create_rectangle(0,0,4,10, fill="yellow")
        self.canvas.move(bullet, (x1+x2)/2 - 2, y1 - 10)
        self.bullets.append(bullet)

    def create_enemies(self):
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                x = 60 + col * 100
                y = 40 + row * 40
                enemy = self.canvas.create_rectangle(0,0,30,20, fill="green")
                self.canvas.move(enemy, x, y)
                self.enemies.append(enemy)

    def update_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, BULLET_SPEED)
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            if by2 < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            else:
                for enemy in self.enemies[:]:
                    ex1, ey1, ex2, ey2 = self.canvas.coords(enemy)
                    if bx2 > ex1 and bx1 < ex2 and by1 < ey2 and by2 > ey1:
                        self.canvas.delete(enemy)
                        self.canvas.delete(bullet)
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        self.score += 10
                        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                        break

    def update_enemies(self):
        move_down = False
        for enemy in self.enemies:
            self.canvas.move(enemy, ENEMY_SPEED * self.enemy_direction, 0)
            x1, y1, x2, y2 = self.canvas.coords(enemy)
            if x1 <= 0 or x2 >= WIDTH:
                move_down = True
        if move_down:
            self.enemy_direction *= -1
            for enemy in self.enemies:
                self.canvas.move(enemy, 0, ENEMY_DROP)
                _, y1, _, y2 = self.canvas.coords(enemy)
                if y2 >= HEIGHT - 40:
                    self.end_game()

    def check_collision(self):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        for enemy in self.enemies:
            ex1, ey1, ex2, ey2 = self.canvas.coords(enemy)
            if px2 > ex1 and px1 < ex2 and py1 < ey2 and py2 > ey1:
                self.end_game()
                break

    def end_game(self):
        if not self.game_over:
            self.game_over = True
            self.canvas.create_text(WIDTH/2, HEIGHT/2, fill="red", text="GAME OVER", font=("Arial", 24))

    def update(self):
        if not self.game_over:
            self.update_bullets()
            self.update_enemies()
            self.check_collision()
            if not self.enemies:
                self.canvas.create_text(WIDTH/2, HEIGHT/2, fill="white", text="YOU WIN!", font=("Arial", 24))
                self.game_over = True
        self.master.after(30, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceInvaders(root)
    root.mainloop()
