import pygame
import sys
from vertexes import Vertex
from random import randint
import random
from numpy import interp
from numpy import median
import logging
import datetime
import math
from screeninfo import get_monitors

proportion = 1
isFullScreen = False
isDarkTheme = False

DEF_WIDTH = 480
DEF_HEIGHT = 360
for m in get_monitors():
    if isFullScreen is True:
        WIN_WIDTH = m.width
        WIN_HEIGHT = m.height
        proportion = median([(WIN_WIDTH / DEF_WIDTH), (WIN_HEIGHT / DEF_HEIGHT)])
    else:
        WIN_WIDTH = DEF_WIDTH
        WIN_HEIGHT = DEF_HEIGHT
print(proportion)

FPS = 60
WHITE = (255, 255, 255)
VERTEX_COUNT = 16
DEEP_DARK_FANTASIES = [-2, 8]  # ♂♂♂♂♂♂♂♂ WEE WEE ♂♂♂♂♂♂♂♂
VERTEX_ROUND_RADIUS_RANGE = [4, 64]
SPEED_RANGE = [-0.01, 0.01]
MAX_NORMAL_DISTANCE = 180
LIGHT_RANGE = [0, 255]


vertex_deep_color = 0

logging.basicConfig(filename="logdoc.log", filemode="w", level=logging.DEBUG)
logging.debug("<--- field are sucessfully loaded --->")

clock = pygame.time.Clock()
window_flags = pygame.SRCALPHA | pygame.NOFRAME  # | pygame.FULLSCREEN
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), window_flags)
sc.set_alpha(0)
logging.debug("<--- the window resolution is set --->\nTotal resolution is: " + str(WIN_WIDTH) + " x " + str(WIN_HEIGHT))

vertexesArray = [Vertex() for _ in range(VERTEX_COUNT)]
logging.debug("<--- a list with vertex instances has been created. --->\nTotal count of vertex is: " + str(VERTEX_COUNT) + "\nTotal vertex position depth range is: " + str(DEEP_DARK_FANTASIES) + "\nTotal vertex round radius range is: " + str(VERTEX_ROUND_RADIUS_RANGE))
logging.debug("-------- APPLICATION SUCESSFULLY STARTED --------")


def find_closest_points(target_vertex, vertex_list, distance):
    closest_vertexes = []
    closest_objects_color = []
    closest_objects_z = []
    rounded_color = (255, 255, 255)
    rounded_size = 1

    # Проверяем каждую точку в списке
    for vertex in vertex_list:
        # Вычисляем расстояние между целевой точкой и текущей точкой
        dx = target_vertex.pos[0] - vertex.pos[0]
        dy = target_vertex.pos[1] - vertex.pos[1]
        calculated_distance = math.sqrt(dx**2 + dy**2)
        # Если расстояние меньше заданного, добавляем точку в результаты
        if calculated_distance < distance:
            closest_vertexes.append(vertex.pos)
            closest_objects_color.append(vertex.color)
            closest_objects_z.append(vertex.round_pos[2])

    closest_vertexes.append(target_vertex.pos)
    closest_objects_color.append(target_vertex.color)
    closest_objects_z.append(target_vertex.round_pos[2])

    rounded_color = median(closest_objects_color)
    rounded_size = abs(median(closest_objects_z))
    rounded_size = (int(interp(rounded_size, DEEP_DARK_FANTASIES, [1, 2])))

    rounded_color = (rounded_color, rounded_color, rounded_color)
    return [closest_vertexes, rounded_color, rounded_size]

for i in vertexesArray:
    i.round_pos = [randint(VERTEX_ROUND_RADIUS_RANGE[1], (WIN_WIDTH - VERTEX_ROUND_RADIUS_RANGE[1])), randint(VERTEX_ROUND_RADIUS_RANGE[1], (WIN_HEIGHT - VERTEX_ROUND_RADIUS_RANGE[1])), random.uniform(DEEP_DARK_FANTASIES[0], DEEP_DARK_FANTASIES[1])]
    i.radius = randint(VERTEX_ROUND_RADIUS_RANGE[0], VERTEX_ROUND_RADIUS_RANGE[1])
    if i.round_pos[2] >= 1.0:
        i.speed = random.uniform(SPEED_RANGE[0], SPEED_RANGE[1]) * i.round_pos[2]
    elif i.round_pos[2] <= -1.0:
        i.speed = random.uniform(SPEED_RANGE[0],SPEED_RANGE[1]) / -(i.round_pos[2])
    elif i.round_pos[2] > -1.0 and i.round_pos[2] < 1.0:
        i.speed = random.uniform(SPEED_RANGE[0],SPEED_RANGE[1])
    else:
        logging.debug("index error, there's no speed in this z pos: " + str(i.speed))
        raise IndexError
    logging.debug("round position: " + str(i.round_pos) + " : radius: " + str(i.radius) + " : --- : vertex position: " + str(i.pos))
    logging.debug(str(datetime.datetime.now()))


while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            logging.debug("-------- END OF PROGRAM --------")
            sys.exit()
    sc.fill((255, 255, 255, 0))

    for i in vertexesArray:
        # print(str(vertexesArray[i].round_pos) + " : " + str(len(vertexesArray)))
        vertex_deep_color = (int(interp(i.round_pos[2], DEEP_DARK_FANTASIES, LIGHT_RANGE)))
        i.color = (vertex_deep_color, vertex_deep_color, vertex_deep_color)
        i.MoveVertex()
        i.pos = [int(i.pos[0]), int(i.pos[1])]
        # print(secondVertex)
        # print(secondVertex.pos, thirdVertex.pos)
        point_list = find_closest_points(i, vertexesArray,MAX_NORMAL_DISTANCE) 
        if len(point_list[0]) > 2:
            pygame.draw.aalines(sc, point_list[1], True, point_list[0], point_list[2])

    pygame.display.flip()
    clock.tick(FPS)
