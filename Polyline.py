"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #5
"""

from Segment import *


class Polyline:
    def __init__(self, segments_array, name=""):
        self.__segments = list(map(lambda segment: Segment(segment.start, segment.end, ""), segments_array))

        # We build a segment out of each two
        # consecutive points in the array. We use a "list" to help with our __getitem__ later on
        self.__name = name

# We define getter and setter functions
    @property
    def segments(self):
        return self.__segments

    @segments.setter
    def segments(self, value):
        self.__segments = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

# We re-define the getitem method to allow us to access each segment by using brackets
    def __getitem__(self, item):
        return self.segments[item]

# We construct a method which returns the total length of the polyline
    def poly_length(self):
        total = 0
        for segment in self.segments:
            total += segment.segment_length()
        return total

    # A method which returns the constituent points as a list of tuples
    def coords(self):
        points = []
        for segment in range(len(self.segments)):
            points.append((self.segments[segment].start.y, self.segments[segment].start.x))
            points.append((self.segments[segment].end.y, self.segments[segment].end.x))
        return points
