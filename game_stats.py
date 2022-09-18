from setting import Settings



class GameStats:
    """Track statistics for Alien invassion"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        
        # start alien invassion game in active state
        self.game_active = False
        # high score shouldn't be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
