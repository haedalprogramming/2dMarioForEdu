from settings import SCREEN_WIDTH


class Camera:
    def __init__(self, world_width):
        self.offset_x   = 0
        self.world_width = world_width

    def update(self, player_rect):
        # 플레이어를 화면 중앙에 맞추되, 레벨 경계 밖으로 나가지 않게 클램프
        target = player_rect.centerx - SCREEN_WIDTH // 2
        self.offset_x = max(0, min(target, self.world_width - SCREEN_WIDTH))

    def apply(self, rect):
        # 실제 그릴 위치를 반환 (월드 좌표 → 화면 좌표)
        import pygame
        return pygame.Rect(rect.x - self.offset_x, rect.y, rect.width, rect.height)
