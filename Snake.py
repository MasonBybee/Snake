import pygame
from sys import exit
from random import randint

# Game Board by https://github.com/MasonBybee
# Snake assets by: https://www.youtube.com/@ClearCode

pygame.init()
game_active = False


def draw_border():
    sides = ["left", "right", "top", "down"]
    for side in sides:
        border_group.add(Border(side))


class Snake(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "head":
            self.original_image = pygame.image.load("graphics/head.png").convert_alpha()
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(topleft=(400, 400))
            self.length = 3
        if type == "body":
            self.original_image = pygame.image.load("graphics/body.png").convert_alpha()
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(topleft=(400, 440))
        if type == "tail":
            self.original_image = pygame.image.load("graphics/tail.png").convert_alpha()
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(topleft=(400, 480))
        self.type = type
        self.facing = "up"
        self.new_facing = "up"
        self.speed = 4
        self.turn_buffer = 5
        self.static = False

    def add_length(self):
        if self.type == "head":
            if len(snake) < self.length:
                snake = [body for body in snake]
                new_snake = Snake("body")
                snake.insert(-2, new_snake)

    def can_turn(self):
        if self.facing in ["left", "right"]:
            return self.rect.y % 40 <= self.turn_buffer
        else:
            return self.rect.x % 40 <= self.turn_buffer

    def player_input(self):
        global game_active
        game_active = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.facing != "right":
            self.new_facing = "left"
        if keys[pygame.K_RIGHT] and self.facing != "left":
            self.new_facing = "right"
        if keys[pygame.K_UP] and self.facing != "down":
            self.new_facing = "up"
        if keys[pygame.K_DOWN] and self.facing != "up":
            self.new_facing = "down"

    def turn_snake(self):
        if self.facing != self.new_facing and self.can_turn():
            self.facing = self.new_facing
            if self.facing == "left":
                self.image = pygame.transform.rotate(self.original_image, 90)
                self.rect.y = round(self.rect.y / 40) * 40
                self.rect.x = self.rect.x - 15
            elif self.facing == "right":
                self.image = pygame.transform.rotate(self.original_image, -90)
                self.rect.y = round(self.rect.y / 40) * 40
                self.rect.x = self.rect.x + 15
            elif self.facing == "up":
                self.image = pygame.transform.rotate(self.original_image, 0)
                self.rect.x = round(self.rect.x / 40) * 40
                self.rect.y = self.rect.y - 15
            elif self.facing == "down":
                self.image = pygame.transform.rotate(self.original_image, 180)
                self.rect.x = round(self.rect.x / 40) * 40
                self.rect.y = self.rect.y + 15

    def follow_leader(self):
        index = snake.sprites().index(self)
        prev_snake = snake.sprites()[index - 1]
        if self.facing != prev_snake.facing:
            self.original_image = pygame.image.load("graphics/body_corner.png")
            self.image = self.original_image.copy()
            self.static = True
            if (self.facing == "right" and prev_snake.facing == "up") or (
                self.facing == "up" and prev_snake.facing == "right"
            ):
                self.image = pygame.transform.rotate(self.original_image, 90)
            if (self.facing == "right" and prev_snake.facing == "down") or (
                self.facing == "down" and prev_snake.facing == "right"
            ):
                self.image = pygame.transform.rotate(self.original_image, 180)
            if (self.facing == "left" and prev_snake.facing == "up") or (
                self.facing == "up" and prev_snake.facing == "left"
            ):
                self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.type != "tail":
            self.original_image = pygame.image.load("graphics/body.png")
            self.image = self.original_image.copy()
            if self.new_facing == "left" or self.facing == "right":
                self.image = pygame.transform.rotate(self.original_image, 90)
                if self.new_facing == "right":
                    self.rect.topright = prev_snake.rect.topleft
                else:
                    self.rect.topleft = prev_snake.rect.topright
            elif self.new_facing == "up":
                self.rect.topleft = prev_snake.rect.bottomleft
            elif self.new_facing == "down":
                self.rect.bottomleft = prev_snake.rect.topleft
            self.facing = self.new_facing

        else:
            if self.new_facing == "left":
                self.image = pygame.transform.rotate(self.original_image, 90)
                self.rect.topleft = prev_snake.rect.topright
            elif self.new_facing == "right":
                self.image = pygame.transform.rotate(self.original_image, -90)
                self.rect.topright = prev_snake.rect.topleft
            elif self.new_facing == "up":
                self.image = pygame.transform.rotate(self.original_image, 0)
                self.rect.topleft = prev_snake.rect.bottomleft
            elif self.new_facing == "down":
                self.image = pygame.transform.rotate(self.original_image, 180)
                self.rect.bottomleft = prev_snake.rect.topleft
            self.facing = self.new_facing

    def move_snake(self):
        if game_active == True:
            if self.facing == "left":
                self.rect.x -= self.speed
            elif self.facing == "right":
                self.rect.x += self.speed
            elif self.facing == "up":
                self.rect.y -= self.speed
            elif self.facing == "down":
                self.rect.y += self.speed

    def update(self):
        if self.type == "head":
            self.player_input()
        else:
            self.follow_leader()
        self.turn_snake()
        # self.move_snake()
        # self.test_movement()


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()


class Border(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.original_image = pygame.image.load("graphics/border.png").convert()
        self.image = self.original_image.copy()
        if side == "left" or side == "top":
            if side == "left":
                self.image = pygame.transform.rotate(self.original_image, 90)
            x_pos = 0
            y_pos = 0
        elif side == "down":
            x_pos = 0
            y_pos = 760
        elif side == "right":
            self.image = pygame.transform.rotate(self.original_image, 90)
            x_pos = 760
            y_pos = 0
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))


screen = pygame.display.set_mode((840, 840))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# create board
checkerboard_surf = pygame.image.load("graphics/checkerboard.png")
checkerboard_rect = checkerboard_surf.get_rect(topright=(40, 40))
border_group = pygame.sprite.Group()
draw_border()

# create snake
snake = pygame.sprite.Group()
for body_part in ["head", "body", "tail"]:
    snake.add(Snake(body_part))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(checkerboard_surf, (80, 80))
    snake.draw(screen)
    snake.update()
    border_group.draw(screen)
    border_group.update()
    pygame.display.flip()
    clock.tick(60)
