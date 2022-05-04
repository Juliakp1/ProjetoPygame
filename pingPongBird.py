import pygame
from classespingpong import birb_pong, coin_pong, pipe_pong

# ----------------- Sounds ------------------- #

pygame.mixer.init()

coinNoise = pygame.mixer.Sound('assets/coinNoise.mp3') # quando coleta a moeda
death = pygame.mixer.Sound('assets/death.mp3') # quando o passarinho bate no cano
flap = pygame.mixer.Sound('assets/flap.mp3') # quando o passarinho pula
whoosh = pygame.mixer.Sound('assets/whoosh.mp3') # quando o passarinho passa pelo cano

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize(assets):

    pygame.init()
    pygame.key.set_repeat(50)

    # ----------------- Assets ----- -------------- #
    flipBirb = pygame.transform.flip(assets['birb'], True, False)
    assets['flipBirb'] = flipBirb
    assets['dreamscape'] = pygame.image.load('assets/dreamscape.png')

    # ----------------- Game States ------------------- #

    statePing = {
        'windowSize': [1200, 600],

        # ------ pipe ---- #
        
        'pipe_pong' : pipe_pong(0, -472, 250),

        # ---- birb_pong ---- #

        'birb_pong' : birb_pong(700, 200, 200, 100),

        # ----- coin ------- #
        'coin_pong' : coin_pong(596, 189, False, 0),

        'last_updated': 0,
        'gravity': 90,
        'hitPipe': False,
        'timer': 5000,
        'fading': False,
        'closedGame': False
    }

    return assets, statePing

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def resets(statePing):
    statePing['hitPipe'] = False
    

    statePing['birb_pong'] = birb_pong(1000, 200, 200, 100)

    statePing['pipe_pong'] = pipe_pong(0, -472, 250)
    
    statePing['coin_pong'] = coin_pong(596, 189, False, 0)

    tiks = pygame.time.get_ticks()
    statePing['last_updated'] = tiks
    statePing['timer'] = 5000

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def rendering_to_screen(window: pygame.Surface, assets, statePing):

    window.blit(assets['background'], [0, 0])
    
    # ----------------- Renders pipe ------------------- #

    statePing['pipe_pong'].rendering_to_screen(window, assets)

    # ----------------- Renders coin and counter ------------------- #

    if statePing['coin_pong'].collected == False:
        window.blit(assets['coin'], statePing['coin_pong'].pos)
    
    coins = str(statePing['coin_pong'].counter)
    window.blit(assets['fontDef_big'].render(coins, True, (0, 0, 0)), (20, 15))
    window.blit(assets['fontDef_big'].render(coins, True, (255, 255, 255)), (18, 13))

    # ----------------- Renders birb ------------------- #

    if statePing['fading'] == False:    
        statePing['birb_pong'].rendering_to_screen(window, assets)



    window.blit(assets['dreamscape'], [0, 0])

    pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(statePing):

    if statePing['hitPipe'] == False:


        # -------------------- Time -----------------------#
        
        tiks = pygame.time.get_ticks()
        deltaT = (tiks - statePing['last_updated']) / 1000
        statePing['last_updated'] = tiks
        
        # ----------- Makes birb bounce and birb not off screen ------------- #

        statePing['birb_pong'].atualiza_status(deltaT, statePing)

        # ----------------- Colision with the pipe and coin ------------------- #

        statePing['hitPipe'] = (statePing['pipe_pong']).verifica_colisao(statePing['birb_pong']) 
        statePing['coin_pong'].verifica_colisao(statePing['birb_pong'])
    
    # ----------------- Timer after hitting pipe ------------------- #

    tiks = pygame.time.get_ticks()
    if statePing['last_updated'] + 500 < tiks:
        return False

    # ------------------------------------------------- #

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            statePing['closedGame'] = True
            return False

    # ----------------- Key Presses ------------------- #

        if ev.type == pygame.KEYDOWN:

            # Controls the pipe
            statePing['pipe_pong'].movimenta(ev)


            # For game reseting
            if ev.key == pygame.K_r and statePing['hitPipe'] == True:
                resets(statePing)
    
    # ----------------- Updates pipe position ------------------- #
    
    statePing['pipe_pong'].atualiza_status(statePing, statePing['coin_pong'])

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def ping_pong_birb(assets, window):

    assets, statePing = inicialize(assets)

    # Custom window
    pygame.display.set_caption('Ping-pong Bird')
    icon = pygame.transform.scale(assets['birb'], (32, 32))
    pygame.display.set_icon(icon)

    statePing['last_updated'] = pygame.time.get_ticks()

    while current_game_state(statePing):
        rendering_to_screen(window, assets, statePing)
    
    return statePing['coin_pong'].counter, statePing['closedGame']

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
