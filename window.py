"""
参考资料：
https://blog.csdn.net/qq_17351161/article/details/89286334
"""
# 导入模块
import pygame
from pygame.locals import *
import math
from sys import exit

# 初始化部分
pygame.init()

# 设置游戏窗口
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("My Game Window")
background = pygame.image.load(r"C:\Users\Sam\Documents\School\BJUT\Classes\SmartControl\AutoParking\background_640x480.jpg").convert()

# 坦克精灵类
tank_image = pygame.image.load(r'C:\Users\Sam\Documents\School\BJUT\Classes\SmartControl\AutoParking\tank.png').convert_alpha()
cannon1_image = pygame.image.load(r'C:\Users\Sam\Documents\School\BJUT\Classes\SmartControl\AutoParking\cannon_1.png').convert_alpha()

class FuzzyController():
    def __init__(self):
        self.dest_x,self.dest_y = 320,480
        self.xy_min,self.xy_max = 0.5,0.9
        self.xylow_max,self.xyhigh_min,self.xyhigh_max = 0.7,0.8,1.1
        self.a_min, self.a_max, self.alow_max,self.ahigh_min,self.ahigh_max = 40,80,15,70,90

    def Fxy(self, x, y):
        #坐标系 以终点中心为原点建立直角坐标系
        x = self.dest_x - x
        y = self.dest_y -y
        try:
            tmp = x/y
        except:
            if x == 0:
                tmp = 1
            else:
                tmp = self.xyhigh_max

        print(f"x = {x}, y = {y}, dx/dy = {tmp}")
        if tmp < 0:
            inverse_flag = -1
            tmp = abs(tmp)
        elif tmp >0:
            inverse_flag = 1
        
        if abs(x) < 5:
            inverse_flag = 0
        def fxyl(tmp):
            res = {
                'xylow':0,
                'xymidian':0,
                'xyhigh': 0
            }
            if tmp < self.xylow_max:
                res['xylow'] = tmp / self.xylow_max

            if tmp > self.xy_min and tmp < self.xy_max:
                if tmp >= 1:
                    res['xymidian'] = -(tmp - 1) / (self.xy_max - 1) + 1
                else:
                    res['xymidian'] = (tmp - self.xy_min) / (1 - self.xy_min)

            if tmp > self.xyhigh_max:
                res['xyhigh'] = 1
                #return res
            elif tmp > self.xyhigh_min:
                res['xyhigh'] = (tmp - self.xyhigh_min) / (self.xyhigh_max - self.xyhigh_min) 
            print(res)
            return res

        return inverse_flag, fxyl(tmp)
                
    def fuzzyInference(self, res):
        """
        Rules:
        if xylow, then angle is low
        if xymidian, then angle is midian
        if xyhigh, then angle is high
        Use simplest method here
        """
        a ,b = 0,0
        if res['xylow'] != 0:
            a += res['xylow'] * self.alow_max / 2
            b += res['xylow']

        if res['xymidian'] != 0:
            a += res['xymidian'] * (self.a_max + self.a_min) / 2
            b += res['xymidian']

        if res['xyhigh'] != 0:
            a += res['xyhigh'] * (self.ahigh_max + self.ahigh_min) / 2
            b += res['xyhigh']

        print(f"a = {a}, b = {b}")
            
        return a/b

    def control(self,x,y):
        flag, res = self.Fxy(x,y)
        if flag < 0:
            return -self.fuzzyInference(res)
        elif flag > 0:
            return self.fuzzyInference(res)
        else:
            return 0

            

class HeroTank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.fuzzyController = FuzzyController()
        self.tank_image = tank_image
        self.cannon1_image = cannon1_image
        self.tank_rect = self.tank_image.get_rect()
        self.tank_h,self.tank_w = self.tank_rect.bottom - self.tank_rect.top, self.tank_rect.right - self.tank_rect.left
        self.init_pos = [50,120]
        self.dest_pos = [320,480]
        self.tank_rect.x, self.tank_rect.y = self.init_pos
        self.current_x,self.current_y = self.init_pos
        self.current_angle = 0
        self.controller_angle = 0
        self.cannon1_rect = self.cannon1_image.get_rect()
        self.tank_route = []
        self.tank_route.append([self.current_x, self.current_y])
        self.speed = 1
    
    def update(self):
        self.controller_angle = self.fuzzyController.control(self.current_x + self.tank_w / 2, self.current_y + self.tank_h)
        print(f"Current controller angle = {self.controller_angle}")
        delta_x = self.speed * math.sin(self.current_angle * math.pi / 180)
        delta_y = self.speed * math.cos(self.current_angle * math.pi / 180)
        #print(delta_x, delta_y)

        if (self.current_x + delta_x) > 0 and (self.current_x+ delta_x) < 640:
            # print(round(self.tank_rect.x+delta_x))
            self.current_x += delta_x
            self.tank_rect.x = self.current_x
        
        if (self.current_y + delta_y) > 0 and (self.current_y+ delta_y) < 480:
            # print(round(self.tank_rect.x+delta_x))
            self.current_y += delta_y
            self.tank_rect.y = self.current_y

        self.tank_route.append([self.current_x, self.current_y])

        #print(self.tank_rect)
        #print(self.tank_rect.x)

        self.rotate(self.current_angle)
        self.current_angle = self.controller_angle

    def turnLeft(self):
        self.controller_angle -= 1
    def turnRight(self):
        self.controller_angle += 1

    def rotate(self, angle):
        # 选择机身
        self.tank_image = pygame.transform.rotate(tank_image, angle)
        self.tank_rect = self.tank_image.get_rect(center=self.tank_rect.center)
        # 旋转炮筒
        self.cannon1_image = pygame.transform.rotate(cannon1_image, angle)
        self.cannon1_rect = self.cannon1_image.get_rect(center=self.cannon1_rect.center)

    def display(self, screen):
        screen.blit(self.tank_image, self.tank_rect)
        self.cannon1_rect.center = self.tank_rect.center
        screen.blit(self.cannon1_image, self.cannon1_rect)

    def save_graph(self):
        import cv2
        img = cv2.imread(r"C:\Users\Sam\Documents\School\BJUT\Classes\SmartControl\AutoParking\background_640x480.jpg")
        #print(img.shape)
        for y,x in self.tank_route:
            img = cv2.circle(img, (int(y+self.tank_w/2),int(x+self.tank_h)), 1, (0,0,255), -1 )
        
        cv2.imwrite(r"C:\Users\Sam\Documents\School\BJUT\Classes\SmartControl\AutoParking\result\res3.jpg", img)

my_tank = HeroTank()
framerate = pygame.time.Clock()

cnt = 0
while True:
    framerate.tick(30)
    cnt += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    key_press = pygame.key.get_pressed()
    if key_press[K_w]:
        pass
        #my_tank.moveUp()
    elif key_press[K_s]:
        pass
        #my_tank.moveDown()
    elif key_press[K_a]:
        my_tank.turnLeft()
    elif key_press[K_d]:
        my_tank.turnRight()
    screen.blit(background, (0, 0))
    my_tank.update()
    my_tank.display(screen)
    if cnt > 450:
        my_tank.save_graph()
        break
    pygame.display.update()


