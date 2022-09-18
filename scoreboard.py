import pygame
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    # a class to report scoring board

    # initilalize scoring attribute
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoring ifo
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        # show ships left at that time
        self.ships = Group()
        for ship_numer in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_numer* ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_level(self):
        # turn level into level image
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # postition the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        # turn high score into render image
        hight_score_str = "High Score - "+"{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(hight_score_str, True, self.text_color, self.settings.bg_color)

        # center the hight score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        # oldScore = open("highScore.txt", "r+"):
        # oldScore = int(f)
        # if oldScore < highScore:
        #     highScore < 


    def prep_score(self):
        # turn the score into a rendered image
        score_str = "Score - "+"{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        # draw score, high score, level, no of ships to the screen 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        # check for new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()