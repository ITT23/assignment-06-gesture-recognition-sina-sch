# $1 gesture recognizer
import numpy as np
import math
from scipy.signal import resample
from dollarpy import Recognizer
import xml.etree.ElementTree as ET
import os

def load_data():
    # star, pigtial, delete_mark, arrow
    data = []
    labels = []
    #gestures = ["star", "pigtial", "delete_mark", "arrow", "rectangle"]
    #gestures = ["circle", "rectangle", "x"]
    gestures = ["caret", "v", "rectangle"]
    NUM_POINTS = 50

    for root, subdirs, files in os.walk('dataset/xml_logs'):
        if 'ipynb_checkpoint' in root:
            continue
        
        if len(files) > 0:
            for f in files:
                if '.xml' in f:
                    fname = f.split('.')[0]
                    label = fname[:-2]
                    
                    xml_root = ET.parse(f'{root}/{f}').getroot()
                    
                    points = []
                    for element in xml_root.findall('Point'):
                        x = element.get('X')
                        y = element.get('Y')
                        points.append([x, y])
                        
                    points = np.array(points, dtype=float)
                    
                    #scaler = StandardScaler()
                    #points = scaler.fit_transform(points)
                    
                    resampled = resample(points, NUM_POINTS)
                    
                    if label in gestures:#not label in labels and label in gestures:
                        data.append((label, resampled))
                        #labels.append(label)

    print("all files loaded successfully", len(data))

    return data

class Recognizer:
    def __init__(self):
        super(Recognizer, self).__init__()
        self.templates = load_data()#[]
        self.new_templates = []

    #def create_templates(self, data):
        #for template

    def main(self):
        for template in self.templates:
            self.addTemplate(template)
    
    def addTemplate(self, template):
        name, points = template
        NUM_POINTS = 50
        #print("name", name)
        #print("points", points)
        #template[1] = resample(template[1], NUM_POINTS)
        points = self.rotateToZero(points)
        points = self.scale_to(points, 250)
        points = self.translate_to(points, 0)
        self.new_templates.append([name, points])

# step 1
    #def resample_points(self):
     #   return resample()

    def measure_distance(self, x1, y1, x2, y2):
        distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance


    # step 2

    def centroid(self, arr):
        length = len(arr)
        sum_x = np.sum(arr[:][0])
        sum_y = np.sum(arr[:][1])
        return sum_x/length, sum_y/length

    def indicative_angle(self, points):
        c = np.mean(points, 0)
        return np.arctan2(c[1] - points[0][1], c[0] - points[0][0])
    
    def rotateToZero(self, points):
        ''' Rotates the points to the indicative angle '''
        angle_to_rotate = self.indicative_angle(points)
        newPoints = self.rotate2D(points, 0, -angle_to_rotate)
        return newPoints
    
    def rotate2D(self, pts, cnt, ang=np.pi/4):
        ''' pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian
        http://gis.stackexchange.com/questions/23587/how-do-i-rotate-the-polygon-about-an-anchor-point-using-python-script'''
        return np.dot(np.array(pts)-cnt, np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]]))+cnt

    def rotate_by(self, points, omega):
        newPoints = np.zeros((1, 2))
        c = np.mean(points, 0)
        for point in points:
            q_x = (point[0] - c[0]) * math.cos(omega) - (point[1] - c[1]) * math.sin(omega) + c[0]
            q_y = (point[0] - c[0]) * math.sin(omega) - (point[1] - c[1]) * math.cos(omega) + c[1]
            #new_points.append([(q_x, q_y)]) # new_points = np.append(new_points, [[q_x,q_y]], 0)
            newPoints = np.append(newPoints, [(q_x, q_y)], 0)
        return newPoints[1:]


    # step 3

    def bounding_box(self, points):
        minX, maxX = np.inf, -np.inf
        minY, maxY = np.inf, -np.inf
        for point in points:
            minX, maxX = min(minX, point[0]), max(maxX, point[0])
            minY, maxY = min(minY, point[1]), max(maxY, point[1])
        return minX, maxX, minY, maxY


    def scale_to(self, points, size):
        newPoints = np.zeros((1, 2))
        min_x, max_x, min_y, max_y = self.bounding_box(points)
        for point in points:
            q_x = point[0] * size / (max_x - min_x)
            q_y = point[1] * size / (max_y - min_y)
            newPoints = np.append(newPoints, [(q_x, q_y)], 0)

        return newPoints

    def translate_to(self, points, k):
        newPoints = np.zeros((1, 2))
        c = np.mean(points, 0)
        for point in points:
            q_x = point[0] + k - c[0]
            q_y = point[1] + k - c[1]
            newPoints = np.append(newPoints, [(q_x, q_y)], 0)

        return newPoints[1:]


    # step 4

    def path_distance(self, A, B):
        d = 0
        for i in range(len(A) - 1):
            d += self.measure_distance(A[i][0], A[i][1], B[i][0], B[i][1])

        return d / len(A)

    def distance_at_angle(self, points, temp_points, theta):
        newPoints = np.zeros((1, 2))
        new_points = self.rotate_by(points, theta)
        d = self.path_distance(new_points, temp_points)
        return d

    def distance_at_best_angle(self, points, template, theta_a, theta_b, delta_theta):
        temp_name, temp_points = template
        phi = 0.5 * (-1 + np.sqrt(5))
        x_1 = phi * theta_a + (1- phi) * theta_b
        f_1 = self.distance_at_angle(points, temp_points, x_1)
        x_2 = phi * theta_b + (1- phi) * theta_a
        f_2 = self.distance_at_angle(points, temp_points, x_2)

        while abs(theta_b - theta_a) > delta_theta:
            if f_1 < f_2:
                theta_b = x_2
                x_2 = x_1
                f_2 = f_1
                x_1 = phi * theta_a + (1 - phi) * theta_b
                f_1 = self.distance_at_angle(points, temp_points, x_1)
            else:
                theta_a = x_1
                x_1 = x_2
                f_1 = f_2
                x_2 = phi * theta_b + (1 - phi) * theta_a
                f_2 = self.distance_at_angle(points, temp_points, x_2)

        return min(f_1, f_2)

    def recognize(self, points):
        templates = self.templates
        points = resample(points, 50)
        points = self.rotateToZero(points)
        points = self.scale_to(points, 250)
        points = self.translate_to(points, 0)
        b = np.inf
        theta = np.pi/4
        delta_theta = np.pi/90
        size = 250
        for template in templates:
            d = self.distance_at_best_angle(points, template, -theta, theta, delta_theta)
            if d < b:
                b = d
                new_template = template
        score = 1 - b/0.5 * np.sqrt(size^2 + size^2)
        return new_template#, score



if __name__ == "__main__":
    #data = load_data()
    recognizer = Recognizer()
    recognizer.main()

