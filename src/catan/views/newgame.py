import pygame
from catan.controllers.game import GameController
from catan.models.game import GameModel

from catan.views.components.button import Button
from catan.util.pathresolver import resolve_path
from catan.views.components.textinput import TextInput
from catan.type import GameMode, PlayerType
from catan.views.game import GameView

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)
TITLE_FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 54)

WATER = pygame.image.load(resolve_path("catan/assets/images/water.png"))

PLAYER_COLOURS = ["red", "orange", "green", "blue", "purple"]

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f'{h:d}:{m:02d}:{s:02d}'


class NewGameView:

    def __init__(self, app):
        self.app = app

        self.time = 900  # seconds

        self.player_1_col = PLAYER_COLOURS[0]
        self.player_2_col = PLAYER_COLOURS[1]
        self.player_3_col = PLAYER_COLOURS[2]
        self.player_4_col = PLAYER_COLOURS[3]

        self.btn_menu = Button("Menu", (10, 10))

        self.btn_classic = Button("Classic (10VP)", (415, 150))
        self.btn_timed = Button("Time limited", (645, 150))

        self.btn_decr_time = Button("<", (1000, 150), size=(40, 50))
        self.txt_time = Button(format_time(self.time), (1050, 150), size=(100, 50))
        self.btn_incr_time = Button(">", (1160, 150), size=(40, 50))

        self.btn_player_1 = Button("Player", (415, 300), size=(105, 50))
        self.btn_ai_1 = Button("AI", (530, 300), size=(105, 50))
        self.ipt_name_1 = TextInput((645, 300))
        self.btn_decr_col_1 = Button("<", (1000, 300), size=(40, 50))
        self.box_col_1 = pygame.Surface((100, 50))
        self.btn_incr_col_1 = Button(">", (1160, 300), size=(40, 50))

        self.btn_player_2 = Button("Player", (415, 360), size=(105, 50))
        self.btn_ai_2 = Button("AI", (530, 360), size=(105, 50))
        self.ipt_name_2 = TextInput((645, 360))
        self.btn_decr_col_2 = Button("<", (1000, 360), size=(40, 50))
        self.box_col_2 = pygame.Surface((100, 50))
        self.btn_incr_col_2 = Button(">", (1160, 360), size=(40, 50))

        self.btn_player_3 = Button("Player", (415, 420), size=(105, 50))
        self.btn_ai_3 = Button("AI", (530, 420), size=(105, 50))
        self.ipt_name_3 = TextInput((645, 420))
        self.btn_decr_col_3 = Button("<", (1000, 420), size=(40, 50))
        self.box_col_3 = pygame.Surface((100, 50))
        self.btn_incr_col_3 = Button(">", (1160, 420), size=(40, 50))

        self.btn_player_4 = Button("Player", (415, 480), size=(105, 50))
        self.btn_ai_4 = Button("AI", (530, 480), size=(105, 50))
        self.ipt_name_4 = TextInput((645, 480))
        self.btn_decr_col_4 = Button("<", (1000, 480), size=(40, 50))
        self.box_col_4 = pygame.Surface((100, 50))
        self.btn_incr_col_4 = Button(">", (1160, 480), size=(40, 50))

        self.btn_start = Button("Start game", (530, 700))

        self.btn_classic.selected = True
        self.btn_player_1.selected = True
        self.btn_player_2.selected = True
        self.btn_player_3.selected = True
        self.btn_player_4.selected = True


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.btn_menu.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.menu_view)

                if self.btn_classic.rect.collidepoint(mouse_pos):
                    self.btn_classic.selected = True
                    self.btn_timed.selected = False

                if self.btn_timed.rect.collidepoint(mouse_pos):
                    self.btn_classic.selected = False
                    self.btn_timed.selected = True
                
                if self.btn_incr_time.rect.collidepoint(mouse_pos):
                    self.time = min(self.time + 300, 5400)  # 90 mins
                    self.txt_time.set_text(format_time(self.time))

                if self.btn_decr_time.rect.collidepoint(mouse_pos):
                    self.time = max(self.time - 300, 900)  # 15 mins
                    self.txt_time.set_text(format_time(self.time))

                if self.btn_player_1.rect.collidepoint(mouse_pos):
                    self.btn_player_1.selected = True
                    self.btn_ai_1.selected = False

                if self.btn_ai_1.rect.collidepoint(mouse_pos):
                    self.btn_player_1.selected = False
                    self.btn_ai_1.selected = True

                if self.btn_decr_col_1.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_1_col)
                    idx = (idx - 1) % len(PLAYER_COLOURS)
                    self.player_1_col = PLAYER_COLOURS[idx]

                if self.btn_incr_col_1.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_1_col)
                    idx = (idx + 1) % len(PLAYER_COLOURS)
                    self.player_1_col = PLAYER_COLOURS[idx]

                if self.btn_player_2.rect.collidepoint(mouse_pos):
                    self.btn_player_2.selected = True
                    self.btn_ai_2.selected = False

                if self.btn_ai_2.rect.collidepoint(mouse_pos):
                    self.btn_player_2.selected = False
                    self.btn_ai_2.selected = True

                if self.btn_decr_col_2.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_2_col)
                    idx = (idx - 1) % len(PLAYER_COLOURS)
                    self.player_2_col = PLAYER_COLOURS[idx]

                if self.btn_incr_col_2.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_2_col)
                    idx = (idx + 1) % len(PLAYER_COLOURS)
                    self.player_2_col = PLAYER_COLOURS[idx]

                if self.btn_player_3.rect.collidepoint(mouse_pos):
                    self.btn_player_3.selected = True
                    self.btn_ai_3.selected = False

                if self.btn_ai_3.rect.collidepoint(mouse_pos):
                    self.btn_player_3.selected = False
                    self.btn_ai_3.selected = True

                if self.btn_decr_col_3.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_3_col)
                    idx = (idx - 1) % len(PLAYER_COLOURS)
                    self.player_3_col = PLAYER_COLOURS[idx]

                if self.btn_incr_col_3.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_3_col)
                    idx = (idx + 1) % len(PLAYER_COLOURS)
                    self.player_3_col = PLAYER_COLOURS[idx]

                if self.btn_player_4.rect.collidepoint(mouse_pos):
                    self.btn_player_4.selected = True
                    self.btn_ai_4.selected = False

                if self.btn_ai_4.rect.collidepoint(mouse_pos):
                    self.btn_player_4.selected = False
                    self.btn_ai_4.selected = True

                if self.btn_decr_col_4.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_4_col)
                    idx = (idx - 1) % len(PLAYER_COLOURS)
                    self.player_4_col = PLAYER_COLOURS[idx]

                if self.btn_incr_col_4.rect.collidepoint(mouse_pos):
                    idx = PLAYER_COLOURS.index(self.player_4_col)
                    idx = (idx + 1) % len(PLAYER_COLOURS)
                    self.player_4_col = PLAYER_COLOURS[idx]

                if self.btn_start.rect.collidepoint(mouse_pos):
                    self.__start_game_with_settings()

                if self.ipt_name_1.rect.collidepoint(mouse_pos):
                    self.ipt_name_1.selected = True
                else:
                    self.ipt_name_1.selected = False

                if self.ipt_name_2.rect.collidepoint(mouse_pos):
                    self.ipt_name_2.selected = True
                else:
                    self.ipt_name_2.selected = False

                if self.ipt_name_3.rect.collidepoint(mouse_pos):
                    self.ipt_name_3.selected = True
                else:
                    self.ipt_name_3.selected = False

                if self.ipt_name_4.rect.collidepoint(mouse_pos):
                    self.ipt_name_4.selected = True
                else:
                    self.ipt_name_4.selected = False

        self.ipt_name_1.on_event(event)
        self.ipt_name_2.on_event(event)
        self.ipt_name_3.on_event(event)
        self.ipt_name_4.on_event(event)


    def on_update(self):
        pass


    def on_render(self, screen):
        screen.fill("black")
        screen.blit(WATER, (0, 0))

        title = TITLE_FONT.render("New game", True, "white")
        width, _ = title.get_rect().size
        screen.blit(title, (1280/2 - width/2, 50))

        self.btn_menu.draw(screen)

        screen.blit(FONT.render("Game mode", True, "white"), (275, 165))
        self.btn_classic.draw(screen)
        self.btn_timed.draw(screen)

        screen.blit(FONT.render("Time limit", True, "white"), (1055, 115))
        self.btn_decr_time.draw(screen)
        self.txt_time.draw(screen)
        self.btn_incr_time.draw(screen)

        screen.blit(FONT.render("Type", True, "white"), (500, 265))
        screen.blit(FONT.render("Enter name", True, "white"), (690, 265))
        screen.blit(FONT.render("Colour", True, "white"), (1065, 265))

        screen.blit(FONT.render("Player 1", True, "white"), (275, 315))
        self.btn_player_1.draw(screen)
        self.btn_ai_1.draw(screen)
        self.ipt_name_1.draw(screen)
        self.btn_decr_col_1.draw(screen)
        self.box_col_1.fill(self.player_1_col)
        screen.blit(self.box_col_1, (1050, 300))
        self.btn_incr_col_1.draw(screen)

        screen.blit(FONT.render("Player 2", True, "white"), (275, 375))
        self.btn_player_2.draw(screen)
        self.btn_ai_2.draw(screen)
        self.ipt_name_2.draw(screen)
        self.btn_decr_col_2.draw(screen)
        self.box_col_2.fill(self.player_2_col)
        screen.blit(self.box_col_2, (1050, 360))
        self.btn_incr_col_2.draw(screen)

        screen.blit(FONT.render("Player 3", True, "white"), (275, 435))
        self.btn_player_3.draw(screen)
        self.btn_ai_3.draw(screen)
        self.ipt_name_3.draw(screen)
        self.btn_decr_col_3.draw(screen)
        self.box_col_3.fill(self.player_3_col)
        screen.blit(self.box_col_3, (1050, 420))
        self.btn_incr_col_3.draw(screen)

        screen.blit(FONT.render("Player 4", True, "white"), (275, 495))
        self.btn_player_4.draw(screen)
        self.btn_ai_4.draw(screen)
        self.ipt_name_4.draw(screen)
        self.btn_decr_col_4.draw(screen)
        self.box_col_4.fill(self.player_4_col)
        screen.blit(self.box_col_4, (1050, 480))
        self.btn_incr_col_4.draw(screen)

        self.btn_start.draw(screen)


    def __start_game_with_settings(self):
        

        game_type = GameMode.FIRST_TO_TEN if self.btn_classic.selected else GameMode.TIME_LIMIT

        player_1_type = PlayerType.PLAYER if self.btn_player_1.selected else PlayerType.AI
        player_2_type = PlayerType.PLAYER if self.btn_player_2.selected else PlayerType.AI
        player_3_type = PlayerType.PLAYER if self.btn_player_3.selected else PlayerType.AI
        player_4_type = PlayerType.PLAYER if self.btn_player_4.selected else PlayerType.AI

        player_1_name = self.ipt_name_1.input_text if self.ipt_name_1.input_text != "" else "Player 1"
        player_2_name = self.ipt_name_2.input_text if self.ipt_name_2.input_text != "" else "Player 2"
        player_3_name = self.ipt_name_3.input_text if self.ipt_name_3.input_text != "" else "Player 3"
        player_4_name = self.ipt_name_4.input_text if self.ipt_name_4.input_text != "" else "Player 4"


        self.app.game_model = GameModel(game_mode=game_type,
                                        game_time_limit=self.time,
                                        player_1_type = player_1_type,
                                        player_2_type = player_2_type,
                                        player_3_type = player_3_type,
                                        player_4_type = player_4_type,
                                        player_1_name = player_1_name,
                                        player_2_name = player_2_name,
                                        player_3_name = player_3_name,
                                        player_4_name = player_4_name,
                                        player_1_colour = self.player_1_col,
                                        player_2_colour = self.player_2_col,
                                        player_3_colour = self.player_3_col,
                                        player_4_colour = self.player_4_col
                                        )

        self.app.game_controller = GameController(self.app.game_model)
        self.app.game_view = GameView(self.app.game_controller, self.app)

        self.app.set_view(self.app.game_view)
