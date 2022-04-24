import pygame, random, time
from testepingpong import ping_pong_birb
from mainMenu import main_menu
from classes1 import *

def inicialize():
    
    pygame.init()
    pygame.key.set_repeat(50)

    # ----------------- States ------------------- #

    state = {
        'birb' : birb(200, 300, 34, 24, -100),


        'gravity': 500,
        'coinCounter': 0,
        'floorHeight': 520,
        'lastUpdated': 0,
        'coins': [

        ],
        'lastCoin' : True,
        'lastPipe': 0,
        'pipeTimer': 5000,
        'pipes': [

        ],

        'powerupTime': 10000,
        'collectCloud': True,
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
    state['birb'].x , state['birb'].y = 200, 300
    state['birb'].vel = 100

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #


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
        state['birb'].y = 100
        state['lastUpdated'] = pygame.time.get_ticks()
        custom_window(assets)
    
    # -------- Lychee ------- #
    if state['collectLychee'] == True:
        state['birb'].size = [17, 12]
        state['lastLychee'] = tiks
        state['collectLychee'] = False
    if tiks - state['lastLychee'] > state['powerupTime'] and tiks - state['lastLychee'] < state['powerupTime'] + 200:
        state['birb'].size = [34, 24]

    # -------- Watermelon ------- #
    if state['collectWatermelon'] == True:
        state['birb'].size = [68, 48]
        state['lastWatermelon'] = tiks
        state['collectWatermelon'] = False
    if tiks - state['lastWatermelon'] > state['powerupTime'] and tiks - state['lastWatermelon'] < state['powerupTime'] + 200:
        state['birb'].size = [34, 24]
    
    # -------- Coffee ------- #  
    if state['collectCoffee'] == True:
        state['pipeSpeed'] = 3
        state['lastCoffee'] = tiks
        state['collectCoffee'] = False
    if tiks - state['lastWatermelon'] > state['powerupTime'] and tiks - state['lastWatermelon'] < state['powerupTime'] + 200:
        state['pipeSpeed'] = 1

    # ----------------- Pipe spawing -------------------- #

    if tiks - state['lastPipe'] > state['pipeTimer']:
        state['lastPipe'] = tiks
        state['pipes'].append(pipe(random.randint(50,370)))
        state['pipeTimer'] = random.choice(range(3000, 5000, 500))
        state['lastCoin'] = True
    
    if tiks - (state['lastPipe']) > state['pipeTimer']/2 and state['lastCoin']:
        state['coins'].append(coin(1200, random.randint(32, 480)))
        state['lastCoin'] = False
    
    # ----------------- Birb Vertical, Floor  and teto detection ------------------- #

    state['birb'].atualiza_status(deltaT, state['floorHeight'], state['gravity'])
    
    for i in state['pipes']:
        i.atualiza_status(deltaT)
        if i.verifica_colisao(state['birb']):
            return False
        if state['birb'].x - state['birb'].size[0] > i.upper_pos[0] and i.pont == False:
            state['coinCounter'] += 1
            i.pont = True
    
    for c in state['coins']:
        c.atualiza_status(deltaT)
        if c.verifica_colisao(state['birb']):
            state['coins'].remove(c)
            state['coinCounter'] +=1
    # --------------------------------------------------- #
    
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            return False

        # ----------------- Inputs ------------------- #
        if ev.type == pygame.KEYDOWN:
            
            # Jumping (only once)
            if (ev.key == pygame.K_UP or ev.key == pygame.K_SPACE or ev.key == pygame.K_w) and state['birb'].jumped == False:
                state['birb'].vel = -200
                state['birb'].jumped = True

            if ev.key == pygame.K_r and state['hitPipe'] == True:
                resets(state)
        
        if ev.type == pygame.KEYUP:
            if (ev.key == pygame.K_UP or ev.key == pygame.K_SPACE or ev.key == pygame.K_w):
                state['birb'].jumped = False


    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def rendering_to_screen(window: pygame.Surface, assets, state):

    # Bg
    window.blit(assets['background'], [0, 0])

    # Floor
    pygame.draw.polygon(window, (200, 0, 0), [(0, state['floorHeight']), (1200, state['floorHeight']), (1200, 600), (0, 600)])

    # Bird
    state['birb'].desenha(assets, window)

    # pipe
    for i in state['pipes']:
        i.desenha(window, assets)
    
    for c in state['coins']:
        c.desenha(window, assets)

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