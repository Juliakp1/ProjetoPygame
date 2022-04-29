import pygame
import random
import json
from pingPongBird import ping_pong_birb
from fruityBirdvel import custom_window

class birb:
    def __init__(self, coord_x, coord_y, size_x, size_y, v):
        self.x = coord_x 
        self.y = coord_y
        self.size = [size_x, size_y]
        self.vel = v
        self.jumped = False
    
    def atualiza_status(self, deltaT, floor_height, gravity):

        # ----------------- Birb Vertical ------------------- #

        self.vel = self.vel + gravity * deltaT
        self.y = self.y + self.vel * deltaT 

        # ----------------- Floor and teto detection ------------------- #

        if self.y > floor_height - self.size[1]:
            self.y = floor_height - self.size[1]
        
        elif self.y < 0:
            self.y =  0

    def desenha(self, assets, window):
        if self.vel > 450:
            birbRotation = -90
        else:
            birbRotation = -self.vel * 0.2

        birb = pygame.transform.rotate(assets['birb'], birbRotation)
        window.blit(birb, [self.x, self.y ])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class pipe:
    def __init__(self, h):
        self.horiz = 1200
        self.height = h
        self.upper_pos = [self.horiz, self.height -600]
        self.lower_pos = [self.horiz, self.height +150]
        self.pont = False
    
    # ------ atualiza posição horizontal dos canos ------- #

    def atualiza_status(self,deltaT, vel):
        self.upper_pos[0] -= vel * deltaT 
        self.lower_pos[0] -= vel * deltaT 
    
    # ------------- desenha os canos na tela -------------- # 

    def desenha(self, window, assets):
        window.blit(assets['pipeTop'], self.upper_pos)
        window.blit(assets['pipeLow'], self.lower_pos)
       # window.blit(assets['coin'], coinPo)
    
    # ------------------------ verifica colisão entre canos e passaro ------------------------- #

    def verifica_colisao(self, birb):
        bird = pygame.Rect(birb.x, birb.y, birb.size[0], birb.size[1])
        upper_pipe = pygame.Rect(self.upper_pos[0], self.upper_pos[1], 64, 600 )
        lower_pipe = pygame.Rect(self.lower_pos[0], self.lower_pos[1], 64, 600 )
        if pygame.Rect.colliderect(bird, upper_pipe) or pygame.Rect.colliderect(bird, lower_pipe):
            return True
        return False
    
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class coin:
    
    def __init__(self, coord_x, coord_y):
        self.x = coord_x
        self.y = coord_y
        self.w = 32
        self.h = 32

        
    # ------ atualiza posição horizontal das moedas ------- #
    
    def atualiza_status(self, deltaT, vel):
        self.x -= vel * deltaT
    
    # ------------- desenha as moedas na tela -------------- # 
    
    def desenha(self, window, assets):
        window.blit(assets['coin'], [self.x, self.y ])
    
    # ----------------- verifica colisão entre moedas e passaro ------------------ #
    def verifica_colisao(self,birb):
        bird = pygame.Rect(birb.x, birb.y, birb.size[0], birb.size[1])
        coin = pygame.Rect(self.x, self.y, self.w, self.h)
        if pygame.Rect.colliderect(bird, coin):
            return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
class collectables:

    def __init__(self, coord_y):
        self.x = 1200
        self.y = coord_y
        self.w = 32
        self.h = 32
        self.selected = random.choice(['cloud', 'coffee', 'jaca', 'lychee', 'star', 'waterm'])
        #self.selected = 'lychee'
        self.collected = False
    
    # ------ atualiza posição horizontal dos coletáveis ------- #

    def atualiza_status(self, deltaT, vel):
        self.x -= vel * deltaT
        
    # ------------- desenha o coletável da vez na tela -------------- # 
    
    def desenha(self, window, assets):
        window.blit(assets[self.selected], [ self.x, self.y ])
    
    # ----------------- verifica colisão entre os coletáveis e passaro ------------------ #
    
    def verifica_colisao(self,birb):
        bird = pygame.Rect(birb.x, birb.y, birb.size[0], birb.size[1])
        collectable = pygame.Rect(self.x, self.y, self.w, self.h)
        if pygame.Rect.colliderect(bird, collectable):
            self.collected = True
            return True

    # ------ atualiza os efeitos de acordo com o coletável ------- #
    def atualiza_efeitos(self, assets, state, window, tiks):
        
        # -------- Lychee ------- #
        if self.selected == 'lychee':
            state['birb'].size = [25.5, 18]
            assets['birb'] = pygame.transform.scale(assets['birb'], (25.5,18))
        
        # -------- Watermelon ------- #
        elif self.selected == 'waterm':
            state['birb'].size = [68,48]
            assets['birb'] = pygame.transform.scale(assets['birb'], (68,48))
        
        # -------- Carambola ------- #
        elif self.selected =='star':
            for i in state['coins']:
                i.w = 48
                i.h = 48
            assets['coin'] = pygame.transform.scale(assets['coin'], (48,48))
        
        # -------- Cloud Portal ------- #
        elif self.selected == 'cloud':
            state['coinCounter'] += ping_pong_birb(assets, window)
            state['birb'].y = 100
            state['lastUpdated'] = pygame.time.get_ticks()
            state['timeC'] = tiks - 16000
            custom_window(assets)
        
        # -------- Coffee ------- #
        elif self.selected == 'coffee':
            state['pipeTimer'] = 2500
            if state['vel'] == state['vel_padrao']:
                state['vel'] *= 1.5
        
        # -------- Jaca ------- #  
        elif self.selected == 'jaca':
            state['pipeTimer'] = 5000
            if state['vel'] == state['vel_padrao']:
                state['vel'] *= 0.5

    # ------------ Volta as condições normais do jogo -------------- #
    def volta_normal(self, assets, state):
        state['birb'].size = [34,24]

        with open('playerPrefs.json', 'r') as arquivo_json:
            skinsString = arquivo_json.read()  
        playerImg = json.loads(skinsString)
        imgBirb = pygame.image.load(playerImg['birb'])
        assets['birb'] = pygame.transform.scale(imgBirb, (34, 24))

        for i in state['coins']:
            i.w = 32
            i.h = 32
        assets['coin'] = pygame.transform.scale(assets['coin'], (32,32))
        state['pipeTimer'] = random.choice(range(3000, 5000, 500))
        state['vel'] = state['vel_padrao']
