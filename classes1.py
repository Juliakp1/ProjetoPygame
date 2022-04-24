import pygame

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

class pipe:
    def __init__(self, h):
        self.horiz = 1200
        self.height = h
        self.upper_pos = [self.horiz, self.height -600]
        self.lower_pos = [self.horiz, self.height +150]
        self.vel = 50
        self.pont = False
    
    # ------ atualiza posição horizontal dos canos ------- #

    def atualiza_status(self,deltaT):
        self.upper_pos[0] -= self.vel * deltaT 
        self.lower_pos[0] -= self.vel * deltaT 
    
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
    
class coin:
    
    def __init__(self, coord_x, coord_y):
        self.x = coord_x
        self.y = coord_y
        self.w = 32
        self.h = 32
        self.vel = 50
        
    # ------ atualiza posição horizontal das moedas ------- #
    
    def atualiza_status(self, deltaT):
        self.x -= self.vel * deltaT
    
    # ------------- desenha as moedas na tela -------------- # 
    
    def desenha(self, window, assets):
        window.blit(assets['coin'], [self.x, self.y ])
    
    # ----------------- verifica colisão entre moedas e passaro ------------------ #
    def verifica_colisao(self,birb):
        bird = pygame.Rect(birb.x, birb.y, birb.size[0], birb.size[1])
        coin = pygame.Rect(self.x, self.y, self.w, self.h)
        if pygame.Rect.colliderect(bird, coin):
            return True


