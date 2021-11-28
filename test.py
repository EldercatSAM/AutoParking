import pygame

from pygame.locals import *

from sys import exit
 
pygame.init()

# 设置游戏窗口
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("My Game Window")
#background = pygame.image.load("background.jpg").convert()

# 坦克精灵类
tank_image = pygame.image.load(r'C:\Users\Sam\Documents\School\BJUT\Classes\智能控制\倒车入库\image\car.png').convert_alpha()		#使用convert_alpha()保留透明信息，而不是convert()

class HeroTank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tank_image = tank_image
        self.tank_rect = self.tank_image.get_rect()

    def display(self,screen):
        screen.blit(self.tank_image, self.tank_rect)

my_tank = HeroTank()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    #screen.blit(background, (0, 0))
    my_tank.display(screen)
    pygame.display.update()