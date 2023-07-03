"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #5
"""
import numpy as np
import math

# A class of 2-dimensional points
class Point2D:

    # Builder function with private fields
    def __init__(self, x, y, id):
        self.__x = x
        self.__y = y
        self.__id = id

    # Getter and setter properties for each of the private fields
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    # Re-defining the string function so that it returns the name of the point and its coordinates
    def __str__(self):
        return f"{self.id}, ({self.x},{self.y})"

    # A method which gives us the distance of a second point from a given point
    def distance_to_point(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5

    # A static method which will give us the distance between any two points
    @staticmethod
    def distance_between_points(point1, point2):
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

    """ A method for moving a point in 2-space. Previously, this was done in the following fashion:
    def point_translate(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        
    We now perform the translation using vector multiplication."""

    def point_translate(self, dx, dy):
        # representing the point in homogenous form
        homogenous_point= np.array([[self.x], [self.y], [1]])
        # turning the requested translation into an array
        translation_matrix = np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])
        # Performing the translation
        new_point= np.dot(homogenous_point, translation_matrix)
        # Normalizing the result
        for element in range(len(new_point)-1):
            new_point[element] = new_point[element]/new_point[-1]
        # Updating the original point
        self.x = new_point[1]
        self.y = new_point[2]

    # A method which will rotate a point a given number of degrees
    def rotation_point(self, theta):
        # representing the point in homogenous form
        homogenous_point = np.array([[self.x], [self.y], [1]])
        # representing the input angle as radians
        theta = theta*(math.pi/180)
        # turning the requested rotation into an array
        rotation_matrix = np.array([[math.cos(theta), -math.sin(theta), 0],
                                    [math.sin(theta), math.cos(theta), 0],
                                    [0, 0, 1]]
                                   )
        # Performing the rotation
        new_point = np.dot(homogenous_point, rotation_matrix)
        # Normalizing the result
        for element in range(len(new_point) - 1):
            new_point[element] = new_point[element] / new_point[-1]
        # Updating the original point
        self.x = new_point[1]
        self.y = new_point[2]
