from enum import Enum


class GameState(Enum):
    PLAYING = "playing"
    DEAD    = "dead"   # 게임 오버
    WIN     = "win"    # 클리어 (추후 구현)
