import pygame
from pygame.sprite import Sprite # Able to create ultiple bullet as a grp using sprite

class Bullet(Sprite): # bullet is as a child class of Sprite
   """ A class to manage bullets fired from the ship"""

   def __init__(self, ai_game):
      """ Create a bullet object at the ship's curent position"""
      super().__init__() # Calls the init method of it's parent class Sprint
      self.screen = ai_game.screen
      self.settings = ai_game.settings
      self.color = self.settings.bullet_color

      # Create A bullet rect at (0, 0) and set correct position | # pygame.Rect is a class,
      #  that will set a rectangle of bulet's height and width
      self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) 
      self.rect.midtop = ai_game.ship.rect.midtop

      # Store the bullet's position as decimal value
      self.y = float(self.rect.y)

   def update(self):
      """ Move the bullet up the screen"""
      # Update the decimal position of the bullet 
      self.y -= self.settings.bullet_speed
      # Update the rectangle position
      self.rect.y = self.y

   def draw_bullet(self):
      """ Draw the bullet to the screen"""
      pygame.draw.rect(self.screen, self.color, self.rect)