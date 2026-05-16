import sys
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    JUMP_FORCE,
    COLOR_SKY, COLOR_WHITE, COLOR_BLACK, COLOR_RED,
)
from game_state import GameState
from camera    import Camera
from player    import Player
from level     import Level
from item      import Mushroom


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.font   = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 28)
        self._reset()

    def _reset(self):
        self.level  = Level()
        self.player = Player(*self.level.player_start)
        self.camera = Camera(self.level.world_width)
        self.state  = GameState.PLAYING

        # 아이템 블록에 버섯 생성 콜백 연결
        for block in self.level.get_item_blocks():
            block.on_bump_callback = self._spawn_mushroom

    # ── 버섯 생성 ────────────────────────────────

    def _spawn_mushroom(self, block):
        # 블록 위 중앙에서 버섯 생성
        m = Mushroom(block.rect.x + 4, block.rect.y - block.rect.height)
        self.level.mushrooms.append(m)

    # ── 메인 루프 ────────────────────────────────

    def run(self):
        while True:
            self._handle_events()
            if self.state == GameState.PLAYING:
                self._update()
            self._draw()
            self.clock.tick(FPS)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.state == GameState.DEAD:
                    self._reset()

        keys = pygame.key.get_pressed()
        if self.state == GameState.PLAYING:
            self.player.handle_input(keys)

    # ── 업데이트 ────────────────────────────────

    def _update(self):
        blocks = self.level.blocks

        # 아이템 블록 애니메이션 업데이트
        for block in self.level.get_item_blocks():
            block.update()

        # 플레이어 업데이트
        self.player.update(blocks)

        # 플레이어가 화면 아래로 떨어지면 시작 위치로 리스폰
        if self.player.rect.top > SCREEN_HEIGHT + 100:
            x, y = self.level.player_start
            self.player.rect.topleft = (x, y)
            self.player.vx = 0
            self.player.vy = 0
            return

        # 몬스터 업데이트
        for enemy in self.level.enemies:
            enemy.update(blocks)
        self.level.enemies = [e for e in self.level.enemies if not e.should_remove]

        # 버섯 업데이트
        for mushroom in self.level.mushrooms:
            mushroom.update(blocks)

        # 충돌 판정
        self._check_player_enemy_collisions()
        self._check_player_mushroom_collisions()

        # 카메라 업데이트
        self.camera.update(self.player.rect)

    def _check_player_enemy_collisions(self):
        STOMP_THRESHOLD = 12  # 픽셀 허용 오차

        for enemy in self.level.enemies:
            if not enemy.alive:
                continue
            if not self.player.rect.colliderect(enemy.rect):
                continue

            # 밟기 판정: 플레이어가 낙하 중이고 발이 몬스터 머리 근처에 있을 때
            stomped = (
                self.player.vy > 0
                and self.player.rect.bottom <= enemy.rect.top + STOMP_THRESHOLD
            )

            if stomped:
                enemy.squish()
                # 바운스 (반 점프력)
                self.player.vy = JUMP_FORCE // 2
            else:
                # 옆이나 아래에서 충돌
                if not self.player.is_invincible:
                    if self.player.is_big:
                        self.player.shrink()
                    else:
                        self.state = GameState.DEAD

    def _check_player_mushroom_collisions(self):
        for mushroom in self.level.mushrooms:
            if mushroom.collected:
                continue
            if self.player.rect.colliderect(mushroom.rect):
                mushroom.collected = True
                self.player.grow()

    # ── 그리기 ──────────────────────────────────

    def _draw(self):
        self.screen.fill(COLOR_SKY)

        offset_x = self.camera.offset_x

        # 블록
        for block in self.level.blocks:
            block.draw(self.screen, offset_x)

        # 버섯
        for mushroom in self.level.mushrooms:
            mushroom.draw(self.screen, offset_x)

        # 몬스터
        for enemy in self.level.enemies:
            enemy.draw(self.screen, offset_x)

        # 플레이어
        self.player.draw(self.screen, offset_x)

        # HUD
        self._draw_hud()

        # 게임 오버 오버레이
        if self.state == GameState.DEAD:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hud(self):
        state_text = "BIG" if self.player.is_big else "SMALL"
        hud = self.small_font.render(f"상태: {state_text}", True, COLOR_WHITE)
        self.screen.blit(hud, (10, 10))

    def _draw_game_over(self):
        # 반투명 검정 오버레이
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        text1 = self.font.render("GAME OVER", True, COLOR_RED)
        text2 = self.small_font.render("R 키를 눌러 재시작", True, COLOR_WHITE)
        self.screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, 180))
        self.screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 250))


if __name__ == "__main__":
    Game().run()
