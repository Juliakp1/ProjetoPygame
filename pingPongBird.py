import pygame, time

#temporary
playerImg = {
    'birb': 'assets/birbGba.png',
    'pipe': 'assets/pipeGba.png',
    'coin': 'assets/coinGba.png',
    'bg': 'assets/bgGba.png'
}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize(playerImg):

    pygame.init()
    pygame.key.set_repeat(50)

    # ----------------- Gets images and fonts ------------------- #

    imgBirb = pygame.image.load(playerImg['birb'])
    imgBirb = pygame.transform.scale(imgBirb, (34, 24))
    flipBirb = pygame.transform.flip(imgBirb, True, False)

    imgPipe = pygame.image.load(playerImg['pipe'])
    imgPipe = pygame.transform.scale(imgPipe, (64, 600))
    pipeTop = pygame.transform.flip(imgPipe, False, True)

    imgCoin = pygame.image.load(playerImg['coin'])
    imgCoin = pygame.transform.scale(imgCoin, (32, 32))

    imgBg = pygame.image.load(playerImg['bg'])
    imgFilter = pygame.image.load('assets/dreamscape.png')

    fontDef = pygame.font.Font('assets/pixelFont.ttf', 60)

    # ----------------- Assets ------------------- #

    assets = {
        'birb': imgBirb,
        'flipBirb': flipBirb,
        'background': imgBg,
        'filter': imgFilter,
        'pipeLow': imgPipe,
        'pipeTop': pipeTop,
        'fontDef': fontDef,
        'coin': imgCoin,
    }

    # ----------------- Game States ------------------- #

    statePing = {
        'windowSize': [1200, 600],
        'mainPipePos': [580, 0],
        'ballPos': [700, 200],
        'ballVel': [200, 100],
        'pipeUpperPos': [580, -472],
        'pipeLowerPos': [580, 250],
        'pipeSpeedV': 8,
        'pipeSpeedH': 1,
        'pipeDirecton': 1,
        'coinPos': [596, 189],
        'gotCoin': False,
        'coinCounter': 0,
        'last_updated': 0,
        'gravity': 90,
        'hitPipe': False,
        'timer': 5000,
        'fading': False,
        'quitGame': False
    }

    return assets, statePing

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def resets(statePing):
    statePing['hitPipe'] = False
    statePing['gotCoin'] = False
    statePing['ballPos'] = [1000, 200]
    statePing['ballVel'] = [200, 100]
    statePing['mainPipePos'] = [580,0]
    statePing['coinCounter'] = 0
    tiks = pygame.time.get_ticks()
    statePing['last_updated'] = tiks
    statePing['timer'] = 5000

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def rendering_to_screen(window: pygame.Surface, assets, statePing):

    window.blit(assets['background'], [0, 0])
    
    # ----------------- Renders pipe ------------------- #

    window.blit(assets['pipeTop'], statePing['pipeUpperPos'])

    window.blit(assets['pipeLow'], statePing['pipeLowerPos'])

    # ----------------- Renders coin and counter ------------------- #

    if statePing['gotCoin'] == False:
        window.blit(assets['coin'], statePing['coinPos'])
    
    coins = str(statePing['coinCounter'])
    window.blit(assets['fontDef'].render(coins, True, (0, 0, 0)), (20, 15))
    window.blit(assets['fontDef'].render(coins, True, (255, 255, 255)), (18, 13))

    # ----------------- Renders birb ------------------- #

    if statePing['fading'] == False:    
        if statePing['ballVel'][0] < 0:
            flipBirb = pygame.transform.rotate(assets['flipBirb'], statePing['ballVel'][1] * 0.25)
            window.blit(flipBirb, statePing['ballPos'])

        else:
            birb = pygame.transform.rotate(assets['birb'], -statePing['ballVel'][1] * 0.25)
            window.blit(birb, statePing['ballPos'])

    # ----------------- Renders Game Over ------------------- #

    if statePing['hitPipe'] == True:
        window.blit(assets['fontDef'].render('Game Over', True, (0, 0, 0)), (165, 170))
        window.blit(assets['fontDef'].render('Game Over', True, (255, 255, 255)), (163, 168)) 
    
    window.blit(assets['filter'], [0, 0])

    pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(statePing):

    if statePing['hitPipe'] == False:

        # ----------------- Makes birb bounce ------------------- #

        tiks = pygame.time.get_ticks()
        deltaT = (tiks - statePing['last_updated']) / 1000
        statePing['last_updated'] = tiks

        statePing['ballPos'][0] = statePing['ballPos'][0] + statePing['ballVel'][0] * deltaT 
        statePing['ballVel'][1] = statePing['ballVel'][1] + statePing['gravity'] * deltaT
        statePing['ballPos'][1] = statePing['ballPos'][1] + statePing['ballVel'][1] * deltaT 

        # ----------------- Makes birb not off screen ------------------- #

        # Horizontally
        if statePing['ballPos'][0] >= statePing['windowSize'][0] - 35 :
            statePing['ballVel'][0] *= -1
            statePing['gotCoin'] = False
            statePing['ballPos'][0] = statePing['windowSize'][0] - 35
        elif statePing['ballPos'][0] < 0:
            statePing['ballVel'][0] *= -1
            statePing['gotCoin'] = False
            statePing['ballPos'][0] = 2

        # Vertically
        if statePing['ballPos'][1] - 30 < 0 or statePing['ballPos'][1] + 30 >= statePing['windowSize'][1]:
            statePing['ballVel'][1] *= -1
            statePing['ballPos'][1] =  statePing['windowSize'][1] - 35

        # ----------------- Colision with the pipe and coin ------------------- #

        # first checks if its in the pipe area horizontally
        if statePing['ballPos'][0] + 32 > statePing['pipeUpperPos'][0] and statePing['ballPos'][0] < statePing['pipeUpperPos'][0] + 64:
            # checks to see if its in the pipe, or got the coin
            if statePing['ballPos'][1] < statePing['pipeUpperPos'][1] + 600 or statePing['ballPos'][1] > statePing['pipeLowerPos'][1] - 20:
                statePing['hitPipe'] = True
            # Coin collision
            if statePing['ballPos'][1] < statePing['coinPos'][1] + 32 and statePing['ballPos'][1] > statePing['coinPos'][1]:
                if statePing['gotCoin'] == False:
                    statePing['gotCoin'] = True
                    statePing['coinCounter'] += 1
        
    # ----------------- Timer after hitting pipe ------------------- #

    tiks = pygame.time.get_ticks()
    if statePing['last_updated'] + 500 < tiks:
        return False

    # ------------------------------------------------- #

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            statePing['quitGame'] = True
            return False

    # ----------------- Key Presses ------------------- #

        if ev.type == pygame.KEYDOWN:

            # Controls the pipe
            if ev.key == pygame.K_UP and statePing['mainPipePos'][1] >= -128:
                statePing['mainPipePos'][1] -= statePing['pipeSpeedV']
            if ev.key == pygame.K_DOWN and statePing['mainPipePos'][1] <= 350:
                statePing['mainPipePos'][1] += statePing['pipeSpeedV']

            # if ev.key == pygame.K_LEFT:
            #     state['mainPipePos'][0] -= state['pipeSpeed']
            # if ev.key == pygame.K_RIGHT:
            #     state['mainPipePos'][0] += state['pipeSpeed']

            # For game reseting
            if ev.key == pygame.K_r and statePing['hitPipe'] == True:
                resets(statePing)
    
    # ----------------- Updates pipe position ------------------- #

    if statePing['coinCounter'] >= 10:

        # Horizontal speed
        if statePing['coinCounter'] >= 50:
            statePing['pipeSpeedH'] = 5
        elif statePing['coinCounter'] >= 40:
            statePing['pipeSpeedH'] = 4
        elif statePing['coinCounter'] >= 30:
            statePing['pipeSpeedH'] = 3
        elif statePing['coinCounter'] >= 20:
            statePing['pipeSpeedH'] = 2
        elif statePing['coinCounter'] >= 10:
            statePing['pipeSpeedH'] = 1

        # Direction of the movement
        if statePing['mainPipePos'][0] <= 0:
            statePing['pipeDirecton'] = 1
        elif statePing['mainPipePos'][0] >= statePing['windowSize'][0] - 64: 
            statePing['pipeDirecton'] = -1
        statePing['mainPipePos'][0] += statePing['pipeSpeedH'] * statePing['pipeDirecton']

    statePing['pipeUpperPos'][0] = statePing['mainPipePos'][0] 
    statePing['pipeLowerPos'][0] = statePing['mainPipePos'][0]
    statePing['coinPos'][0] = statePing['mainPipePos'][0] + 15

    statePing['pipeUpperPos'][1] = statePing['mainPipePos'][1] -472
    statePing['pipeLowerPos'][1] = statePing['mainPipePos'][1] + 250
    statePing['coinPos'][1] = statePing['mainPipePos'][1] + 189

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def ping_pong_birb(playerImg, window):

    assets, statePing = inicialize(playerImg)

    # Custom window
    pygame.display.set_caption('Ping-pong Bird')
    icon = pygame.transform.scale(assets['birb'], (32, 32))
    pygame.display.set_icon(icon)

    while current_game_state(statePing):
        rendering_to_screen(window, assets, statePing)
    
    return statePing['coinCounter']

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':
    window = pygame.display.set_mode((1200, 600), vsync=True, flags=pygame.SCALED)
    ping_pong_birb(playerImg, window)
    pygame.quit()