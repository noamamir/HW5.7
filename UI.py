"""
Names: Jeffrey Aaron Cohen, Tom Yenon
Student Numbers: 941190399, 316595735
Course Name: Object-Oriented Programming for Geographic Information
Course Number: 014845
Homework #5
"""
# Note to self: Need to fill in pathfinder algorithm, and the optimal path refresh

import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import messagebox

import numpy as np
import tkintermapview

from Polygon import *
from Polyline import *
from Graph import *
from Route import *


class UI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{800}x{600}")  # Initializing the user interface, with buttons etc.
        self.title("Technion Pathfinder Widget")  # We changed the title here to make it less technical

        toolbar_frame = tk.Frame(self, width=800, height=50, bg="gray")
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        load_polygons_button = tk.Button(toolbar_frame, text="Load Polygons", command=self.load_polygons)
        load_polygons_button.pack(side=tk.LEFT)

        load_routes_button = tk.Button(toolbar_frame, text="Load Routes", command=self.load_routes)
        load_routes_button.pack(side=tk.LEFT)

        start_point_button = tk.Button(toolbar_frame, text="Choose Start Point", command=self.pick_start_point)
        start_point_button.pack(side=tk.LEFT)

        end_point_button = tk.Button(toolbar_frame, text="Choose End Point", command=self.pick_end_point)
        end_point_button.pack(side=tk.LEFT)

        pathfinder_button = tk.Button(toolbar_frame, text="Find Shortest Path", command=self.pathfinder)
        pathfinder_button.pack(side=tk.LEFT)

        exit_button = tk.Button(toolbar_frame, activebackground='red', text="Exit", command=self.close)
        exit_button.pack(side=tk.RIGHT)

        clear_map_button = tk.Button(toolbar_frame, text="Clear Map", command=self.clear_map)
        clear_map_button.pack(side=tk.RIGHT)

        refresh_button = tk.Button(toolbar_frame, text="Refresh", command=self.clear_endpoints)
        refresh_button.pack(side=tk.RIGHT)

        # create map widget
        self.map_widget = self.init_map()
        # self.map_widget.add_left_click_map_command(self.left_click_event)

        # We set global fields for use across different functions
        self.start_polygon: Polygon = Polygon()
        self.end_polygon: Polygon = Polygon()
        self.polygon_list = []
        self.path_list = []
        self.picking_start_point: bool = False
        self.picking_end_point: bool = False
        self.selectedPathCords = []
        self.routes_loaded = 0
        self.polygons_loaded: bool = False
        self.chose_start_point: bool = False
        self.chose_end_point: bool = False
        self.graph = []
        self.polyline_number = 0
        self.points = []
        self.vertex_number = []  # Keeping track of how many vertices there are to each polyline

    def init_map(self):
        try:
            # create map widget
            map_widget = tkintermapview.TkinterMapView(self, width=800, height=600, corner_radius=0)
            map_widget.pack(side=tk.BOTTOM)

            # set current widget position and zoom
            map_widget.set_position(32.777653, 35.023630)  # Technion, Israel
            map_widget.set_zoom(16)

            # map_widget.add_left_click_map_command(self.left_click_event)

            return map_widget
        except Exception as e:
            print(f"Error: {e}")

    def left_click_event(self, coordinates_tuple):
        if not (self.routes_loaded and self.polygons_loaded):
            messagebox.showerror("Error", "Please load elements onto the Map first.")
        closest_polygon = Polygon()  # A placeholder value
        minimum_distance = np.inf  # Initializing the current smallest distance as infinity
        # We run through all the vertices of all the polygons to find the closest one to our point
        for polygon in range(len(self.polygon_list)):
            for point in range(len(self.polygon_list[polygon].coords)):
                current_distance = ((coordinates_tuple[0] - self.polygon_list[polygon].coords[point][0]) ** 2 +
                                    (coordinates_tuple[1] - self.polygon_list[polygon].coords[point][1]) ** 2) ** 0.5
            if minimum_distance > current_distance:
                minimum_distance = current_distance
                closest_polygon = self.polygon_list[polygon]
        # We assign it as the start or end polygon, depending on the mode we are in, and highlight it on the map
        if self.picking_start_point is True:
            if self.end_polygon.coords is not closest_polygon.coords:
                self.start_polygon = closest_polygon
                self.map_widget.set_polygon(self.start_polygon.coords, outline_color="#90EE90", fill_color="#8D0D80")
                self.chose_start_point = True
            else:
                messagebox.showerror("Error", "polygon was already chosen, choose a different polygon")
        elif self.picking_end_point is True:
            if self.start_polygon.coords is not closest_polygon.coords:
                self.end_polygon = closest_polygon
                self.map_widget.set_polygon(self.end_polygon.coords, outline_color="#90EE90", fill_color="#8D0D80")
                self.chose_end_point = True
            else:
                messagebox.showerror("Error", "polygon was already chosen, choose a different polygon")
        else:
            messagebox.showerror("Error", "Must be in start point or end point mode")

    # This function will allow us to load the paths into Polyline objects
    def load_routes(self):
        if not self.polygons_loaded:
            messagebox.showerror("Error", "Must load polygons first")
            return

        file_path = self.browse_file()  # Finding the file path

        if file_path == '':
            messagebox.showerror("Error", "Illegal file path, please try again")
            return


        file_vertices = open(file_path, "r")  # Accessing the file
        self.polyline_number = -1  # This index will allow us to count how many polylines we have in programming terminology
        for line in file_vertices:
            if line.startswith('#'):
                self.polyline_number = self.polyline_number + 1  # Signifies that we have found a new polyline to make
                self.vertex_number.append(0)  # Restarting the count of vertices in this polyline
            else:
                separated_points = line.split(',')
                if len(separated_points) != 2 or separated_points[0] == '\n' or separated_points[1] == '\n':
                    messagebox.showerror("Error", f"File contains illegal coordinate pair")
                    return

                self.points.append(Point2D(float(separated_points[1]), float(separated_points[0]),
                                           self.vertex_number[self.polyline_number]))  # We read the
                # coordinates in reverse order so that they will fit the x,y format of Point2D
                self.vertex_number[self.polyline_number] = self.vertex_number[self.polyline_number] + 1  # Showing that we added another
                # vertex
                if len(self.points) >= 2:  # If we have more than two points, we want to add the next line to the map
                    coords_to_print = [(self.points[-1].y, self.points[-1].x), (self.points[-2].y, self.points[-2].x)]
                    self.map_widget.set_path(coords_to_print, color="grey", width=3)
        self.routes_loaded = 1
        if self.polygons_loaded:  # Meaning, we have loaded both the routes and polygons; we will want to
            # create our graph
            start_vertex = 0
            for i in range(self.polyline_number):
                for polygon in self.polygon_list:
                    if polygon.isInside(self.points[start_vertex]):  # Start Polygon
                        s_polygon = polygon
                    if polygon.isInside(self.points[start_vertex + self.vertex_number[i]]):
                        t_polygon = polygon
                self.path_list.append(
                    Route(s_polygon, t_polygon, i, self.points[start_vertex:(start_vertex + self.vertex_number[i])]))
                start_vertex = start_vertex + self.vertex_number[i]  # updating the starting vertex
            self.graph.append(Graph(self.path_list, self.polygon_list))

    # This function allows us to load the polygons into Polygon objects.
    def load_polygons(self):
        file_path = self.browse_file()  # Finding the file path

        if file_path == '':
            messagebox.showerror("Error", "Illegal file path, please try again")
            return

        file_vertices = open(file_path, "r", encoding='utf8')  # Saving the file path as an object, taking into account
        # that it has Hebrew characters
        # We make placeholder arrays into which we will read the file:
        names = []
        coordinate_pairs = []
        num_of_vertices = []
        i = -1  # We start at -1 because the first line is a name. This index allows each polygon to be a separate array
        existing_polygon = 0  # We start off having never seen the polygon before
        for line in file_vertices:  # This for loop reads each line into its appropriate array
            if line.startswith('#'):
                names.append(line.strip('#'))
                i = i + 1
                existing_polygon = 0  # this index tells us we are at a new polygon
            else:
                separated_points = line.split(',')
                if len(separated_points) != 2 or separated_points[0] == '\n' or separated_points[1] == '\n':
                    messagebox.showerror("Error", f"File contains illegal coordinate pair")
                    return

                coordinate_pairs.append((float(separated_points[1]), float(separated_points[0])))  # We read the
                # coordinates in reverse order so that they will fit the x,y format of Point2D
                # We add a loop to keep track of how many vertices this polygon has
                if not existing_polygon:  # meaning, this is the first vertex in a polygon
                    num_of_vertices.append(existing_polygon + 1)
                else:
                    num_of_vertices[i] = existing_polygon + 1
                existing_polygon = existing_polygon + 1

        self.polygons_loaded = True
        if self.routes_loaded == 1:  # Meaning, we have loaded both the routes and polygons; we will want to
            # create our graph
            start_vertex = 0
            for i in range(self.polyline_number):
                for polygon in self.polygon_list:
                    if polygon.isInside(self.points[start_vertex]):  # Start Polygon
                        s_polygon = polygon
                    if polygon.isInside(self.points[start_vertex + self.vertex_number[i]]):
                        t_polygon = polygon
                self.path_list.append(
                    Route(s_polygon, t_polygon, i, self.points[start_vertex:(start_vertex + self.vertex_number[i])]))
                start_vertex = start_vertex + self.vertex_number[i]  # updating the starting vertex
            self.graph.append(Graph(self.path_list, self.polygon_list))

        # Now, we construct the polygon objects from the name and a list of Point2D objects
        self.polygon_list = []
        already_read_vertices = 0  # This will allow us not to lose our place when creating the polygons
        for i in range(len(names)):
            points = []
            for vertex in range(num_of_vertices[i]):
                points.append(
                    Point2D(coordinate_pairs[already_read_vertices][0], coordinate_pairs[already_read_vertices][1],
                            vertex))
                already_read_vertices = already_read_vertices + 1
            current_name = names[i]
            self.polygon_list.append(Polygon(points, current_name))
            # Finally, we add the polygons to the map
        for polygon in self.polygon_list:
            self.map_widget.set_polygon(polygon.coords, outline_color="black", fill_color="turquoise")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("txt Files", "*.txt")])
        return file_path

    def clear_map(self):
        # Clearing Graphically
        self.map_widget.delete_all_polygon()
        self.map_widget.delete_all_path()

        # Clearing the memory
        self.polygon_list = []
        self.path_list = []
        self.polygons_loaded = False
        self.routes_loaded = 0

    def pick_start_point(self):
        if self.chose_start_point is True:
            messagebox.showerror("Error", "To choose a different start point, hit Refresh")
        self.picking_start_point = True
        self.picking_end_point = False
        self.map_widget.add_left_click_map_command(self.left_click_event)

        # TODO: only set choose start point after actually choosing it

    def pick_end_point(self):
        if self.chose_end_point is True:
            messagebox.showerror("Error", "To choose a different end point, hit Refresh")
        self.picking_start_point = False
        self.picking_end_point = True
        self.map_widget.add_left_click_map_command(self.left_click_event)

        # TODO: only set choose end point after actually choosing it

    def pathfinder(self):
        """Calling the pathfinder function, which will also mark the shortest path on the map"""
        if self.start_polygon.id is not None and self.end_polygon.id is not None:
            self.selectedPathCords = self.graph[0].shortestPath(self.start_polygon, self.end_polygon)

            for path in self.selectedPathCords:
                self.map_widget.set_path(path, color="orange", width=5)

    def resetChosenRoutes(self):
        for path in self.selectedPathCords:
            self.map_widget.set_path(path, color="gray", width=5)

    # We reset the selections for start and end polygons and take off their color on the map, same for optimal path
    def clear_endpoints(self):
        if self.chose_start_point is True:
            self.map_widget.set_polygon(self.start_polygon.coords, outline_color="black", fill_color="turquoise")
        if self.chose_end_point is True:
            self.map_widget.set_polygon(self.end_polygon.coords, outline_color="black", fill_color="turquoise")
        self.start_polygon = Polygon()
        self.end_polygon = Polygon()
        self.chose_start_point = 0
        self.chose_end_point = 0
        self.polyline_number = 0
        self.points = []
        self.vertex_number = []
        if len(self.selectedPathCords) > 0:
            """Reset the optimal path. Then, """
            self.resetChosenRoutes()

    def close(self):
        self.destroy()

    def run(self):
        self.mainloop()
