import pygame, time
pygame.mixer.init

# The default values
playerImg = {
    'birb': 'assets/birbOG.png',
    'pipe': 'assets/pipeOG.png',
    'coin': 'assets/coinOG.png',
    'bg': 'assets/bgOG.png',
    'floor': 'assets/floorOG.png'
}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize():

    # ----------------- Renames Window ------------------- #

    pygame.display.set_caption('Main Menu')
    icon = pygame.image.load(playerImg['birb'])
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)

    # ----------------- Birds ------------------- #
    birds = [
        'assets/birbOG.png',
        'assets/birbPink.png',
        'assets/birbPurp.png',
        'assets/birbBaby.png',
        'assets/birbGba.png',
        'assets/birbGrey.png',
        'assets/birbRainbow.png',
        'assets/birbStone.png',
        'assets/birbNega.png',
        'assets/birbSepia.png',
        'assets/birbCrystal.png',
        'assets/birbGhost.png',
        'assets/birbLight.png',
        'assets/birbShadow.png'
    ]

    # ----------------- Pipes ------------------- #
    pipes = [
        'assets/pipeOG.png',
        'assets/pipePink.png',
        'assets/pipePurp.png',
        'assets/pipeBlue.png',
        'assets/pipeGba.png',
        'assets/pipeGrey.png',
        'assets/pipeRainbow.png',
        'assets/pipeSepia.png',
        'assets/pipeLight.png',
        'assets/pipeShadow.png'
    ]

    # ----------------- Coins ------------------- #
    coins = [ 
        'assets/coinOG.png',
        'assets/coinPurp.png',
        'assets/coinBaby.png',
        'assets/coinGba.png',
        'assets/coinGrey.png',
        'assets/coinRainbow.png',
        'assets/coinStone.png',
        'assets/coinNega.png',
        'assets/coinSepia.png',
        'assets/coinMine.png',
        'assets/coinLight.png',
        'assets/coinShadow.png'
    ]

    # ----------------- Backgrounds ------------------- #
    backgrounds = [
        'assets/bgOG.png',
        'assets/bgGba.png',
        'assets/bgSepia.png',
        'assets/bgMine.png',
        'assets/bgLight.png',
        'assets/bgShadow.png'
    ]

    # ----------------- Floors ------------------- #
    floors = [
        'assets/floorOG.png'
        'assets/floorGba.png'
        'assets/floorSepia.png'
    ]

    # ----------------- States ------------------- #
    state = {

        'menus': {
            'Main menu': ['Start Game !', 'Birds', 'Pipes', 'Coins', 'Backgrounds', 'Floors'],
            'Birds': birds,
            'Pipes': pipes,
            'Coins': coins,
            'Backgrounds': backgrounds,
            'Floors': floors,
        },
        'currentMenu': 'Main menu',
        'currentItem': 0,
        'currentMenuIndex': 0,
        'inMainMenu': True
    
    }

    return state

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
    fontDef = pygame.font.Font('assets/pixelFont.ttf', 60)

    # ----------------- Assets ------------------- #

    assets = {
        'birb': imgBirb,
        'background': imgBg,
        'pipeLow': imgPipe,
        'pipeTop': pipeTop,
        'fontDef': fontDef,
        'coin': imgCoin,
        'floor': imgFloor
    }

    return assets

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(state, assets):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:

            # ----------------- Enters a menu ------------------- #
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_e:

                if state['inMainMenu'] == True:

                    if state['menus']['Main menu'][state['currentItem']] == 'Start Game !':
                        return False
                    else:
                        state['currentMenu'] = state['menus'][state['currentMenu']][state['currentItem']]
                        state['inMainMenu'] = False

                # ----------------- Loads selected images ------------------- #
                else:

                    # Bird
                    if state['currentItem'] == 1:
                        imgBirb = pygame.image.load(state['menus']['Birds'][state['currentItem']])
                        imgBirb = pygame.transform.scale(imgBirb, (34, 24))
                        assets['birb'] = imgBirb

                    # Pipes
                    elif state['currentItem'] == 2:
                        imgPipe = pygame.image.load(state['menus']['Pipes'][state['currentItem']])
                        imgPipe = pygame.transform.scale(imgPipe, (64, 600))
                        pipeTop = pygame.transform.flip(imgPipe, False, True)
                        assets['pipeLow'] = imgPipe
                        assets['pipeTop'] = pipeTop
                    
                    # Coins
                    elif state['currentItem'] == 3:
                        imgCoin = pygame.image.load(state['menus']['Coins'][state['currentItem']])
                        imgCoin = pygame.transform.scale(imgCoin, (32, 32))
                        assets['coin'] = imgCoin

                    # Bg
                    elif state['currentItem'] == 4:
                        assets['bg'] = pygame.image.load(state['menus']['Backgrounds'][state['currentItem']])

                    # Floors
                    elif state['currentItem'] == 5:
                        assets['floor'] = pygame.image.load(state['menus']['Floors'][state['currentItem']])

                state['currentItem'] = 0
            
            # ----------------- Goes up and down menus ------------------- #

            if event.key == pygame.K_UP:
                state['currentItem'] -= 1
                if state['currentItem'] < 0:
                    state['currentItem'] = len(state['menus'][state['currentMenu']]) - 1

            if event.key == pygame.K_DOWN:
                state['currentItem'] += 1
                if state['currentItem'] >= len(state['menus'][state['currentMenu']]):
                    state['currentItem'] = 0

            if event.key == pygame.K_ESCAPE:
                state['currentMenu'] = 'Start Game !'
                state['currentMenuIndex'] = 0
                state['currentItem'] = 0

    print(state['currentMenu'])

    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def render_to_screen(state, assets, window):
    
    window.blit(assets['background'], [0, 0])

    window.blit(assets['fontDef'].render('Fruity Bird', True, (0, 0, 0)), (750, 170))
    window.blit(assets['fontDef'].render('Fruity Bird', True, (255, 255, 255)), (748, 168)) 

    for i in range(len(state['menus'][state['currentMenu']])):
        text = state['menus'][state['currentMenu']][i]
        if i == state['currentItem']:
            text = '> ' + text
        else:
            text = '  ' + text
        text_image = assets['fontDef'].render(text, True, (0, 0, 0))
        window.blit(text_image, (10, 10 + (i + 1) * 60))
        text_image = assets['fontDef'].render(text, True, (255, 255, 255))
        window.blit(text_image, (8, 8 + (i + 1) * 60))

    pygame.display.update()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def main_menu(window):

    state = inicialize()
    assets = loads_images(playerImg)

    while current_game_state(state, assets):
        render_to_screen(state, assets, window)

    return assets

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':

    window = pygame.display.set_mode((1200, 600), vsync=True, flags=pygame.SCALED)
    main_menu(window)
    pygame.quit()