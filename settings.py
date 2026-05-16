# 게임 전체 설정 상수 모음 - 이 파일만 수정하면 게임 느낌을 바꿀 수 있어!

# 화면
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 500
FPS           = 60
TITLE         = "2D 마리오 클론"

# 물리
GRAVITY        = 0.6    # 매 프레임 vy에 더해지는 값 (클수록 무거움)
MAX_FALL_SPEED = 14     # 낙하 최대 속도 (픽셀/프레임)
JUMP_FORCE     = -14    # 점프 시 vy 초기값 (음수 = 위 방향)

# 플레이어
PLAYER_SPEED     = 4
PLAYER_SMALL_W   = 32
PLAYER_SMALL_H   = 32
PLAYER_BIG_W     = 32
PLAYER_BIG_H     = 58
INVINCIBLE_TIME  = 120  # 무적 지속 프레임 수 (60fps 기준 2초)

# 몬스터
ENEMY_SPEED      = 2
SQUISH_TIME      = 20   # 밟힌 후 사라지기까지 프레임 수

# 버섯
MUSHROOM_SPEED   = 2

# 타일
TILE_SIZE        = 32

# 색상 (R, G, B)
COLOR_SKY          = (107, 140, 255)
COLOR_PLAYER       = (220, 50,  50)   # 작은 마리오 (빨강)
COLOR_PLAYER_BIG   = (255, 140,  0)   # 큰 마리오 (주황)
COLOR_ENEMY        = (139,  90, 43)   # 몬스터 (갈색)
COLOR_ENEMY_SQUISH = (100,  60, 20)   # 밟힌 몬스터
COLOR_BLOCK        = (180, 120, 60)   # 일반 벽돌 블록
COLOR_ITEM_BLOCK   = (255, 200,  0)   # 아이템 블록 (노랑)
COLOR_ITEM_USED    = (160, 130, 80)   # 사용된 블록 (회색빛)
COLOR_MUSHROOM     = (255,  50,  50)  # 버섯
COLOR_FLOOR        = ( 80,  80,  80)  # 바닥
COLOR_WHITE        = (255, 255, 255)
COLOR_BLACK        = (  0,   0,   0)
COLOR_RED          = (255,   0,   0)
