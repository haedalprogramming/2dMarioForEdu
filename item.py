import pygame
from settings import MUSHROOM_SPEED, TILE_SIZE, COLOR_MUSHROOM
from block import apply_gravity, move_and_collide


class Mushroom:
    def __init__(self, x, y):
        size      = TILE_SIZE - 4
        self.rect = pygame.Rect(x, y, size, size)
        self.vx   = MUSHROOM_SPEED  # 항상 오른쪽으로 이동
        self.vy   = 0.0
        self.on_ground = False
        self.collected = False

    def update(self, blocks):
        if self.collected:
            return
        apply_gravity(self)
        move_and_collide(self, blocks)

    def draw(self, screen, offset_x):
        if self.collected:
            return
        draw_rect = pygame.Rect(
            self.rect.x - offset_x, self.rect.y,
            self.rect.width, self.rect.height,
        )
        pygame.draw.ellipse(screen, COLOR_MUSHROOM, draw_rect)
        pygame.draw.ellipse(screen, (0, 0, 0), draw_rect, 2)
        # 버섯 점
        cx, cy = draw_rect.centerx, draw_rect.centery - 4
        pygame.draw.circle(screen, (255, 255, 255), (cx - 5, cy), 3)
        pygame.draw.circle(screen, (255, 255, 255), (cx + 5, cy), 3)
