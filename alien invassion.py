from cmath import rect
import sys
from time import sleep
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import os

class AlienInvassion:
   """Overall class to manage game assets and behaviours"""

   def __init__(self):
      """Initailize the game, and create game resources"""
      pygame.init()
      self.settings = Settings()

      # Creating the screen
      self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
      pygame.display.set_caption("Alien Invassion")
      
      #Create an innstance to store game statistic and score board
      self.stats = GameStats(self)
      self.sb = Scoreboard(self)

      # Ship initialization
      self.ship = Ship(self) # Ship class takes 2 parameters,2nd parameter is ai, i.e self itsel. The AlienInavsion class itself.
      
      # Create Bullet
      self.bullets = pygame.sprite.Group()

      # create Alien
      self.aliens = pygame.sprite.Group()

      self._create_fleet()

      self.play_button = Button(self, "Play")

      # Set Backgrounf color | Creating attribute for background color | RGB color
      self.bg_color = self.settings.bg_color

   def run_game(self):
      """Start the main loop for the game"""
      while True:
         self.checkEvets()
         if self.stats.game_active:
            self.ship.update()
            # _at the begining as it's an helper method
            self._update_bullets()
            self._update_aliens()

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
         elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)

   def _check_play_button(self, mouse_pos):
      """start a new game when the player clicks play"""
      button_clicked = self.play_button.rect.collidepoint(mouse_pos)
      if self.play_button.rect.collidepoint(mouse_pos):
         # reset the game speed in settings with reseting dynamic settings
         self.settings.initialize_dynamic_settings()
         # reset the gae start first
         self.stats.reset_stats()
         self.stats.game_active = True
         self.sb.prep_score()
         self.sb.prep_level()

         # get rid of any remaining aliens and bullets
         self.aliens.empty()
         self.bullets.empty()

         # createba new fleet and center the ship
         self._create_fleet()
         self.ship.center_ship()
         
         # hide the mouse courser
         pygame.mouse.set_visible(False)
     
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
      #                           size gives 2 touples {int, int}
      alien_width, alien_height = alien.rect.size
      # letting a bit of space b/w two aliens to allowing them to move
      #                          calculating nu of aliens we can have
      available_space_x = self.settings.screen_width - (2 * alien_width) 
      # Alien + sapce for alien
      numbers_aliens_x = available_space_x // (2 * alien_width)

      # Determine the number of rows that fit on the screen
      ship_height = self.ship.rect.height
      available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
      number_rows = available_space_y // (2 * alien_height)

      # CREATE THE 1ST fleet of aliens
      # a nested for loop to control up and dows and alien rows
      for row_number in range(number_rows):
         for alien_number in range(numbers_aliens_x):
            self._create_alien(alien_number, row_number)

   def _check_fleet_edges(self):
      """respond appropriately if nay aliens have reached an edge"""
      for alien in self.aliens.sprites():
         if alien.check_edges():
            self._change_fleet_directions()
            break

   def _change_fleet_directions(self):
      """"Drop the entire fleet and change the fleet's direction"""
      for alien in self.aliens.sprites():
         alien.rect.y += self.settings.fleet_drop_speed
      # changiing the direction symbol to +1 -> -1 to change te direction
      self.settings.fleet_direction *= -1

   def _create_alien(self, alien_number, row_number):
      # Create an alien and place it in row
      alien = Alien(self)
      alien_width, alien_height = alien.rect.size
      alien.x = alien_width + (2* alien_width * alien_number)
      alien.rect.x = alien.x
      alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
      # self.aliens refers to the sprite group
      self.aliens.add(alien)

   def _update_aliens(self):
      """chec if the fleet is at the edge. Then, update the positions of all aliens in the fleet"""
      self._check_fleet_edges()
      self.aliens.update()
      #look for alien ship collision
      if pygame.sprite.spritecollideany(self.ship, self.aliens):
         self._ship_hit()

      # look for aliens hitting the ground
      self._check_aliens_bottom()

   def _ship_hit(self):
      """respond to ship being hit by the aliens"""
      if self.stats.ships_left > 0:
         # dec no of ship available and update score board for ships
         self.stats.ships_left -= 1
         self.sb.prep_ships()

         # get rid of any remaininga aliens and bullets
         self.aliens.empty()
         self.bullets.empty()

         # create a new float of aliens and center ship
         self._create_fleet()
         self.ship.center_ship()

         #pause
         sleep(0.5)
      else:
         self.stats.game_active = False
         pygame.mouse.set_visible(True)

   def _check_aliens_bottom(self):
      """check if any aliens are at the bottom""" 
      screen_rect = self.screen.get_rect() 
      for alien in self.aliens.sprites():
         if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship is hit
            self._ship_hit()
            break

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
      self._check_bullet_alien_collisions()

   def _check_bullet_alien_collisions(self):
      """Respond to bullet-alien collissions"""
      # check for any bullets that have hit an alien
      # if so, get rud of the bullet and the allien
      """I can costomise the hit, to hit and blast slow, and super bullet video 12, 3:00"""
      """ 
      groupcollide is a method created in sprite class takes 2 argument to begin with, "self.bullets, self.aliens" 
      if any of the grp'll overlap or collide. it create an dictionary[bullet] = alien
      """
      # what to happend with the entities after getting collide/detected to be collided with the aliem, [True, True], idx0 = bullet, idx1 = alien
      collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
      # collisions is a dic of all the collisiion happen
      if collisions:
         for aliens in collisions.values():
            self.stats.score += self.settings.alien_points * len(aliens)
         self.sb.prep_score()
         self.sb.check_high_score()

      # reloading the fleet after complete destruction of the fleet
      if not self.aliens:
         # destroy existing bulets and create new fleet
         self.bullets.empty()
         self._create_fleet()
         self.settings.increase_speed()

         # inc the level
         self.stats.level += 1
         self.sb.prep_level()
               
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

      # draw a score board
      self.sb.show_score()

      # draw the play button
      if not self.stats.game_active:
         self.play_button.draw_button()

      # Make the most recently drawn screen visible.
      pygame.display.flip()

if __name__ == '__main__':
   # make a game insatance, and run the game 
   ai = AlienInvassion()
   ai.run_game()