import math
import heapq

from Point2D import Point2D
from Polygon import Polygon


class Graph:
    def __init__(self, route_list, polygon_list):
        self.route_list = route_list
        self.polygon_list = polygon_list
        self.graph = self.create_graph()

    def calculate_distance(self, point1: Point2D, point2: Point2D):
        # Calculate the Euclidean distance between two 2D points
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def create_graph(self):
        # Create a graph representing the adjacency matrix
        graph = {}
        for polygon in self.polygon_list:
            graph[polygon] = {}

        # Calculate distances between polygons' points and populate the graph
        for i, polygon1 in enumerate(self.polygon_list):
            for j, polygon2 in enumerate(self.polygon_list):
                if i != j:
                    shortest_distance = float('inf')
                    for point1 in polygon1:
                        for point2 in polygon2:
                            # Calculate distance between points
                            distance = self.calculate_distance(point1, point2)
                            if distance < shortest_distance:
                                shortest_distance = distance

                    # Add the shortest distance between the polygons to the graph
                    graph[polygon1][polygon2] = shortest_distance

        return graph

    def dijkstra(self, start: Polygon, end: Polygon):
        # Initialize distances dictionary with infinite distance for all vertices
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0

        # Initialize priority queue with start vertex and its distance
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # If current vertex is the destination, return the distance
            if current_vertex == end:
                return distances[current_vertex]

            # Skip if the current distance is already greater than the known distance
            if current_distance > distances[current_vertex]:
                continue

            # Iterate over neighboring vertices and update distances
            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight

                # Update the distance if it's shorter than the known distance
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        # If no path found, return None
        return None

    def shortestPath(self, start, end):
        shortest_distance = self.dijkstra(start, end)

        if shortest_distance is not None:
            print(f"The shortest distance between {start} and {end} is {shortest_distance}")
        else:
            print(f"No path found between {start} and {end}")
