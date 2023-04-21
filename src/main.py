import pygame

from catan.models.game import GameModel
from catan.views.game import GameView
from catan.views.menu import MenuView
from catan.views.newgame import NewGameView
from catan.controllers.game import GameController
from catan.util.pathresolver import resolve_path


SCREEN_FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = "The Settlers of Catan"
ICON_PATH = resolve_path("catan/assets/images/icon.png")


class Catan:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_icon(pygame.image.load(ICON_PATH))
        self.clock = pygame.time.Clock()
        
    
    def on_init(self):
        # testing saving and loading game files
        g = GameModel()
        GameModel.save_to_file(g, "game.json")
        
        # create game MVC
        self.game_model = GameModel.load_from_file("game.json")
        self.game_controller = GameController(self.game_model)

        self.game_view = GameView(self.game_controller, self)
        self.menu_view = MenuView(self)
        self.new_game_view = NewGameView(self)

        # initial view
        self.current_view = self.menu_view
        self.running = True


    def set_view(self, view):
        self.current_view = view


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        self.current_view.on_event(event)


    def on_update(self):
        self.current_view.on_update()
        self.clock.tick(30)


    def on_render(self):
        self.current_view.on_render(self.screen)
        pygame.display.flip()


    def on_execute(self):
        self.on_init()
        while(self.running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_update()
            self.on_render()
        self.on_cleanup()


    def on_cleanup(self):
        pygame.quit()


if __name__ == "__main__":
    c = Catan()
    c.on_execute()
