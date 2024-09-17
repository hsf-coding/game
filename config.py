class Config:
    def __init__(self):
        # 游戏窗口配置，音乐配置
        self.screen_width = 1000
        self.screen_height = 800
        self.background_music = "resources/music/background_music.mp3"
        self.click_sound = "resources/music/click_sound.mp3"

    def get_screen_size(self):
        return (self.screen_width, self.screen_height)

class GameState:
    MENU = 1
    READY = 2
    PLAYING = 3
    GAME_OVER1 = 4
    GAME_OVER2 = 5