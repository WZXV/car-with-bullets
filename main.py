import math
import random
import pygame

pygame.init()


WINDOW = pygame.display.set_mode((1920, 1080))

clock = pygame.time.Clock()
FPS = 60

black = (0, 0, 0)
white = (255, 255, 255)

#create bullet group
bullet_group = pygame.sprite.Group()


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, image, height, width):
        super().__init__()
        self.x = x - width / 2
        self.y = y - height / 2
        self.image = pygame.transform.scale(image, (height, width))
        self.height = height
        self.width = width

        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((height, width), pygame.SRCALPHA, 32)
        self.surface.blit(self.image, (0, 0))

        # movment
        self.angle = 0
        self.speed = 0 # to change angle

    def draw(self):
        global WINDOW

        self.rect.topleft = (int(self.x), int(self.y))
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface_rect = self.surface.get_rect(topleft=self.rect.topleft)
        new_rect = rotated.get_rect(center=surface_rect.center)
        WINDOW.blit(rotated, new_rect.topleft)

    def shoot(self):
        return Bullet(self.rect.center[0], self.rect.center[1])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 10
        self.image = pygame.transform.scale(pygame.image.load("images/bullet.png").convert_alpha(), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 2

        if self.rect.y <= -WINDOW.get_height() + 1100:
            self.kill()





car = Car(800, 800, pygame.image.load("images/lamborghini.png").convert_alpha(), 60, 120)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(bullet_group) >= 3:
                    pass
                else:
                 bullet_group.add(car.shoot())

    WINDOW.fill(black)
    pygame.draw.line(WINDOW, (0, 255, 0), (0, 540), (1920, 540))

    car.draw()

    #update bullet
    bullet_group.update()
    bullet_group.draw(WINDOW)


    pressed = pygame.key.get_pressed()
    car.speed *= 0.9
    if pressed[pygame.K_s]: car.speed += 0.5
    if pressed[pygame.K_w]: car.speed -= 0.5

    if pressed[pygame.K_d]: car.angle += car.speed / 2
    if pressed[pygame.K_a]: car.angle -= car.speed / 2  # 7
    if car.x < 0:
        car.x = 0
    elif car.x > 1920:
        car.x = 1920
    else:
        car.x -= car.speed * math.sin(math.radians(car.angle))  # 8
    if car.y < 540:
        car.y = 540
    elif car.y > 950:
        car.y = 950
    else:
        car.y -= car.speed * math.cos(math.radians(-car.angle))  # 8

    bullet_group.draw(WINDOW)


    clock.tick(FPS)
    pygame.display.flip()