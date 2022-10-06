from .OtherSprites import *

class Track:
    def __init__(self, pygame, pygame_gui, manager, sur, all_sprites_list, bg):
        # draw checpoints on the track
        self.pygame = pygame
        self.pygame_gui = pygame_gui
        self.manager = manager
        self.all_sprites_list = all_sprites_list
        self.background = bg
        self.sur = sur

        self.start_finish = get_start_finish(1, self.sur)
        
        # register the start/finish line
        self.all_sprites_list.add(self.start_finish)
        self.all_sprites_list.update()
        self.checkpoints = get_checkpoints(1, sur)

        self.lap = Lap(self.checkpoints, all_sprites_list, sur)

        self.lap.draw()

    def resize(self, sur, x, y, oldwinx, oldwiny):
        for checkpoint in self.checkpoints:
            checkpoint.resize()
            self.all_sprites_list.add(checkpoint)
            self.all_sprites_list.update()
        self.start_finish.resize(x, y, oldwinx, oldwiny)



class Lap:
    def __init__(self, checkpoints, all_sprites_list, sur):
        self.sur = sur
        self.all_sprites_list = all_sprites_list
        self.time = 0
        self.lap = False
        self.checkpoints_unhit = checkpoints
        self.checkpoints_hit = []
    def check_if_hit_checkpoint(self, car):
        try:
            checkpoint = self.checkpoints_unhit[0]
            # if the car is in the checkpoint
            if checkpoint.rect.colliderect(car.rect):
                if checkpoint not in self.checkpoints_hit:
                    # add the checkpoint to the hit checkpoints
                                    

                    self.all_sprites_list.remove(checkpoint)
                    self.checkpoints_hit.append(checkpoint)
                    # remove the checkpoint from the unhit checkpoints
                    
                    self.checkpoints_unhit.remove(checkpoint)
                    

                    
                    # check if all checkpoints are hit
                    if len(self.checkpoints_unhit) == 0:
                        self.lap = True
                    else:
                        self.all_sprites_list.remove(self.checkpoints_unhit[0])
                        self.checkpoints_unhit[0] = HiglightedCheckpoint(self.checkpoints_unhit[0].x, self.checkpoints_unhit[0].y, self.checkpoints_unhit[0].x2, self.checkpoints_unhit[0].y2, self.checkpoints_unhit[0].angle, self.checkpoints_unhit[0].sur)
                        self.all_sprites_list.add(self.checkpoints_unhit[0])
                        self.all_sprites_list.update()
                    
            self.all_sprites_list.update()
        except:
            pass
    
    def draw(self):
        # draw the checkpoints
        self.checkpoints_unhit = get_checkpoints(1, self.sur)

        for checkpoint in self.checkpoints_unhit:
            self.all_sprites_list.add(checkpoint)
        self.checkpoints_hit = []
        self.all_sprites_list.update()

                        


# (21, 179)
# (59, 216)
# (167, 73)
# (125, 99)
# (588, 7)
# (544, 40)
# (674, 396)
# (628, 335)

def get_checkpoints(num, sur):
    return {
        1: [HiglightedCheckpoint(21, 179, 59, 216, 0, sur), Checkpoint(167, 73, 125, 99, 0, sur), Checkpoint(588, 7, 544, 40, 0, sur), Checkpoint(628, 335, 674, 396, 0, sur)],
    }[num]

def get_start_finish(num, sur):
    return {
        1: Start_Finish(434, 525, sur.get_width(), sur.get_height(), sur, 180),
    }[num]