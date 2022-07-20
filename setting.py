class Settings:
   """A class to store all settings for Alien Invassion"""

   def __init__(self):
      """ initize the game's settings"""
      # Screen Settings
      # Creating the screen height and width
      self.screen_width = 1200
      self.screen_height = 800
      # Set Backgrounf color | Creating attribute for background color | RGB color
      self.bg_color = (230, 230, 230)

      # Ship speed 
      self.ship_speed = 1.2

      # Bullet settings
      self.bullet_speed = 1.0
      self.bullet_width = 3
      self.bullet_height = 15
      self.bullet_color = (60,60,60)
      self.bullet_allowed = 4
