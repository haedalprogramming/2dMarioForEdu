import pygame
from settings import (
    PLAYER_SPEED, JUMP_FORCE,
    PLAYER_SMALL_W, PLAYER_SMALL_H,
    PLAYER_BIG_W, PLAYER_BIG_H,
    INVINCIBLE_TIME,
    COLOR_PLAYER, COLOR_PLAYER_BIG,
)
from block import apply_gravity, move_and_collide

# Pygame 화면 좌표계: y가 아래 방향이 양수, 위 방향이 음수
# 그래서 JUMP_FORCE는 음수 값을 사용한다.


class Player:
    def __init__(self, x, y):
        self.rect     = pygame.Rect(x, y, PLAYER_SMALL_W, PLAYER_SMALL_H)
        self.vx       = 0.0
        self.vy       = 0.0
        self.on_ground = False

        self.is_big         = False
        self.is_invincible  = False
        self.invincible_timer = 0

    # ── 입력 처리 ──────────────────────────────

    def handle_input(self, keys):
        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and self.on_ground:
            self.vy = JUMP_FORCE

    # ── 업데이트 ────────────────────────────────

    def update(self, blocks):
        apply_gravity(self)
        move_and_collide(self, blocks)
        self._update_invincibility()

    def _update_invincibility(self):
        if self.is_invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.is_invincible = False

    # ── 상태 변화 ───────────────────────────────

    def grow(self):
        """버섯을 먹어 커짐. 발 위치(rect.bottom)는 유지."""
        if not self.is_big:
            self.is_big      = True
            bottom           = self.rect.bottom
            self.rect.width  = PLAYER_BIG_W
            self.rect.height = PLAYER_BIG_H
            self.rect.bottom = bottom

    def shrink(self):
        """몬스터에 맞아 작아짐 + 무적 시간 부여."""
        if self.is_big:
            self.is_big      = False
            bottom           = self.rect.bottom
            self.rect.width  = PLAYER_SMALL_W
            self.rect.height = PLAYER_SMALL_H
            self.rect.bottom = bottom
            self.is_invincible   = True
            self.invincible_timer = INVINCIBLE_TIME

    # ── 그리기 ──────────────────────────────────

    def draw(self, screen, offset_x):
        # 무적 중에는 깜빡임 효과 (짝수 프레임만 그림)
        if self.is_invincible and self.invincible_timer % 6 < 3:
            return

        color    = COLOR_PLAYER_BIG if self.is_big else COLOR_PLAYER
        draw_rect = pygame.Rect(
            self.rect.x - offset_x, self.rect.y,
            self.rect.width, self.rect.height,
        )
        pygame.draw.rect(screen, color, draw_rect)
        pygame.draw.rect(screen, (0, 0, 0), draw_rect, 2)
