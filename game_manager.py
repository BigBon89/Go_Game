import pygame


class GameManger:
    def __init__(self):
        self.font = None
        self.stone_black = None
        self.stone_white = None
        self.rock = None
        self.monster = None

    def load_assets(self):
        pygame.font.init()
        self.font = pygame.font.Font("assets/Verdana.ttf", 40)
        self.rock = pygame.image.load("image/rock.png")
        self.monster = pygame.image.load("image/monster.png")

