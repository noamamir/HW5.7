"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #3
"""

from Point2D import *
import math


# We build a class of ellipsoidal objects, which is based off of a center point and two axial distances
class Ellipse:
    def __init__(self, *args):
        if len(args) == 4:  # if all arguments are given, we use them all
            self.__center = args[0]
            self.__a = abs(args[1])
            self.__b = abs(args[2])
            self.__name = args[3]
        elif len(args) == 3:  # if no name is given, we leave the name field blank
            self.__center = args[0]
            self.__a = abs(args[1])
            self.__b = abs(args[2])
            self.__name = ""
        else:  # if no values are given, we default to the unit ellipse
            self.__center = Point2D(0, 0, 'center')
            self.__a = 1
            self.__b = 1
            self.__name = "Unit Ellipse"

    # We create setter and getter functions for all the fields

    @property
    def center(self):
        return self.__center

    @center.setter
    def center(self, value):
        self.__center = value

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = abs(value)

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = abs(value)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    # Property which returns the area of the ellipse
    @property
    def area(self):
        return math.pi * self.a * self.b

    # We redefine the string to display different properties of the ellipse
    def __str__(self):
        return f'{self.name}: x= {self.center.x}, y= {self.center.y}, a={self.a}, b={self.b}, Area = {self.area}'

    # A method which will move the center of the ellipse
    def ellipse_translate(self, dx, dy):
        self.center.x += dx
        self.center.y += dy
