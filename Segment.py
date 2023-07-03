"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #5
"""
from Point2D import Point2D


# We construct a class of line segments
class Segment:
    def __init__(self, start, end, name="John Wick"):
        self.__start = start
        self.__end = end
        self.__name = name
        # we add in the coordinates of the center of the segment
        self.x_center = ((self.end.x - self.start.x) / 2) + self.start.x
        self.y_center = ((self.end.y - self.start.y) / 2) + self.start.y

        # We create setter and getter functions for all the fields

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value):
        self.__end = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    # We set a format for printing segments
    def __str__(self):
        return f'{self.name}: Start Point = {self.start}, End Point = {self.end}'

    # A method for determining the length of a segment
    def segment_length(self):
        return Point2D.distance_between_points(self.start, self.end)
