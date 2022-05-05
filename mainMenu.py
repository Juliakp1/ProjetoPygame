import pygame, json
from filePathDump import filePaths
from pingPongBird import ping_pong_birb


# ----------------- Sounds ------------------- #

pygame.mixer.init()
menuNoise = pygame.mixer.Sound('assets/menuClick.mp3')


# ----------------- Def Images ------------------- #

playerImgDef = {
    'birb': 'assets/birbOG.png',
    'pipe': 'assets/pipeOG.png',
    'coin': 'assets/coinOG.png',
    'bg': 'assets/bgOG.png',
    'floor': 'assets/floorOG.png'
}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize():

    pygame.init()

    # checks if there is a controller
    try:
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
    except:
        pygame.joystick.quit()
        joystick = 0

    # ----------------- Renames Window ------------------- #

    pygame.display.set_caption('Main Menu')
    icon = pygame.image.load(playerImgDef['birb'])
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)

    # ----------------- Loads external stuff ------------------- #

    birds, pipes, coins, backgrounds, floors = filePaths()

    with open('ranking.json', 'r') as arquivo_json:
        ranksString = arquivo_json.read()
    ranking = json.loads(ranksString)

    tiks = pygame.time.get_ticks()

    # ----------------- States ------------------- #

    state = {

        'menus': {
            'Main menu': ['Start Game !', 'Skins', 'Name', 'Rankings', 'Ping Pong Bird', 'Exit'],
            'Skins': ['Birds', 'Pipes', 'Coins', 'Backgrounds', 'Floors', 'Reset Skins'],
            'Birds': birds,
            'Pipes': pipes,
            'Coins': coins,
            'Backgrounds': backgrounds,
            'Floors': floors,
            'Name': ['__________Change Name____'],
            'Rankings': ranking,
            'Ping Pong Bird': ['placeholder3'],
            'Reset Skins': ['placeholder1'],
            'Exit': ['placeholder2']
        },

        'currentMenu': 'Main menu',
        'currentItem': 0,
        'currentMenuIndex': 0,
        'inMainMenu': True,
        'pressedKey': False,

        'lastUpdated': tiks,
        'birbPos': [500, 300],
        'birbVel': -100,
        'birbFloor': 380,

        'nameChosen': 'aaa',
        'currentLetter': 0,
        'closedGame': False,
        'joystick': joystick
    
    }

    return state

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def printRankings(state, assets, window):

    i = 0
    for scores in state['menus']['Rankings'].items():
        scores = str(scores)
        scores = scores [1:(len(scores)-1)]
        text_image = assets['fontDef'].render(scores, True, (0, 0, 0))
        window.blit(text_image, (10, 10 + (i + 1) * 30))
        text_image = assets['fontDef'].render(scores, True, (255, 255, 255))
        window.blit(text_image, (8, 8 + (i + 1) * 30))
        i += 1

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def reset_skins():
    """
    estabele todas as skins para a versão padrão
    """

    playerImg = {
    'birb': 'assets/birbOG.png',
    'pipe': 'assets/pipeOG.png',
    'coin': 'assets/coinOG.png',
    'bg': 'assets/bgOG.png',
    'floor': 'assets/floorOG.png'
    }
                    
    updatedJson = json.dumps(playerImg)
    with open('playerPrefs.json', 'w') as arquivo_json:
        arquivo_json.write(updatedJson)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def name_changer(state, assets, window):
    """
    abre uma tela que possibilita a alteração do nome do usuário
    """

    while True:

        # ---------------- Bg e 'current name' -------------------- #

        window.blit(assets['background'], [0, 0])
        currentNameTxt = assets['fontDef'].render('Current Name:', True, (0, 0, 0))
        window.blit(currentNameTxt, (12, 32))
        currentNameTxt = assets['fontDef'].render('Current Name:', True, (255, 255, 255))
        window.blit(currentNameTxt, (10, 30))
        name = assets['fontDef'].render(state['nameChosen'], True, (0, 0, 0))
        window.blit(name, (12, 62))
        name = assets['fontDef'].render(state['nameChosen'], True, (255, 255, 255))
        window.blit(name, (10, 60))

        # ------------------------------------ #

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return False

            if event.type == pygame.KEYDOWN and state['pressedKey'] == False:
                
                # ------------------------------------ #
                
                if (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN) and state['nameChosen'] != 'aaa':
                    state['currentMenu'] = 'Main menu'
                    state['currentMenuIndex'] = 0
                    state['currentItem'] = 0
                    state['inMainMenu'] = True
                    return False

                # ------------------------------------ #

                if not (event.key == pygame.K_BACKSPACE or event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):

                    state['pressedKey'] = True
                    key = event.unicode
                    key = str(key)

                    if state['currentLetter'] >= 3:
                        state['currentLetter'] = 0
                    
                    # ---------------- Troca o nome uma letra por vez -------------------- #

                    pastName = state['nameChosen']
                    if state['currentLetter'] == 0:
                        newName = key + pastName[1] + pastName[2]
                    elif state['currentLetter'] == 1:
                        newName = pastName[0] + key + pastName[2]
                    elif state['currentLetter'] == 2:
                        newName = pastName[0] + pastName[1] + key
                    state['nameChosen'] = newName
                    state['currentLetter'] += 1

                # ------------------------------------ #

            if event.type == pygame.KEYUP:
                state['pressedKey'] = False

        pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def loads_images(playerImg):
    """
    carrega as imagens e cria o assets

    Argumento
    ---------
    playerImg : dicionário que armazena as skins escolhidas pelo usuário

    """

    # ----------------- Loads Images ------------------- #

    #  Geral  #
    imgBirb = pygame.image.load(playerImg['birb'])
    imgBirb = pygame.transform.scale(imgBirb, (34, 24))

    imgPipe = pygame.image.load(playerImg['pipe'])
    imgPipe = pygame.transform.scale(imgPipe, (64, 600))
    pipeTop = pygame.transform.flip(imgPipe, False, True)

    imgCoin = pygame.image.load(playerImg['coin'])
    imgCoin = pygame.transform.scale(imgCoin, (32, 32))

    imgBg = pygame.image.load(playerImg['bg'])

    imgFloor = pygame.image.load(playerImg['floor'])

    #  Frutas  #
    imgCloud = pygame.image.load('assets/fruitCloud.png')
    imgCloud = pygame.transform.scale(imgCloud, (32, 32))

    imgCoffee = pygame.image.load('assets/fruitCoffee.png')
    imgCoffee = pygame.transform.scale(imgCoffee, (32, 32))

    imgJaca = pygame.image.load('assets/fruitJaca.png')
    imgJaca = pygame.transform.scale(imgJaca, (32, 32))

    imgLychee = pygame.image.load('assets/fruitLychee.png')
    imgLychee = pygame.transform.scale(imgLychee, (32, 32))

    imgStar = pygame.image.load('assets/fruitStar.png')
    imgStar = pygame.transform.scale(imgStar, (32, 32))

    imgWatermelon = pygame.image.load('assets/fruitWatermelon.png')
    imgWatermelon = pygame.transform.scale(imgWatermelon, (32, 32))

    imgCoco = pygame.image.load('assets/fruitCoco.png')
    imgCoco = pygame.transform.scale(imgCoco, (32, 32))

    imgAmar = pygame.image.load('assets/fruitAmar.png')
    imgAmar = pygame.transform.scale(imgAmar, (32, 32))

    #  Fontes  #
    pygame.font.init()
    fontDef = pygame.font.Font('assets/pixelFont.ttf', 30)
    fontDef_big = pygame.font.Font('assets/pixelFont.ttf', 60)

    # ----------------- Assets ------------------- #

    assets = {
        'birb': imgBirb,
        'background': imgBg,
        'pipeLow': imgPipe,
        'pipeTop': pipeTop,
        'fontDef': fontDef,
        'fontDef_big' : fontDef_big,
        'coin': imgCoin,
        'floor': imgFloor,
        'cloud': imgCloud,
        'coffee': imgCoffee,
        'jaca' : imgJaca,
        'lychee': imgLychee,
        'star': imgStar,
        'waterm': imgWatermelon,
        'coco': imgCoco,
        'amar': imgAmar
    }

    return assets

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def removesUnwated(string, group):
    """
    remove a parte desnecessário do caminho do arquivo

    Argumentos
    ----------
    string : caminho da imagem 
    group : qual grupo de imagens, ela pertence ( ex. background )

    Exemplo
    -------
    assets/birbOG.png --> OG

    """

    if group == 'Backgrounds':
        extra = 'bgg'
    else:
        extra = group

    lenStart = len(extra) + len('assets/') - 1
    lenEnd = len(string) - 4
    finalString = string[lenStart:lenEnd]

    return finalString

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def renderBirb(state, assets, window):
    """
    movimenta o passaro do menu
    """

    tiks = pygame.time.get_ticks()
    deltaT = (tiks - state['lastUpdated']) /1000
    state['lastUpdated'] = tiks

    state['birbVel'] = state['birbVel'] + 300 * deltaT
    state['birbPos'][1] = state['birbPos'][1] + state['birbVel'] * deltaT 

    if state['birbPos'][1] > state['birbFloor']:
        state['birbVel'] = -230
        state['birbPos'][1] = state['birbFloor'] - 1

    birbRotation = -state['birbVel'] * 0.2
    birb = pygame.transform.rotate(assets['birb'], birbRotation)
    window.blit(birb, state['birbPos'])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def menu_choosing(state, assets):

    state['pressedKey'] = True
    pygame.mixer.Sound.play(menuNoise)

    if state['inMainMenu'] == True:

        if state['menus']['Main menu'][state['currentItem']] == 'Start Game !':
            return False
        else:
            state['currentMenuIndex'] = state['currentItem']
            state['inMainMenu'] = False
            state['currentItem'] = 0
            state['currentMenu'] = state['menus']['Main menu'][state['currentMenuIndex']]
        
    # Menu Skins
    elif state['currentMenu'] == 'Skins':
        state['currentMenuIndex'] = state['currentItem']
        state['currentItem'] = 0
        state['currentMenu'] = state['menus']['Skins'][state['currentMenuIndex']]

    # Menu Name
    elif state['currentMenu'] == 'Name':
        name_changer(state, assets, window)
        state['currentMenu'] = 'Main menu'
        state['currentMenuIndex'] = 0
        state['inMainMenu'] = True
        state['pressedKey'] = True

    # ----------------- Loads selected images ------------------- #
    elif state['currentMenu'] in ['Birds', 'Pipes', 'Coins', 'Backgrounds', 'Floors']:
        changedImg = 0

        # Bird
        if state['currentMenuIndex'] == 0:
            changedImg = 'birb'

        # Pipes
        elif state['currentMenuIndex'] == 1:
            changedImg = 'pipe'
        
        # Coins
        elif state['currentMenuIndex'] == 2:
            changedImg = 'coin'

        # Bg
        elif state['currentMenuIndex'] == 3:
            changedImg = 'bg'

        # Floors
        elif state['currentMenuIndex'] == 4:
            changedImg = 'floor'

        # ----------------- Updates the json ------------------- #
        if changedImg != 0:
            with open('playerPrefs.json', 'r') as arquivo_json:
                skinsString = arquivo_json.read()  
            playerImg = json.loads(skinsString)

            skinMenu = state['menus'][state['currentMenu']][state['currentItem']]
            playerImg[changedImg] = skinMenu

            updatedJson = json.dumps(playerImg)
            with open('playerPrefs.json', 'w') as arquivo_json:
                arquivo_json.write(updatedJson)  

    state['currentItem'] = 0

    return state

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(state, assets, window):
    """
    - captura os eventos do usuário
    - realiza a troca de telas no menu
    
    """

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            state['nameChosen'] ='aba'
            state['closedGame'] = True

        if event.type == pygame.KEYDOWN:

            # ----------------- Enters a menu ------------------- #
            if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_e) and state['pressedKey'] == False:
                state = menu_choosing(state, assets)
            
            # ----------------- Goes up and down menus in Keyboard ------------------- #

            if event.key == pygame.K_UP and state['pressedKey'] == False:
                state['currentItem'] -= 1
                if state['currentItem'] < 0:
                    state['currentItem'] = len(state['menus'][state['currentMenu']]) - 1
                state['pressedKey'] = True

            if event.key == pygame.K_DOWN and state['pressedKey'] == False:
                state['currentItem'] += 1
                if state['currentItem'] >= len(state['menus'][state['currentMenu']]):
                    state['currentItem'] = 0
                state['pressedKey'] = True

            if event.key == pygame.K_ESCAPE:
                state['currentMenu'] = 'Main menu'
                state['currentMenuIndex'] = 0
                state['currentItem'] = 0
                state['inMainMenu'] = True
        
        elif event.type == pygame.KEYUP:
            state['pressedKey'] = False

        # ----------------- Goes up and down menus in Joystick ------------------- #

        elif pygame.joystick.get_init():
            if state['joystick'].get_axis(1) < -0.9 and state['pressedKey'] == False:
                state['currentItem'] -= 1
                if state['currentItem'] < 0:
                    state['currentItem'] = len(state['menus'][state['currentMenu']]) - 1
                state['pressedKey'] = True
            elif state['joystick'].get_axis(1) > 0.9 and state['pressedKey'] == False:
                state['currentItem'] += 1
                if state['currentItem'] >= len(state['menus'][state['currentMenu']]):
                    state['currentItem'] = 0
                state['pressedKey'] = True

            if state['joystick'].get_axis(1) > -0.9 and state['joystick'].get_axis(1) < 0.9:
                state['pressedKey'] = False
    
        # ----------------- Clicking controller ------------------- #
            if event.type == pygame.JOYBUTTONDOWN:
                state['joystick'].rumble(0.2, 0.4, 100)
                if (state['joystick'].get_button(1) or state['joystick'].get_button(7)) != True:
                    state = menu_choosing(state, assets)

                else:
                    state['currentMenu'] = 'Main menu'
                    state['currentMenuIndex'] = 0
                    state['currentItem'] = 0
                    state['inMainMenu'] = True

            if event.type == pygame.JOYBUTTONUP:
                state['pressedKey'] = False

    # ----------------- Other menus ------------------- #

    if state['currentMenu'] == 'Reset Skins':
        reset_skins()
        state['currentMenu'] = 'Main menu'
        state['currentMenuIndex'] = 0
        state['inMainMenu'] = True

    if state['currentMenu'] == 'Ping Pong Bird':
        coin, state['closedGame'] = ping_pong_birb(assets, window)
        state['currentMenu'] = 'Main menu'
        state['currentMenuIndex'] = 0
        state['inMainMenu'] = True
    
    if state['currentMenu'] == 'Exit':
        state['closedGame'] = True
        
    # ------------------------------------ #
    
    if state['closedGame'] == True:
        state['nameChosen'] ='aba'
        return False
    
    # ------------------------------------ #

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def render_to_screen(state, assets, window):
    """
    desenha as imagens na tela
    """
    window.blit(assets['background'], [0, 0])
    window.blit(assets['pipeTop'], (600, -300))
    window.blit(assets['pipeLow'], (600, 400))
    window.blit(assets['coin'], (615, 340))
    window.blit(assets['floor'], [0, 520])

    renderBirb(state, assets, window)

    window.blit(assets['fontDef_big'].render('Fruity Bird', True, (0, 0, 0)), (795, 150))
    window.blit(assets['fontDef_big'].render('Fruity Bird', True, (255, 255, 255)), (793, 148)) 

    
    for i in range(len(state['menus'][state['currentMenu']])):

        if state['currentMenu'] == 'Rankings':
            printRankings(state, assets, window)
            
        else:
            if state['currentMenu'] == 'Main menu' or state['currentMenu'] == 'Skins':
                text = state['menus'][state['currentMenu']][i]
            else:
                text = removesUnwated(state['menus'][state['currentMenu']][i], state['currentMenu'])

            # ------------- Shows the little '>' -------------- #
            if i == state['currentItem']:
                text = '> ' + text
            else:
                text = '  ' + text
            text_image = assets['fontDef'].render(text, True, (0, 0, 0))
            window.blit(text_image, (10, 10 + (i + 1) * 30))
            text_image = assets['fontDef'].render(text, True, (255, 255, 255))
            window.blit(text_image, (8, 8 + (i + 1) * 30))

    pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def main_menu(window):

    with open('playerPrefs.json', 'r') as arquivo_json:
        skinsString = arquivo_json.read()  
    playerImg = json.loads(skinsString)
    assets = loads_images(playerImg)

    state = inicialize()

    while current_game_state(state, assets, window):

        with open('playerPrefs.json', 'r') as arquivo_json:
            skinsString = arquivo_json.read()  
        playerImg = json.loads(skinsString)
        assets = loads_images(playerImg)

        render_to_screen(state, assets, window)

    if state['nameChosen'] == 'aaa':
        name_changer(state, assets, window)

    return assets, state['nameChosen'], state['closedGame'] 

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':

    window = pygame.display.set_mode((1200, 600), vsync=True, flags=pygame.SCALED)
    main_menu(window)
    pygame.quit()