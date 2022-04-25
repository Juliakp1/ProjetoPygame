import pygame


# ----------------- Sounds ------------------- #

pygame.mixer.init()

coinNoise = pygame.mixer.Sound('assets/coinNoise.mp3')
death = pygame.mixer.Sound('assets/death.mp3')
flap = pygame.mixer.Sound('assets/flap.mp3')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class birb_pong :
    def __init__(self, coord_x, coord_y, vel_h, vel_v):
        self.pos_X = coord_x
        self.pos_Y = coord_y
        self.vel_H = vel_h
        self.vel_V = vel_v
    
    def rendering_to_screen(self, window, assets):
        if self.vel_H < 0:
            flipBirb = pygame.transform.rotate(assets['flipBirb'], self.vel_V * 0.25)
            window.blit(flipBirb, [self.pos_X, self.pos_Y])

        else:
            birb = pygame.transform.rotate(assets['birb'], -self.vel_V * 0.25)
            window.blit(birb, [self.pos_X, self.pos_Y])
    

    # dentro da função current_game_state
    def atualiza_status(self, deltaT, statePing):
        
        # ----------------- Makes birb bounce ------------------- #
        self.pos_X += self.vel_H * deltaT 
        self.vel_V += statePing['gravity'] * deltaT
        self.pos_Y += self.vel_V * deltaT 

        # ----------------- Makes birb not off screen ------------------- #

        # Horizontally
        if self.pos_X >= statePing['windowSize'][0] - 35 :
            self.vel_H *= -1
            statePing['coin_pong'].collected = False
            self.pos_X = statePing['windowSize'][0] - 35
            pygame.mixer.Sound.play(flap)
        elif self.pos_X < 0:
            self.vel_H *= -1
            statePing['coin_pong'].collected = False
            self.pos_X = 2
            pygame.mixer.Sound.play(flap)

        # Vertically
        if self.pos_Y - 30 < 0 or self.pos_Y + 30 >= statePing['windowSize'][1]:
            self.vel_V *= -1
            self.pos_Y =  statePing['windowSize'][1] - 35
            pygame.mixer.Sound.play(flap)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    
class pipe_pong:
    def __init__(self, main_y, upper_y, lower_y):
        self.horiz = 580 
        self.main_pos = [self.horiz, main_y]
        self.upper_pos = [self.horiz, upper_y]
        self.lower_pos = [self.horiz, lower_y]
        self.speed_v = 8
        self.speed_h = 0
        self.direction = 1
    
    def rendering_to_screen(self, window, assets):
        
        window.blit(assets['pipeTop'], self.upper_pos)

        window.blit(assets['pipeLow'], self.lower_pos)
    
    # dentro da função current_game_state

    # ---------- verifica colisao entre os canos e a moeda --------------- #
    def verifica_colisao(self, birb_pong):
        bird = pygame.Rect(birb_pong.pos_X, birb_pong.pos_Y, 34, 24)
        upper_pipe = pygame.Rect(self.upper_pos[0], self.upper_pos[1], 64, 600 )
        lower_pipe = pygame.Rect(self.lower_pos[0], self.lower_pos[1], 64, 600 )
        if pygame.Rect.colliderect(bird, upper_pipe) or pygame.Rect.colliderect(bird, lower_pipe):
            pygame.mixer.Sound.play(death)
            return True
        return False

    # dentro da função current_game_state
    # -------- movimenta os canos verticalmente ----------- #
    def movimenta(self, ev):
        if ev.key == pygame.K_UP and self.main_pos[1] >= -128:
            self.main_pos[1] -= self.speed_v
            #self.upper_pos[1] -= self.speed_v
            #self.lower_pos[1] -= self.speed_v
        if ev.key == pygame.K_DOWN and self.main_pos[1] <= 350:
            self.main_pos[1] += self.speed_v
            #self.upper_pos[1] += self.speed_v
            #self.lower_pos[1] += self.speed_v
    
    # dentro da função current_game_state

    def atualiza_status(self, statePing, coin_pong):

        # aumenta a velocidade horizontal conforme o numero de moedas
        if coin_pong.counter >= 10:

            # Horizontal speed
            if coin_pong.counter >= 50:
                self.speed_h = 5
            elif coin_pong.counter >= 40:
                self.speed_h = 4
            elif coin_pong.counter >= 30:
                self.speed_h = 3
            elif coin_pong.counter >= 20:
                self.speed_h = 2
            elif coin_pong.counter >= 10:
                self.speed_h = 1

            # Direction of the movement
            if self.upper_pos[0] <= 0:
                self.direction = 1
            elif self.upper_pos[0] >= statePing['windowSize'][0] - 64: 
                self.direction = -1
            self.upper_pos[0] += self.speed_h * self.direction
            self.upper_pos[1] += self.speed_h * self.direction

        # atualiza a posição da moeda
        coin_pong.pos[0] = self.upper_pos[0] + 15
        coin_pong.pos[1] = self.lower_pos[1] - 71
        
        # atualiza a posição vertical dos canos
        self.upper_pos[1] = self.main_pos[1] -472
        self.lower_pos[1] = self.main_pos[1] + 250
        
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class coin_pong:
    def __init__(self, coord_x, coord_y, gotCoin, coinCounter):
        self.pos = [coord_x, coord_y]
        self.collected = gotCoin
        self.counter = coinCounter
    
    # dentro da função current_game_state

    # ---------- verifica colisao entre o passaro e a moeda --------------- #
    def verifica_colisao(self, birb_pong):
        bird = pygame.Rect(birb_pong.pos_X, birb_pong.pos_Y, 34, 24)
        coin = pygame.Rect(self.pos[0], self.pos[1], 32, 32 )
        if pygame.Rect.colliderect(bird, coin) and self.collected == False:
            self.collected = True
            self.counter += 1
            pygame.mixer.Sound.play(coinNoise)

