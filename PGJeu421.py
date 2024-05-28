import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1380, 720
DICE_SIZE = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("421 Game")

class Player:
    def __init__(self, color):
        self.score = 0
        self.color = color

    def reset_score(self):
        self.score = 0
        
class Game:
    def __init__(self, player):
        self.player = player
        self.dice_rolled = False

    def check_victory(self):
        return self.player.score >= 100 or sorted(die.value for die in dice) == [1, 2, 4]
    
    def reroll_dice(self):
        for die in dice:
            die.value = random.randint(1, 6)
        self.player.score += sum(die.value for die in dice)
        self.dice_rolled = True
        if self.check_victory():
            global game_over
            game_over = True

    def reroll_sixes(self):
        for die in dice:
            if die.value == 6:
                self.player.score -= 6
                die.value = random.randint(1, 6)
                self.player.score += die.value
        if self.check_victory():
            global game_over
            game_over = True

    
    def reset(self):
        self.player.score = 0
        self.dice_rolled = False
        for die in dice:
            die.value = random.randint(1, 6)
        global game_over
        game_over = False

dice_images = [pygame.image.load(f'dice{i}.png') for i in range(1, 7)]
dice_sound = pygame.mixer.Sound('dice_sound.wav')

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
        self.visible = True

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def was_clicked(self, event):
        if self.visible and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.rect.collidepoint(x, y):
                return True
        return False
    
button = Button(50, 50, 200, 50, "Reroll 6")
reroll_button = Button(300, 50, 200, 50, "Roll Dice")
restart_button = Button(550, 50, 200, 50, "Restart")

player1 = Player((0, 0, 255))
player2 = Player((255, 0, 0))
active_player = player1

game_over = False
running = True
turn_over = False

game = Game(active_player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif button.was_clicked(event):
            if any(die.value == 6 for die in dice):
                game.reroll_sixes()
                dice_sound.play()
            else:
                turn_over = True
        elif reroll_button.was_clicked(event):
            game.reroll_dice()
            dice_sound.play()
            if not any(die.value == 6 for die in dice):
                turn_over = True
        elif restart_button.was_clicked(event):
            game.reset()
            player1.reset_score()
            player2.reset_score()
            active_player = player1
            game = Game(active_player)
            turn_over = False

    if turn_over:
        active_player = player1 if active_player == player2 else player2
        game.player = active_player
        turn_over = False

    screen.fill((255, 255, 255))

    font = pygame.font.Font(None, 64)
    if active_player == player1:
        text = font.render("Player 1's turn", True, (0, 0, 0))
    else:
        text = font.render("Player 2's turn", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 1.3, HEIGHT // 10 - 60))
    
    if game.dice_rolled:
        for die in dice:
            die.draw(screen)

    if game.dice_rolled and any(die.value == 6 for die in dice):
        button.draw(screen)
        button.visible = True
        reroll_button.visible = False
    else:
        reroll_button.draw(screen)
        reroll_button.visible = True
        button.visible = False

    restart_button.draw(screen)

    font = pygame.font.Font(None, 32)
    text = font.render(f"Player 1 Score: {player1.score}", True, player1.color)
    screen.blit(text, (WIDTH // 1.3, HEIGHT // 10))
    text = font.render(f"Player 2 Score: {player2.score}", True, player2.color)
    screen.blit(text, (WIDTH // 1.3, HEIGHT // 10 + 40))

    if game.check_victory():
        game_over = True

    if game_over:
        font = pygame.font.Font(None, 64)
        text = font.render("You win!", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 3, HEIGHT // 4))
        button.visible = False
        reroll_button.visible = False

    pygame.display.flip()

pygame.quit()