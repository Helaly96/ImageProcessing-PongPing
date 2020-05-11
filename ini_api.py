import configparser
import numpy as np

class API():

    def __init__(self):

        #class parameters
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.pts0 = np.array([(0,0),(0,0),(0,0),(0,0)])
        self.pts1 = np.array([(0,0),(0,0),(0,0),(0,0)])
        self.pts2 = np.array([(0,0),(0,0),(0,0),(0,0)])
        self.points = [[0, 0], [0, 0]]

        #filling the parameters
        self.read_stadium_points()
        self.read_crop_points()

    #reading from the ini file
    def read_stadium_points(self):
        self.pts0[0] = tuple(map(int, self.config['stadium']['first_player_point_1'].split(',')))
        self.pts0[1] = tuple(map(int, self.config['stadium']['first_player_point_2'].split(',')))
        self.pts0[2] = tuple(map(int, self.config['stadium']['first_player_point_3'].split(',')))
        self.pts0[3] = tuple(map(int, self.config['stadium']['first_player_point_4'].split(',')))

        self.pts1[0] = tuple(map(int, self.config['stadium']['second_player_point_1'].split(',')))
        self.pts1[1] = tuple(map(int, self.config['stadium']['second_player_point_2'].split(',')))
        self.pts1[2] = tuple(map(int, self.config['stadium']['second_player_point_3'].split(',')))
        self.pts1[3] = tuple(map(int, self.config['stadium']['second_player_point_4'].split(',')))

        self.pts2[0] = tuple(map(int, self.config['stadium']['net_point_1'].split(',')))
        self.pts2[1] = tuple(map(int, self.config['stadium']['net_point_2'].split(',')))
        self.pts2[2] = tuple(map(int, self.config['stadium']['net_point_3'].split(',')))
        self.pts2[3] = tuple(map(int, self.config['stadium']['net_point_4'].split(',')))
    def read_crop_points(self):
        self.points[0][1] = int(self.config['crop']['crop_point_01'])
        self.points[1][1] = int(self.config['crop']['crop_point_11'])
        self.points[0][0] = int(self.config['crop']['crop_point_00'])
        self.points[1][0] = int(self.config['crop']['crop_point_10'])


    #helpers
    def get_stadium_points(self):
        return self.pts0,self.pts1,self.pts2
    def get_crop_points(self):
        return self.points


    crop_point_01 = 321
    crop_point_11 = 711
    crop_point_00 = 329
    crop_point_10 = 1559