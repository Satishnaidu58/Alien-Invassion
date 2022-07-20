import sys
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvassion:
   """Overall class to manage game assets and behaviours"""

   def __init__(self):
      """Initailize the game, and create game resources"""
      pygame.init()
      self.settings = Settings()

      # Creating the screen
      self.screen = pygame.display.set_mode(
         (self.settings.screen_width, self.settings.screen_height))
      pygame.display.set_caption("Alien Invassion")
      
      # Ship initialization
      self.ship = Ship(self) # Ship class takes 2 parameters,2nd parameter is ai, i.e self itsel. The AlienInavsion class itself.
      
      # Create Bullet
      self.bullets = pygame.sprite.Group()

      # create Alien
      self.aliens = pygame.sprite.Group()

      self._create_fleet()

      # Set Backgrounf color | Creating attribute for background color | RGB color
      self.bg_color = self.settings.bg_color

   def run_game(self):
      """Start the main loop for the game"""
      while True:
         self.checkEvets()
         self.ship.update()
         self._update_bullets()
         self._update_screen()

   def checkEvets(self):
      """Reaspond to keypress and mouse evenst"""
      # Watch for keyboard and mouse events 
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            sys.exit()
         elif event.type == pygame.KEYDOWN:
            self.checkKeyDownEvents(event)
         elif event.type == pygame.KEYUP:
            self.checkKeyUpEvents(event)
         
   def checkKeyDownEvents(self, event):
      """ Respond to keyPress and mouse events"""
      # Move Right
      if event.key == pygame.K_RIGHT:
         self.ship.moving_right = True # Contiously move the ship to right on keyPress
      # Move Left
      if event.key == pygame.K_LEFT:
         self.ship.moving_left = True  #  Contiously move the ship to left on keyPress
      elif event.key == pygame.K_q:
         sys.exit()
      elif event.key == pygame.K_SPACE:
         self._fire_bullet() # helper method
         
   def checkKeyUpEvents(self, event):
      """ Resond to KEY RELEASE """
      # Stop Moving Right
      if event.key == pygame.K_RIGHT:
         self.ship.moving_right = False # stop moving the ship to right on keyUp
      # Stop Moving Left
      if event.key == pygame.K_LEFT:
         self.ship.moving_left = False # stop moving the ship to left on KeyUp

   def _create_fleet(self):
      """ Create the fleet of aliens"""
      # Create an alien and find the nu of aliens in a row
      # spacing b/w each aliens is to one alien width

      alien = Alien(self)
      alien_width = alien.rect.width
      available_space_x = self.settings.screen_width - (2 * alien_width) # letting a bit of space b/w two aliens to allowing them to move
      # calculating nu of aliens we can have
      numbers_aliens_x = available_space_x // (2 * alien_width) #Alien + sapce for alien

      # CREATE THE 1ST ROW
      for alien_number in range(numbers_aliens_x):
         self._create_alien(alien_number)


   def _create_alien(self, alien_number):
      # Create an alien and place it in row
      alien = Alien(self)
      alien_width = alien.rect.width










      
      """ ********** 16:19 video 10**********"""
      alien.x = alien_width + (2* alien_width * alien_number)
      alien.rect.x = alien.x
      self.aliens.add(alien) #self.aliens refers to the sprite group

   def _fire_bullet(self):
      """ Create a new bullet and it to the bullets group"""
      if len(self.bullets) < self.settings.bullet_allowed:
         new_bullet = Bullet(self)
         self.bullets.add(new_bullet)
   
   def _update_bullets(self):
      """ Update the position of bullets and get rid of old bullets"""
      # Update the position
      self.bullets.update()
      # Get rid of bullets that have disappeared
      for bullet in self.bullets.copy():
         if bullet.rect.bottom <= 0:
            self.bullets.remove(bullet)
         # print(len(self.bullets))
               
   def _update_screen(self):
      """ Update images on the screen, and """
      # Redraw the screen during each pass through the loop | using settings class
      self.screen.fill(self.bg_color)
      # Redraw the ship
      self.ship.blitme()
      # redraw bullet
      for bullet in self.bullets.sprites():
         bullet.draw_bullet()
      # Reddraw aliens
      self.aliens.draw(self.screen)

      # Make the most recently drawn screen visible.
      pygame.display.flip()


if __name__ == '__main__':
   # make a game insatance, and run the game 
   ai = AlienInvassion()
   ai.run_game()