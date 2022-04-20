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

    state = {

        'menus': {
            'Main menu': ['Birds', 'Pipes', 'Coins', 'Backgrounds', 'Floors'],
            'Birds': 0,
            'Pipes': 0,
            'Coins': 0,
            'Backgrounds': 0,
            'Floors': 0,
        },
        'currentlySelected': 0,
    
    }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def current_game_state():
    0

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

def main_menu(window):

    state, assets = inicialize()

    while current_game_state(state):
        0

    return playerImg

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

if __name__ == '__main__':

    window = pygame.display.set_mode((1200, 600), vsync=True, flags=pygame.SCALED)
    main_menu(window)
    pygame.quit()