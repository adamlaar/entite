import pygame, random, sys
from pygame._sdl2 import Window
import math

pygame.init()
pygame.display.set_caption("entité")

display_info = pygame.display.Info()
window_size = (display_info.current_w, display_info.current_h)
thirdwidth = display_info.current_w/3
thirdheight = display_info.current_h/3

surface = pygame.display.set_mode((thirdwidth, thirdheight))

clock = pygame.time.Clock()
blinkcount = 0
blinktick, animationtick = pygame.time.get_ticks(), pygame.time.get_ticks()
safepos = random.randint(0,8)
level = 1
blinking = False
blinking_phase = True
death = False

aol = pygame.image.load("AOL.png")
aol = pygame.transform.scale(aol, (100, 100))
msn = pygame.image.load("MSN.png")
msn = pygame.transform.scale(msn, (100, 100))
icq = pygame.image.load("ICQ.png")
icq = pygame.transform.scale(icq, (100, 100))
emoticonlist = [aol,msn,icq]
emoticoncount = 0
ballcolor = (75,175,75)
background = (255,255,255)
window = Window.from_display_module()
arial24 = pygame.font.SysFont("arial",50)
gameover = arial24.render("GAME OVER", True, (255, 0, 0))
youwin = arial24.render("YOU WIN", True, (0, 255, 0))
window.position = (display_info.current_w/2-thirdwidth/2,display_info.current_h/2-thirdheight/2)
dangerrects = [(0,0), (thirdwidth/3, 0), (thirdwidth/3*2-1,0), (0,thirdheight/3),(0,thirdheight/3*2),(thirdwidth/3,thirdheight/3),(thirdwidth/3,thirdheight/3*2),(thirdwidth/3*2-1,thirdheight/3*2),(thirdwidth/3*2-1,thirdheight/3)]

def movement():
    global continuer, left, right, up, down
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
           
    touchesPressees = pygame.key.get_pressed()
    if not touchesPressees[pygame.K_LEFT]:
        left = False
    if touchesPressees[pygame.K_LEFT] and not left and window.position[0] > 0:
        window.position = (window.position[0] - thirdwidth, window.position[1])
        left = True
       
    if not touchesPressees[pygame.K_RIGHT]:
        right = False
    if touchesPressees[pygame.K_RIGHT] and not right and window.position[0] < thirdwidth:
        window.position = (window.position[0] + thirdwidth, window.position[1])
        right = True
       
    if not touchesPressees[pygame.K_UP]:
        up = False
    if touchesPressees[pygame.K_UP] and not up and window.position[1] > 0:
        window.position = (window.position[0], window.position[1] - thirdheight)
        up = True

    if not touchesPressees[pygame.K_DOWN]:
        down = False
    if touchesPressees[pygame.K_DOWN]  and not down and window.position[1] < thirdheight*2:
        window.position = (window.position[0], window.position[1] + thirdheight)
        down = True
       
def is_player_safe():
    for rects in range(len(dangerrects)):
        if rects == safepos:
            if abs(window.position[0]//3 - math.floor(dangerrects[rects][0])) <= 5:
                if abs(window.position[1]//3 - math.floor(dangerrects[rects][1])) <= 5:
                    return True
    return False

def memory():
    global safepos, blinking, blinktick, blinkcount, blinking_phase, level, ballcolor, continuer, background
    tickmemory = pygame.time.get_ticks()
    
    if tickmemory - blinktick >= 500/level:
        blinktick = tickmemory
        if blinking_phase:
            blinking = not blinking
            blinkcount += 1
            if blinkcount >= 6:
                blinking_phase = False
                blinkcount = 0
                blinking = False
        else:
            blinkcount += 1
            if blinkcount >= 6:
                blinking_phase = True 
                blinkcount = 0
                if not is_player_safe():
                    death = True
                    continuer = False
                safepos = random.randint(0, 8)
                level += 0.1
    if level >= 3.0:
        continuer = False
    elif level >= 2.5:
        ballcolor = (255,255,255)
        background = (0,0,0)
#        window.position = (window.position[0]+random.randint(-1,1),window.position[1]+random.randint(-1,1))
    elif level >= 1.3:
        ballcolor = (255,0,0)
        
def draw():
    global surface, dangerrect, blinking, ballcolor, emoticoncount, emoticonlist, animationtick
    surface.fill(background)
    surface.blit(emoticonlist[emoticoncount],(thirdwidth/2-50, thirdheight/2-50))
    tickani = pygame.time.get_ticks()
    if tickani - animationtick >= 100:
        emoticoncount += 1
        animationtick = tickani
        if emoticoncount > 2:
            emoticoncount = 0

    if blinking:
        for rects in range(len(dangerrects)):
            dangerrect = pygame.Rect((dangerrects[rects][0], dangerrects[rects][1]), (thirdwidth/3, thirdheight/3))
            if rects != safepos:
                pygame.draw.rect(surface, (230,230,230), dangerrect, width=0)
            else:
                pygame.draw.rect(surface, (90,90,90), dangerrect, width=0)

    pygame.display.flip()
   
continuer = True
while continuer:
    movement()
    memory()
    draw()

if not death:
    surface.fill((255,255,255))
    surface.blit(gameover,(thirdwidth/2-150, thirdheight/2-25))
    pygame.display.flip()
    pygame.time.wait(2000)
else:
    surface.fill((255,255,255))
    surface.blit(youwin,(thirdwidth/2-102, thirdheight/2-25))
    pygame.display.flip()
    pygame.time.wait(3000)

sys.exit()
pygame.quit()