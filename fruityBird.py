import pygame, random, json
from pingPongBird import ping_pong_birb
from mainMenu import main_menu
from classesfruity import *

# ----------------- Sounds ------------------- #

pygame.mixer.init()

coinNoise = pygame.mixer.Sound('assets/coinNoise.mp3')
death = pygame.mixer.Sound('assets/death.mp3')
flap = pygame.mixer.Sound('assets/flap.mp3')
whoosh = pygame.mixer.Sound('assets/whoosh.mp3')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize():
    
    pygame.init()
    pygame.key.set_repeat(50)

    # ----------------- States ------------------- #

    state = {

        'birb' : birb(200, 300, 34, 24, -100),
        'hitPipe': False,

        'gravity': 500,
        'floorHeight': 520,
        'lastUpdated': 0,
        'lastRestart': 0,
        'timeElapsed': 0,
        'nameChosen': 'asd',

        'coinCounter': 0,
        'coins': [],
        'lastCoin' : True,

        'lastPipe': 0,
        'pipeTimer': 5000,
        'pipes': [],

        'powerupTime': 10000,
        'collectCloud': False,
        'collectLychee': False,
        'lastLychee': 0,
        'collectWatermelon': False,
        'lastWatermelon': 0,
        'collectCoffee': False,
        'lastCoffee': 0,
        'collectJaca': False,
        'lastJaca': 0,
        'collectStar': False,

    }

    return state

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def resets(state):

    assets, nameChosen = main_menu(window)

    state['hitPipe'] = False
    state['lastRestart'] = pygame.time.get_ticks()
    state['lastPipe'] = pygame.time.get_ticks()
    state['coinCounter'] = 0
    state['lastCoin'] = True
    state['birb'].x , state['birb'].y = 200, 300
    state['birb'].vel = 100
    state['pipes'] = []
    state['coins'] = []
    state['nameChosen'] = nameChosen

    return assets

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def updates_ranking(nameChosen, coinCounter):

    with open('ranking.json', 'r') as arquivo_json:
        rankString = arquivo_json.read()  
    ranks= json.loads(rankString)

    # ----------------- Adds new score ------------------- # 

    if nameChosen not in ranks:
        ranks[nameChosen] = coinCounter
    else:
        if ranks[nameChosen] < coinCounter:
            ranks[nameChosen] = coinCounter

    # ----------------- Checks top 15 ------------------- #

    if len(ranks) > 15:
        lowestScore = 0
        for names in ranks:
            if ranks[names] < lowestScore:
                lowestScore = lowestScore
                lowestName = names
        del ranks[lowestName]

    ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}

    updatedJson = json.dumps(ranks)
    with open('ranking.json', 'w') as arquivo_json:
        arquivo_json.write(updatedJson)  

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

    state['timeElapsed'] = (tiks - state['lastRestart']) / 1000

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Collectables -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

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
        for i in state['pipes']:
            i.vel *= 2
        for i in state['coins']:
            i.vel *= 2
        state['lastCoffee'] = tiks
        state['collectCoffee'] = False
    if tiks - state['lastCoffee'] > state['powerupTime'] and tiks - state['lastCoffee'] < state['powerupTime'] + 200:
        for i in state['pipes']:
            i.vel /= 2
        for i in state['coins']:
            i.vel /= 2

    # -------- Jaca ------- #  
    if state['collectJaca'] == True:
        for i in state['pipes']:
            i.vel /= 2
        for i in state['coins']:
            i.vel /= 2
        state['lastJaca'] = tiks
        state['collectJaca'] = False
    if tiks - state['lastJaca'] > state['powerupTime'] and tiks - state['lastJaca'] < state['powerupTime'] + 200:
        for i in state['pipes']:
            i.vel *= 2
        for i in state['coins']:
            i.vel *= 2

    # -------- Carambola ------- #  
    if state['collectStar'] == True:
        state['coinCounter'] += range(3, 6)
        state['collectStar'] = False

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

    # --------------------------- Pipe spawing ------------------------------- #

    if tiks - state['lastPipe'] > state['pipeTimer']:
        state['lastPipe'] = tiks
        state['pipes'].append(pipe(random.randint(50,370)))
        state['pipeTimer'] = random.choice(range(3000, 5000, 500))
        state['lastCoin'] = True

    
    if tiks - (state['lastPipe']) > state['pipeTimer']/2 and state['lastCoin']:
        state['coins'].append(coin(1200, random.randint(32, 480)))
        state['lastCoin'] = False
    
    # ----------------- Pipe, Coin, Floor and ceiling detection ------------------- #

    state['birb'].atualiza_status(deltaT, state['floorHeight'], state['gravity'])
    
    for i in state['pipes']:
        i.atualiza_status(deltaT)
        if i.verifica_colisao(state['birb']):
            state['hitPipe'] = True
            pygame.mixer.Sound.play(death)
        if state['birb'].x - state['birb'].size[0] > i.upper_pos[0] and i.pont == False:
            state['coinCounter'] += 1
            pygame.mixer.Sound.play(whoosh)
            i.pont = True
    
    for c in state['coins']:
        c.atualiza_status(deltaT)
        if c.verifica_colisao(state['birb']):
            state['coins'].remove(c)
            state['coinCounter'] +=1
            pygame.mixer.Sound.play(coinNoise)

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
            
            if ev.key == pygame.K_ESCAPE:
                state['hitPipe'] = True
        
        if ev.type == pygame.KEYUP:
            if (ev.key == pygame.K_UP or ev.key == pygame.K_SPACE or ev.key == pygame.K_w):
                state['birb'].jumped = False
                pygame.mixer.Sound.play(flap)

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def rendering_to_screen(window: pygame.Surface, assets, state):

    # Bg
    window.blit(assets['background'], [0, 0])

    # pipe
    for i in state['pipes']:
        i.desenha(window, assets)
    
    for c in state['coins']:
        c.desenha(window, assets)

    # Coin counter
    coins = str(state['coinCounter'])
    window.blit(assets['fontDef_big'].render(coins, True, (0, 0, 0)), (20, 65))
    window.blit(assets['fontDef_big'].render(coins, True, (255, 255, 255)), (18, 63))

    # Timer
    numb = state['timeElapsed']
    time = str.format(f'{numb:.2f}')
    window.blit(assets['fontDef_big'].render(time, True, (0, 0, 0)), (20, 15))
    window.blit(assets['fontDef_big'].render(time, True, (255, 255, 255)), (18, 13))

    # Floor
    window.blit(assets['floor'], [0, 520])

    # Bird
    state['birb'].desenha(assets, window)

    if state['hitPipe'] == True:
        window.blit(assets['fontDef_big'].render('Game Over', True, (0, 0, 0)), (165, 170))
        window.blit(assets['fontDef_big'].render('Game Over', True, (255, 255, 255)), (163, 168))

    pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':

    window = pygame.display.set_mode([1200, 600], vsync=True, flags=pygame.SCALED)
    clickedX = False

    # ----------------- Main menu and characters ------------------- #
    state = inicialize()
    assets = resets(state)
    custom_window(assets)

    rendering_to_screen(window, assets, state)

    while current_game_state(state, assets):
        rendering_to_screen(window, assets, state)

        # ----------------- Game over ------------------- #
        while state['hitPipe'] == True:

            tiks = pygame.time.get_ticks()
            deltaT = (tiks - state['lastUpdated']) / 1000
            state['lastUpdated'] = tiks
            state['birb'].atualiza_status(deltaT, state['floorHeight'], state['gravity'])
            rendering_to_screen(window, assets, state)

            for i in state['pipes']:
                i.vel = 0
            for i in state['coins']:
                i.vel = 0

            for ev in pygame.event.get():

                updates_ranking(state['nameChosen'], state['coinCounter'])

                if ev.type == pygame.QUIT:
                    clickedX = True
                    state['hitPipe'] = False
                    break
                if ev.type == pygame.KEYDOWN: 
                    if ev.key == pygame.K_r or ev.key == pygame.K_ESCAPE:
                        assets = resets(state)
                        custom_window(assets)
        # ------------------------------------------------ #

        if clickedX == True: 
            break
            

    pygame.quit()