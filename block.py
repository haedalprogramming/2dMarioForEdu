import pygame
from settings import (
    COLOR_BLOCK, COLOR_ITEM_BLOCK, COLOR_ITEM_USED,
    GRAVITY, MAX_FALL_SPEED,
)


# ──────────────────────────────────────────────
# 공유 물리 헬퍼 함수
# Player, Enemy, Mushroom 모두 이 함수를 재사용한다.
# ──────────────────────────────────────────────

def apply_gravity(entity):
    """매 프레임 중력을 적용한다. on_ground 플래그는 여기서 리셋."""
    if not entity.on_ground:
        entity.vy = min(entity.vy + GRAVITY, MAX_FALL_SPEED)
    entity.on_ground = False  # 충돌 해결 단계에서 True로 복원됨


def move_and_collide(entity, blocks):
    """
    분리축(Split-Axis) 충돌 해결:
    X 이동 → X 충돌 해결 → Y 이동 → Y 충돌 해결
    이 순서를 지켜야 모서리에서 끼는 버그를 방지할 수 있다.
    """
    # ── X축 ──
    entity.rect.x += int(entity.vx)
    for b in blocks:
        if entity.rect.colliderect(b.rect):
            if entity.vx > 0:
                entity.rect.right = b.rect.left
            else:
                entity.rect.left  = b.rect.right
            entity.vx = 0

    # ── Y축 ──
    entity.rect.y += int(entity.vy)
    for b in blocks:
        if entity.rect.colliderect(b.rect):
            if entity.vy > 0:       # 낙하 → 블록 위에 착지
                entity.rect.bottom = b.rect.top
                entity.on_ground   = True
            else:                   # 점프 중 블록 아래 충돌 → 블록 치기
                entity.rect.top = b.rect.bottom
                if isinstance(b, ItemBlock):
                    b.bump()
            entity.vy = 0


# ──────────────────────────────────────────────
# 블록 클래스
# ──────────────────────────────────────────────

class Block:
    def __init__(self, x, y, w, h, color=None):
        self.rect  = pygame.Rect(x, y, w, h)
        self.color = color or COLOR_BLOCK

    def draw(self, screen, offset_x):
        draw_rect = pygame.Rect(
            self.rect.x - offset_x, self.rect.y,
            self.rect.width, self.rect.height,
        )
        pygame.draw.rect(screen, self.color, draw_rect)
        # 테두리로 입체감 표현
        pygame.draw.rect(screen, (0, 0, 0), draw_rect, 1)


class ItemBlock(Block):
    """아래에서 치면 버섯이 나오는 노란 블록 (?)"""

    BUMP_FRAMES = 8   # 범프 애니메이션 지속 프레임

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, COLOR_ITEM_BLOCK)
        self.has_item    = True
        self.bumping     = False
        self.bump_timer  = 0
        self.bump_offset = 0      # 위로 튀어오르는 픽셀 오프셋

        # 버섯을 생성할 콜백 (main.py에서 주입)
        self.on_bump_callback = None

    def bump(self):
        if self.has_item and not self.bumping:
            self.bumping    = True
            self.bump_timer = self.BUMP_FRAMES
            self.has_item   = False
            self.color      = COLOR_ITEM_USED
            if self.on_bump_callback:
                self.on_bump_callback(self)

    def update(self):
        if self.bumping:
            progress = self.bump_timer / self.BUMP_FRAMES
            # 위로 8px 올라갔다가 내려오는 사인 곡선 모방
            self.bump_offset = int(-8 * progress * (1 - progress) * 4)
            self.bump_timer -= 1
            if self.bump_timer <= 0:
                self.bumping     = False
                self.bump_offset = 0

    def draw(self, screen, offset_x):
        draw_rect = pygame.Rect(
            self.rect.x - offset_x,
            self.rect.y + self.bump_offset,
            self.rect.width, self.rect.height,
        )
        pygame.draw.rect(screen, self.color, draw_rect)
        pygame.draw.rect(screen, (0, 0, 0), draw_rect, 1)
        # 아이템이 남아 있으면 '?' 표시
        if self.has_item:
            font = pygame.font.SysFont(None, 24)
            txt  = font.render("?", True, (0, 0, 0))
            screen.blit(txt, (draw_rect.x + 10, draw_rect.y + 8))
