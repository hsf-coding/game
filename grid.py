import pygame
import random
from tile import Tile
from config import GameState

GRID_SIZE = 6
TILE_SIZE = 80
MARGIN = 30
MATCH_COUNT = 3

class Grid:
    def __init__(self, maxlayer):
        self.maxlayer = maxlayer
        self.tiles = []
        self.clicked_tiles = []
        self.image_paths = [
            'resources/picture/tile1.jpg',
            'resources/picture/tile2.jpg',
            'resources/picture/tile3.jpg',
            'resources/picture/tile4.jpg',
            'resources/picture/tile5.jpg',
            'resources/picture/tile6.jpg',
            'resources/picture/tile7.jpg',
            'resources/picture/tile8.jpg',
            'resources/picture/tile9.jpg',
            'resources/picture/tile10.jpg',
            'resources/picture/tile11.jpg',
            'resources/picture/tile12.jpg'
        ]
        self.mouse_down = False
        self.create_grid()

    def create_grid(self):
        # 初始化网格
        num_tiles_per_image = (GRID_SIZE * GRID_SIZE * self.maxlayer) // len(self.image_paths)
        num_tiles_per_image = (num_tiles_per_image // 3) * 3
        tiles_list = [image_path for image_path in self.image_paths for _ in range(num_tiles_per_image)]
        
  
        random.shuffle(tiles_list)
        
        self.tiles = [
            [
                [Tile(row, col, tiles_list.pop(), layer, offset_x=layer*5, offset_y=layer*5, margin=MARGIN)
                 for layer in range(self.maxlayer)]
                for col in range(GRID_SIZE)
            ]
            for row in range(GRID_SIZE)
        ]

    def handle_click(self, pos, ui_manager):
        if not self.mouse_down:
            return

        ui_manager.click_sound.play()
        x, y = pos

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                top_tile = self.get_top_tile(row, col)
                if top_tile:
                    tile_x = col * (TILE_SIZE + MARGIN) + top_tile.offset_x
                    tile_y = row * (TILE_SIZE + MARGIN) + top_tile.offset_y

                    if tile_x <= x < tile_x + TILE_SIZE and tile_y <= y < tile_y + TILE_SIZE:
                        if top_tile.can_be_clicked(self.get_top_layer(row, col)):
                            self.clicked_tiles.append((top_tile, top_tile.image_path))
                            new_image = random.choice(self.image_paths)
                            top_tile.set_image(new_image)
                            self.remove_top_tile(row, col)
                            self.check_for_matches(ui_manager)
                        return



    def is_grid_empty(self):
        for row in self.tiles:
            for layers in row:
                for tile in layers:
                    if tile is not None:
                        return False
        return True
    
    def remove_top_tile(self, row, col):
        #移除指定位置的最上层方块
        for i in range(len(self.tiles[row][col]) - 1, -1, -1):
            if self.tiles[row][col][i]:
                self.tiles[row][col][i] = None
                break

    def check_for_matches(self, ui_manager):
        #检查底部区域是否有匹配的方块
        matches = self.find_matches()
        if matches:
            self.remove_matches(matches)  
        if not matches and self.no_match_count() >= 7:
            ui_manager.game_state = GameState.GAME_OVER1
        if self.is_grid_empty():
            ui_manager.game_state = GameState.GAME_OVER2
        

    def find_matches(self):
        #查找底部区域的匹配方块
        image_count = {}
        matches = []

        for _, image_path in self.clicked_tiles:
            if image_path in image_count:
                image_count[image_path] += 1
            else:
                image_count[image_path] = 1

        for image_path, count in image_count.items():
            if count >= MATCH_COUNT:
                matched_tiles = [(tile, img) for tile, img in self.clicked_tiles if img == image_path]
                matches.append(matched_tiles[:MATCH_COUNT])
        return matches

    def remove_matches(self, matches):
        #移除匹配的方块
        for match in matches:
            for tile, _ in match:
                self.clicked_tiles.remove((tile, _))  

    def no_match_count(self):
        image_count = {}
        for _, image_path in self.clicked_tiles:
            if image_path in image_count:
                image_count[image_path] += 1
            else:
                image_count[image_path] = 1

        non_three_match_patterns = 0

        for count in image_count.values():
            if count < 3:
                non_three_match_patterns += count
        return non_three_match_patterns

    def print(self, screen):
        for row in self.tiles:
            for layers in row:
                for tile in layers:
                    if tile:
                        tile.print(screen)
        self.print_bottom(screen)

    def print_bottom(self, screen):
        bottom_width = (TILE_SIZE + MARGIN) * 7
        bottom_x = 15
        bottom_y = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN

        pygame.draw.rect(screen, (0, 0, 0), (bottom_x - MARGIN, bottom_y - MARGIN, bottom_width + 2 * MARGIN,120), 2)

        for i, (tile, original_image_path) in enumerate(self.clicked_tiles):
            if i >= 7:
                break
            x = bottom_x + i * (TILE_SIZE + MARGIN)
            y = bottom_y
            temp_tile = Tile(tile.row, tile.col, original_image_path, tile.layer, margin=MARGIN)
            temp_tile.print_at(screen, x, y)

    def get_top_tile(self, row, col):
        #获取指定位置的最上层方块
        for tile in reversed(self.tiles[row][col]):
            if tile:
                return tile
        return None

    def get_top_layer(self, row, col):
        #获取指定位置的最上层图层编号
        return max(tile.layer for tile in self.tiles[row][col] if tile)
