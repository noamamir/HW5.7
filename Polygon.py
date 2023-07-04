"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #5
"""
from Point2D import Point2D


class Polygon:
    def __init__(self, points=None, id=None):
        if points is None:
            points = []
        self.points = points
        self.id = id
        
    @property
    def coords(self):
        """
                Get the polygon coordinates as a list of tuples.

                Returns:
                    List of tuples representing the polygon coordinates- [(y1, x1), (y2, x2), ...]
                """
        # We begin by initializing the list into which we will place our tuples
        coordinate_list = []
        for point in self.points:
            coordinate_list.append((point.y,point.x))
        return coordinate_list
        
    def isInside(self, point):
        """
        Check if a given point is inside the polygon.

        Args:
            point (Point2D): The point to check.

        Returns:
            bool: True if the point is inside the polygon, False otherwise.
        """
        num_points = len(self.points)
        inside = False
        
        for i in range(num_points):
            current_point = self.points[i]
            next_point = self.points[(i + 1) % num_points]
            
            if (
                (point.y > min(current_point.y, next_point.y)) and
                (point.y <= max(current_point.y, next_point.y)) and
                (point.x <= max(current_point.x, next_point.x)) and
                (current_point.y != next_point.y)
            ):
                x_intersect = (
                    (point.y - current_point.y) * (next_point.x - current_point.x) / 
                    (next_point.y - current_point.y) + current_point.x
                )
                
                if current_point.x == next_point.x or point.x <= x_intersect:
                    inside = not inside
        
        return inside