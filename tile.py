import pygame

TILE_SIZE = 80
MARGIN = 10  # 间隔大小

class Tile:
    def __init__(self, row, col, image_path, layer, offset_x=0, offset_y=0, margin=MARGIN):
        self.row = row
        self.col = col
        self.layer = layer  # 添加图层属性
        self.selected = False
        self.image_path = image_path
        self.image = pygame.image.load(image_path) if image_path else None
        self.size = TILE_SIZE
        self.margin = margin  # 间隔属性
        self.offset_x = offset_x
        self.offset_y = offset_y

    def set_image(self, image_path):
        self.image_path = image_path
        self.image = pygame.image.load(image_path) if image_path else None

    def print(self, screen):
        x = self.col * (self.size + self.margin) + self.offset_x
        y = self.row * (self.size + self.margin) + self.offset_y
        image = pygame.transform.scale(self.image, (self.size, self.size))
        screen.blit(image, (x, y))
        # 绘制方块的黑色边框
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.size, self.size), 2)

    def print_at(self, screen, x, y):#在指定位置渲染方块
        if self.image:
            image = pygame.transform.scale(self.image, (self.size, self.size))
            screen.blit(image, (x, y))
        else:
            color = (255, 0, 0) if self.selected else (0, 0, 255)
            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)

        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.size, self.size), 2)

    def can_be_clicked(self, top_layer):
        #判断方块是否可以被点击，只有最前面的图层才能点击
        return self.layer == top_layer

