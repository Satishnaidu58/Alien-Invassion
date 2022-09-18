class Settings:
   """A class to store all settings for Alien Invassion"""

   def __init__(self):
      """ initize the game's static settings"""
      # Screen Settings
      # Creating the screen height and width
      self.screen_width = 1200
      self.screen_height = 800
      # Set Backgrounf color | Creating attribute for background color | RGB color
      self.bg_color = (230, 230, 230)

      # Ship speed 
      self.ship_speed = 1.2
      self.ship_limit = 3

      # Bullet settings
      self.bullet_speed = 1.0
      self.bullet_width = 3
      self.bullet_height = 15
      self.bullet_color = (60,60,60)
      self.bullet_allowed = 4

      # Alien settings
      self.alien_speed = 1.0
      # downwards movement
      self.fleet_drop_speed = 7
      # settings for to and fro mothion | x - axis direction = [1, -1]
      self.fleet_direction = 1

      # how fast game speedup
      self.speedup_scale = 1.1

      self.initialize_dynamic_settings()

   def initialize_dynamic_settings(self):
      # initialize settings that changes on levelup's
      self.ship_speed = 1.2
      self.bullet_speed = 1.0
      self.alien_speed = 1.0
      # settings for to and fro mothion | x - axis direction = [1, -1]
      self.fleet_direction = 1

      # score
      self.alien_points = 1

   def increase_speed(self):
      # increse the speeed for level-ups
      self.ship_speed *= self.speedup_scale
      self.bullet_speed *= self.speedup_scale
      self.alien_speed *= self.speedup_scale
      
