# -------- Cloud Portal ------- #
'''
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

    # -------- Jaca ------- #  
    if state['collectJaca'] == True:
        for i in state['pipes']:
            i.vel /= 2
        for i in state['coins']:
            i.vel /= 2
        state['lastJaca'] = tiks
        state['collectJaca'] = False

    # -------- Carambola ------- #  
    if state['collectStar'] == True:
        state['coinCounter'] += range(3, 6)
        state['collectStar'] = False
'''

# 'powerupTime': 10000,
        # 'collectCloud': True,
        # 'collectLychee': False,
        # 'lastLychee': 0,
        # 'collectWatermelon': False,
        # 'lastWatermelon': 0,
        # 'collectCoffee': False,
        # 'lastCoffee': 0,
        # 'collectJaca': False,
        # 'lastJaca': 0,
        # 'collectStar': False,