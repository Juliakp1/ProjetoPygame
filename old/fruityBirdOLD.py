import pygame, random, time
from pingPongBird import ping_pong_birb
from mainMenu import main_menu

def inicialize():
    
    pygame.init()
    pygame.key.set_repeat(50)

    # ----------------- States ------------------- #

    state = {

        'birbPos': [200, 300],
        'birbVel': -100,
        'birbSize': [34, 24],
        'jumped': False,
        'gravity': 500,
        'coinCounter': 0,
        'floorHeight': 520,
        'lastUpdated': 0,

        'pipeSpeed': 1,
        'lastPipe': 0,
        'pipeTimer': 2000,

        'powerupTime': 10000,
        'collectCloud': False,
        'collectLychee': False,
        'lastLychee': 0,
        'collectCoffee': False,
        'lastCoffee': 0,
        'collectWatermelon': False,
        'lastWatermelon': 0

    }

    return state

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def resets(state):
    state['hitPipe'] = False
    state['coinCounter'] = 0
    state['birbPos'] = [200, 300]
    state['birbVel'] = 100

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def spawnNewPipe():

    print('New pipe!')

    # randHeight = random.randint(50, 550)
    # spawnHoriz = 1200

    # mainPipePos = [spawnHoriz, randHeight]
    # pipeUpperPos = [spawnHoriz, randHeight - 300]
    # pipeLowerPos = [spawnHoriz, randHeight + 100]
    # coinPos = [spawnHoriz, randHeight + 50]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def custom_window(assets):

    pygame.display.set_caption('Fruity Bird')
    icon = pygame.transform.scale(assets['birb'], (32, 32))
    pygame.display.set_icon(icon)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(state, assets):

    # ----------------- Time ------------------- #

    tiks = pygame.time.get_ticks()
    deltaT = (tiks - state['lastUpdated']) / 1000
    state['lastUpdated'] = tiks

    # ----------------- * Collectables * ------------------- #

    # -------- Cloud Portal ------- #

    if state['collectCloud'] == True:
        state['coinCounter'] += ping_pong_birb(assets, window)
        state['collectCloud'] = False
        state['birbPos'][1] = 100
        state['lastUpdated'] = pygame.time.get_ticks()
        custom_window(assets)
    
    # -------- Lychee ------- #
    if state['collectLychee'] == True:
        state['birbSize'] = [17, 12]
        state['lastLychee'] = tiks
        state['collectLychee'] = False
    if tiks - state['lastLychee'] > state['powerupTime'] and tiks - state['lastLychee'] < state['powerupTime'] + 200:
        state['birbSize'] = [34, 24]

    # -------- Watermelon ------- #
    if state['collectWatermelon'] == True:
        state['birbSize'] = [68, 48]
        state['lastWatermelon'] = tiks
        state['collectWatermelon'] = False
    if tiks - state['lastWatermelon'] > state['powerupTime'] and tiks - state['lastWatermelon'] < state['powerupTime'] + 200:
        state['birbSize'] = [34, 24]
    
    # -------- Coffee ------- #  
    if state['collectCoffee'] == True:
        state['pipeSpeed'] = 3
        state['lastCoffee'] = tiks
        state['collectCoffee'] = False
    if tiks - state['lastWatermelon'] > state['powerupTime'] and tiks - state['lastWatermelon'] < state['powerupTime'] + 200:
        state['pipeSpeed'] = 1

    # ----------------- Birb Vertical ------------------- #

    state['birbVel'] = state['birbVel'] + state['gravity'] * deltaT
    state['birbPos'][1] = state['birbPos'][1] + state['birbVel'] * deltaT 

    # ----------------- Pipe spawing -------------------- #

    if tiks - state['lastPipe'] > state['pipeTimer']:
        spawnNewPipe()
        state['lastPipe'] = tiks


    # ----------------- Floor detection ------------------- #

    if state['birbPos'][1] > state['floorHeight'] - state['birbSize'][1]:
        state['birbPos'][1] = state['floorHeight'] - state['birbSize'][1]

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

    window = pygame.display.set_mode([1200, 600], vsync=True, flags=pygame.SCALED)

    # ----------------- Main menu and characters ------------------- #
    assets = main_menu(window)
    
    state = inicialize()
    custom_window(assets)

    rendering_to_screen(window, assets, state)

    while current_game_state(state, assets):
        rendering_to_screen(window, assets, state)

    pygame.quit()