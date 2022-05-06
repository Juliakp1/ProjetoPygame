import pygame, random, json
from mainMenu import main_menu
from classesfruityvel import *

# ----------------- Sounds ------------------- #

pygame.mixer.init()

coinNoise = pygame.mixer.Sound('assets/coinNoise.mp3') # quando coleta a moeda
death = pygame.mixer.Sound('assets/death.mp3') # quando o passarinho bate no cano
flap = pygame.mixer.Sound('assets/flap.mp3') # quando o passarinho pula
whoosh = pygame.mixer.Sound('assets/whoosh.mp3') # quando o passarinho passa pelo cano
frootYes = pygame.mixer.Sound('assets/frootYes.mp3') # quando é coletado algum power up
frootNo = pygame.mixer.Sound('assets/frootNo.mp3') # quando o efeito do power up acaba

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize():
    
    pygame.init()
    pygame.key.set_repeat(50)

    # checks if there is a controller
    try:
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
    except:
        pygame.joystick.quit()
        joystick = 0
    
    # Says if it is connected or not
    if pygame.joystick.get_init():
        print('Controller connected!')
    else:
        print('No controller connected!')

    # ----------------- States ------------------- #

    state = {
        # birb
        'birb' : Birb(200, 300, 34, 24, -100),

        # pipe 
        'hitPipe': False,
        'lastPipe': 0,
        'pipeTimer': 5000,
        'pipes': [],

        # floor 
        'floorHeight': 520,
        'floorPos' : [[0,520], [600,520], [1200,520]],

        # coins
        'coinCounter': 0,
        'coins': [],
        'newCoin' : True,

        # collectables
        'newCollectable': True,
        'collectable': 'none',
        'contador': 5, # conta a quantidade de canos que já passaram (começa no 5 para que apareça um collectable logo no começo)
        'timeCollectable': 0, # momento em que o collectable foi coletado
        
        # geral 
        'lastUpdated': 0,
        'lastRestart': 0,
        'timeElapsed': 0,
        'nameChosen': 'asd',
        'vel': 100,
        'vel_padrao': 100,
        'closedGame': False,
        'joystick': joystick

    }

    return state

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def resets(state):
    """
    reinicia o valor das variáveis 
    """
    assets, nameChosen, state['closedGame'] = main_menu(window)

    # birb
    state['birb'] = Birb(200, 300, 34, 24, -100)

    # pipe
    state['pipes'] = []
    state['hitPipe'] = False
    state['lastPipe'] = pygame.time.get_ticks()
    
    # floor
    state['floorPos'] = [[0,520], [600,520], [1200,520]]
    
    # coins
    state['coins'] = []
    state['coinCounter'] = 0
    state['newCoin'] = True

    # collectable
    state['newCollectable'] = True
    state['collectable'] = 'none'
    state['contador'] = 5


    # geral
    state['lastRestart'] = pygame.time.get_ticks()
    state['nameChosen'] = nameChosen
    state['lastUpdated'] = pygame.time.get_ticks()
    
    # velocidade (de pipes, coins, collectables)
    state['vel'] = 100
    state['vel_padrao'] = 100
    state['muda_vel'] = True

    return assets, state['closedGame']

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def updates_ranking(nameChosen, coinCounter):
    """
    atualiza o ranking

    Argumentos
    -----------
    nameChosen : nome digitado pelo usuário
    coinCounter : quantidade de ponto que o usuário fez

    """

    # ----------------- Abre o arquivo do ranking ------------------- # 
    with open('ranking.json', 'r') as arquivo_json:
        rankString = arquivo_json.read()  
    ranks= json.loads(rankString)

    # ----------------- Adiciona a nova pontuação ------------------- # 

    if nameChosen not in ranks:
        ranks[nameChosen] = coinCounter
    else:
        if ranks[nameChosen] < coinCounter:
            ranks[nameChosen] = coinCounter

    # ----------------- Compara a pontuação em questão com a menor colocada  ------------------- #

    if len(ranks) > 15:
        lowestScore = 10 ** 7
        for names in ranks:
            if ranks[names] < lowestScore:
                lowestScore = ranks[names]
                lowestName = names
        if lowestScore > 10 ** 7:
            del ranks[lowestName]

    ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)} # organiza o ranking em ordem crescente

    # reescreve o ranking com as modificações efetuadas na função
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
    """
    - cria um novo objeto das classes Pipe, Coin e Collectable de acordo com tempo de cada um
    -  atualiza a posição dos objetos e verifa a colisão de cada um em relação ao birb

    """
    # ----------------- Tempo ------------------- #

    tiks = pygame.time.get_ticks()
    deltaT = (tiks - state['lastUpdated']) / 1000
    state['lastUpdated'] = tiks

    state['timeElapsed'] = (tiks - state['lastRestart']) / 1000


    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

    # --------------------------- Pipe, Coin e Collectable spawing ------------------------------- #

    # modifica o tempo entre um cano e outro de acordo com a pontuação 
    if state['coinCounter'] >= 120:
        state['pipeTimer'] = random.choice(range(1000, 3000, 500))
    elif state['coinCounter'] >= 60:
        state['pipeTimer'] = random.choice(range(2000, 4000, 500))
    else:
        state['pipeTimer'] = random.choice(range(3000, 5000, 500))

    # adiciona o novo cano
    if tiks - state['lastPipe'] > state['pipeTimer']:
        state['lastPipe'] = tiks
        state['pipes'].append(Pipe(random.randint(50,370)))
        state['pipeTimer'] = random.choice(range(3000, 5000, 500))
        state['newCoin'] = True
        state['contador'] += 1
        
    # adiciona a nova moeda 
    if tiks - (state['lastPipe']) > state['pipeTimer']/2 and state['newCoin']:
        state['coins'].append(Coin(1200, random.randint(32, 480)))
        state['newCoin'] = False 
    
    # adiciona o novo collectable
    if state['contador'] > 6 and tiks - state['lastPipe'] > 1500 and state['newCollectable']:
        state['collectable'] = Collectables(random.randint(32,480))
        state['newCollectable'] = False
        state['contador'] = 0

    
    # ----------------- Pipe, Coin, Floor and ceiling detection ------------------- #

    state['birb'].atualiza_status(deltaT, state['floorHeight'])
    
    # atualiza a posição vertical e verifica a colisão de cada cano com o birb
    for i in state['pipes']:
        i.atualiza_status(deltaT, state['vel'])
        if i.verifica_colisao(state['birb']):
            state['hitPipe'] = True
            pygame.mixer.Sound.play(death)
        if state['birb'].x - state['birb'].size[0] > i.upper_pos[0] and i.passou == False:
            state['coinCounter'] += 1
            pygame.mixer.Sound.play(whoosh)
            i.passou = True
    
    # atualiza a posição vertical e verifica a colisão de cada moeda com o birb
    for c in state['coins']:
        c.atualiza_status(deltaT, state['vel'])
        if c.verifica_colisao(state['birb']):
            state['coins'].remove(c)
            state['coinCounter'] +=1
            pygame.mixer.Sound.play(coinNoise)
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Collectables -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

    if state['collectable'] != 'none':
        state['collectable'].atualiza_status(deltaT, state['vel'])
        
        if state['collectable'].collected == False and state['collectable'].verifica_colisao(state['birb']):
            pygame.mixer.Sound.play(frootYes)
            state['timeCollectable'] = tiks
            state['collectable'].atualiza_efeitos(assets, state, window, tiks)
            
        if state['collectable'].collected == True:
            if tiks - state['timeCollectable'] > 15000:
                pygame.mixer.Sound.play(frootNo)
                state['collectable'].volta_normal( assets, state)
                state['collectable'] = 'none'
                state['newCollectable'] = True
            else:
                state['collectable'].atualiza_efeitos(assets, state,window, tiks)
        
        elif state['collectable'].x < 0:
            state['newCollectable'] = True

    # ---------- Movimentação do chão ----------- #
    for f in state['floorPos']:
        f[0] -= state['vel'] * deltaT
        if f[0] <= - 600:
            f[0] = 900

    # --------------------- Mudança da velocidade geral -----------------------------#
    if state['coinCounter'] != 0 and state['coinCounter'] % 20 == 0 and state['muda_vel'] and state['vel_padrao'] < 400:
        state['vel_padrao'] += 20
        state['vel'] = state['vel_padrao']
        state['muda_vel'] = False
    elif state['coinCounter'] % 20 != 0:
        state['muda_vel'] = True  

    # --------------------------------------------------- #
    
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            state['closedGame'] = True
        
        state['birb'].movimenta(ev, flap, state)
        
    if state['closedGame'] == True:
        return False

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def rendering_to_screen(window: pygame.Surface, assets, state):
    """
    desenha os itens na tela
    """
    # Bg
    window.blit(assets['background'], [0, 0])

    # Pipe
    for i in state['pipes']:
        i.desenha(window, assets)
    
    for c in state['coins']:
        c.desenha(window, assets)

    # Collectable
    if state['collectable'] != 'none':
        if state['collectable'].collected == False:
            state['collectable'].desenha(window, assets)

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
    for f in state['floorPos']:
        window.blit(assets['floor'], f)
 
    # Birb
    state['birb'].desenha(assets, window)

    # Game Over
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
    assets, state['closedGame'] = resets(state)
    custom_window(assets)

    rendering_to_screen(window, assets, state)

    while current_game_state(state, assets):
        rendering_to_screen(window, assets, state)

        # ----------------- Game over ------------------- #
        while state['hitPipe'] == True:

            tiks = pygame.time.get_ticks()
            deltaT = (tiks - state['lastUpdated']) / 1000
            state['lastUpdated'] = tiks
            state['birb'].atualiza_status(deltaT, state['floorHeight'])
            rendering_to_screen(window, assets, state)

 
            state['vel'] = 0

            for ev in pygame.event.get():

                updates_ranking(state['nameChosen'], state['coinCounter'])

                if ev.type == pygame.QUIT:
                    clickedX = True
                    state['hitPipe'] = False
                    break
                if ev.type == pygame.KEYDOWN: 
                    if ev.key == pygame.K_r or ev.key == pygame.K_ESCAPE or ev.key == pygame.K_RETURN:
                        assets, state['closedGame'] = resets(state)
                        custom_window(assets)

                if ev.type == pygame.JOYBUTTONDOWN:
                    assets, state['closedGame'] = resets(state)
                    custom_window(assets)
                    
        # ------------------------------------------------ #

        if clickedX == True: 
            break
            

    pygame.quit()
