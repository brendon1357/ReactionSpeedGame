import pygame
from sys import exit
import random


def start_screen():
    pygame.init()
    begin_screen = pygame.display.set_mode((800, 600))
    intro_font = pygame.font.SysFont("arial", 36)

    intro_message_1 = intro_font.render("REACTION SPEED GAME", True, (0, 255, 255))
    begin_screen.blit(intro_message_1, [800 / 2 - intro_message_1.get_width() / 2, 10])

    intro_message_3 = intro_font.render("Left arrow key => move Left", True, (255, 255, 255))
    begin_screen.blit(intro_message_3, [800 / 2 - intro_message_3.get_width() / 2, 100])

    intro_message_4 = intro_font.render("Right arrow key => move Right", True, (255, 255, 255))
    begin_screen.blit(intro_message_4, [800 / 2 - intro_message_4.get_width() / 2, 200])

    intro_message_5 = intro_font.render("Spacebar => Jump", True, (255, 255, 255))
    begin_screen.blit(intro_message_5, [800 / 2 - intro_message_5.get_width() / 2, 300])

    intro_message_6 = intro_font.render("Press spacebar to start game", True, (255, 255, 255))
    begin_screen.blit(intro_message_6, [800 / 2 - intro_message_6.get_width() / 2, 400])

    intro_screen = True

    while intro_screen:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro_screen = False
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        pygame.display.update()


def display_instructions(screen):
    display_font = pygame.font.SysFont("arial", 21)

    display_message_1 = display_font.render("F - Pause game for instructions", True, (255, 255, 255))
    screen.blit(display_message_1, (10, 10))

    display_message_2 = display_font.render("C - Resume playing", True, (255, 255, 255))
    screen.blit(display_message_2, (10, 40))

    display_message_2 = display_font.render("ESC - Exit game ", True, (255, 255, 255))
    screen.blit(display_message_2, (10, 70))


def display_waves(screen, wave_num):
    wave_font = pygame.font.SysFont("arial", 21)

    waves_survived = wave_font.render("Waves Survived: " + str(wave_num), True, (0, 255, 255))
    screen.blit(waves_survived, [1000 / 2 - waves_survived.get_width() / 2, 10])


def is_collision(character, enemy):
    if character.colliderect(enemy):
        return True
    else:
        return False


def collision_ground(ground, enemy):
    if ground.colliderect(enemy):
        return True
    else:
        return False


def game_over(screen, font):
    screen.fill((0, 0, 0))
    lose_message = font.render("GAME OVER, press R to restart or ESC to exit", True, (255, 255, 255))
    screen.blit(lose_message, [800 / 2 - lose_message.get_width() / 2, 275])


def main():
    char_x = 440
    char_y = 500
    char_width = 25
    char_height = 25
    char_y_change = 0
    char_x_change = 0
    y_grav = 6

    wave_num = 0

    info_msg = False
    collide_enemy = False
    collision_enemy_ground = False
    stop_enemy_movement = False
    char_stop_movement = False

    ground_x = 0
    ground_y = 575
    ground_width = 800
    ground_height = 25

    clock = pygame.time.Clock()

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    color_blue = (0, 0, 255)
    color_char = (123, 44, 58)

    num_of_enemies = 12
    enemy_x = []
    enemy_y = []
    enemy_y_change = []

    for i in range(num_of_enemies):
        enemy_x.append(random.randint(0, 775))
        enemy_y.append(random.randint(0, 0))
        enemy_y_change.append(6)
        num_of_enemies = num_of_enemies

    isJump = False
    jumpCount = 10

    run = True

    while run:

        screen.fill((0, 0, 0))

        font = pygame.font.SysFont("arial", 30)

        display_instructions(screen)

        display_waves(screen, wave_num)

        character = pygame.draw.rect(screen, color_char, (char_x, char_y, char_width, char_height))
        ground = pygame.draw.rect(screen, (100, 111, 125), (ground_x, ground_y, ground_width, ground_height))

        char_y += y_grav

        for i in range(num_of_enemies):
            enemy = pygame.draw.rect(screen, color_blue, (enemy_x[i], enemy_y[i], 25, 25))
            enemy_y[i] += enemy_y_change[i]

            if stop_enemy_movement:
                enemy_y_change[i] = 0

            elif not stop_enemy_movement:
                enemy_y_change[i] = 6

            collision = is_collision(character, enemy)

            if collision:
                collide_enemy = True

            elif collide_enemy:
                game_over(screen, font)
                info_msg = False

            elif ground.colliderect(enemy):
                enemy_y[i] = 0
                enemy_x[i] = random.randint(0, 775)

            elif collision_ground(ground, enemy):
                collision_enemy_ground = True

        if collision_enemy_ground:
            wave_num += 1
            collision_enemy_ground = False

        if char_y >= 550:
            char_y = 550
        elif char_y <= 10:
            char_y = 10

        elif char_x >= 800 - char_width:
            char_x = 800 - char_width
        elif char_x <= 0:
            char_x = 0

        if info_msg:
            info_message_1 = font.render("Left and Right arrow keys to move", True, (255, 255, 255))
            info_message_2 = font.render("Spacebar to jump", True, (255, 255, 255))
            screen.blit(info_message_1, [800 / 2 - info_message_1.get_width() / 2, 300])
            screen.blit(info_message_2, [800 / 2 - info_message_2.get_width() / 2, 400])

        if isJump:
            if jumpCount >= -10:
                char_y -= (jumpCount * abs(jumpCount)) * 0.5
                jumpCount -= 1

            else:
                jumpCount = 10
                isJump = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT and not char_stop_movement:
                    char_x_change = 5

                elif event.key == pygame.K_LEFT and not char_stop_movement:
                    char_x_change = -5

                elif event.key == pygame.K_SPACE and char_y == 550 and not char_stop_movement:
                    isJump = True

                elif event.key == pygame.K_f:

                    info_msg = True
                    stop_enemy_movement = True
                    char_stop_movement = True

                elif event.key == pygame.K_c and info_msg:

                    info_msg = False
                    stop_enemy_movement = False
                    char_stop_movement = False

                    if char_y < 550:
                        isJump = True

                    y_grav = 6

                elif event.key == pygame.K_r:
                    main()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_RIGHT:
                    if char_x_change > 0:
                        char_x_change = 0

                elif event.key == pygame.K_LEFT:
                    if char_x_change < 0:
                        char_x_change = 0

        if char_stop_movement:
            char_x_change = 0
            char_y_change = 0
            isJump = False
            y_grav = 0

        char_x += char_x_change
        char_y += char_y_change

        pygame.display.update()
        clock.tick(60)


start_screen()
