'''Checks how many points the use can tile within the screen
give a certain time. 

TODO:
    1. The safe zone's circle and the center used for calculations don't seem 
    to be the same. Check on this. 
    2. 

'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ReferenceListProperty, NumericProperty
from kivy.properties import ObjectProperty
from kivy.graphics import Ellipse, Color, Line
import random
from math import sqrt, cos, sin
import copy

    
def make_circle_points(origin, radius):
    '''
    

    Parameters
    ----------
    origin : list
        list w 2 elements, the x and y coods
    radius : float
        radius of the circle

    Returns
    -------
    circle_xy : list
        List with containing the x and y coords
        of the points defining a circle's perimeter
        as *separate* entries. eg. [0,0,0,1,0,2]
        instead of [[0,0], [0,1], [0,2] ]

    '''
    thetas = range(0, int(2*3.14*100), 5)
    thetas = [ each*0.01 for each in thetas]
    
    circle_xy = []
    x_origin, y_origin = origin
    for angle in thetas:
        x, y = radius*cos(angle), radius*sin(angle)       
        circle_point = [ x+x_origin, y+y_origin]
        circle_xy += circle_point
    return circle_xy

class TargetCircle(Widget):
    circle_center=[0,0]

class CenterDot(Widget):
    pass

class TileGame(Widget):

    safe_zone_location = [0,0]
    
    mean_point_distance = 0
    status = StringProperty('Safe')
    cg_x = NumericProperty(0)
    cg_y = NumericProperty(0)
    centre_gravity = ReferenceListProperty(cg_x,cg_y)
    touch_number = 0
    cg_dot_size = 20
    
    cg_xy = []
    
    safezone_r = 30
    
    lives_left = NumericProperty(5)
    num_points = StringProperty('0')

    
        
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
        self.num_points = str(len(self.all_points))

    
    def find_CG(self):
        if len(self.all_points)>1:
            self.cg_x = sum([ pt[0]  for pt in self.all_points])/len(self.all_points)
            self.cg_y = sum([ pt[1]  for pt in self.all_points])/len(self.all_points)
            self.cg_xy = [self.cg_x, self.cg_y]
    def calc_cg_to_target_dist(self):
        self.safe_zone_location = self.center
        
        with self.canvas:
            Color(0,1,0,0.1)                
            Ellipse(pos=[self.center_x,   self.center_y],
                                size=(5,5), rgba=(0,1,0,0.1))

        if len(self.cg_xy)>1:
            cg_to_centre = euclidean_distance(self.cg_xy, 
                                                      self.safe_zone_location)
            print(self.center, self.cg_xy)
            if cg_to_centre > self.safezone_r:
                self.status = 'Go Back!'
                self.lives_left -= 1
                print(self.lives_left)
                if self.lives_left < 1:
                    self.status = 'LEVEL FAIL!!'
                    
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
        distances = [0]*len(point_combinations)
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
    x1, y1 = pt1
    x2, y2 = pt2
    return sqrt((x1-x2)**2+(y1-y2)**2)
        
    


class TileItApp(App):
    def build(self): 
        return TileGame()

if __name__ == '__main__':
	TileItApp().run()