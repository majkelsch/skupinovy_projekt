# --- Konfigurační konstanty ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "Tahová RPG Hra"
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GREY = (150, 150, 150)
YELLOW = (200, 200, 0)

# Stavy hry
GAME_STATES = {
    "EXPLORATION": 0,
    "COMBAT": 1,
    "GAME_OVER": 2,
    "WIN": 3 # Win state here will mean completing a specific goal if implemented, not running out of rooms
}