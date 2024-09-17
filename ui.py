import pygame
import time
from config import GameState,Config
from game import Game

class UIManager:
    def __init__(self):
        self.config = Config()
        self.font = pygame.font.SysFont(None, 66)
        self.game_state = GameState.MENU
        self.game = None
        self.last_update_time = 0

        self.background_music = pygame.mixer.Sound("resources/music/background_music.mp3")
        self.click_sound = pygame.mixer.Sound("resources/music/click_sound.mp3")

        pygame.mixer.init()  
        pygame.mixer.music.load(self.config.background_music) 
        pygame.mixer.music.play(-1) 

        self.settings_visible = False
        self.sound_on = True
        self.music_on = True
        self.sound_volume = 0.5
        self.music_volume = 0.5
        
        self.background_music.set_volume(self.music_volume)
        self.click_sound.set_volume(self.sound_volume)
        pygame.mixer.music.set_volume(self.music_volume)

        self.last_click_time = 0  # Time of the last click
        self.debounce_delay = 0.2  # 200 ms debounce delay

    def set_game(self, game):
        self.game = game

    def print(self, screen, game):
        #print different content based on the game state
        if self.game_state == GameState.MENU:
            self.print_menu(screen)
        elif self.game_state == GameState.READY:
            self.print_mode(screen)
            if self.settings_visible:  # Check if settings are visible
                self.print_settings(screen)   
        elif self.game_state == GameState.PLAYING:
            self.print_backgrounding(screen)
            self.print_time(screen, game.time)
            game.print(screen) 
        elif self.game_state == GameState.GAME_OVER1:
            self.print_menu2(screen)   
        elif self.game_state == GameState.GAME_OVER2:
            self.print_menu3(screen)       
             
    def print_mode(self, screen):
        chinese_font = pygame.font.Font('typeface/SimHei.ttf', 28)
        background_image = pygame.image.load('resources/picture/background2.jpg')  # Update with the correct path
        background_image = pygame.transform.scale(background_image, screen.get_size())  # Scale the image to fit the screen
        screen.blit(background_image, (0, 0))  # Draw the background at (0, 0)

        button_text = chinese_font.render("游戏规则：", True, (0, 0, 0))
        screen.blit(button_text, (50, 250))
        button_text = chinese_font.render("在给定时间内，玩家在点击卡牌后，", True, (0, 0, 0))
        screen.blit(button_text, (50, 300))
        button_text = chinese_font.render("卡牌会移动到屏幕下方的槽位中。", True, (0, 0, 0))
        screen.blit(button_text, (50, 350))
        button_text = chinese_font.render("槽位一共可以储存7张卡牌，", True, (0, 0, 0))
        screen.blit(button_text, (50, 400))
        button_text = chinese_font.render("槽内有三个相同的卡牌会进行消除。", True, (0, 0, 0))
        screen.blit(button_text, (50, 450))
        button_text = chinese_font.render("简单模式给定时间60s,1个图层", True, (0, 0, 0))
        screen.blit(button_text, (50, 500))
        button_text = chinese_font.render("困难模式给定时间100s，3个图层", True, (0, 0, 0))
        screen.blit(button_text, (50, 550))
        button_text = chinese_font.render("挑战模式给定时间120s，5个图层", True, (0, 0, 0))
        screen.blit(button_text, (50, 600))

        # easy mode
        easy_button = pygame.Rect(750, 250, 200, 80)
        pygame.draw.rect(screen, (0, 255, 0), easy_button)  # Main menu button
        easy_text = chinese_font.render("简单模式", True, (0, 0, 0))
        screen.blit(easy_text, (800, 270))

        # hard mode
        hard_button = pygame.Rect(750, 400, 200, 80)  # Adjust the position and size as needed
        pygame.draw.rect(screen, (0, 0, 255), hard_button)  # Mode button color
        hard_text = chinese_font.render("困难模式", True, (0, 0, 0))
        screen.blit(hard_text, (800, 420))  

        # hell mode
        hell_button = pygame.Rect(750, 550, 200, 80)  # Adjust the position and size as needed
        pygame.draw.rect(screen, (255, 0, 0), hell_button)  # Mode button color
        hell_text = chinese_font.render("挑战模式", True, (0, 0, 0))
        screen.blit(hell_text, (800, 570))  

        #设置按钮
        set_button = pygame.Rect(750, 100, 200, 80)  # Adjust the position and size as needed
        pygame.draw.rect(screen, (100, 100, 100), set_button)  # Mode button color
        set_text = chinese_font.render("设置", True, (0, 0, 0))
        screen.blit(set_text, (820, 120))

        mouse_pos = pygame.mouse.get_pos()  # Detect button clicks
        if pygame.mouse.get_pressed()[0]:
            if not self.settings_visible:  #避免在设置页面打开的时候，直接点击模式进入游戏，引起不必要的bug
                if easy_button.collidepoint(mouse_pos):
                    self.game.time = 60
                    self.game.set_maxlayer(1)  # Set maxlayer to 1
                    self.game_state = GameState.PLAYING
                elif hard_button.collidepoint(mouse_pos):
                    self.game.time = 100
                    self.game.set_maxlayer(3)  # Set maxlayer to 3
                    self.game_state = GameState.PLAYING
                elif hell_button.collidepoint(mouse_pos):
                    self.game.time = 120
                    self.game.set_maxlayer(5)  # Set maxlayer to 5
                    self.game_state = GameState.PLAYING
                elif set_button.collidepoint(mouse_pos):
                    self.settings_visible = True
                #print(f"Settings visible: {self.settings_visible}")  # Debug line

    def print_settings(self, screen):
        #print settings menu
        chinese_font = pygame.font.Font('typeface/SimHei.ttf', 36)
        pygame.draw.rect(screen, (255, 255, 255), (100, 100, 600, 400))
        self.sound_slider_rect = pygame.Rect(350, 300, 250, 20)   #音量调节条
        self.music_slider_rect = pygame.Rect(350, 350, 250, 20)   #音量调节条
        
        # Sound Button
        sound_text = chinese_font.render(f"点击音效: {'OFF' if self.sound_on else 'ON'}", True, (0, 0, 0))
        screen.blit(sound_text, (150, 150))
        sound2_text = chinese_font.render(f"点击音效:", True, (0, 0, 0))
        screen.blit(sound2_text, (150, 290))
        pygame.draw.rect(screen, (0, 0, 0), self.sound_slider_rect)
        pygame.draw.rect(screen, (0, 255, 0), (self.sound_slider_rect.left + int(self.sound_volume * self.sound_slider_rect.width), self.sound_slider_rect.top, 10, self.sound_slider_rect.height))

        # Music Button
        music_text = chinese_font.render(f"背景音乐: {'OFF' if self.music_on else 'ON'}", True, (0, 0, 0))
        screen.blit(music_text, (150, 220))
        music2_text = chinese_font.render(f"背景音乐:", True, (0, 0, 0))
        screen.blit(music2_text, (150, 340))
        pygame.draw.rect(screen, (0, 0, 0), self.music_slider_rect)
        pygame.draw.rect(screen, (0, 255, 0), (self.music_slider_rect.left + int(self.music_volume * self.music_slider_rect.width), self.music_slider_rect.top, 10, self.music_slider_rect.height))

        # Back Button
        back_button = pygame.Rect(500, 450, 200, 50)
        pygame.draw.rect(screen, (200, 50, 50), back_button)
        back_text = chinese_font.render("返回", True, (255, 255, 255))
        screen.blit(back_text, (back_button.left + 70, back_button.top + 10))

        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 600, 400), 2)  # Black border

        mouse_pos = pygame.mouse.get_pos()  # Detect button clicks
        mouse_pressed = pygame.mouse.get_pressed()[0]

        current_time = time.time()  # Get the current time in seconds

        if mouse_pressed and current_time - self.last_click_time > self.debounce_delay:
            if self.sound_slider_rect.collidepoint(mouse_pos):
                self.sound_volume = (mouse_pos[0] - self.sound_slider_rect.left) / self.sound_slider_rect.width
                self.sound_volume = min(max(self.sound_volume, 0), 1)
                self.click_sound.set_volume(self.sound_volume)  # Update sound effect volume
            if self.music_slider_rect.collidepoint(mouse_pos):
                self.music_volume = (mouse_pos[0] - self.music_slider_rect.left) / self.music_slider_rect.width
                self.music_volume = min(max(self.music_volume, 0), 1)
                pygame.mixer.music.set_volume(self.music_volume)  # Update music volume

            if back_button.collidepoint(mouse_pos):
                self.settings_visible = False  # Hide settings when back button is clicked
            if pygame.Rect(300, 150, 100, 50).collidepoint(mouse_pos):
                self.sound_on = not self.sound_on
            if pygame.Rect(300, 220, 100, 50).collidepoint(mouse_pos):
                self.music_on = not self.music_on

            # Toggle sound and music based on button states
            self.click_sound.set_volume(self.sound_volume if self.sound_on else 0)
            pygame.mixer.music.set_volume(self.music_volume if self.music_on else 0)

            self.last_click_time = current_time  # Update last click time

    def print_menu(self, screen):
        #渲染主菜单
        chinese_font = pygame.font.Font('typeface/SimHei.ttf', 48)
        background_image = pygame.image.load('resources/picture/background.png')  # Update with the correct path
        background_image = pygame.transform.scale(background_image, screen.get_size())  # Scale the image to fit the screen
        screen.blit(background_image, (0, 0))  # Draw the background at (0, 0)

        # Start Button
        start_button = pygame.Rect(650, 650, 200, 80)
        pygame.draw.rect(screen, (30, 125, 150), start_button)  # 主界面按钮
        button_text = chinese_font.render("开始游戏", True, (255, 255, 255))
        screen.blit(button_text, (650, 670))

        # Quit Button
        quit_button = pygame.Rect(150, 650, 200, 80)  # Adjust the position and size as needed
        pygame.draw.rect(screen, (200, 50, 50), quit_button)  # Quit button color
        quit_text = chinese_font.render("退出游戏", True, (255, 255, 255))
        screen.blit(quit_text, (150, 670))  # Adjust position as needed

        mouse_pos = pygame.mouse.get_pos()  # 检测按钮点击
        if pygame.mouse.get_pressed()[0]:
            if start_button.collidepoint(mouse_pos):
                self.game_state = GameState.READY
            elif quit_button.collidepoint(mouse_pos):
                pygame.quit()
                quit()  # Exit the application

    def print_time(self, screen, time):
        #在屏幕上渲染玩家的剩余时间
        chinese_font = pygame.font.Font('typeface/SimHei.ttf', 48)
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）

        # 检查是否已经过了 1 秒
        if current_time - self.last_update_time >= 1000 and self.game_state == GameState.PLAYING:
            if self.game.time > 0:
                self.game.time -= 1  # 每过 1 秒减少 1
            self.last_update_time = current_time  # 更新上次时间

        # 渲染剩余时间
        time_text = chinese_font.render(f"时间: {self.game.time}", True, (0, 0, 0))
        screen.blit(time_text, (750, 10))

        # 当时间为0时，可以设置游戏状态为结束
        if self.game.time == 0:
            self.game_state = GameState.GAME_OVER1

    def print_backgrounding(self, screen):
        backgrounding_image = pygame.image.load('resources/picture/background2.jpg')  # Update with the correct path
        backgrounding_image = pygame.transform.scale(backgrounding_image, screen.get_size())  # Scale the image to fit the screen
        screen.blit(backgrounding_image, (0, 0))  # Draw the background at (0, 0)

    def print_menu2(self, screen):
        """渲染主菜单"""
        chinese_font = pygame.font.Font('typeface/SimHei.ttf', 48)
        background_image = pygame.image.load('resources/picture/background.png')  # Update with the correct path
        background_image = pygame.transform.scale(background_image, screen.get_size())  # Scale the image to fit the screen
        screen.blit(background_image, (0, 0))  # Draw the background at (0, 0)

        # newgame Button
        newgame_button = pygame.Rect(600, 650, 200, 80)
        pygame.draw.rect(screen, (30, 125, 150), newgame_button)  # 主界面按钮
        button_text = chinese_font.render("新的游戏", True, (255, 255, 255))
        screen.blit(button_text, (600, 670))

        # Quit Button
        quit_button = pygame.Rect(200, 650, 200, 80)  # Adjust the position and size as needed
        pygame.draw.rect(screen, (200, 50, 50), quit_button)  # Quit button color
        quit_text = chinese_font.render("退出游戏", True, (255, 255, 255))
        screen.blit(quit_text, (200, 670))  # Adjust position as needed

        tip1_text = chinese_font.render("游戏结束！", True, (100, 0, 0))
        screen.blit(tip1_text, (400, 170))

        tip2_text = chinese_font.render("你失败了！", True, (100, 0, 0))
        screen.blit(tip2_text, (400, 220))

        mouse_pos = pygame.mouse.get_pos()  # 检测按钮点击
        if pygame.mouse.get_pressed()[0]:
            if newgame_button.collidepoint(mouse_pos):
                self.game_state = GameState.READY
                self.game.reset()
            elif quit_button.collidepoint(mouse_pos):
                pygame.quit()
                quit() 



    def print_menu3(self, screen):
        #渲染主菜单
        chinese_font = pygame.font.Font('typeface/SimHei.ttf', 48)
        background_image = pygame.image.load('resources/picture/background.png')  # Update with the correct path
        background_image = pygame.transform.scale(background_image, screen.get_size())  # Scale the image to fit the screen
        screen.blit(background_image, (0, 0))  # Draw the background at (0, 0)

        # newgame Button
        newgame_button = pygame.Rect(600, 650, 200, 80)
        pygame.draw.rect(screen, (30, 125, 150), newgame_button)  # 主界面按钮
        button_text = chinese_font.render("新的游戏", True, (255, 255, 255))
        screen.blit(button_text, (600, 670))

        # Quit Button
        quit_button = pygame.Rect(200, 650, 200, 80)  # Adjust the position and size as needed
        pygame.draw.rect(screen, (200, 50, 50), quit_button)  # Quit button color
        quit_text = chinese_font.render("退出游戏", True, (255, 255, 255))
        screen.blit(quit_text, (200, 670))  # Adjust position as needed

        tip1_text = chinese_font.render("游戏结束！", True, (0, 0, 100))
        screen.blit(tip1_text, (400, 170))

        tip2_text = chinese_font.render("你成功了！", True, (0, 0, 100))
        screen.blit(tip2_text, (400, 220))

        mouse_pos = pygame.mouse.get_pos()  # 检测按钮点击
        if pygame.mouse.get_pressed()[0]:
            if newgame_button.collidepoint(mouse_pos):
                self.game_state = GameState.READY
                self.game.reset()
            elif quit_button.collidepoint(mouse_pos):
                pygame.quit()
                quit()  # Exit the application


