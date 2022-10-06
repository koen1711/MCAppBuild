from .Menus import *
from .GameClass import * 
import pygame


class Handler:
    def __init__(self,cc):
        self.hit_last_time = False
        self.cc = cc
    def EventHandler(self, pygame_gui, event, curgame, play_btn, back_btn, reverse_btn, text, gameui, loading_screen, x, y, window_surface, background, manager, all_sprites_list, is_running, mm):
        cc = self.cc
        if event.type == pygame.QUIT:
                is_running = False
            

        # if play_btn is clicked, then start the game
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_btn:
                loading_screen = LoadingScreen(manager, window_surface)
                cc.appear()
                
                
            
            if event.ui_element == cc.back_btn:
                cc.previous_car()

            elif event.ui_element == cc.next_btn:
                cc.next_car()
            
            elif event.ui_element == cc.select_btn:
                cc.select_car()
                cc.disappear()
            
            elif event.ui_element == back_btn:
                play_btn = curgame.end_game()
                curgame = None
                background = pygame.transform.scale(pygame.image.load("background.png"), (x, y))
                play_btn.kill()
                mm.play_btn.kill()
                mm = MainMenu(manager, window_surface)
                play_btn = mm.play_btn
                reverse_btn.kill()
                text.kill()
                gameui.engine_status_text.kill()
                gameui.reverse_btn.kill()
                gameui = None
                text = None
                reverse_btn = None
            elif event.ui_element == reverse_btn:
                if gameui is not None:
                    curgame.player.reverse()
                    if curgame.player.reversing:
                        text = gameui.change_engine_status("Engine Status: Reversing")
                        reverse_btn = gameui.reverse_btn
                        text = gameui.engine_status_text
                    else:

                        text = gameui.change_engine_status("Engine Status: Forward")
                        reverse_btn = gameui.reverse_btn
                        text = gameui.engine_status_text

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                print(pygame.mouse.get_pos())
                # get the color of the pixel at the mouse position and print it in rgb values and hex
                print(window_surface.get_at(pygame.mouse.get_pos()))
                print(background.get_at(pygame.mouse.get_pos()))

            
                
        if curgame is not None:
            if curgame.player is not None:
                v = curgame.player.check_hit_finish(curgame.track.start_finish)
                if v == True:
                    if self.hit_last_time == False:
                        if curgame.track.lap.lap == True:
                            curgame.track.lap.lap = False
                            curgame.track.lap.draw()

                            curgame.laps_increase()
                            self.hit_last_time = True
                else:
                    self.hit_last_time = False
                gameui.update_lap_text(curgame.laps)
        manager.process_events(event)
        

        return curgame, play_btn, back_btn, reverse_btn, text, gameui, loading_screen, background, manager, all_sprites_list, is_running, mm
    def BaseUpdates(self, manager, time_delta, all_sprites_list, window_surface, curgame):
        manager.update(time_delta)
        all_sprites_list.update()
        all_sprites_list.draw(window_surface)
        if curgame is not None and curgame.player is not None:
            if curgame.track is not None:
                curgame.track.lap.check_if_hit_checkpoint(curgame.player)
        return manager, all_sprites_list, window_surface