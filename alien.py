import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
   """ A class to represent A single Alien in the fleet"""

   def __init__(self, ai_game):
      """ Intialize the alien and set its starting position"""
      super().__init__()
      self.screen = ai_game.screen
      self.settings = ai_game.settings

      # Load the alien image and set rect attributes
      self.image = pygame.image.load("Images/alien.bmp")
      self.rect = self.image.get_rect()

      # start each new alien near alien near the top left of the screem
      self.rect.x = self.rect.width
      self.rect.y = self.rect.height

      # Store the alien's exact horizontal position
      self.x = float(self.rect.x)
   

   def update(self):
      """Move the alien to the right or left"""
      self.x += (self.settings.alien_speed * self.settings.fleet_direction)
      self.rect.x = self.x

   def check_edges(self):
      """ If one of the alien checks the edge, return True if alien is at edge of screen"""
      screen_rect = self.screen.get_rect()
      if self.rect.right >= screen_rect.right or self.rect.left <= 0:
         return True