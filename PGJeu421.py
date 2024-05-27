import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1380, 720  # Change these values to your desired window size
DICE_SIZE = 50

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Game:

    def check_victory(self):
        return sorted(die.value for die in dice) == [1, 2, 4]
    
# Load the dice images
dice_images = [pygame.image.load(f'dice{i}.png') for i in range(1, 7)]

class Dice:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = random.randint(1, 6)

    def draw(self, screen):
        screen.blit(dice_images[self.value - 1], (self.x, self.y))

# Create the dice
dice = [Dice(50 + i * (DICE_SIZE + 300), HEIGHT // 2) for i in range(3)]
#dice[0].value = 1
#dice[1].value = 4
#dice[2].value = 2
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, self.rect.move(10, 10))

    def was_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
button = Button(50, 50, 200, 50, "Reroll 6s")

game_over = False
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif button.was_clicked(event):
            for die in dice:
                if die.value == 6:
                    die.value = random.randint(1, 6)

    screen.fill((255, 255, 255))

    for die in dice:
        die.draw(screen)

    if any(die.value == 6 for die in dice):
        button.draw(screen)

    game = Game()
    if game.check_victory():
        game_over = True

    if game_over:
        font = pygame.font.Font(None, 64)
        text = font.render("You win!", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 10, HEIGHT // 10))
        
    pygame.display.flip()


pygame.quit()