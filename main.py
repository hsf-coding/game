import pygame
from game import Game
from config import Config
from config import GameState
from ui import UIManager


def main():
        # 加载配置
        config = Config()

        pygame.init()
        screen = pygame.display.set_mode(config.get_screen_size())
        pygame.display.set_caption("猫了个猫")

        clock = pygame.time.Clock()

        ui_manager = UIManager()
        game = Game()
        ui_manager.set_game(game)


        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        game.grid.mouse_down = True
                        pos = pygame.mouse.get_pos()
                        game.grid.handle_click(pos, ui_manager)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  
                        game.grid.mouse_down = False

            screen.fill((255, 255, 255))  
            ui_manager.print(screen, game) 
            pygame.display.flip()
            clock.tick(30) 

        pygame.quit()



if __name__ == "__main__":
        main()
