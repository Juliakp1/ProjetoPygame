import pygame, json
from filePathDump import filePaths
pygame.mixer.init

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
            'Main menu': ['Start Game !', 'Birds', 'Pipes', 'Coins', 'Backgrounds', 'Floors', 'Name', 'Reset Skins', 'Rankings', 'Exit'],
            'Birds': birds,
            'Pipes': pipes,
            'Coins': coins,
            'Backgrounds': backgrounds,
            'Floors': floors,
            'Name': ['aaa'],
            'Rankings': ranking,
            'Reset Skins': ['assets/aaaaaFail.png'],
            'Exit': ['assets/aaaFail.png']
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
        'currentLetter': 0
    
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

    playerImg = playerImg = {
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

    window.blit(assets['background'], [0, 0])
    currentNameTxt = assets['fontDef'].render('Current Name:', True, (255, 255, 255))
    window.blit(currentNameTxt, (12, 32))
    currentNameTxt = assets['fontDef'].render('Current Name:', True, (0, 0, 0))
    window.blit(currentNameTxt, (10, 30))
    name = assets['fontDef'].render(state['nameChosen'], True, (255, 255, 255))
    window.blit(name, (12, 62))
    name = assets['fontDef'].render(state['nameChosen'], True, (0, 0, 0))
    window.blit(name, (10, 60))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN and state['pressedKey'] == False:
            
            if event.key == pygame.K_ESCAPE:
                state['currentMenu'] = 'Main menu'
                state['currentMenuIndex'] = 0
                state['currentItem'] = 0
                state['inMainMenu'] = True
                return False

            state['pressedKey'] = True
            key = event.unicode
            key = str(key)

            if state['currentLetter'] >= 3:
                state['currentLetter'] = 0
                
            pastName = state['nameChosen']
            if state['currentLetter'] == 0:
                newName = key + pastName[1] + pastName[2]
            elif state['currentLetter'] == 1:
                newName = pastName[0] + key + pastName[2]
            elif state['currentLetter'] == 2:
                newName = pastName[0] + pastName[1] + key
            state['nameChosen'] = newName
            state['currentLetter'] += 1

        if event.type == pygame.KEYUP:
            state['pressedKey'] = False

    pygame.display.update()

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def loads_images(playerImg):

    # ----------------- Loads Images ------------------- #

    imgBirb = pygame.image.load(playerImg['birb'])
    imgBirb = pygame.transform.scale(imgBirb, (34, 24))

    imgPipe = pygame.image.load(playerImg['pipe'])
    imgPipe = pygame.transform.scale(imgPipe, (64, 600))
    pipeTop = pygame.transform.flip(imgPipe, False, True)

    imgCoin = pygame.image.load(playerImg['coin'])
    imgCoin = pygame.transform.scale(imgCoin, (32, 32))

    imgBg = pygame.image.load(playerImg['bg'])

    imgFloor = pygame.image.load(playerImg['floor'])

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
        'floor': imgFloor
    }

    return assets

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def removesUnwated(string, group):

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

def current_game_state(state, assets, window):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:

            # ----------------- Enters a menu ------------------- #
            if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_e) and state['pressedKey'] == False:
                state['pressedKey'] = True
                pygame.mixer.Sound.play(menuNoise)

                if state['inMainMenu'] == True:

                    if state['menus']['Main menu'][state['currentItem']] == 'Start Game !':
                        return False
                    else:
                        state['currentMenu'] = state['menus'][state['currentMenu']][state['currentItem']]
                        state['currentMenuIndex'] = state['currentItem']
                        state['inMainMenu'] = False

                if state['currentMenu'] == 'Name':
                    changingName = True
                    while changingName == True:
                        changingName = name_changer(state, assets, window)
                    state['currentMenu'] = 'Main menu'
                    state['currentMenuIndex'] = 0
                    state['inMainMenu'] = True

                # ----------------- Loads selected images ------------------- #
                elif state['currentMenuIndex'] in [1, 2, 3, 4, 5]:

                    # Bird
                    if state['currentMenuIndex'] == 1:
                        changedImg = 'birb'

                    # Pipes
                    elif state['currentMenuIndex'] == 2:
                        changedImg = 'pipe'
                    
                    # Coins
                    elif state['currentMenuIndex'] == 3:
                        changedImg = 'coin'

                    # Bg
                    elif state['currentMenuIndex'] == 4:
                        changedImg = 'bg'

                    # Floors
                    elif state['currentMenuIndex'] == 5:
                        changedImg = 'floor'

                    # ----------------- Updates the json ------------------- #

                    with open('playerPrefs.json', 'r') as arquivo_json:
                        skinsString = arquivo_json.read()  
                    playerImg = json.loads(skinsString)

                    
                    print([state['currentItem']])
                    playerImg[changedImg] = state['menus'][state['currentMenu']][state['currentItem']]

                    updatedJson = json.dumps(playerImg)
                    with open('playerPrefs.json', 'w') as arquivo_json:
                        arquivo_json.write(updatedJson)  

                state['currentItem'] = 0
            
            # ----------------- Goes up and down menus ------------------- #

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
        
        if event.type == pygame.KEYUP:
            state['pressedKey'] = False

    # ----------------- Other menus ------------------- #

    if state['currentMenu'] == 'Reset Skins':
        reset_skins()
        state['currentMenu'] = 'Main menu'
        state['currentMenuIndex'] = 0
        state['inMainMenu'] = True

    if state['currentMenuIndex'] == 9:
        return False
    
    # ------------------------------------ #

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def render_to_screen(state, assets, window):
    
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
            if state['currentMenu'] == 'Main menu':
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

    return assets, state['nameChosen']

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':

    window = pygame.display.set_mode((1200, 600), vsync=True, flags=pygame.SCALED)
    main_menu(window)
    pygame.quit()