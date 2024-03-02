
# import necessary libraries
import pygame
import random

"""
The random module will be used to generate random positions for the food in the game.
"""


# setting up some initial parameters
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20

"""
Here we define the width and height of our game window, both set to 600 pixels. The BLOCK_SIZE is set to 20, which will be the size of our snake and food blocks.
"""

pygame.font.init()
score_font = pygame.font.SysFont("consolas", 20)  # or any other font you'd like
score = 0

"""
We initialise the font module in pygame, which allows us to display text on the game window. We also set up a score_font variable which will be used to display the score. score variable is initialized to 0.


Next, we define some colors using RGB (Red, Green, Blue) tuples. We will use these colors to draw our snake and food:
"""

# color definition
WHITE = (255, 255, 255)
RED = (255, 0, 0)

"""
We initialise Pygame and set up our display window. pygame.display.set_mode() creates a window and returns a Surface object representing the screen. We also create a Clock object which we will use to control the game's frame rate:
"""

# initialise pygame
pygame.init()

# setting up display
win = pygame.display.set_mode((WIDTH, HEIGHT))

# setting up clock
clock = pygame.time.Clock()

"""
We initialise our snake's position to be the centre of the screen. The snake's speed is set to 20 pixels per frame in the y-direction. We also set teleport_walls to True. This will allow the snake to pass through walls and appear on the opposite side of the screen. If False, running through a wall will result in a game over.
"""

# snake and food initialisation
snake_pos = [[WIDTH//2, HEIGHT//2]]
snake_speed = [0, BLOCK_SIZE]

teleport_walls = True  # set this to True to enable wall teleporting

"""
Generating Food
We define a function generate_food() to generate the food's position:
"""

def generate_food():
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        food_pos = [x, y]
        if food_pos not in snake_pos:
            return food_pos

"""
We want the food to appear at a random position within the screen, but not where the snake currently is. So we use a while loop to keep generating a new position until we get one that is not part of the snake. The random.randint() function is used to generate random numbers for the x and y coordinates, which we then multiply by BLOCK_SIZE to ensure that the food aligns with our grid (defined by BLOCK_SIZE).

Now let's call the generate_food() function to set the initial position of the food:
"""

food_pos = generate_food()


#Next, let's make the function for drawing the actual objects:

def draw_objects():
    win.fill((0, 0, 0))
    for pos in snake_pos:
        pygame.draw.rect(win, WHITE, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
    # Render the score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))  # draws the score on the top-left corner

"""
We draw the snake, the food, and the score onto the screen. We first clear the screen by filling it with black using win.fill(). Then we draw each part of the snake as a white square, and the food as a red square, using pygame.draw.rect(). We also create a text Surface for the score using score_font.render(), and draw it onto the screen at position (10, 10) using win.blit().

Now for updating the snake's position:
"""

"""
In update_snake(), we update the position of the snake based on its speed. The new head position is calculated by adding the speed to the current head position. If teleport_walls is True, we check if the new head position is outside of the screen, and if it is, we wrap it to the opposite side.
"""

def update_snake():
    global food_pos, score
    new_head = [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]]
    
    if teleport_walls:
        # if the new head position is outside of the screen, wrap it to the other side
        if new_head[0] >= WIDTH:
            new_head[0] = 0
        elif new_head[0] < 0:
            new_head[0] = WIDTH - BLOCK_SIZE
        if new_head[1] >= HEIGHT:
            new_head[1] = 0
        elif new_head[1] < 0:
            new_head[1] = HEIGHT - BLOCK_SIZE
    if new_head == food_pos:
        food_pos = generate_food() # generate new food
        score += 1  # increment score when food is eaten
    else:
        snake_pos.pop() # remove the last element from the snake
    
        snake_pos.insert(0, new_head) # add the new head to the snake

"""
We then check if the new head position is at the food position. If it is, we generate a new food position and increment the score. Otherwise, we remove the last element of the snake to maintain its length. Finally, we add the new head to the snake.

Let's now handle how the game ends:
"""

def game_over():
    # game over when snake hits the boundaries or runs into itself
    if teleport_walls:
        return snake_pos[0] in snake_pos[1:]
    else:
        return snake_pos[0] in snake_pos[1:] or \
            snake_pos[0][0] > WIDTH - BLOCK_SIZE or \
            snake_pos[0][0] < 0 or \
            snake_pos[0][1] > HEIGHT - BLOCK_SIZE or \
            snake_pos[0][1] < 0

"""
The game_over() function checks the conditions for the game to be over. If teleport_walls is True, the game ends only if the snake runs into itself. Otherwise, the game also ends if the snake hits the boundaries.

Game over screen
"""
"""
In game_over_screen(), we display a game over message along with the final score. We first clear the screen, then we create a new font for the game over message and a text Surface with the message. We then draw the text onto the center of the screen and update the display.
"""
def game_over_screen():
    global score
    win.fill((0, 0, 0))
    game_over_font = pygame.font.SysFont("consolas", 50)
    game_over_text = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()  # replay the game
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()  # quit the game
                    return

"""
The rest of game_over_screen() is a loop that waits for the player to press a key. If the player presses 'r', the game is restarted. If the player presses 'q' or closes the window, the game quits.

Let's handle user input and make the main game loop:
"""
"""
The run() function is the main game loop. We first reset the game state by initializing the snake position, snake speed, food position, and score. Then we enter a loop that runs as long as the game is running.

Inside the loop, we handle events. If the window is closed, we set running to False to end the game. We also check if any keys are pressed:
"""
"""
In this section, we handle the arrow key presses to control the snake's movement. If the up arrow key is pressed and the snake is moving down, we ignore the key press. We do similar checks and updates for the other three directions. This setup ensures that the snake can't instantly turn 180 degrees.
"""

def run():
    global snake_speed, snake_pos, food_pos, score
    snake_pos = [[WIDTH//2, HEIGHT//2]]
    snake_speed = [0, BLOCK_SIZE]
    food_pos = generate_food()
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_UP]:
                    # when UP is pressed but the snake is moving down, ignore the input
                    if snake_speed[1] == BLOCK_SIZE:
                        continue
                    snake_speed = [0, -BLOCK_SIZE]
                if keys[pygame.K_DOWN]:
                    # when DOWN is pressed but the snake is moving up, ignore the input
                    if snake_speed[1] == -BLOCK_SIZE:
                        continue
                    snake_speed = [0, BLOCK_SIZE]
                if keys[pygame.K_LEFT]:
                    # when LEFT is pressed but the snake is moving right, ignore the input
                    if snake_speed[0] == BLOCK_SIZE:
                        continue
                    snake_speed = [-BLOCK_SIZE, 0]
                if keys[pygame.K_RIGHT]:
                    # when RIGHT is pressed but the snake is moving left, ignore the input
                    if snake_speed[0] == -BLOCK_SIZE:
                        continue
                    snake_speed = [BLOCK_SIZE,0]
        if game_over():
            game_over_screen()
            return
        update_snake()
        draw_objects()
        pygame.display.update()
        clock.tick(15)  # limit the frame rate to 15 FPS

"""
After handling the events, we check if the game is over. If it is, we display the game over screen and exit the function. If it's not, we update the snake's position, draw the objects onto the screen, and update the display. We then delay the loop to limit the frame rate to 15 frames per second using clock.tick().

Finally, we call run() to start the game:
"""

if __name__ == '__main__':
    run()
