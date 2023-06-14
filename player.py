from settings import *
import pygame
import math
from map import world_map
from ray_casting import mapping
from menu import get_sens
from menu import run_menu


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.sens = get_sens()
        # collisions parameters
        self.side = 50


    @property
    def pos(self):
        return self.x, self.y

    def detect_collisions(self, dx, dy):
        if dx != 0:
            delta_x = (self.side // 2) * abs(dx) / dx
            if mapping(self.x + dx + delta_x, self.y + delta_x) in world_map:
                dx = 0
            if mapping(self.x + dx + delta_x, self.y - delta_x) in world_map:
                dx = 0
        if dy != 0:
            delta_y = (self.side // 2) * abs(dy) / dy
            if mapping(self.x + delta_y, self.y + dy + delta_y) in world_map:
                dy = 0
            if mapping(self.x - delta_y, self.y + dy + delta_y) in world_map:
                dy = 0
        self.x += dx
        self.y += dy
#        print(dx, '   ', dy)

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.mouse.set_visible(True)
            run_menu()
            # print("menu otkrito")
        if keys[pygame.K_SPACE]:
            if keys[pygame.K_w]:
                dx = player_speed * cos_a * 3
                dy = player_speed * sin_a * 3
                self.detect_collisions(dx, dy)
            if keys[pygame.K_s]:
                dx = -player_speed * cos_a * 3
                dy = -player_speed * sin_a * 3
                self.detect_collisions(dx, dy)
        else:
            if keys[pygame.K_w]:
                dx = player_speed * cos_a
                dy = player_speed * sin_a
                self.detect_collisions(dx, dy)
            if keys[pygame.K_s]:
                dx = -player_speed * cos_a
                dy = -player_speed * sin_a
                self.detect_collisions(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collisions(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collisions(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.005
        if keys[pygame.K_RIGHT]:
            self.angle += 0.005

    def mouse_control(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += diff * self.sens

