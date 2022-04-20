import pygame, time

# The default values
playerImg = {
    'birb': 'assets/birbGba.png',
    'pipe': 'assets/pipeGba.png',
    'coin': 'assets/coinGba.png',
    'bg': 'assets/bgGba.png'
}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def inicialize():

    # ----------------- Renames Window ------------------- #


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
    floors = []

    # ----------------- States ------------------- #
    state = {

        'menus': {
            'Main menu': ['Birds', 'Pipes', 'Coins', 'Backgrounds', 'Floors'],
            'birds': birds,
            'pipes': pipes,
            'coins': coins,
            'backgrounds': backgrounds,
            'floors': floors,
        },
        'currentlySelected': 0,
    
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
    }

    return assets

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state(state):


    return True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def render_to_screen(state, assets, window):
    0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def main_menu(window):

    state, assets = inicialize()

    # while current_game_state(state):
    #     render_to_screen(state, assets, window)

    assets = loads_images(playerImg)

    return assets

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':

    window = pygame.display.set_mode((1200, 600), vsync=True, flags=pygame.SCALED)
    main_menu(window)
    pygame.quit()