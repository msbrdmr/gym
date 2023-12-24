import pygame
import random

WIDTH, HEIGHT = 630, 480
ROW, COLUMN = 30, 40
FPS = 10

# snake and apple variables
snake_dir = ''  # This code is used to create a variable for the snake's direction. This variable will be used to store the snake's direction. The snake's direction will be either up, down, left, or right.
snake_list = []  # This code is used to create a list for the snake. This list will be used to store the snake's body parts. Each body part will be stored as a list of two numbers. The first number will be the X position of the body part. The second number will be the Y position of the body part.

apple_pos = []
snake_eat = False
snake_dead = False
score = 0


def snake_generating(SnakeList, SnakeDir):  # This function is used to generate the snake and its direction. It first checks if the snake list is empty. If it is, then it will generate the snake. If it is not, then it will check if the snake direction is empty. If it is, then it will generate the snake direction. If it is not, then it will return the snake list and snake direction.
    if len(SnakeList) == 0:  # If the snake has not been generated yet, then the snake list will be empty. This code is used to check if the snake list is empty. If it is, then it will generate the snake.
        # head
        x = random.randrange(3, COLUMN - 1)
        y = random.randrange(3, ROW - 1)
        # Here, I will create a variable for the snake's head. This variable will be used to store the snake's head. The snake's head will be stored as a list of two numbers. The first number will be the X position of the head. The second number will be the Y position of the head.
        # First element of the snake list is the head of the snake.
        SnakeList.append([x, y])

        # body
        SnakeList.append(random.choice(
            [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]))  # Based on the snake's head, 4 possible body parts can be generated. This code is used to generate the snake's body. It first creates a list of 4 possible body parts. Then, it selects one of the 4 possible body parts. Then, it appends the selected body part to the snake list.

        # tail
        # This x is the x position of the tail, last element of the snake list.
        x = SnakeList[-1][0]
        # This y is the y position of the tail, last element of the snake list.
        y = SnakeList[-1][1]
        # currently, x,y is tail position, so, as I have appended only one body, snake have 2 elements in the list, so, I am taking the last element of the list, which is the tail position.

        # 4 possible positions for 3rd body part that will be the tail.
        temp = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        # This code is used to remove the head from the list of possible body parts. This is done to prevent the tail from being generated in the same position as the head. Since therte is 2 squares
        temp.remove([SnakeList[0][0], SnakeList[0][1]])
        # in the snake, for the second added body part, there is 4 possible positions for the third body part. So, I am removing the head from the list of possible body parts, so that the tail will not be generated in the same position as the head.

        SnakeList.append(random.choice(temp))
        # Now, snake with 3 body parts is generated.

    if len(SnakeDir) == 0:
        # initail direction
        dir_list = ['right', 'left', 'up', 'down']
        if SnakeList[0][0] > SnakeList[1][0]:
            # IF the head is to the right of the second body part, then the snake cannot move left.
            dir_list.remove('left')
        if SnakeList[0][1] > SnakeList[1][1]:
            # If the head is below the second body part, then the snake cannot move up.
            dir_list.remove('up')
        if SnakeList[0][0] < SnakeList[1][0]:
            # If the head is to the left of the second body part, then the snake cannot move right.
            dir_list.remove('right')
        if SnakeList[0][1] < SnakeList[1][1]:
            # if the head is above the second body part, then the snake cannot move down.
            dir_list.remove('down')
        SnakeDir = random.choice(dir_list)
        # Now snake has a direction.

    return SnakeList, SnakeDir


def apple_generating(SnakeList, ApplePos):
    if len(ApplePos) == 0:
        # apple generating
        x = random.randrange(1, COLUMN + 1)
        y = random.randrange(1, ROW + 1)
        while [x, y] in SnakeList:
            # THis code allows to generate the apple in a random position that is not occupied by the snake repeatedly until the apple is generated in a position that is not occupied by the snake.
            x = random.randrange(1, COLUMN + 1)
            y = random.randrange(1, ROW + 1)
        ApplePos = [x, y]

    return ApplePos


def updating_snake(SnakeDir, SnakeList, SnakeEat, SnakeDead):
    # This function will be called on each game loop. It will update the snake's position based on the snake's direction. It will also update the snake's body based on whether the snake ate the apple or not.
    if not SnakeDead:
        if not SnakeEat:
            SnakeList.pop(-1)
            # IF the snake did not eat the apple, then the last element of the snake list will be removed. This is done to make the snake move.
        else:
            SnakeEat = False
            # If the snake ate the apple, then the last element of the snake list will not be removed. This is done to make the snake grow.

        if SnakeDir == 'up':
            SnakeList.insert(0, [SnakeList[0][0], SnakeList[0][1] - 1])
            # If the snake is moving up, then the snake's head will be inserted at the beginning of the snake list with y decremented by 1 since new head pos will be up.Head is copied and inserted at the beginning of the list based on the direction of the snake.
        if SnakeDir == 'down':
            SnakeList.insert(0, [SnakeList[0][0], SnakeList[0][1] + 1])
            # If the snake is moving down, then the snake's head will be inserted at the beginning of the snake list with y incremented by 1 since new head pos will be down.
        if SnakeDir == 'right':
            SnakeList.insert(0, [SnakeList[0][0] + 1, SnakeList[0][1]])
            # If the snake is moving right, then the snake's head will be inserted at the beginning of the snake list with x incremented by 1 since new head pos will be right.
        if SnakeDir == 'left':
            SnakeList.insert(0, [SnakeList[0][0] - 1, SnakeList[0][1]])
            # If the snake is moving left, then the snake's head will be inserted at the beginning of the snake list with x decremented by 1 since new head pos will be left.

    return SnakeList, SnakeEat


def collision(SnakeList, ApplePos, SnakeDir, SnakeEat, SnakeDead, Score):
    # apple and snake head
    # This function is also called on each game loop. It will check if the snake ate the apple or not. It will also check if the snake collided with the wall or itself.
    if SnakeList[0] == ApplePos:
        SnakeEat = True
        Score += 1
        ApplePos = []

    # snake head and wall
    if SnakeList[0][1] == 1 and SnakeDir == 'up':
        SnakeDead = True
    if SnakeList[0][1] == 30 and SnakeDir == 'down':
        SnakeDead = True
    if SnakeList[0][0] == 1 and SnakeDir == 'left':
        SnakeDead = True
    if SnakeList[0][0] == 40 and SnakeDir == 'right':
        SnakeDead = True
    # Abve code is used to check if the snake collided with the wall. If the snake collided with the wall, then the snake will die.

    # snake head and snake body
    if SnakeList[0] in SnakeList[1:]:
        SnakeDead = True
    # This code is used to check if the snake collided with itself. If the snake collided with itself, then the snake will die.

    # On each call, move,  collision with itself, walls and food is checked.
    return SnakeEat, SnakeDead, Score, ApplePos


pygame.init()
pygame.display.set_caption('Snake Game')
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial_bold', 380)
running = True

while running:
    # This is the game loop. It will run until the snake dies or the user closes the window.

    # First, the snake and apple will be generated. The check for snake generation like if snake exists, if snake direction exists, if apple exists, will be done in the snake_generating and apple_generating functions.

    snake_list, snake_dir = snake_generating(snake_list, snake_dir)
    apple_pos = apple_generating(snake_list, apple_pos)

    snake_list, snake_eat = updating_snake(
        snake_dir, snake_list, snake_eat, snake_dead)

    # Then the snake will be updated. The check for snake update like if snake is dead, if snake ate the apple, will be done in the updating_snake function.

    snake_eat, snake_dead, score, apple_pos = collision(
        snake_list, apple_pos, snake_dir, snake_eat, snake_dead, score)
    # After update, if theres no apple or wall collision, then the snake will be moved, also if there is apple collision, then the snake will grow, if there is wall collision, then the snake will die. This checks will be done in the collision function. If the returned apple_pos is empty, then the apple will be generated again, in the apple_generating function. also snake_eat bool will be set to false, so that the snake will move in the updating_snake function.

    # Above code is used to control the snake. If the user presses the right arrow key, then the snake will move right. If the user presses the left arrow key, then the snake will move left. If the user presses the down arrow key, then the snake will move down. If the user presses the up arrow key, then the snake will move up. If the user presses the escape key, then the game will end.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # If the user closes the window, then the game will end.
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # If the user presses the escape key, then the game will end.
                running = False
                break
            if event.key == pygame.K_RIGHT and not snake_dir == 'left':
                # If the user presses the right arrow key, then the snake will move right if the snake is not moving left.
                snake_dir = 'right'
            if event.key == pygame.K_LEFT and not snake_dir == 'right':
                # If the user presses the left arrow key, then the snake will move left if the snake is not moving right.
                snake_dir = 'left'
            if event.key == pygame.K_DOWN and not snake_dir == 'up':
                # If the user presses the down arrow key, then the snake will move down if the snake is not moving up.
                snake_dir = 'down'
            if event.key == pygame.K_UP and not snake_dir == 'down':
                # If the user presses the up arrow key, then the snake will move up if the snake is not moving down.
                snake_dir = 'up'

    # draw background
    display.fill((67, 70, 75))

    # borders: top, bottom, right, left
    pygame.draw.rect(display, 'WHITE', (15, 15, 40 * 15, 1))
    pygame.draw.rect(display, 'WHITE', (15, 31 * 15, 40 * 15, 1))
    pygame.draw.rect(display, 'WHITE', (41 * 15, 15, 1, 30 * 15))
    pygame.draw.rect(display, 'WHITE', (15, 15, 1, 30 * 15))

    # score text
    if snake_dead:
        # This code is used to display the score on the screen.
        img = font.render(str(score), True, (125, 85, 85))
    else:
        img = font.render(str(score), True, (57, 60, 65))
    display.blit(img, img.get_rect(
        center=(20 * 15 + 15, 15 * 15 + 15)).topleft)

    # apple
    if len(apple_pos) > 0:
        pygame.draw.rect(
            display, 'RED', (apple_pos[0] * 15 + 1, apple_pos[1] * 15 + 1, 13, 13))

    # snake body
    for part in snake_list[1:]:
        pygame.draw.rect(display, (180, 180, 180),
                         (part[0] * 15 + 1, part[1] * 15 + 1, 13, 13))
    # snake head
    pygame.draw.rect(
        display, 'WHITE', (snake_list[0][0] * 15 + 1, snake_list[0][1] * 15 + 1, 13, 13))

    pygame.display.update()
    # This code is used to set the frame rate of the game. The clock.tick function will pause the game until the time since the last call to clock.tick is equal to 1/FPS seconds. So, if FPS is 10, then the game will run at 10 frames per second.
    clock.tick(FPS)

    if snake_dead:
        running = False

pygame.quit()