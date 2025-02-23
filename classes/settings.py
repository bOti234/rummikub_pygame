class Settings():
	def __init__(self, fps: int = 60, gamemode: str = "normal",  screen_width: int = 800, screen_height: int = 600, game_size: int = 40):
		self.fps: int = fps
		self.gamemode: str = gamemode
		self.screen_width: int = screen_width
		self.screen_height: int = screen_height
		self.fullscreen_width: int = screen_width
		self.fullscreen_height: int = screen_height
		self.game_size: int = game_size
		self.mastervolume: float = 0.5
		self.musicvolume: float = 0.5
		self.gamesoundvolume: float = 0.5