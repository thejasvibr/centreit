'''Checks how many points the use can tile within the screen
give a certain time. 

'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ReferenceListProperty, NumericProperty
from kivy.graphics import Ellipse, Color
import datetime as dt
import random
from math import sqrt
import copy

class TileGame(Widget):
    mean_point_distance = 0
    status = StringProperty('Safe')
    cg_x = NumericProperty(0)
    cg_y = NumericProperty(0)
    centre_gravity = ReferenceListProperty(cg_x,cg_y)
    touch_number = 0
    cg_dot_size = 20
    safe_zone_size = 30
    cg_xy = []

    
        
    def on_touch_down(self, touch):
        self.choose_random_color()
        self.touch_number += 1 
        

        with self.canvas:
            Color(*self.value_range)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
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

    
    def find_CG(self):
        if len(self.all_points)>1:
            print(self.all_points)
            self.cg_x = sum([ pt[0]  for pt in self.all_points])/len(self.all_points)
            self.cg_y = sum([ pt[1]  for pt in self.all_points])/len(self.all_points)
            self.cg_xy = [self.cg_x, self.cg_y]
    def calc_cg_to_target_dist(self):
        self.safe_zone_location = [self.center_x, self.center_y]
        if len(self.cg_xy)>1:
            cg_to_centre = euclidean_distance(self.cg_xy, 
                                                      self.safe_zone_location)
            if cg_to_centre > self.safe_zone_size:
                self.status = 'DANGER'
            else:
                self.status = 'Saaaafe'
                

def interpoint_distances(all_pts):
    '''
    Calculates the distance between one point to the other.

    Parameters
    ----------
    all_pts: list
        List with tuples representing x,y points

    Returns
    -------
    distances : list
        List with distances between all points. 

    Example
    -------
    >>> xy_pts = [[0,1], [0,2], [0,3]]
    >>> dists = interpoint_distances(xy_pts)
    >>> print(dists)
    [1,2,1]
    '''
    if len(all_pts) == 1:
        return None
    else:
        num_pts = len(all_pts)
        point_combinations = all_point_combinations(num_pts)
        print(len(point_combinations))
        distances = [0]*len(point_combinations)
        print(point_combinations)
        for index, (pt1, pt2) in enumerate(point_combinations):
            pt1pt2_dist = euclidean_distance(all_pts[pt1], all_pts[pt2])
            distances[index] = pt1pt2_dist
        return distances

def all_point_combinations(number_of_points):
    all_pt_combis = []
    for i in range(number_of_points):
        for j in range(i+1, number_of_points):
            all_pt_combis.append([i,j])
    return all_pt_combis
    
    
def euclidean_distance(pt1, pt2):
    '''


    Parameters
    ----------
    pt1, pts : list
        List with x and y coordinates
    Returns
    -------
    distance : float
    '''
    print(f"{pt1},{pt2}")
    x1, y1 = pt1
    x2, y2 = pt2
    return sqrt((x1-x2)**2+(y1-y2)**2)
    
    
    
    
        




class TileItApp(App):
	def build(self):
		return TileGame()




if __name__ == '__main__':
	TileItApp().run()