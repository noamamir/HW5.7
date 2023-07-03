"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #5
"""
import math

import numpy as np

class Graph:
    def __init__(self, route_list, polygon_list):
        """
        Initializes a Graph object.

        Args:
            route_list (list): A list of routes.
            polygon_list (list): A list of polygons.

        The method initializes the route_list, polygon_list, and matrix attributes of the Graph object.
        It also populates the matrix with the lengths of routes between polygons.
        """
        self.route_list = route_list
        self.polygon_list = polygon_list
        self.matrix = np.zeros((len(self.polygon_list), len(self.polygon_list)))

        # Populate the matrix with the lengths of routes between polygons
        for i in range(len(self.polygon_list)):
            for j in range(len(self.polygon_list)):
                for route in self.route_list:
                    if (route.s_polygon == self.polygon_list[i] and route.t_polygon == self.polygon_list[j]) or \
                            (route.s_polygon == self.polygon_list[j] and route.t_polygon == self.polygon_list[i]):
                        self.matrix[i][j] = route.poly_length()

    def shortestPath(self, start, end, map_widget):
        """
        Finds the shortest path between two polygons in the graph.

        Args:
            start: The starting polygon.
            end: The ending polygon.
            map_widget: A widget used for displaying the path.

        Returns:
            list: The shortest path as a list of polygons.

        The method uses Dijkstra's algorithm to find the shortest path between two polygons.
        It takes into account the distances between polygons and uses a map_widget to display the path.
        """
        start_index = self.polygon_list.index(start)
        end_index = self.polygon_list.index(end)

        if start_index == -1 or end_index == -1:
            raise Exception("Start or end polygon not found in the list.")

        num_vertices = len(self.polygon_list)
        distances = [np.inf] * num_vertices
        predecessors = [None] * num_vertices
        visited = [False] * num_vertices

        distances[start_index] = 0

        while True:
            min_distance = np.inf
            current_index = -1

            # Find the vertex with the minimum distance that has not been visited
            for i in range(num_vertices):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    current_index = i

            # Exit the loop if all vertices have been visited or the current vertex is the destination
            if current_index == -1 or current_index == end_index:
                break

            visited[current_index] = True

            # Update the distances and predecessors of neighboring vertices
            for neighbor in range(num_vertices):
                if self.matrix[current_index][neighbor] > 0 and not visited[neighbor]:
                    new_distance = distances[current_index] + self.matrix[current_index][neighbor]
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = current_index

        if predecessors[end_index] is None:
            raise Exception("No path found from start to end.")

        # Reconstruct the shortest path from the predecessors
        path = []
        current_index = end_index
        while current_index != start_index:
            path.append(self.polygon_list[current_index])
            current_index = predecessors[current_index]
        path.append(self.polygon_list[start_index])
        path.reverse()
        coordinates_forPath = []

        # Display the shortest route on the map widget
        for i in range(len(path) - 1):
            s_polygon = path[i]
            t_polygon = path[i + 1]
            shortest_route = None
            min_distance = np.inf

            current_polygon = path[i]
            next_polygon = path[i+1]

            for route in self.route_list:
                if ((route.s_polygon == current_polygon and route.t_polygon == next_polygon) or
                        (route.s_polygon == next_polygon and route.t_polygon == current_polygon)):
                    distance = route.poly_length()
                    if distance < min_distance:
                        min_distance = distance
                        shortest_route = route
            coordinates_forPath += shortest_route.coords

            if next_polygon == path[-1]:
                break
        map_widget.set_path(coordinates_forPath, color="orange", width=5)

