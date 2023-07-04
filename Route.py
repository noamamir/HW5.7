"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #5
"""
from Polyline import *
from Point2D import *

class Route(Polyline):
    def __init__(self, s_polygon, t_polygon, id, points):

        # We initialize our variables
        self.s_polygon = s_polygon
        self.t_polygon = t_polygon
        self.points = points
        self.id = id

        # We create the list of segments for which to initialize the polyline constructor
        segments_array = []
        for i in range(len(points)-1):
            segments_array.append(Segment(points[i], points[i+1], "segment" + str(i)))
        Polyline.__init__(self, segments_array, id)

    @property
    def coords(self):
        """
                Get the route coordinates as a list of tuples.

                Returns:
                    List of tuples representing the polygon coordinates- [(x1, y1), (x1, y1), ...]
                """
        # We begin by initializing the list into which we will place our tuples
        coordinate_list = []
        for point in self.points:
            coordinate_list.append((point.x, point.y))
        return coordinate_list

