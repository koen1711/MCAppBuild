from .Track import Track
from threading import Thread
from pygame_gui.core import ObjectID
import json
from .AllCars import number_to_class
from .CarSprite import CarSprite
import pygame_gui

class Game:
    def __init__(self, pygame, pygame_gui, all_sprites_list, background, manager, play_btn, window_surface, carnumber):
        self.carnumber = carnumber
        self.window_surface = window_surface
        self.pygame_gui = pygame_gui
        self.pygame = pygame
        self.all_sprites_list = all_sprites_list
        self.background = background
        self.manager = manager
        self.play_btn = play_btn
        self.is_running = True
        self.time = 0
        self.track = None
        self.lapsrequired = 3
        self.laps = 1
        self.laptime = []
        self.bestlap = 0
        self.bestlaptime = 0
        self.player = None
        self.game_ended = False
        self.bg = self.pygame.image.load("background.png")
        self.start_game()
    def start_game(self): 
        x, y = self.window_surface.get_size()
        # get the track required from the data.json 
        with open("Utils/data.json", "r") as f:
            data = json.load(f)
            track = data["cars"][f"{self.carnumber}"]["track"]

        img = self.pygame.transform.scale(self.pygame.image.load(f"Tracks/{track}.png"), (x, y))
        self.bg = img
        self.background.blit(img, (0, 0))
        self.play_btn.kill()
        self.track = Track(self.pygame, self.pygame_gui, self.manager, self.window_surface, self.all_sprites_list, self.background)
        def ThreadedFunction2():
            cla = number_to_class(self.carnumber)
            car = self.pygame.image.load("Cars/car" + str(self.carnumber) + ".png")
            player = CarSprite(car, 440, 532, cla, self.background, self.window_surface, 360)  # color, x, y, width, height // 
            
            self.player = player
            self.all_sprites_list.add(player)
            self.pygame.display.update()
        Thread(target=ThreadedFunction2).start()
        

    def end_game(self):
        
        # destroy all sprites
        for sprite in self.all_sprites_list:
            sprite.kill()
        # destroy all ui elements
        for element in self.manager.get_root_container().elements:
            # except back button and play button
            if element.object_ids != ObjectID("back_btn", "ui") and element.object_ids != ObjectID("play_btn", "ui"):
                element.kill()

        img = self.pygame.image.load("background.png")
        self.background.blit(img, (0, 0))
        play_btn = self.pygame_gui.elements.UIButton(relative_rect=self.pygame.Rect((250, 275), (300, 50)),text='Play',manager=self.manager,
        object_id=ObjectID(class_id='@play_btn',
        object_id='@play_btn'))
        self.player.kill()
        self.pygame.display.update()
        self.game_ended = True
        self.play_btn = play_btn
        self.bg = img
        


        return play_btn
    def respawn(self):
        

        if len(self.track.lap.checkpoints_hit) == 0:
            
            x = self.track.start_finish.rect.center[0]
            y = self.track.start_finish.rect.center[1]
            self.player.reset(x, y, self.track.start_finish.angle)
        else:
            x = self.track.lap.checkpoints_hit[-1].rect.center[0]
            y = self.track.lap.checkpoints_hit[-1].rect.center[1]
            self.player.reset(x, y, self.track.lap.checkpoints_hit[-1].angle)
    def finish(self):
        # make modal with results
        modal = pygame_gui.elements.UIWindow(relative_rect=self.pygame.Rect((250, 275), (300, 50)), manager=self.manager, window_display_title="Results", object_id=ObjectID(class_id='@modal', object_id='@modal'))
        pygame_gui.elements.UILabel(relative_rect=self.pygame.Rect((0, 0), (300, 50)), text=f"Best Lap: {self.bestlaptime}", manager=self.manager, container=modal)
        pygame_gui.elements.UILabel(relative_rect=self.pygame.Rect((0, 50), (300, 50)), text=f"Total Time: {self.time}", manager=self.manager, container=modal)
        pygame_gui.elements.UILabel(relative_rect=self.pygame.Rect((0, 100), (300, 50)), text=f"Laps: {self.laps}", manager=self.manager, container=modal)
        
        # check if the player has gotten the required time to unlock the next car
        with open("Utils/data.json", "r") as f:
            data = json.load(f)
            time_required = data["track"][f"{data['cars'][f'{self.carnumber}']['track']}"]["time_required_to_pass"] / self.player.max_speed
            if self.time < time_required:
                data["cars"][f"{self.carnumber + 1}"]["unlocked"] = True
                with open("Utils/data.json", "w") as f:
                    json.dump(data, f, indent=4)
                # make a text_label to tell the player that they have unlocked the next car
                pygame_gui.elements.UILabel(relative_rect=self.pygame.Rect((0, 150), (300, 50)), text="You have unlocked the next car!", manager=self.manager, container=modal)
            else:
                # make text saying that the player has not unlocked the next car
                pygame_gui.elements.UILabel(relative_rect=self.pygame.Rect((0, 150), (300, 50)), text="You have not unlocked the next car :(", manager=self.manager, container=modal)
        self.manager.get_root_container().elements.append(modal)
        self.pygame.display.update()
        self.game_ended = True

    def handle_event(self, keys):
        pygame = self.pygame
        player = self.player
        if keys[pygame.K_LEFT]:
            player.turn("left")
        if keys[pygame.K_RIGHT]:
            player.turn("right")
        if keys[pygame.K_UP]:
            player.accelerate()
        if keys[pygame.K_DOWN]:
            player.brake()
        if keys[pygame.K_SPACE]:
            player.brake()
        if keys[pygame.K_w]:
            player.accelerate()
        if keys[pygame.K_a]:
            player.turn("left")
        if keys[pygame.K_d]:
            player.turn("right")
        if keys[pygame.K_s]:
            player.brake()
        if keys[pygame.K_ESCAPE]:
            self.play_btn = self.end_game()
            self.is_running = False
        player.check_out_of_bounds(self, self.window_surface)
    def update_time(self, time):
        self.time += time
    def laps_increase(self):
        self.laps += 1
        if self.laps == self.lapsrequired:
            self.finish()
            self.end_game()
        # set best lap
        if self.bestlaptime == 0:
            self.bestlaptime = self.laptime[-1]
            self.bestlap = self.laps
        elif self.laptime[-1] < self.bestlaptime:
            self.bestlaptime = self.laptime[-1]
            self.bestlap = self.laps
    

