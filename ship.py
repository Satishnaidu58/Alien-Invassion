import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
   """A class to manage the ship"""

   def __init__(self, ai_game):
      """ Initiialize the ship and set it's starting loaction"""
      # initializing parent class constructor
      super().__init__()
      self.screen = ai_game.screen
      self.settings = ai_game.settings
      self.screen_rect = ai_game.screen.get_rect()

      # Load the ship image and get its rect
      self.image = pygame.image.load("Images/ship.bmp")
      self.rect = self.image.get_rect()

      # Start each new shipp at the bottom ceneter of the screen
      self.rect.midbottom = self.screen_rect.midbottom

      # store a decimal value for the ship's horizontal position
      self.x = float(self.rect.x)

      # Movement flag
      self.moving_right = False
      self.moving_left = False

   # movement of ship
   def update(self):
      """ Update the ship position based on the movement flag"""
      # update the ship's value, not the rectangle
      # Move right till right of screen
      if self.moving_right and self.rect.right < self.screen_rect.right:
         self.x += self.settings.ship_speed
      # move left till left of screen
      if self.moving_left and self.rect.left > 0:
         self.x -= self.settings.ship_speed

      # Update rect object from self.x 
      self.rect.x = self.x

   def blitme(self):
      """ Draw the ship at its current location"""
      self.screen.blit(self.image, self.rect)

   def center_ship(self):
      """center the ship on the screen"""
      self.rect.midbottom = self.screen_rect.midbottom
      self.x = float(self.rect.x)