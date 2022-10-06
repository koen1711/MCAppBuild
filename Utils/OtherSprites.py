import pygame


class Start_Finish(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, screen, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        
        self.angle = angle
        self.image = pygame.image.load("start.png")
        self.image = pygame.transform.rotozoom(self.image, angle, 0.5)
        self.image = pygame.transform.scale(self.image, (x/10, y/18))
        # 416/800
        # 536/600

        # calculate the position with the calculations 416/800 and 536/600

        #newx = (btn.relative_rect.x / oldwinx) * x
        #newy = (btn.relative_rect.y / oldwiny) * y

        newx = (x / 800) * width
        newy = (y / 600) * height
        self.rect = self.image.get_rect()

        # scale the image\
        

        self.rect.x = newx
        self.rect.y = newy

        self.start_mask = pygame.mask.from_surface(self.image)

        self.draw(screen)


        self.start_mask = pygame.mask.from_threshold(self.image,(255,255,255),(1,1,1))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def resize(self, x, y, curwindowx, curwindowy):
        self.image = pygame.transform.scale(self.image, (x/10, y/18))
        newx = (self.rect.x / curwindowx) * x
        newy = (self.rect.y / curwindowy) * y
        self.rect.center = (newx, newy)
        self.rect.x = newx
        self.rect.y = newy

        # calculate the size of the image


        self.start_mask = pygame.mask.from_surface(self.image)
    
class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, x2, y2, angle, sur):
        self.sur = sur
        self.angle = angle
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

        self.image = None
        self.image = pygame.image.load("checkpoint.png")
        self.image = pygame.transform.rotozoom(self.image, self.angle, 0.5)
        surx, sury = sur.get_size()

        # calculate the position with the calculations 416/800 and 536/600

        x = (x / 800) * surx
        y = (y / 600) * sury
        x2 = (x2 / 800) * surx
        y2 = (y2 / 600) * sury

        # calculate the size that is between x and x2 and y and y2
        right_numberx = x2 - x
        right_numbery = y2 - y
        right_numbery = abs(right_numbery)
        right_numberx = abs(right_numberx)
            
        self.image = pygame.transform.scale(self.image, (right_numberx, right_numbery))
        # 416/800
        # 536/600

        # calculate the position with the calculations 416/800 and 536/600

        #newx = (btn.relative_rect.x / oldwinx) * x
        #newy = (btn.relative_rect.y / oldwiny) * y

        
        self.rect = self.image.get_rect()

        # scale the image
        
        # calculate the position of the image
        self.rect.x = x
        self.rect.y = y

        self.start_mask = pygame.mask.from_surface(self.image)

        self.start_mask = pygame.mask.from_threshold(self.image,(255,255,255),(1,1,1))
    def resize(self):
        surx, sury = self.sur.get_size()

        x = self.x
        y = self.y
        x2 = self.x2
        y2 = self.y2

        x = (x / 800) * surx
        y = (y / 600) * sury
        x2 = (x2 / 800) * surx
        y2 = (y2 / 600) * sury

        right_numberx = abs(x2 - x)
        right_numbery = abs(y2 - y)

        # calculate the size of the image

        self.image = pygame.transform.scale(self.image, (right_numberx, right_numbery))
        self.rect.x = x
        self.rect.y = y

        self.start_mask = pygame.mask.from_surface(self.image)

        #self.x = x
        #self.y = y
        #self.x2 = x2
        #self.y2 = y2


class HiglightedCheckpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, x2, y2, angle, sur):
        self.sur = sur
        self.angle = angle
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

        self.image = None
        self.image = pygame.image.load("hcheckpoint.png")
        self.image = pygame.transform.rotozoom(self.image, angle, 0.5)
        self.image = pygame.transform.rotozoom(self.image, 90, 0.5)
        surx, sury = sur.get_size()

        # calculate the position with the calculations 416/800 and 536/600

        x = (x / 800) * surx
        y = (y / 600) * sury
        x2 = (x2 / 800) * surx
        y2 = (y2 / 600) * sury

        # calculate the size that is between x and x2 and y and y2
        right_numberx = x2 - x
        right_numbery = y2 - y
        right_numbery = abs(right_numbery)
        right_numberx = abs(right_numberx)
            
        self.image = pygame.transform.scale(self.image, (right_numberx, right_numbery))
        # 416/800
        # 536/600

        # calculate the position with the calculations 416/800 and 536/600

        #newx = (btn.relative_rect.x / oldwinx) * x
        #newy = (btn.relative_rect.y / oldwiny) * y

        
        self.rect = self.image.get_rect()

        # scale the image
        
        # calculate the position of the image
        self.rect.x = x
        self.rect.y = y

        self.start_mask = pygame.mask.from_surface(self.image)

        self.start_mask = pygame.mask.from_threshold(self.image,(255,255,255),(1,1,1))
    def resize(self):
        surx, sury = self.sur.get_size()

        x = self.x
        y = self.y
        x2 = self.x2
        y2 = self.y2

        x = (x / 800) * surx
        y = (y / 600) * sury
        x2 = (x2 / 800) * surx
        y2 = (y2 / 600) * sury

        right_numberx = abs(x2 - x)
        right_numbery = abs(y2 - y)

        # calculate the size of the image

        self.image = pygame.transform.scale(self.image, (right_numberx, right_numbery))
        self.rect.x = x
        self.rect.y = y

        self.start_mask = pygame.mask.from_surface(self.image)

        #self.x = x
        #self.y = y
        #self.x2 = x2
        #self.y2 = y2
