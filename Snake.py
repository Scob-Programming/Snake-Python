# Pygame module based Snake game
# by Paul M Scobie 05/22/2019
import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_x = 800
display_y = 600

game_display = pygame.display.set_mode((display_x, display_y))
icon = pygame.image.load('snakeapple.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Snake by Paul M Scobie')
snake_img = pygame.image.load('snakehead.png')
apple_img = pygame.image.load('snakeapple.png')
block_size = 20
fps_limit = 7
direction = 'right'
clock = pygame.time.Clock()
small_font = pygame.font.SysFont('comicsansms', 25)
medium_font = pygame.font.SysFont('comicsansms', 50)
large_font = pygame.font.SysFont('comicsansms', 80)


def score(score):
    text = small_font.render('Score: '+str(score), True, white)
    game_display.blit(text, [0,0])


def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        game_display.fill(black)
        message_to_screen('Paused',
                          white,
                          -100,
                          'large')
        message_to_screen('Press C to Continue or Q to Quit',
                          white,
                          25,
                          'small')
        pygame.display.update()
        clock.tick(5)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        game_display.fill(black)
        message_to_screen("Welcome to Snake",
                          red,
                          -100,
                          "large")
        message_to_screen('Do Eat Apples',
                          white,
                          -30,
                          'small')
        message_to_screen('Do Not Eat Yourself',
                          white,
                          10,
                          'small')
        message_to_screen('Do Not Touch The Wall',
                          white,
                          50,
                          'small')
        message_to_screen('Press C to Play, P to Pause, or Q to Quit',
                          white,
                          180,
                          'small')
        pygame.display.update()
        clock.tick(15)


def snake(blocksize, snakelist):
    if direction == 'right':
        head = pygame.transform.rotate(snake_img, 270)
    if direction == 'left':
        head = pygame.transform.rotate(snake_img, 90)
    if direction == 'up':
        head = snake_img
    if direction == 'down':
        head = pygame.transform.rotate(snake_img, 180)

    game_display.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(game_display, green, [XnY[0], XnY[1], blocksize, blocksize])


def text_objects(text, color, size):
    if size == "small":
        text_surface = small_font.render(text, True, color)
    elif size == "medium":
        text_surface = medium_font.render(text, True, color)
    elif size == "large":
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    text_surface, text_rectangle = text_objects(msg, color, size)
    text_rectangle.center = (display_x / 2), (display_y / 2) + y_displace
    game_display.blit(text_surface, text_rectangle)


def game_loop():
    global direction
    game_exit = False
    game_over = False
    difficulty = fps_limit
    snake_list = []
    snake_length = 1
    lead_x = display_x / 2
    lead_y = display_y / 2
    lead_x_change = 0
    lead_y_change = 0
    rand_apple_x = random.randrange(0, display_x - block_size, block_size)
    rand_apple_y = random.randrange(0, display_y - block_size, block_size)

    while not game_exit:

        while game_over:
            game_display.fill(black)
            message_to_screen("Game Over",
                              red,
                              -200,
                              'large')
            message_to_screen('Press C to play again or Q to Quit',
                              white,
                              50,
                              'small')
            message_to_screen('Score: ' + str(round((snake_length - 1) / 2)),
                              white,
                              -20,
                              'small')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_exit = True
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0
        if lead_x >= display_x or lead_x < 0 or lead_y >= display_y or lead_y < 0:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        game_display.fill(black)
        score(round((snake_length - 1) / 2))
        apple_thickness = 20
        game_display.blit(apple_img, (rand_apple_x, rand_apple_y))

        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
        for each_segment in snake_list[:-1]:
            if each_segment == snake_head:
                game_over = True
        snake(block_size, snake_list)
        pygame.display.update()

        if rand_apple_x <= lead_x <= rand_apple_x + (apple_thickness - block_size) and rand_apple_y <= lead_y <= rand_apple_y + (apple_thickness - block_size):
            rand_apple_x = random.randrange(0, display_x - apple_thickness, apple_thickness)
            rand_apple_y = random.randrange(0, display_y - apple_thickness, apple_thickness)
            snake_length += 2
            difficulty = fps_limit + round(snake_length / 6)
        print(snake_head)
        print(snake_list)
        clock.tick(difficulty)

    pygame.display.update()
    pygame.quit()
    quit()


game_intro()
game_loop()
