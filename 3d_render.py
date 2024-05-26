import pygame
import sys
import math

def shoot_picture(screen, clock, width, height, object_scene, camera, color = (255,255,255)):
    screen.fill((0, 0, 0))
    for object in object_scene:
        for edge in object.edges:
            start_vertex = object.vertices[edge[0] - 1]
            end_vertex = object.vertices[edge[1] - 1]
            start_x, start_y = camera.project(start_vertex)
            end_x, end_y = camera.project(end_vertex)
            pygame.draw.line(screen, color, (start_x + width // 2, start_y + height // 2),
                             (end_x + width // 2, end_y + height // 2))

    pygame.display.flip()
    clock.tick(60)

class Object3D:
    def __init__(self, object_file, start_coordinates=[0, 0, 0], connect_all_vertices = False):
        self.coordinates = start_coordinates
        self.vertices = []
        self.edges = []
        with open(object_file, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue  # Comment line, skip
                elif line.startswith('v '):
                    coordinates = [float(coord) for coord in line.strip().split()[1:]]
                    self.vertices.append(coordinates)
                elif line.startswith('f ') and connect_all_vertices == False:
                    edges = [int(edge.split('/')[0]) for edge in line.strip().split()[1:]]
                    self.edges.append(edges)
        if connect_all_vertices == True:
            for i in range(len(self.vertices) - 1):
                for j in range(len(self.vertices)):
                    self.edges.append((i, j + 1))
        for vertice in self.vertices:
            vertice[0] += start_coordinates[0]
            vertice[1] += start_coordinates[1]
            vertice[2] += start_coordinates[2]


    def rotate_x(self, angle):
        for i in range(len(self.vertices)):
            y, z = self.vertices[i][1] - self.coordinates[1], self.vertices[i][2] - self.coordinates[2]
            self.vertices[i][1] = y * math.cos(angle) - z * math.sin(angle) + self.coordinates[1]
            self.vertices[i][2] = y * math.sin(angle) + z * math.cos(angle) + self.coordinates[2]

    def rotate_y(self, angle):
        for i in range(len(self.vertices)):
            x, z = self.vertices[i][0] - self.coordinates[0], self.vertices[i][2] - self.coordinates[2]
            self.vertices[i][0] = x * math.cos(angle) - z * math.sin(angle) + self.coordinates[0]
            self.vertices[i][2] = x * math.sin(angle) + z * math.cos(angle) + self.coordinates[2]

    def rotate_z(self, angle):
        for i in range(len(self.vertices)):
            x, y = self.vertices[i][0] - self.coordinates[0], self.vertices[i][1] - self.coordinates[1]
            self.vertices[i][0] = x * math.cos(angle) - y * math.sin(angle) + self.coordinates[0]
            self.vertices[i][1] = x * math.sin(angle) + y * math.cos(angle) + self.coordinates[1]

    def move(self, distance_x, distance_y, distance_z):
        self.coordinates[0] += distance_x
        self.coordinates[1] += distance_y
        self.coordinates[2] += distance_z
        for vertice in self.vertices:
            vertice[0] += distance_x
            vertice[1] += distance_y
            vertice[2] += distance_z
    
    def scale(self, scale_x, scale_y, scale_z):
        for vertice in self.vertices:
            vertice[0] -= self.coordinates[0]
            vertice[1] -= self.coordinates[1]
            vertice[2] -= self.coordinates[2]
            vertice[0] *= scale_x
            vertice[1] *= scale_y
            vertice[2] *= scale_z
            vertice[0] += self.coordinates[0]
            vertice[1] += self.coordinates[1]
            vertice[2] += self.coordinates[2]

    def print_pos(self):
        print("Position: X: {}, Y: {}, Z: {}".format(*self.coordinates))

    def print_vertices(self):
        for vertex in self.vertices:
            print("Vertex: X: {}, Y: {}, Z: {}".format(*vertex))


class Camera3D:
    def __init__(self, position):
        self.coordinates = position

    def move(self, distance_x, distance_y, distance_z):
        self.coordinates[0] += distance_x
        self.coordinates[1] += distance_y
        self.coordinates[2] += distance_z

    def rotate_x(self, angle):
        y, z = self.coordinates[1], self.coordinates[2]
        self.coordinates[1] = y * math.cos(angle) - z * math.sin(angle)
        self.coordinates[2] = y * math.sin(angle) + z * math.cos(angle)

    def rotate_y(self, angle):
        x, z = self.coordinates[0], self.coordinates[2]
        self.coordinates[0] = x * math.cos(angle) - z * math.sin(angle)
        self.coordinates[2] = x * math.sin(angle) + z * math.cos(angle)

    def print_pos(self):
        print("Position: X: {}, Y: {}, Z: {}".format(*self.coordinates))

    def project(self, vertex):
        fov = 500
        distance = 5

        x, y, z = vertex[0] - self.coordinates[0], vertex[1] - self.coordinates[1], vertex[2] - self.coordinates[2]

        if z != 0:
            factor = fov / z
            x = x * factor
            y = y * factor

        return x, y


def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    pyramid_filepath = "objects\\pyramid.obj"
    cube_filepath = "objects\\cube.obj"
    cat_filepath = "objects\\cat.obj"
    heart_filepath = "objects\\heart1.obj"


    pyramid = Object3D(pyramid_filepath, [0, 0, 0], True)
    cube = Object3D(cube_filepath, [-4.5, 0, 0], True)
    cat = Object3D(cat_filepath, [2.5, 0, 0], False)
    heart = Object3D(heart_filepath, [0,-1,0], False)
    scene = [pyramid, cube, cat, heart]
    camera = Camera3D([0, 0, -5])
    heart.scale(1,-1,1)
    active_camera = camera
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pyramid.rotate_y(math.pi/360)
        cat.rotate_z(math.pi/360)
        shoot_picture(screen,clock, screen_width, screen_height, scene, active_camera)


if __name__ == "__main__":
    main()
