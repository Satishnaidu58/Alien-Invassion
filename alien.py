import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
   """ A class to represent A single Alien in the fleet"""

   def __init__(self, ai_game):
      """ Intialize the alien and set its starting position"""
      super().__init__()
      self.screen = ai_game.screen

      # Load the alien image and set rect attributes
      self.image = pygame.image.load("Images/alien.bmp")
      self.rect = self.image.get_rect()

      # start each new alien near alien near the top left of the screem
      self.rect.x = self.rect.width
      self.rect.y = self.rect.height

      # Store the alien's exact horizontal position
      self.x = float(self.rect.x)