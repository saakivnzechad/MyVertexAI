import pygame
from components.vertexes import Vertex
from random import randint
import random
import numpy
from screeninfo import get_monitors
from components.Audiolistener import MicrophoneListener
from asyncio import Queue
import asyncio

proportion = 1
isFullscreenreen = False
isDarkTheme = True
isDebug = True

DEF_WIDTH = 960
DEF_HEIGHT = 960

FPS = 30
WHITE = (255, 255, 255)
VERTEX_COUNT = 32
DEEP_DARK_FANTASIES = [-2, 8]  # ♂♂♂♂♂♂♂♂ WEE WEE ♂♂♂♂♂♂♂♂
VERTEX_ROUND_RADIUS_RANGE = [8, 96]
SPEED_RANGE = [-0.01, 0.01]
MAX_NORMAL_DISTANCE = DEF_HEIGHT / 2
LIGHT_RANGE = [0, 128]

for m in get_monitors():
    if isFullscreenreen is True:
        WIN_WIDTH = m.width
        WIN_HEIGHT = m.height
        proportion = numpy.median([(WIN_WIDTH / DEF_WIDTH), (WIN_HEIGHT / DEF_HEIGHT)])
    else:
        WIN_WIDTH = DEF_WIDTH
        WIN_HEIGHT = DEF_HEIGHT

async def main():
    clock = pygame.time.Clock()
    pygame.font.init()
    window_flags = pygame.SRCALPHA | pygame.NOFRAME  # | pygame.FULLscreenREEN
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), window_flags)
    screen.set_alpha(0)
    font = pygame.font.Font(None, 12)

    queue = Queue()
    listener = MicrophoneListener(queue)
    running = True
    vertexesArray = [Vertex() for _ in range(VERTEX_COUNT)]
    vertex_deep_color = 0
    
    for i in vertexesArray:
        i.round_pos = [randint(VERTEX_ROUND_RADIUS_RANGE[1], (WIN_WIDTH - VERTEX_ROUND_RADIUS_RANGE[1])), randint(VERTEX_ROUND_RADIUS_RANGE[1], (WIN_HEIGHT - VERTEX_ROUND_RADIUS_RANGE[1])), random.uniform(DEEP_DARK_FANTASIES[0], DEEP_DARK_FANTASIES[1])]
        i.radius = randint(VERTEX_ROUND_RADIUS_RANGE[0], VERTEX_ROUND_RADIUS_RANGE[1])
        if i.round_pos[2] >= 1.0:
            i.speed = random.uniform(SPEED_RANGE[0], SPEED_RANGE[1]) * i.round_pos[2]
        elif i.round_pos[2] <= -1.0:
            i.speed = random.uniform(SPEED_RANGE[0],SPEED_RANGE[1]) / -(i.round_pos[2])
        elif i.round_pos[2] > -1.0 and i.round_pos[2] < 1.0:
            i.speed = random.uniform(SPEED_RANGE[0], SPEED_RANGE[1])
        else:
            raise IndexError
    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if isDarkTheme:
            screen.fill((0, 0, 0, 0))
        else:
            screen.fill((255, 255, 255, 0))

        await listener.listen()
        if not queue.empty():
            amplitude = await queue.get()
            amplitude = numpy.clip((amplitude / 100), 1, 64)

        for i in vertexesArray:
            vertex_deep_color = (int(numpy.interp(i.round_pos[2], DEEP_DARK_FANTASIES, LIGHT_RANGE)))
            i.color = (vertex_deep_color, vertex_deep_color, vertex_deep_color)
            i.MoveVertex(amplitude)
            i.pos = [int(i.pos[0]), int(i.pos[1])]
            point_list = find_closest_points(i, vertexesArray, MAX_NORMAL_DISTANCE, amplitude)
            if len(point_list[0]) > 1:
                pygame.draw.aalines(screen, point_list[1], True, point_list[0], point_list[2])

        if isDebug is True:
            fps = numpy.round(clock.get_fps(), 2)
            fps_text = font.render(f"FPS: {str(fps)}", True, (255, 0, 0))
            screen.blit(fps_text, (10, 10))
            amplitude_text = font.render(f"Amp: {str(numpy.round(amplitude, 3))}", True, (255, 120, 0))
            screen.blit(amplitude_text, (10, 20))


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def find_closest_points(target_vertex, vertex_list, distance, amplitude):
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
        calculated_distance = numpy.sqrt(dx**2 + dy**2)
        # Если расстояние меньше заданного, добавляем точку в результаты
        if calculated_distance < distance:
            closest_vertexes.append(vertex.pos)
            closest_objects_color.append(vertex.color)
            closest_objects_z.append(vertex.round_pos[2])

    closest_vertexes.append(target_vertex.pos)
    closest_objects_color.append(target_vertex.color)
    closest_objects_z.append(target_vertex.round_pos[2])

    rounded_color = numpy.median(closest_objects_color)
    rounded_size = abs(numpy.median(closest_objects_z))
    rounded_size = (int(numpy.interp(rounded_size, DEEP_DARK_FANTASIES, [1, 2])))

    rounded_color = [rounded_color, rounded_color, rounded_color]
    rounded_color[1] = numpy.clip((rounded_color[1] * (1 + amplitude / 2)), 0, 255)
    rounded_color[2] = numpy.clip((rounded_color[2] * (1 + amplitude / 4)), 0, 255)
    rounded_size *= amplitude
    rounded_size = int(numpy.clip(rounded_size, 1, 32))

    rounded_color = (rounded_color[0], rounded_color[2], rounded_color[1])

    return [closest_vertexes, rounded_color, rounded_size]

if __name__ == "__main__":
    asyncio.run(main())
