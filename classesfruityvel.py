import pygame
import random
import json
from pingPongBird import ping_pong_birb
from fruityBirdvel import custom_window

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
class Birb:
    """
    Classe birb que cria um objeto do tipo birb, no caso o passaro
    """ 

    def __init__(self, coord_x, coord_y, size_x, size_y, v):
        """
        Argumentos
        ----------------
        coord_x (int) : coordenada x inicial
        coord_y (int) : coordenada y inicial
        size_x (float) : largura do birb
        size_y (float) : comprimento do birb
        v (float) : velocidade vertical do birb
        -----------------

        jumped (bool) : True caso o birb pular, False caso contrário, ou quando o pulo 
        jump(int) : velocidade vertical do birb quando ele pula
        gravity(int) : gravidade

        """
        self.x = coord_x 
        self.y = coord_y
        self.size = [size_x, size_y]
        self.vel = v
        self.jumped = False
        self.jump = -200
        self.gravity = 500
    
    def atualiza_status(self, deltaT, floor_height):
        """
        atualiza a posição do birb

        Argumentos
        ---------------
        deltaT (float) : variação de tempo em segundos
        floor_height (int) : altura do chão

        """
        # ----------------- atualiza a posição vertical do birb ------------------- #

        self.vel = self.vel + self.gravity * deltaT
        self.y = self.y + self.vel * deltaT 

        # ----------------- garante que o birb fique dentro da tela ------------------- #

        # em relação ao chão
        if self.y > floor_height - self.size[1]:
            self.y = floor_height - self.size[1]
        
        # em relação ao teto
        elif self.y < 0:
            self.y =  0

    def desenha(self, assets, window):
        """
        desenha o birb na tela 

        Argumentos
        ---------------
        window : variável que armazena a janela do pygame
        assets: dicionário que armazena fontes e imagens

        """
        if self.vel > 450:
            birbRotation = -90
        else:
            birbRotation = -self.vel * 0.2

        birb = pygame.transform.rotate(assets['birb'], birbRotation)
        window.blit(birb, [self.x, self.y ])
    
    def movimenta(self, ev, flap, state):
        """
        movimentação do birb a partir de inputs do usuário

        Argumentos
        ---------------
        ev : evento no pygame
        flap : som para quando o passarinho pula
        state : dicionario com as variáveis principais do jogo

        """
        # ----------------- Inputs Controller ------------------- #
        if ev.type == pygame.JOYBUTTONDOWN and self.jumped == False: 
            pygame.mixer.Sound.play(flap)
            state['joystick'].rumble(0.2, 0.4, 100)
            self.vel = self.jump
            self.jumped = True
        
        if ev.type == pygame.JOYBUTTONUP:
            self.jumped = False


        # ----------------- Inputs Keyboard ------------------- #
        if ev.type == pygame.KEYDOWN: 
            # Jumping (only once)
            if (ev.key == pygame.K_UP or ev.key == pygame.K_SPACE or ev.key == pygame.K_w) and self.jumped == False:
                pygame.mixer.Sound.play(flap)
                self.vel = self.jump
                self.jumped = True
            
            if ev.key == pygame.K_ESCAPE:
                state['hitPipe'] = True
        
        if ev.type == pygame.KEYUP:
            if (ev.key == pygame.K_UP or ev.key == pygame.K_SPACE or ev.key == pygame.K_w):
                self.jumped = False

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class Pipe:
    """
    Classe pipe que cria um objeto do tipo pipe, no caso os canos
    """ 
    def __init__(self, h):
        """
        Argumentos
        ----------------
        h (float) : altura sorteada do conjunto de canos ( cano de cima e cano de baixo )

        -----------------
        horiz (float) : posição vertical do cano
        upper_pos : lista com a posição horizontal e vertical do cano de cima
        lower_pos : lista com a posição horizontal e vertical do cano de baixo
        passou (bool) : True caso o birb passou do cano em questão, False caso contrário

        """
        self.horiz = 1200
        self.height = h
        self.upper_pos = [self.horiz, self.height -600]
        self.lower_pos = [self.horiz, self.height +150]
        self.passou = False
    

    def atualiza_status(self,deltaT, vel):
        """
        atualiza a posição horizontal dos canos

        Argumentos
        ---------------
        deltaT (float) : variação de tempo em segundos
        vel (float) : velocidade horizontal geral do jogo

        """
        self.upper_pos[0] -= vel * deltaT 
        self.lower_pos[0] -= vel * deltaT 
    
    # ------------- desenha os canos na tela -------------- # 

    def desenha(self, window, assets):
        """
        desenha os canos na tela

        Argumentos
        ---------------
        window : variável que armazena a janela do pygame
        assets: dicionário que armazena fontes e imagens

        """
        window.blit(assets['pipeTop'], self.upper_pos)
        window.blit(assets['pipeLow'], self.lower_pos)
    
    # ------------------------ verifica colisão entre canos e passaro ------------------------- #

    def verifica_colisao(self, birb):
        """
        verifa a colisão entre os canos e o birb
        
        Argumento
        ---------------
        birb : classe birb

        """
        bird = pygame.Rect(birb.x, birb.y, birb.size[0], birb.size[1])
        upper_pipe = pygame.Rect(self.upper_pos[0], self.upper_pos[1], 64, 600 )
        lower_pipe = pygame.Rect(self.lower_pos[0], self.lower_pos[1], 64, 600 )
        if pygame.Rect.colliderect(bird, upper_pipe) or pygame.Rect.colliderect(bird, lower_pipe):
            return True
        return False
    
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

class Coin:
    """
    Classe coin que cria as moedas
    """ 
    def __init__(self, coord_x, coord_y):
        """
        Argumentos
        ----------------
        coord_x (int) : coordenada x inicial
        coord_y (int) : coordenada y inicial

        -----------------
        w (float): largura da moeda
        h (float): altura da moeda

        """
        
        self.x = coord_x
        self.y = coord_y
        self.w = 32
        self.h = 32

    
    def atualiza_status(self, deltaT, vel):
        """
        atualiza a posição horizontal da moeda

        Argumentos
        ---------------
        deltaT (float) : variação de tempo em segundos
        vel (float) : velocidade horizontal geral do jogo

        """
        self.x -= vel * deltaT
    
    def desenha(self, window, assets):
        """
        desenha os canos na tela

        Argumentos
        ---------------
        window : variável que armazena a janela do pygame
        assets: dicionário que armazena fontes e imagens

        """
        window.blit(assets['coin'], [self.x, self.y ])
    
    def verifica_colisao(self,birb):
        """
        verifa a colisão entre a moeda e o birb
        
        Argumento
        ---------------
        birb : classe birb

        """
        bird = pygame.Rect(birb.x, birb.y, birb.size[0], birb.size[1])
        coin = pygame.Rect(self.x, self.y, self.w, self.h)
        if pygame.Rect.colliderect(bird, coin):
            return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
class Collectables:
    """
    Classe coletáveis que guarda todas as variáveis relacionadas a cada moeda
    """ 
    def __init__(self, coord_y):
        """
        Argumentos
        ----------------
        coord_y (float) : coordenada y aleatória inicial

        -----------------
        x (float) : posição vertical do cano
        w (float) : largura do coletável
        y (float) : comprimento do coletável
        selected : seleciona um dos coletáveis da lista 
        collected : True caso o coletável seja coletado, False caso contrário

        """
        self.x = 1200
        self.y = coord_y
        self.w = 32
        self.h = 32
        self.selected = random.choice(['cloud', 'coffee', 'jaca', 'lychee', 'star', 'waterm', 'coco', 'amar'])
        self.collected = False
    

    def atualiza_status(self, deltaT, vel):
        """
        atualiza a posição horizontal do coletável
        """
        self.x -= vel * deltaT
    
    def desenha(self, window, assets):
        """
        desenha o coletável da vez na tela
        """
        window.blit(assets[self.selected], [ self.x, self.y ])
    
    
    def verifica_colisao(self,birb):
        """
        verifica colisão entre coletável e birb
        """
        bird = pygame.Rect(birb.x, birb.y, birb.size[0], birb.size[1])
        collectable = pygame.Rect(self.x, self.y, self.w, self.h)
        if pygame.Rect.colliderect(bird, collectable):
            self.collected = True
            return True

    def atualiza_efeitos(self, assets, state, window, tiks):
        """
        atualiza os efeitos de acordo com o coletável
        """
        
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
            coins, state['closedGame'] = ping_pong_birb(assets, window)
            state['coinCounter'] += coins
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
        
        # -------- Coco ------- #  
        elif self.selected == 'coco':
            state['birb'].jump = -100

        # -------- Amarula ------- #  
        elif self.selected == 'amar':
            state['birb'].jump = -300

    def volta_normal(self, assets, state):
        """
        volta as condições normais do jogo
        """
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
        state['birb'].jump = -200