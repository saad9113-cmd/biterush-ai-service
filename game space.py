import pygame
import serial
import json
import random

# -------- SERIAL SETUP --------
try:
    arduino = serial.Serial('COM7', 9600, timeout=1)  # CHANGE COM PORT
except:
    arduino = None
    print("Arduino not connected")

# -------- GAME SETUP --------
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Jet Shooter")

clock = pygame.time.Clock()

# -------- LOAD IMAGES --------
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

bg = pygame.image.load("space_bg.jpg")
bg = pygame.transform.scale(bg, (600, 600))

explosion_imgs = [
    pygame.image.load("exp1.png"),
    pygame.image.load("exp2.png"),
    pygame.image.load("exp3.png")
]

# -------- PLAYER --------
player = pygame.Rect(280, 500, 40, 40)
bullets = []
enemies = []

score = 0
level = 1

# -------- LOAD SCORES --------
try:
    with open("scores.json", "r") as f:
        scores = json.load(f)
except:
    scores = []

# -------- FUNCTIONS --------
def update_scores(new_score):
    scores.append(new_score)
    scores.sort(reverse=True)
    top3 = scores[:3]

    with open("scores.json", "w") as f:
        json.dump(scores, f)

    return top3

def draw_text(text, x, y):
    font = pygame.font.Font(None, 36)
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

# -------- GAME LOOP --------
running = True
game_over = False

while running:
    screen.blit(bg, (0, 0))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------- SERIAL INPUT --------
    if arduino:
        try:
            if arduino.in_waiting > 0:
                command = arduino.readline().decode().strip()

                if not game_over:
                    if command == "LEFT":
                        player.x -= 10
                    elif command == "RIGHT":
                        player.x += 10
                    elif command == "UP":
                        player.y -= 10
                    elif command == "DOWN":
                        player.y += 10
                    elif command == "SHOOT":
                        bullets.append(pygame.Rect(player.x + 15, player.y, 5, 10))
        except:
            pass

    # -------- LIMIT PLAYER --------
    player.x = max(0, min(WIDTH - player.width, player.x))
    player.y = max(0, min(HEIGHT - player.height, player.y))

    if not game_over:
        # -------- BULLETS --------
        for bullet in bullets[:]:
            bullet.y -= 10
            if bullet.y < 0:
                bullets.remove(bullet)
            else:
                screen.blit(bullet_img, (bullet.x, bullet.y))

        # -------- ENEMIES --------
        if random.randint(1, 30) == 1:
            enemies.append(pygame.Rect(random.randint(0, 560), 0, 40, 40))

        for enemy in enemies[:]:
            enemy.y += 3 + level
            screen.blit(enemy_img, (enemy.x, enemy.y))

            # GAME OVER
            if enemy.colliderect(player):
                top3 = update_scores(score)
                game_over = True

        # -------- COLLISION --------
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    # Explosion animation
                    for img in explosion_imgs:
                        screen.blit(img, (enemy.x, enemy.y))
                        pygame.display.update()
                        pygame.time.delay(40)

                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 10

                    if score % 50 == 0:
                        level += 1
                    break

        # -------- DRAW PLAYER --------
        screen.blit(player_img, (player.x, player.y))

        # -------- DISPLAY --------
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Level: {level}", 10, 40)

    else:
        # -------- GAME OVER SCREEN --------
        draw_text("GAME OVER", 220, 250)
        draw_text(f"Final Score: {score}", 200, 300)
        draw_text("Top 3 Scores:", 200, 350)

        for i, s in enumerate(top3):
            draw_text(f"{i+1}. {s}", 250, 380 + i*30)

    pygame.display.update()
    clock.tick(30)

pygame.quit()