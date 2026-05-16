import pygame
from settings import (
    ENEMY_SPEED, SQUISH_TIME, TILE_SIZE,
    COLOR_ENEMY, COLOR_ENEMY_SQUISH,
)
from block import apply_gravity, move_and_collide


class Enemy:
    def __init__(self, x, y, size=TILE_SIZE):
        self.rect        = pygame.Rect(x, y, size, size)
        self.vx          = -ENEMY_SPEED  # 처음엔 왼쪽으로 이동
        self.vy          = 0.0
        self.on_ground   = False
        self.alive       = True
        self.squish_timer = 0  # >0이면 납작해진 채로 잠시 대기

    def update(self, blocks):
        if not self.alive:
            if self.squish_timer > 0:
                self.squish_timer -= 1
            return

        apply_gravity(self)
        move_and_collide(self, blocks)
        self._check_edge(blocks)

    def _check_edge(self, blocks):
        """낭떠러지 앞에서 방향 전환."""
        if not self.on_ground:
            return
        # 현재 진행 방향 한 칸 앞 발아래를 확인
        look_x  = (self.rect.right + 2) if self.vx > 0 else (self.rect.left - 3)
        foot_y  = self.rect.bottom + 4
        probe   = pygame.Rect(look_x, foot_y, 2, 2)
        has_ground = any(probe.colliderect(b.rect) for b in blocks)
        if not has_ground:
            self.vx = -self.vx

    def squish(self):
        """플레이어에게 밟혔을 때 호출."""
        self.alive        = False
        self.squish_timer = SQUISH_TIME

    @property
    def should_remove(self):
        return not self.alive and self.squish_timer <= 0

    def draw(self, screen, offset_x):
        draw_x = self.rect.x - offset_x

        if not self.alive:
            # 납작하게 표시
            flat_rect = pygame.Rect(draw_x, self.rect.bottom - 8, self.rect.width, 8)
            pygame.draw.rect(screen, COLOR_ENEMY_SQUISH, flat_rect)
            return

        draw_rect = pygame.Rect(draw_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, COLOR_ENEMY, draw_rect)
        pygame.draw.rect(screen, (0, 0, 0), draw_rect, 2)

        # 눈 (방향에 따라 위치 변경)
        eye_y = draw_rect.y + 8
        if self.vx < 0:  # 왼쪽으로 이동 중
            pygame.draw.circle(screen, (255, 255, 255), (draw_x + 8,  eye_y), 4)
            pygame.draw.circle(screen, (0, 0, 0),       (draw_x + 7,  eye_y), 2)
        else:
            pygame.draw.circle(screen, (255, 255, 255), (draw_x + 24, eye_y), 4)
            pygame.draw.circle(screen, (0, 0, 0),       (draw_x + 25, eye_y), 2)
