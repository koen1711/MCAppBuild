import math
import pygame
import time

class CarSprite( pygame.sprite.Sprite ):
    """ Car Sprite with basic acceleration, turning, braking and reverse """

    def __init__( self, car_image, x, y, cla, background, ws, rotations=360 ):
        """ A car Sprite which pre-rotates up to <rotations> lots of
            angled versions of the image.  Depending on the sprite's
            heading-direction, the correctly angled image is chosen.
            The base car-image should be pointing North/Up.          """
        pygame.sprite.Sprite.__init__(self)
        # Pre-make all the rotated versions
        # This assumes the start-image is pointing up-screen
        # Operation must be done in degrees (not radians)
        self.rot_img   = []
        self.min_angle = ( 360 / rotations ) 
        x2, y2 = ws.get_size()
        x2 = x2 / 40
        y2 = y2 / 40
        for i in range( rotations ):
            # This rotation has to match the angle in radians later
            # So offet the angle (0 degrees = "north") by 90° to be angled 0-radians (so 0 rad is "east")
            
            rotated_image  = pygame.transform.scale(car_image, (x2, y2))
            rotated_image = pygame.transform.rotozoom( rotated_image, 360-90-( i*self.min_angle ), 1 )
            # Scale is 800/40 and 600/40 = 20 and 15
            
            self.rot_img.append( rotated_image )
        self.min_angle = math.radians( self.min_angle )   # don't need degrees anymore
        # define the image used
        self.image       = self.rot_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = ( x, y )
        # movement
        self.reversing = False
        self.heading   = 0                           # pointing right (in radians)
        self.speed     = 0    
        self.velocity  = pygame.math.Vector2( 0, 0 )
        self.position  = pygame.math.Vector2( x, y )
        self.OutOfTrack = False
        self.timer = 0
        self.scar = cla("Car")
        
        self.mask = pygame.mask.from_threshold(background,(1,1,1, 255),(0,0,0,255))
        # make another mask for the color: (14, 209, 69, 255)
        self.mask2 = pygame.mask.from_threshold(background,(14,209,69, 255),(0,0,0,255))
        
        self.basic_turn()

    def basic_turn(self, angle_degrees=180):
        """ Turn the car around when game initiated """	
        self.heading = math.radians( angle_degrees ) 
        # Decide which is the correct image to display
        image_index = int( self.heading / self.min_angle ) % len( self.rot_img )
        # Only update the image if it's changed
        if ( self.image != self.rot_img[ image_index ] ):
            x,y = self.rect.center
            self.image = self.rot_img[ image_index ]
            self.rect  = self.image.get_rect()
            self.rect.center = (x,y)

    def turn( self, direction ):
        """ Adjust the angle the car is heading, if this means using a 
            different car-image, select that here too """
        angle_degrees = 1
        if ( direction == "left" ):
            angle_degrees = -self.scar.turn_speed
        else:
            angle_degrees = self.scar.turn_speed
        if not self.speed == 0:
            self.heading += math.radians( angle_degrees ) 
            # Decide which is the correct image to display
            image_index = int( self.heading / self.min_angle ) % len( self.rot_img )
            # Only update the image if it's changed
            if ( self.image != self.rot_img[ image_index ] ):
                x,y = self.rect.center
                self.image = self.rot_img[ image_index ]
                self.rect  = self.image.get_rect()
                self.rect.center = (x,y)

    def accelerate( self ):
        """ Increase the speed either forward or reverse """
        if ( not self.reversing ):
            self.speed += self.scar.max_speed / 100
        else: 
            self.speed -= self.scar.max_speed / 100

    def brake( self ):
        """ Slow the car by half """
        speed = self.speed - (self.scar.max_speed / 50)
        if self.reversing:
            if ( abs( speed ) < 0.01 ):
                self.speed = 0
            else:
                self.speed += self.scar.max_speed / 50
        else:
            if ( speed < 0.01 ):
                self.speed = 0
            else:
                self.speed -= self.scar.max_speed / 50


    def reverse( self ):
        """ Change forward/reverse, reset any speed to 0 """
        if self.speed == 0:
            self.speed = 0
            self.reversing = not self.reversing
        else:
            self.brake()

    def update( self ):
        """ Sprite update function, calcualtes any new position """
        self.velocity.from_polar( ( self.speed, math.degrees( self.heading ) ) )
        self.position += self.velocity
        self.rect.center = ( round(self.position[0]), round(self.position[1] ) )

    def check_out_of_bounds(self, game, pg):
        if self.rect.x < 0:
            game.respawn()
        if self.rect.x > pg.get_width():
            game.respawn()
        if self.rect.y < 0:
            game.respawn()
        if self.rect.y > pg.get_height():
            game.respawn()
    def resize(self, x, y, curwindowx, curwindowy):
        for i in range(len(self.rot_img)):
            self.rot_img[i] = pygame.transform.scale(self.rot_img[i], (x/60, y/60))
        self.image = self.rot_img[0]
        self.rect = self.image.get_rect()
        # calculate the new position
        
        newx = (self.position[0] / curwindowx) * x
        newy = (self.position[1] / curwindowy) * y
        self.rect.center = (newx, newy)
        self.rect.x = newx
        self.rect.y = newy
        self.position = pygame.math.Vector2(newx, newy)
        # set new scaled positioin
    
    def check_hit_finish(self, finish):
        if self.rect.colliderect(finish):
            return True
        else:
            return False
    def reset(self, x, y, angle):
        self.rect.center = (x, y)
        self.position = pygame.math.Vector2(x, y)
        self.rect.x = x
        self.rect.y = y
        self.speed = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.heading = 0
        self.basic_turn(angle)
        self.update()

    def out_of_track(self, game):
        
        if self.OutOfTrack == False:
            # start the timer
            self.OutOfTrack = True
            self.timer = time.time()
        # check if the timer is over 3 seconds, if so respawn
        
        if time.time() - self.timer > 3:
            game.respawn()
            self.OutOfTrack = False
    def return_to_track(self):
        if self.timer != 0:
            self.OutOfTrack = False
            delta = time.time() - self.timer
            self.timer = 0
            return delta
        else:
            return 0
        


        