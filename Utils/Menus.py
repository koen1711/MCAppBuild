from cgitb import text
import pygame_gui
import pygame
from pygame_gui.core import ObjectID
import json
import time

# ['UIButton', 'UIDropDownMenu', 'UIHorizontalScrollBar', 'UIHorizontalSlider', 'UIImage', 'UILabel', 'UIPanel', 'UIProgressBar', 'UIScreenSpaceHealthBar', 'UIScrollingContainer', 'UISelectionList', 'UIStatusBar', 'UITextBox', 'UITextEntryLine', 'UITooltip', 'UIVerticalScrollBar', 'UIWindow', 'UIWorldSpaceHealthBar', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'ui_button', 'ui_drop_down_menu', 'ui_horizontal_scroll_bar', 'ui_horizontal_slider', 'ui_image', 'ui_label', 'ui_panel', 'ui_progress_bar', 'ui_screen_space_health_bar', 'ui_scrolling_container', 'ui_selection_list', 'ui_status_bar', 'ui_text_box', 'ui_text_entry_line', 'ui_tool_tip', 'ui_vertical_scroll_bar', 'ui_window', 'ui_world_space_health_bar']


class MainMenu:
    def __init__(self, manager, ws):
        self.window_surface = ws
        self.manager = manager
        self.play_btn = None
        self.setup_btns(manager)
    
    def setup_btns(self, manager):
        # width ratio: 800/300 = 2.6666666666666665
        # height ratio: 600/50 = 12
        x, y = self.window_surface.get_size()
        self.play_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x/2 - ((x/2.6666666666666665)/2), y/2 - ((y/12)/2)), ((x/2.6666666666666665, y/12))),text='Play',manager=manager,
        object_id=ObjectID(class_id='@play_btn',
        object_id='@play_btn'))
    def resize(self, btn, x, y, oldwinx, oldwiny):
        rectx = btn.relative_rect.width
        recty = btn.relative_rect.height
        # calculate the new position of the button
        newx = (btn.relative_rect.x / oldwinx) * x
        newy = (btn.relative_rect.y / oldwiny) * y
        # calculate the new size of the button
        newrectx = (rectx / oldwinx) * x
        newrecty = (recty / oldwiny) * y
        # set the new position and size of the button
        btn.set_dimensions((newrectx, newrecty))
        btn.set_position((newx, newy))

class GameUI:
    def __init__(self, manager, ws):
        self.window_surface = ws
        self.manager = manager
        self.reverse_btn = None
        self.engine_status_text = None
        self.lap_counter = None
        self.setup_btns(manager)

    def setup_btns(self, manager):
        # width ratio: 800/100 = 2.6666666666666665
        # height ratio: 600/30 = 20
        # calculate the position of the button

        x, y = self.window_surface.get_size()
        # calculate the size of the button
        rectx = x/8
        recty = y/12

        textrectx = x/4
        textrecty = y/12
        
        lap_counterx = x/2
        lap_countery = y/30

        reverse_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(x/2 - ((x/2.6666666666666665)/2), ((y/30)/2), rectx, recty),text='Reverse',manager=manager,
        object_id=ObjectID(class_id='@reverse_btn',
        object_id='@reverse_btn'))
        engine_status_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(x/1.5 - ((x/2.6666666666666665)/2), ((y/30)/2), textrectx, textrecty),text='Engine Status: Forward',manager=manager,
        object_id=ObjectID(class_id='@engine_status_text',
        object_id='@engine_status_text'))
        self.reverse_btn = reverse_btn
        self.engine_status_text = engine_status_text

        lap_counter = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(x/2 - ((x/0.75)/2), ((y/0.6)/2), lap_counterx, lap_countery),text='Lap: 1/3',manager=manager,
        object_id=ObjectID(class_id='@lap_counter',
        object_id='@lap_counter'))
        self.lap_counter = lap_counter
    def resize(self, btn, x, y, oldwinx, oldwiny):
        rectx = btn.relative_rect.width
        recty = btn.relative_rect.height
        # calculate the new position of the button
        newx = (btn.relative_rect.x / oldwinx) * x
        newy = (btn.relative_rect.y / oldwiny) * y
        # calculate the new size of the button
        newrectx = (rectx / oldwinx) * x
        newrecty = (recty / oldwiny) * y
        # set the new position and size of the button
        btn.set_dimensions((newrectx, newrecty))
        btn.set_position((newx, newy))
    def change_engine_status(self, text):
        self.engine_status_text.set_text(text)
    def update_lap_text(self, text):
        self.lap_counter.set_text(f"Laps: {text}/3")
    def make_time_penalty(self):
        # make a text box that says "Time Penalty" and then disappears after 2 seconds
        # make it fade in and then then fade out
        width, height = self.window_surface.get_size()
        text_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width/2) + (100 / 2), (height/2) + (50 / 2), 100, 50),text='Time Penalty for 10 seconds',manager=self.manager,
        object_id=ObjectID(class_id='@time_penalty',
        object_id='@time_penalty'))
        self.penalty_text = text_label
        text_label.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_IN)

        time.sleep(2)
        text_label.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT)
        text_label.kill()
        text_label = None

class LoadingScreen:
    def __init__(self, manager, ws):
        self.window_surface = ws
        self.manager = manager
        self.uiwindow = None
        self.setup_screen(manager)
    def setup_screen(self, manager):
        uiwindow = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((0, 0), (self.window_surface.get_size())),image_surface=pygame.image.load('loadingscreen.jpg'),manager=manager,
        object_id=ObjectID(class_id='@uiwindow',
        object_id='@uiwindow'))
        self.uiwindow = uiwindow
    def resize(self, btn, x, y, oldwinx, oldwiny):
        if btn.__class__ == pygame_gui.elements.UIWindow:
            rectx = btn.rect.width
            recty = btn.rect.height
            # calculate the new position of the button
            newx = (btn.rect.x / oldwinx) * x
            newy = (btn.rect.y / oldwiny) * y
            # calculate the new size of the button
            newrectx = (rectx / oldwinx) * x
            newrecty = (recty / oldwiny) * y
            # set the new position and size of the button
            pygame_gui.elements.UIWindow.set_dimensions(btn, (newrectx, newrecty))
            pygame_gui.elements.UIWindow.set_position(btn, (newx, newy))

        
        
        
class Time:
    def __init__(self, manager, ws):
        self.window_surface = ws
        self.manager = manager
        self.timer_text = None
        self.time = 0
        self.setup_time(manager)
    def setup_time(self, manager):
        x, y = self.window_surface.get_size()
        time_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x/2 - ((x/2.6666666666666665)/2), y/2 - ((y/12)/2)), ((x/2.6666666666666665, y/12))),text='Time: 0',manager=manager,
        object_id=ObjectID(class_id='@time_text',
        object_id='@time_text'))
        self.timer_text = time_text
    def resize(self, btn, x, y, oldwinx, oldwiny):
        rectx = btn.relative_rect.width
        recty = btn.relative_rect.height
        # calculate the new position of the button
        newx = (btn.relative_rect.x / oldwinx) * x
        newy = (btn.relative_rect.y / oldwiny) * y
        # calculate the new size of the button
        newrectx = (rectx / oldwinx) * x
        newrecty = (recty / oldwiny) * y
        # set the new position and size of the button
        btn.set_dimensions((newrectx, newrecty))
        btn.set_position((newx, newy))
    def change_time(self, time):
        self.time += time
        self.timer_text.set_text(f'Time: {self.time}')


class ChooseCar:
    def __init__(self, manager, ws):
        with open('Utils/data.json') as f:
            self.json = json.load(f)["cars"]
        self.number = 1
        self.window_surface = ws
        self.manager = manager
        self.uiwindow = None
        self.car_chosen = None
        
        self.setup_screen(manager)
    
    def setup_screen(self, manager):
        self.uiwindow = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (self.window_surface.get_size())),manager=manager,
        object_id=ObjectID(class_id='@uiwindow',
        object_id='@uiwindow'))
        
        uiwindow = self.uiwindow
        # make sure uiwindow is not to be clicked away
        uiwindow.is_blocking = True
        # destroy the window close button
        uiwindow.close_window_button = None

        # position the picture in the middle of the uiwindow
        # the buttons under the picture
        self.picture = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((self.window_surface.get_size()[0]/2 - (self.window_surface.get_size()[0]/2.6666666666666665)/2, self.window_surface.get_size()[1]/4 - (self.window_surface.get_size()[1]/2.6666666666666665)/4), (self.window_surface.get_size()[0]/2.6666666666666665, self.window_surface.get_size()[1]/2.6666666666666665)),image_surface=pygame.image.load(f'Cars/Car1.png'),manager=manager,
        
        container=uiwindow)
        
        self.track = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 100), (100, 100)),text=self.json[str(self.number)]["track"],manager=manager,
        container=uiwindow)

        self.number_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (100, 100)),text='1',manager=manager,
        container=uiwindow)

        self.next_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((362.5, 325), (100, 50)),text='Next',manager=manager,
        container=uiwindow, object_id=ObjectID(class_id='@primary_btn', object_id='#primary_btn'))
        
        self.back_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((362.5, 375), (100, 50)),text='Back',manager=manager,
        container=uiwindow, object_id=ObjectID(class_id='@secondary_btn', object_id='#secondary_btn'))
        
        self.select_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((362.5, 425), (100, 50)),text='Select',manager=manager,
        container=uiwindow, object_id=ObjectID(class_id='@primary_btn', object_id='#primary_btn'))
        
        self.disappear()
    
    def resize(self, x, y, oldwinx, oldwiny):
        btn = self.uiwindow
        if btn.__class__ == pygame_gui.elements.UIWindow:
            rectx = btn.rect.width
            recty = btn.rect.height
            # calculate the new position of the button
            newx = (btn.rect.x / oldwinx) * x
            newy = (btn.rect.y / oldwiny) * y
            # calculate the new size of the button
            newrectx = (rectx / oldwinx) * x
            newrecty = (recty / oldwiny) * y
            # set the new position and size of the button
            pygame_gui.elements.UIWindow.set_dimensions(btn, (newrectx, newrecty))
            pygame_gui.elements.UIWindow.set_position(btn, (newx, newy))

            # loop through all the buttons in the window
            for btn in self.manager.elements:
                if btn.container == self.uiwindow:
                    self.resize(btn, x, y, oldwinx, oldwiny)


    def resize_btn(self, btn, x, y, oldwinx, oldwiny):
        rectx = btn.relative_rect.width
        recty = btn.relative_rect.height
        # calculate the new position of the button
        newx = (btn.relative_rect.x / oldwinx) * x
        newy = (btn.relative_rect.y / oldwiny) * y
        # calculate the new size of the button
        newrectx = (rectx / oldwinx) * x
        newrecty = (recty / oldwiny) * y
        # set the new position and size of the button
        btn.set_dimensions((newrectx, newrecty))
        btn.set_position((newx, newy))
    
    def appear(self):
        self.uiwindow.show()
    
    def disappear(self):
        self.uiwindow.hide()
    
    def select_car(self):
        self.car_chosen = self.json[str(self.number)]
    
    def next_car(self):
        self.number += 1
        if self.number > 15:
            self.number = 1
        car = self.json[f"{self.number}"]
        self.picture = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((self.window_surface.get_size()[0]/2 - (self.window_surface.get_size()[0]/2.6666666666666665)/2, self.window_surface.get_size()[1]/4 - (self.window_surface.get_size()[1]/2.6666666666666665)/4), (self.window_surface.get_size()[0]/2.6666666666666665, self.window_surface.get_size()[1]/2.6666666666666665)),image_surface=pygame.image.load(f'Cars/Car{self.number}.png'),manager=self.manager,
        container=self.uiwindow)
        self.track.set_text(car["track"])
        if car["unlocked"] == False:
            self.select_btn.disable()
        else:
            self.select_btn.enable()
        self.number_text.set_text(str(self.number))
    
    def previous_car(self):
        self.number -= 1
        if self.number < 1:
            self.number = 15
        car = self.json[f"{self.number}"]
        self.picture = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((self.window_surface.get_size()[0]/2 - (self.window_surface.get_size()[0]/2.6666666666666665)/2, self.window_surface.get_size()[1]/4 - (self.window_surface.get_size()[1]/2.6666666666666665)/4), (self.window_surface.get_size()[0]/2.6666666666666665, self.window_surface.get_size()[1]/2.6666666666666665)),image_surface=pygame.image.load(f'Cars/Car{self.number}.png'),manager=self.manager,
        container=self.uiwindow)
        self.track.set_text(car["track"])
        if car["unlocked"] == False:
            self.select_btn.disable()
        else:
            self.select_btn.enable()
        self.number_text.set_text(str(self.number))
