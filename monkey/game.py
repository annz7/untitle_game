import pygame
import random
pygame.init()

banana = pygame.image.load('imagine/banana.png')
banana = pygame.transform.scale(banana, (banana.get_width()//55, banana.get_height()//55))
ananas = pygame.image.load('imagine/pineapple.png')
ananas = pygame.transform.scale(ananas, (ananas.get_width()//80, ananas.get_height()//80))
trash = pygame.image.load('imagine/trash.png')
trash = pygame.transform.scale(trash, (trash.get_width()//40, trash.get_height()//40))
walkRight = [pygame.image.load('imagine/player1_right1.png'), pygame.image.load('imagine/player1_right2.png'),
             pygame.image.load('imagine/player1_right3.png'), pygame.image.load('imagine/player1_right4.png'),
             pygame.image.load('imagine/player1_right5.png'), pygame.image.load('imagine/player1_right6.png'),
             pygame.image.load('imagine/player1_right7.png'), pygame.image.load('imagine/player1_right8.png')]
walkLeft = [pygame.image.load('imagine/1monkey.png'), pygame.image.load('imagine/player1_left2.png'),
            pygame.image.load('imagine/player1_left3.png'), pygame.image.load('imagine/player1_left4.png'),
            pygame.image.load('imagine/player1_left5.png'), pygame.image.load('imagine/player1_left6.png'),
            pygame.image.load('imagine/player1_left7.png'), pygame.image.load('imagine/player1_left8.png'),]
StandPlayer = [pygame.image.load('imagine/player1_left1.png'),pygame.image.load('imagine/player1_right1.png')]
bg = pygame.image.load('imagine/back.png')
w = 900
h = 473
floor = h - 10

class player:
    def __init__(self):
        self.width = 56 - 5
        self.height = 91 - 5
        self.speed = 5
        self.x = 50
        self.y = floor - self.height

class palm:
    def __init__(self, x, y, width, height):
        self.x = x
        self.width = width
        self.height = height
        self.y = y

class ball:
    def __init__(self, x, y, color, typ, speed):
        self.x = x
        self.y = y
        self.size = 20
        self.color = color
        self.typ = typ
        self.speed = speed

run = True
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Monkey")

clock = pygame.time.Clock()

isJump = False
timeJump = 9

animCount = 0
left = False
right = False
face = 1

score = 0
life = 5


def drawWin():
    global animCount
    win.blit(bg, (0, 0))
    #for i in palms:
    #    pygame.draw.rect(win, (0, 200, 200), (i.x, i.y, i.width, i.height))
    for i in balls:
        win.blit(i.color, (i.x, i.y))
    if animCount >= 40:
        animCount = 0
    if right:
        win.blit(walkRight[animCount // 5], (player1.x, player1.y))
        animCount += 1
    elif left:
        win.blit(walkLeft[animCount // 5], (player1.x, player1.y))
        animCount += 1
    else:
        if face == -1:
            win.blit(StandPlayer[0], (player1.x, player1.y))
        else:
            win.blit(StandPlayer[1], (player1.x, player1.y))
    font = pygame.font.Font(None, 40)
    text = font.render("Score: " + str(score), True, (0, 0, 0))
    win.blit(text, [w-200, 10])
    text = font.render("Lifes: " + str(life), True, (0, 0, 0))
    win.blit(text, [w - 200, 50])
    pygame.display.update()

player1 = player()
palms = []
for i in range(5):
    palm1 = palm(w // 5 * i + 100, h - 620, 70, 500)
    palms.append(palm1)
balls = []
time = -1
while run:
    if life == 0:
        run = False
    clock.tick(60)
    time += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    balls_speed = 1
    if score > 1000:
        balls_speed = 5
    elif score > 500:
        balls_speed = 4
    elif score > 200:
        balls_speed = 3
    elif score > 100:
        balls_speed = 2
    if time % 100 == 0:
        l = random.randint(1, 10)
        if l < 5:
            palm_number = random.randint(0, 4)
            balls.append(ball(palms[palm_number].x + palms[palm_number].width/2, palms[palm_number].y, ananas, 'pineapple', balls_speed))
            balls[len(balls) - 1].x -= balls[0].size / 2
        elif l < 8:
            palm_number = random.randint(0, 4)
            balls.append(ball(palms[palm_number].x + palms[palm_number].width / 2, palms[palm_number].y, banana, 'banana', balls_speed))
            balls[len(balls) - 1].x -= balls[0].size / 2
        else:
            palm_number = random.randint(0, 4)
            balls.append(ball(palms[palm_number].x + palms[palm_number].width / 2, palms[palm_number].y, trash, 'trash', balls_speed))
            balls[len(balls) - 1].x -= balls[0].size / 2
    for i in balls:
        i.y += i.speed
        logic = True
        if bool(pygame.Rect(i.x, i.y, i.size, i.size).colliderect(pygame.Rect(player1.x, player1.y, player1.width, player1.height))):
            if i.typ == 'banana':
                score += 50
                balls.remove(i)
                logic = False
            elif i.typ == 'pineapple':
                score += 10
                balls.remove(i)
                logic = False
            else:
                score -= 30
                balls.remove(i)
                logic = False
        if logic:
            if i.y + i.size >= floor:
                if i.typ != 'trash':
                    life -= 1
                balls.remove(i)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player1.x > 10:
        player1.x -= player1.speed
        face = -1
        left = True
        right = False
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player1.x + player1.width <= w - 10:
        player1.x += player1.speed
        face = 1
        left = False
        right = True
    else:
        left = False
        right = False
        animCount = 0

    if not isJump:
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            isJump = True
    else:
        if timeJump >= -9:
            if timeJump >= 0:
                player1.y -= timeJump ** 2 / 2
            else:
                player1.y += timeJump ** 2 / 2
            timeJump -= 1
        else:
            timeJump = 9
            isJump = False
    drawWin()

pygame.draw.rect(win, (0,0,200), pygame.Rect(200, 100, w - 400, h - 200))
pygame.draw.rect(win, (0, 200, 200), pygame.Rect(210, 110, w - 420, h - 220))
font = pygame.font.Font(None, 70)
text = font.render("Score: " + str(score), True, (0, 0, 0))
win.blit(text, [w/2 - 100, h/2 + 50])
font = pygame.font.Font(None, 100)
text = font.render("Game over", True, (0, 0, 0))
win.blit(text, [w/2 - 200, h/2 - 50])
pygame.display.update()
while not run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True
    if keys[pygame.K_ESCAPE]:
        run = True

pygame.quit()