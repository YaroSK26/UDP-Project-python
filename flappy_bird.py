#importovanie knzinic
import pygame
from pygame.locals import *
import random

#pajgejm
pygame.init()

#fps
clock = pygame.time.Clock()
fps = 300

#rozmery obrazovky
screen_width = 864
screen_height = 836

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#definovanie fonti
font = pygame.font.SysFont("comic sans MS", 60)
menu_font = pygame.font.SysFont('gabriola', 140)

#definovanie farieb
white = (255, 255, 255)

#defiovanie premennych
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#nacitavanie obrazkov
bg = pygame.image.load("img/etika.webp")
ground_img = pygame.image.load("img/ground.png")
reset_button_img = pygame.image.load("img/chleba.png")
menu_img = pygame.image.load("img/menu.png")
endless_button = pygame.image.load('img/endless1.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def main_menu():
    pygame.display.set_caption('Menu')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # lave tlacitko mysi
                    # kuka ci mys je na tlacitku
                    button_x = screen_width // 2 - endless_button.get_width() // 2
                    button_y = screen_height // 2 - endless_button.get_height() // 2
                    button_rect = endless_button.get_rect(topleft=(button_x, button_y))

                    if button_rect.collidepoint(event.pos):
                        game_over = False
                        #zacni hru
                        return

        screen.blit(bg, (0, 0))

        MENU_TEXT = menu_font.render('Flappy Bird', True, '#111111')
        screen.blit(MENU_TEXT, (screen_width // 2 - MENU_TEXT.get_width() // 2, screen_height // 6 - MENU_TEXT.get_height() // 2))
        endless_button_x = screen_width // 2 - endless_button.get_width() // 2
        endless_button_y = screen_height // 2 - endless_button.get_height() // 2
        screen.blit(endless_button, (endless_button_x, endless_button_y))

        pygame.display.update()
        clock.tick(fps)
main_menu()

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


#sprite class animacia postavy , images 
class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        #meni obrazky
        self.index =  0 
        #meni rychlost menenia obrazkov
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f"img/bird{num}.png")   
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect  = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):
        #nastavovanie gravity
        if flying == True:
            self.vel += 0.5
            if self.vel >8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)



        if game_over == False:
            #jumping
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            #nastavovanie aby pri drzani mysi fÄ¾epi neskakal
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked = False

            # cooldown na obrazky -animacia
            self.counter += 1 
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1 
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]



                #rotating bird po skakani , 
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        else:
             self.image = pygame.transform.rotate(self.images[self.index],-90)



#definovanie pipy
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/etika.png')
        self.rect = self.image.get_rect()
        
        # pozicia 1 je z vrchu, -1  z dola
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        

#chleba
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        
        action = False

        #pozicia kurozra
        pos = pygame.mouse.get_pos()

        #ci je mys nad chlebom
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True


        #chleba
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

#nastavenie kde bude flappy zacinat a kde budu pipy
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

#chleba instancia
button = Button(screen_width // 2.5, screen_height // 2.5, reset_button_img)
menu_button = Button(screen_width // 2.5, screen_height // 2, menu_img)

def start_game():
    global flying, game_over, score
    flying = True
    game_over = False
    score = reset_game()

def main_menu():
    pygame.display.set_caption('Menu')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the mouse click is within the button bounds
                    button_x = screen_width // 2 - endless_button.get_width() // 2
                    button_y = screen_height // 2 - endless_button.get_height() // 2
                    button_rect = endless_button.get_rect(topleft=(button_x, button_y))

                    if button_rect.collidepoint(event.pos):
                        start_game()
                        return
        screen.blit(bg, (0, 0))
        MENU_TEXT = menu_font.render('Flappy Bird', True, '#111111')
        screen.blit(MENU_TEXT, (screen_width // 2 - MENU_TEXT.get_width() // 2, screen_height // 6 - MENU_TEXT.get_height() // 2))
        endless_button_x = screen_width // 2 - endless_button.get_width() // 2
        endless_button_y = screen_height // 2 - endless_button.get_height() // 2
        screen.blit(endless_button, (endless_button_x, endless_button_y))
        pygame.display.update()
        clock.tick(fps)

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0,0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_scroll , 768))
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width/2.1), 20)              
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe=Pipe(screen_width,int(screen_height / 2) + pipe_height,-1)
            top_pipe=Pipe(screen_width,int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()
    if game_over == True:
        if menu_button.draw() == True:
            main_menu()
        if button.draw() == True:
            start_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()
pygame.quit()
