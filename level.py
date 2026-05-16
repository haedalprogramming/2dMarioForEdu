from settings import TILE_SIZE, COLOR_BLOCK, COLOR_FLOOR
from block import Block, ItemBlock
from enemy import Enemy

# ──────────────────────────────────────────────
# ASCII 타일맵
# 문자 의미:
#   B = 일반 블록 (벽돌)
#   Q = 아이템 블록 (버섯)
#   E = 몬스터 스폰 위치
#   F = 바닥 (Floor, 더 어두운 색)
#   ' ' (공백) = 하늘
# ──────────────────────────────────────────────

TILE_MAP = [
    #0         1         2         3         4         5         6
    #0123456789012345678901234567890123456789012345678901234567890123456789
    "                                                                      ",  # 0
    "                                                                      ",  # 1
    "                    Q            Q    Q                               ",  # 2
    "                                                                      ",  # 3
    "      BBBBBB                         BBBBBB                           ",  # 4
    "                                                                      ",  # 5
    "          E       E         E                     E                   ",  # 6
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",  # 7 바닥
]


class Level:
    def __init__(self):
        self.blocks   = []
        self.enemies  = []
        self.mushrooms = []   # 게임 중 버섯이 추가되는 리스트
        self.player_start = (64, 192)
        self._load(TILE_MAP)

    def _load(self, tile_map):
        rows = len(tile_map)
        cols = max(len(row) for row in tile_map)
        self.world_width = cols * TILE_SIZE

        for row_idx, row in enumerate(tile_map):
            for col_idx, char in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE

                if char == 'B':
                    self.blocks.append(Block(x, y, TILE_SIZE, TILE_SIZE))
                elif char == 'F':
                    self.blocks.append(Block(x, y, TILE_SIZE, TILE_SIZE, COLOR_FLOOR))
                elif char == 'Q':
                    self.blocks.append(ItemBlock(x, y, TILE_SIZE))
                elif char == 'E':
                    # 몬스터는 타일 위에 올라와 있어야 하므로 y는 그대로 사용
                    self.enemies.append(Enemy(x, y - TILE_SIZE + TILE_SIZE, TILE_SIZE))

    def get_item_blocks(self):
        from block import ItemBlock
        return [b for b in self.blocks if isinstance(b, ItemBlock)]
