'''Checks how many points the use can tile within the screen
give a certain time. 

In progress...
> Managed to get reset function in place
> Now need to get the reset button to trigger the reset 
    > User's clicking on the button shouldn't cause a dot to appear!

FEATURE LIST:
    1. Add a reset button which bring the user to a fresh start
    2. 


TODO:
    1. The safe zone's circle and the center used for calculations don't seem 
    to be the same. Check on this. 
    2. The calculation of CG-to-touch point seems to somehow be asymmetric -  check this out. 

'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ReferenceListProperty, NumericProperty
from kivy.graphics import Ellipse, Color, InstructionGroup
import random
import copy

from calculate import  euclidean_distance

class TargetCircle(Widget):
    circle_center=[0,0]

class CenterDot(Widget):
    pass

class TileGame(Widget):

    safe_zone_location = [0,0]
    
    mean_point_distance = 0
    status = StringProperty('')
    cg_x = NumericProperty(0)
    cg_y = NumericProperty(0)
    centre_gravity = ReferenceListProperty(cg_x,cg_y)
    touch_number = 0
    cg_dot_size = 20
    
    cg_xy = []
    
    safezone_r = 30
    
    lives_left = NumericProperty(5)
    num_points = StringProperty('0')

    one_dot = []
    all_dots = []
        
    def on_touch_down(self, touch):
        self.choose_random_color()
        self.touch_number += 1 
        
        if self.status != 'Level fail..restart app':
            d = 30.
            self.one_dot = InstructionGroup()
            self.one_dot.add(Color(*self.value_range))
            self.one_dot.add(Ellipse(pos=(touch.x - d / 2, touch.y - d / 2),
                                     size=(d, d)))
            
            self.canvas.add(self.one_dot)
            self.all_dots.append(self.one_dot)
                
            self.current_point = [touch.x, touch.y]
            self.build_point_collection()
            self.find_CG()
            self.calc_cg_to_target_dist()
            

    def choose_random_color(self):
        value_range = random.sample(range(10,75),3)
        self.value_range = (each*0.01 for each in value_range)
	
    def build_point_collection(self):
        if self.touch_number==1:
            self.all_points = [copy.copy(self.current_point)]
        else:
            self.all_points +=  [self.current_point]
        self.num_points = str(len(self.all_points))

    
    def find_CG(self):
        if len(self.all_points)>1:
            self.cg_x = sum([ pt[0]  for pt in self.all_points])/len(self.all_points)
            self.cg_y = sum([ pt[1]  for pt in self.all_points])/len(self.all_points)
            self.cg_xy = [self.cg_x, self.cg_y]
    def calc_cg_to_target_dist(self):
        self.safe_zone_location = self.center


        if len(self.cg_xy)>1:
            cg_to_centre = euclidean_distance(self.cg_xy, 
                                                      self.safe_zone_location)
            print(self.center, self.cg_xy)
            if cg_to_centre > self.safezone_r:
                self.status = 'Go Back!'
                self.lives_left -= 1
                print(self.lives_left)
                if self.lives_left < 1:
                    self.status = "Level fail..restart app"
                    

                    
            else:
                self.status = 'Saaaafe'
                
    def reset_action(self, button):
        '''
        Resets important aspects of the game
        
        1) self.status --> Saafe
        2) removes the Ellipses on the screen
        3) Sets lives back to starting amount
        4) clears all points from point collection

        Returns
        -------
        None.

        '''
        self.status = 'Saaafe'
        self.lives_left = 5
        self.all_points = []
        self.touch_number = 0
        
        for each_dot in self.all_dots:
            self.canvas.remove(each_dot)


class TileItApp(App):
    def build(self): 
        return TileGame()

if __name__ == '__main__':
	TileItApp().run()