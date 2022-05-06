import pygame


# ----------------- Sounds ------------------- #

pygame.mixer.init()

coinNoise = pygame.mixer.Sound('assets/coinNoise.mp3')
death = pygame.mixer.Sound('assets/death.mp3')
flap = pygame.mixer.Sound('assets/flap.mp3')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class Birb_pong :
    def __init__(self, coord_x, coord_y, vel_h, vel_v):
        self.pos_X = coord_x
        self.pos_Y = coord_y
        self.vel_H = vel_h
        self.vel_V = vel_v
        self.gravity = 90
    
    
    def rendering_to_screen(self, window, assets):
        """
        modifica a imagem do birb dependendo para o lado que ele está indo

        Argumentos
        ---------------
        window : variável que armazena a janela do pygame
        assets: dicionário que armazena fontes e imagens
        """

        # quando o birb bate na parede esquerda
        if self.vel_H < 0:
            flipBirb = pygame.transform.rotate(assets['flipBirb'], self.vel_V * 0.25)
            window.blit(flipBirb, [self.pos_X, self.pos_Y])

        else:
            birb = pygame.transform.rotate(assets['birb'], -self.vel_V * 0.25)
            window.blit(birb, [self.pos_X, self.pos_Y])
    
    def atualiza_status(self, deltaT, statePing):
        """
        atualiza a posição vertical e horizontal do pássaro

        Argumentos
        ---------------
        deltaT (float) : variação de tempo em segundos
        statePing : dicionario com as variáveis principais do jogo

        """
        
        # ----------------- Movimenta o birb ------------------- #

        self.pos_X += self.vel_H * deltaT 
        self.vel_V += self.gravity * deltaT
        self.pos_Y += self.vel_V * deltaT 

        # ----------------- Garante que o birb não saia da tela ------------------- #

        # Horizontal
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

        # Vertical
        if self.pos_Y - 30 < 0 or self.pos_Y + 30 >= statePing['windowSize'][1]:
            self.vel_V *= -1
            self.pos_Y =  statePing['windowSize'][1] - 35
            pygame.mixer.Sound.play(flap)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
    
class Pipe_pong:
    def __init__(self, main_y, upper_y, lower_y):
        self.horiz = 580 
        self.main_pos = [self.horiz, main_y]
        self.upper_pos = [self.horiz, upper_y]
        self.lower_pos = [self.horiz, lower_y]
        self.speed_v = 8
        self.speed_h = 0
        self.direction = 1
    
    def rendering_to_screen(self, window, assets):
        """
        desenha os canos na tela
        """
        
        window.blit(assets['pipeTop'], self.upper_pos)
        window.blit(assets['pipeLow'], self.lower_pos)
    
    def verifica_colisao(self, birb_pong):
        """
        verifica colisao entre os canos e a moeda
        """

        bird = pygame.Rect(birb_pong.pos_X, birb_pong.pos_Y, 34, 24)
        upper_pipe = pygame.Rect(self.upper_pos[0], self.upper_pos[1], 64, 600 )
        lower_pipe = pygame.Rect(self.lower_pos[0], self.lower_pos[1], 64, 600 )
        if pygame.Rect.colliderect(bird, upper_pipe) or pygame.Rect.colliderect(bird, lower_pipe):
            pygame.mixer.Sound.play(death)
            return True
        return False

    def movimenta(self, ev, joystick):
        """
        movimenta o cano verticalmente
        """

        # controller ver
        if pygame.joystick.get_init():
            if joystick.get_axis(1) > 0.6:
                self.main_pos[1] += self.speed_v/4
            if joystick.get_axis(1) < -0.6:
                self.main_pos[1] -= self.speed_v/4
        
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP and self.main_pos[1] >= -128:
                self.main_pos[1] -= self.speed_v

            if ev.key == pygame.K_DOWN and self.main_pos[1] <= 350:
                self.main_pos[1] += self.speed_v
    
    def atualiza_status(self, statePing, coin_pong):
        """
        atualiza a posição dos canos e modifica a velocidade horizontal
        """

        # aumenta a velocidade horizontal conforme o numero de moedas
        if coin_pong.counter >= 10:

            # velocidade horizontal
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

            # direção do moviemnto
            if self.upper_pos[0] <= 0:
                self.direction = 1
            elif self.upper_pos[0] >= statePing['windowSize'][0] - 64: 
                self.direction = -1
            
            if self.lower_pos[0] <= 0:
                self.direction = 1
            elif self.lower_pos[0] >= statePing['windowSize'][0] - 64: 
                self.direction = -1

            self.upper_pos[0] += self.speed_h * self.direction
            self.lower_pos[0] += self.speed_h * self.direction

        # atualiza a posição da moeda
        coin_pong.pos[0] = self.upper_pos[0] + 15
        coin_pong.pos[1] = self.lower_pos[1] - 71
        
        # atualiza a posição vertical dos canos
        self.upper_pos[1] = self.main_pos[1] -472
        self.lower_pos[1] = self.main_pos[1] + 250
        
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class Coin_pong:
    def __init__(self, coord_x, coord_y, gotCoin, coinCounter):
        self.pos = [coord_x, coord_y]
        self.collected = gotCoin
        self.counter = coinCounter

    def verifica_colisao(self, birb_pong):
        """
        verifica colisão entre o pássaro e a moeda
        """

        bird = pygame.Rect(birb_pong.pos_X, birb_pong.pos_Y, 34, 24)
        coin = pygame.Rect(self.pos[0], self.pos[1], 32, 32 )
        if pygame.Rect.colliderect(bird, coin) and self.collected == False:
            self.collected = True
            self.counter += 1
            pygame.mixer.Sound.play(coinNoise)