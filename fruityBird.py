import pygame, random, time
from pingPongBird import *

#temporary
playerImg = {
    'birb': 'assets/birbGba.png',
    'pipe': 'assets/pipeGba.png',
    'coin': 'assets/coinGba.png',
    'bg': 'assets/bgGba.png'
}

def inicialize(playerImg):
    
    pygame.init()
    pygame.key.set_repeat(50)

    # ----------------- Gets images and fonts ------------------- #

    imgBirb = pygame.image.load(playerImg['birb'])
    imgBirb = pygame.transform.scale(imgBirb, (34, 24))

    imgPipe = pygame.image.load(playerImg['pipe'])
    imgPipe = pygame.transform.scale(imgPipe, (64, 600))
    pipeTop = pygame.transform.flip(imgPipe, False, True)

    imgCoin = pygame.image.load(playerImg['coin'])
    imgCoin = pygame.transform.scale(imgCoin, (32, 32))

    imgBg = pygame.image.load(playerImg['bg'])

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

    # ----------------- States ------------------- #

    state = {

        'windowSize': [1200, 600],
        'floorHeight': 520,
        'birbPos': [200, 300],
        'birbVel': -100,
        'jumped': False,
        'gravity': 500,
        'pipeSpeed': 1,
        'coinCounter': 0,
        'lastUpdated': 0,

        'collectCloud': False,
        'collectLychee': False

    }

    window = pygame.display.set_mode(state['windowSize'], vsync=True, flags=pygame.SCALED)

    return window, assets, state

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def title_screen():
    0
    # TODO 

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def resets(state):
    state['hitPipe'] = False
    state['coinCounter'] = 0
    state['birbPos'] = [200, 300]
    state['birbVel'] = 100

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def spawnNewPipe():

    randHeight = random.randint(0, )
    spawnHoriz = 1200

    mainPipePos = [spawnHoriz, randHeight]
    # pipeUpperPos = [spawnHoriz, randHeight - 300]
    # pipeLowerPos = [spawnHoriz, randHeight + 100]
    # coinPos = [spawnHoriz, randHeight + 50]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(state):

    # ----------------- Collectables ------------------- #

    if state['collectCloud'] == True:
        state['coinCounter'] += pingPongBirb(playerImg, window)
        state['collectCloud'] = False
    
    if state['collectLychee'] == True:
        # alter stuff here
        state['collectLychee'] = False

    # ----------------- Birb Vertical ------------------- #

    tiks = pygame.time.get_ticks()
    deltaT = (tiks - state['lastUpdated']) / 1000
    state['lastUpdated'] = tiks

    state['birbVel'] = state['birbVel'] + state['gravity'] * deltaT
    state['birbPos'][1] = state['birbPos'][1] + state['birbVel'] * deltaT 

    # ----------------- Pipe spawing -------------------- #

    # if tiks % 2000 == 0:
    #     spawnNewPipe()

    # ----------------- Floor detection ------------------- #

    if state['birbPos'][1] > state['floorHeight'] - 28:
        state['birbPos'][1] = state['floorHeight'] - 28

    # --------------------------------------------------- #
    
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            return False

        # ----------------- Inputs ------------------- #
        if ev.type == pygame.KEYDOWN:
            
            # Jumping (only once)
            if (ev.key == pygame.K_UP or ev.key == pygame.K_SPACE or ev.key == pygame.K_w) and state['jumped'] == False:
                state['birbVel'] = -200
                state['jumped'] = True

            if ev.key == pygame.K_r and state['hitPipe'] == True:
                resets(state)
        
        if ev.type == pygame.KEYUP:
            if (ev.key == pygame.K_UP or ev.key == pygame.K_SPACE or ev.key == pygame.K_w):
                state['jumped'] = False


    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def rendering_to_screen(window: pygame.Surface, assets, state):

    # Bg
    window.blit(assets['background'], [0, 0])

    # Floor
    pygame.draw.polygon(window, (200, 0, 0), [(0, state['floorHeight']), (1200, state['floorHeight']), (1200, 600), (0, 600)])

    # Bird
    if state['birbVel'] > 450:
        birbRotation = -90
    else:
        birbRotation = -state['birbVel'] * 0.2

    birb = pygame.transform.rotate(assets['birb'], birbRotation)
    window.blit(birb, state['birbPos'])

    # Coin counter
    coins = str(state['coinCounter'])
    window.blit(assets['fontDef'].render(coins, True, (0, 0, 0)), (20, 15))
    window.blit(assets['fontDef'].render(coins, True, (255, 255, 255)), (18, 13))

    pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':

    window, assets, state = inicialize(playerImg)

    # Custom window
    pygame.display.set_caption('Fruity Bird')
    icon = pygame.transform.scale(assets['birb'], (32, 32))
    pygame.display.set_icon(icon)

    rendering_to_screen(window, assets, state)

    while title_screen():
        0
        # TODO (probs new file or somethin)

    while current_game_state(state):
        rendering_to_screen(window, assets, state)

    pygame.quit()