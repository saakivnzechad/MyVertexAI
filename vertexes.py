import math
class Vertex(object):
    """
    Class for vertexes and them moving
    ...

    Attributes
    --------
    round_pos : list
        x,y,z coordinate of vertex round. Minimal range is > 1/2 of radius for x,y.
    pos : list
        actual x,y position of vertex
    radius : int
        radius of vertex round. makes the range of the circle along which the vertex will move
    WIDTH : int
        actual window width
    HEIGHT : int
        actual window height
    angle : int
        actual angle of vertex
    isNormal : bool
        is exemp of vertex be a normal
    color : any
        color of vertex

    Methods
    --------
    MoveVertex(speed=1):
        move the vertex in range of the circle
    """
    def __init__(self, round_pos=[33, 33, 1], pos=[-32, 0], radius=64, angle=0, WIDTH=640, HEIGHT=480, speed=[0.0005, 0.05], isNormal=False, color=(0, 0, 0)) -> None:
        """
        set every base attributes for Vertex object

        Parameters
        --------
        round_pos : list
            x,y,z coordinate of vertex round. Minimal range is > 1/2 of radius for x,y.
        pos : list
            actual x,y position of vertex
        radius : int
            radius of vertex round. makes the range of the circle along which the vertex will move
        WIDTH : int
            actual window width
        HEIGHT : int
            actual window height
        angle : int
            actual angle of vertex
        isNormal : bool
            is exemp of vertex be a normal
        """
        self.round_pos = round_pos
        self.pos = pos
        self.radius = radius
        self.angle = angle
        self.speed = speed
        self.isNormal = isNormal
        self.color = color
        # x coordinate of vertex round checker
        if self.round_pos[0] < radius:
            self.round_pos[0] = radius + 1
        elif self.round_pos[0] > (WIDTH - radius):
            self.round_pos[0] = (WIDTH - radius) - 1
        # y coordinate of vertex round checker    
        if self.round_pos[1] < radius:
            self.round_pos[1] = radius + 1
        elif self.round_pos[1] > (HEIGHT - radius):
            self.round_pos[1] = (HEIGHT - radius) - 1

    def MoveVertex(self):
        self.pos[0] = self.round_pos[0] + self.radius * math.cos(self.angle)
        self.pos[1] = self.round_pos[1] + self.radius * math.sin(self.angle)
        self.angle += self.speed
