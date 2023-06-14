import pygame
from settings import *
from player import Player
from sprites_object import *
from ray_casting import ray_casting
from drawing import Drawing
from menu import run_menu

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

choice = run_menu()
print('ok')
if choice == 1:
    pygame.mouse.set_visible(False)
    sc_map = pygame.Surface((MINIMAP_RES))

    sprites = Sprites()
    clock = pygame.time.Clock()
    player = Player()
    drawing = Drawing(sc, sc_map)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        player.movement()

        drawing.background(player_angle)
        walls = ray_casting(player, drawing.textures)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])

    #    drawing.world(player.pos, player.angle)

        drawing.fps(clock)
        drawing.mini_map(player)

        pygame.display.flip()
        clock.tick()
