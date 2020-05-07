'''Checks how many points the use can tile within the screen
give a certain time. 

'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ReferenceListProperty, NumericProperty
from kivy.graphics import Ellipse, Color
import datetime as dt
import random

import numpy as np 
from scipy.spatial import distance_matrix, distance


class TileGame(Widget):
    mean_point_distance = 0
    status = StringProperty('Safe')
    cg_x = NumericProperty(0)
    cg_y = NumericProperty(0)
    centre_gravity = ReferenceListProperty(cg_x,cg_y)
    touch_number = 0
    cg_dot_size = 20
    safe_zone_size = 60

    def __init__(self, **kwargs):
        super(TileGame, self).__init__(**kwargs)
        self.safe_zone_location = [self.width / 2, self.height / 2]
        print("MIAOW",self.safe_zone_location)  
        
    def on_touch_down(self, touch):
        self.choose_random_color()
        self.touch_number += 1 
        

        with self.canvas:
            Color(*self.value_range)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

        self.current_point = np.array([touch.x, touch.y]).reshape(1,2)
        self.build_point_collection()
        self.calculate_distance_matrix()
        
        self.mean_inter_point_distance()
        self.find_CG()

    def choose_random_color(self):
        value_range = random.sample(range(10,75),3)
        self.value_range = (each*0.01 for each in value_range)
	
   
    def build_point_collection(self):
        if self.touch_number==1:
            self.all_points = self.current_point.copy()
        else:
            self.all_points = np.row_stack((self.all_points, 
                                            self.current_point))
    def calculate_distance_matrix(self):
        self.dist_mat = distance_matrix(self.all_points,
                                        self.all_points)
    
    def unique_and_no_self_points(self, twod_array):
        try:
            inds = np.tril_indices_from(twod_array)
            return twod_array[inds].flatten()
        except:
            pass

    def mean_inter_point_distance(self):
        mean_dist = np.mean(self.unique_and_no_self_points(self.dist_mat))
        
        if mean_dist is None:
            pass
        else:
            self.mean_point_distance = float(mean_dist)
    
    def find_CG(self):
        if self.all_points.shape[0]>1:
            self.cg_x, self.cg_y = np.mean(self.all_points, 0).tolist()

    def calc_cg_to_target_dist(self):
        cg_xy = np.array([self.cg_x, self.cg_y])
        zone_centre = np.array(safe_zone_location)
        cg_to_centre = distance.euclidean(cg_xy, zone_centre)
        print(cg_to_centre)
        if cg_to_centre > safe_zone_size:
            self.status = 'Woah'
        
            
        
    
    
        




class TileItApp(App):
	def build(self):
		return TileGame()




if __name__ == '__main__':
	TileItApp().run()