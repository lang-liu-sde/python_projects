import pygame
import random
import math

# 1 - init interface
pygame.init()
screen = pygame.display.set_mode((800,600)) #tuple width*height
pygame.display.set_caption('airplane war') #set title
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
bgImg = pygame.image.load('bg.png')
#添加背景音效
pygame.mixer.music.load('bg.wav')
pygame.mixer.music.play(-1) #单曲循环
#添加射中音效
sound = pygame.mixer.Sound('exp.wav')
# add player
playerImg = pygame.image.load('player.png')
playerX = 400
playerY = 500
playerStep = 0 # 0 stop, + move right, - move left
#add score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
def show_score():
    text = f'score: {score}' #f表示可以直接在其中添加变量
    score_render = font.render(text, True, (0, 255, 0)) #渲染
    screen.blit(score_render, (10,10))
# game over
is_over = False
over_font = pygame.font.Font('freesansbold.ttf', 64)
def check_is_over():
    if is_over:
        text = 'Game Over!'
        over_render = over_font.render(text, True, (255, 0, 0)) #渲染
        screen.blit(over_render, (250, 250))
# add enemy
number_of_enemies = 6
class Enemy(): #build enemy class
    def __init__(self):
        self.img = pygame.image.load('enemy.png')
        self.x = random.randint(100, 700)
        self.y = random.randint(0, 300)
        self.step = random.randint(2, 6)
    #被击中后恢复其位置
    def reset(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(0, 300)
enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy())

#两点之间的距离
def distance(bx, by, ex, ey):
    a = bx - ex 
    b = by - by 
    return math.sqrt(a*a + b*b)

class Bullet():
    def __init__(self):
        self.img = pygame.image.load('bullet.png')
        self.x = playerX + 16
        self.y = playerY - 10
        self.step = 10 # bullet speed
    #击中
    def hit(self):
        global score
        for e in enemies:
            if distance(self.x, self.y, e.x, e.y) < 10:
                sound.play()
                bullets.remove(self)
                e.reset() 
                score += 1
bullets = [] # save 现有的 bullets

def show_bullets():
    for b in bullets:
        screen.blit(b.img, (b.x, b.y))
        b.hit() #尝试是否击中目标
        b.y -= b.step
        if b.y < 0:
            bullets.remove(b)

def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.img, (e.x, e.y))
        e.x += e.step
        if e.x > 800-64 or e.x < 0:
            e.step *= -1 #敌人碰壁反弹
            e.y += 40
            if e.y > 450:
                is_over = True
                print('game over')
                enemies.clear()

def process_events():
    global playerStep
    global running
    for event in pygame.event.get(): #将发生的事件返回，比如前键盘等
        if event.type == pygame.QUIT: #pygame中定义的常量
            running = False
        if event.type == pygame.KEYDOWN: #事件类型为按下键
            if event.key == pygame.K_RIGHT: #判断按下哪个键
                playerStep = 5
            elif event.key == pygame.K_LEFT:
                playerStep = -5
            elif event.key == pygame.K_SPACE: #空格键是按下的，所以在KEYDOWN事件中
                bullets.append(Bullet())
        if event.type == pygame.KEYUP:
            playerStep = 0

def move_player():
    global playerX #在方法里面改变全局变量的值要加上global
    playerX += playerStep
    if playerX > 800-64: #边界控制注意减去飞机的size
        playerX = 800-64
    elif playerX < 0:
        playerX = 0

# 2 - game loop
running = True
while running:
    screen.blit(bgImg,(0,0)) #画一个东西,pygame坐标系左上角为(0，0)，要先画这个背景图，再画其他，否则将盖住其他图片
    show_score()
    process_events() #处理事件
    screen.blit(playerImg,(playerX,playerY))
    move_player()
    show_enemy()
    show_bullets()
    check_is_over()
    pygame.display.update()  #界面更新一定！！
#相当于每个循环画一帧画，将背景加入
# finished,画面正常开启，点击×，关闭画面

# 3 - add background image
# 4 - display player
# 5 - move player
# 6 - control boundary, the size of player 64*64
# 7 - keyboard event
# 8 - add enemy
# 9 - move enemy
# 10 - enemy down and random position
# 11 - multiple enemy
# 12 - 响应空格键 （发射子弹）
# 13 - add bullets
# 14 - 发射子弹
# 15 - 射中检测之距离
# 16 - 射中检测
# 17 - 添加音效
# 18 - 添加分数
# 19 - display score
# 20 - game over
# 21 - hint of game over
