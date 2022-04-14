import pygame
import time

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize():

    pygame.init()
    pygame.key.set_repeat(50)

    inicialTime = time.time()

    # ----------------- Gets images and fonts ------------------- #

    imgBirb = pygame.image.load('assets/birb9.png')
    imgBirb = pygame.transform.scale(imgBirb, (34, 24))
    imgPipe = pygame.image.load('assets/pipe1.png')
    imgPipe = pygame.transform.scale(imgPipe, (64, 600))
    imgCoin = pygame.image.load('assets/coin.png')
    imgBg = pygame.image.load('assets/bg1.png')
    pipeTop = pygame.transform.flip(imgPipe, False, True)

    fontDef = pygame.font.Font('assets/pixelFont.ttf', 60)

    # ----------------- Assets ------------------- #

    assets = {
        'birb': imgBirb,
        'background': imgBg,
        'pipeLow': imgPipe,
        'pipeTop': pipeTop,
        'fontDef': fontDef,
        'coin': imgCoin,
    }

    # ----------------- Game States ------------------- #

    state = {
        'windowSize': [1200, 600],
        'mainPipePos': [580, 0],
        'ballPos': [700, 200],
        'ballVel': [200, 100],
        'pipeUpperPos': [0, -472],
        'pipeLowerPos': [0, 250],
        'pipeSpeedV': 8,
        'pipeSpeedH': 1,
        'pipeDirecton': 1,
        'coinPos': [16, 189],
        'gotCoin': False,
        'coinCounter': 0,
        'last_updated': 0,
        'accele': 50,
        'hitPipe': False,
        'time': inicialTime
    }

    window = pygame.display.set_mode(state['windowSize'], vsync=True, flags=pygame.SCALED)

    return window, assets, state

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def resets(state):
    state['hitPipe'] = False
    state['gotCoin'] = False
    state['ballPos'] = [400, 200]
    state['ballVel'] = [200, 100]
    state['mainPipePos'] = [580,0]
    state['coinCounter'] = 0
    tiks = pygame.time.get_ticks()
    state['last_updated'] = tiks

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def rendering_to_screen(window: pygame.Surface, assets, state):

    window.blit(assets['background'], [0, 0])
    
    # ----------------- Renders pipe ------------------- #

    window.blit(assets['pipeTop'], state['pipeUpperPos'])

    window.blit(assets['pipeLow'], state['pipeLowerPos'])

    # ----------------- Renders coin and counter ------------------- #

    if state['gotCoin'] == False:
        window.blit(assets['coin'], state['coinPos'])
    
    coins = str(state['coinCounter'])
    window.blit(assets['fontDef'].render(coins, True, (0, 0, 0)), (20, 15))
    window.blit(assets['fontDef'].render(coins, True, (255, 255, 255)), (18, 13))

    # ----------------- Renders birb ------------------- #
    
    if state['ballVel'][0] < 0:
        flipBirb = pygame.transform.flip(assets['birb'], True, False)
        #flipBirb = pygame.transform.rotate(flipBirb, -state['ballVel'][1] * 0.1)
        window.blit(flipBirb, state['ballPos'])

    else:
        #assets['birb'] = pygame.transform.rotate(assets['birb'], state['ballVel'][1] * 0.1)
        window.blit(assets['birb'], state['ballPos'])

    # ----------------- Renders Game Over ------------------- #

    if state['hitPipe'] == True:
        window.blit(assets['fontDef'].render('Game Over', True, (0, 0, 0)), (165, 170))
        window.blit(assets['fontDef'].render('Game Over', True, (255, 255, 255)), (163, 168))

    pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(state):

    if state['hitPipe'] == False:

        # ----------------- Makes birb bounce ------------------- #

        tiks = pygame.time.get_ticks()
        deltaT = (tiks - state['last_updated']) / 1000
        state['last_updated'] = tiks

        state['ballPos'][0] = state['ballPos'][0] + state['ballVel'][0] * deltaT 
        state['ballVel'][1] = state['ballVel'][1] + state['accele'] * deltaT
        state['ballPos'][1] = state['ballPos'][1] + state['ballVel'][1] * deltaT 

        # ----------------- Makes birb not off screen ------------------- #

        # Horizontally
        if state['ballPos'][0] >= state['windowSize'][0] - 35 :
            state['ballVel'][0] *= -1
            state['gotCoin'] = False
            state['ballPos'][0] = state['windowSize'][0] - 35
        elif state['ballPos'][0] < 0:
            state['ballVel'][0] *= -1
            state['gotCoin'] = False
            state['ballPos'][0] = 2

        # Vertically
        if state['ballPos'][1] - 30 < 0 or state['ballPos'][1] + 30 >= state['windowSize'][1]:
            state['ballVel'][1] *= -1
            state['ballPos'][1] =  state['windowSize'][1] - 35

        # ----------------- Colision with the pipe and coin ------------------- #

        # first checks if its in the pipe area horizontally
        if state['ballPos'][0] + 30 > state['pipeUpperPos'][0] and state['ballPos'][0] < state['pipeUpperPos'][0] + 64:
            # checks to see if its in the pipe, or got the coin
            if state['ballPos'][1] < state['pipeUpperPos'][1] + 600 or state['ballPos'][1] > state['pipeLowerPos'][1] - 20:
                state['hitPipe'] = True
            # Coin collision
            if state['ballPos'][1] < state['coinPos'][1] + 20 and state['ballPos'][1] > state['coinPos'][1]:
                if state['gotCoin'] == False:
                    state['gotCoin'] = True
                    state['coinCounter'] += 1

    # ----------------- Key Presses ------------------- #

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False

        if ev.type == pygame.KEYDOWN:

            # Controls the pipe
            if ev.key == pygame.K_UP and state['mainPipePos'][1] >= -128:
                state['mainPipePos'][1] -= state['pipeSpeedV']
            if ev.key == pygame.K_DOWN and state['mainPipePos'][1] <= 350:
                state['mainPipePos'][1] += state['pipeSpeedV']

            # if ev.key == pygame.K_LEFT:
            #     state['mainPipePos'][0] -= state['pipeSpeed']
            # if ev.key == pygame.K_RIGHT:
            #     state['mainPipePos'][0] += state['pipeSpeed']

            # For game reseting
            if ev.key == pygame.K_r and state['hitPipe'] == True:
                resets(state)
    
    # ----------------- Updates pipe position ------------------- #

    if state['coinCounter'] >= 10:

        # Horizontal speed
        if state['coinCounter'] >= 50:
            state['pipeSpeedH'] = 5
        elif state['coinCounter'] >= 40:
            state['pipeSpeedH'] = 4
        elif state['coinCounter'] >= 30:
            state['pipeSpeedH'] = 3
        elif state['coinCounter'] >= 20:
            state['pipeSpeedH'] = 2
        elif state['coinCounter'] >= 10:
            state['pipeSpeedH'] = 1

        # Direction of the movement
        if state['mainPipePos'][0] <= 0:
            state['pipeDirecton'] = 1
        elif state['mainPipePos'][0] >= state['windowSize'][0] - 64: 
            state['pipeDirecton'] = -1
        state['mainPipePos'][0] += state['pipeSpeedH'] * state['pipeDirecton']

    state['pipeUpperPos'][0] = state['mainPipePos'][0] 
    state['pipeLowerPos'][0] = state['mainPipePos'][0]
    state['coinPos'][0] = state['mainPipePos'][0] + 16

    state['pipeUpperPos'][1] = state['mainPipePos'][1] -472
    state['pipeLowerPos'][1] = state['mainPipePos'][1] + 250
    state['coinPos'][1] = state['mainPipePos'][1] + 189

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':
    window, assets, state = inicialize()
    while current_game_state(state):
        rendering_to_screen(window, assets, state)
    pygame.quit()