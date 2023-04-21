import pygame
import os

from catan.views.components.button import Button
from catan.views.components.textinput import TextInput
from catan.util.pathresolver import resolve_path

FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 18)
TITLE_FONT = pygame.font.Font(resolve_path("catan/assets/fonts/EightBitDragon-anqx.ttf"), 54)
SAVES_PATH = resolve_path("saves")  # src/saves/


class LoadGameView:

    def __init__(self, app):
        self.app = app

        self.saves = os.listdir(SAVES_PATH)
        self.saves_per_page = 5

        self.page = 1
        self.last_page = len(self.saves) // self.saves_per_page + 1
        self.page_info = self.__format_page_text(self.page, self.last_page)

        self.btn_menu = Button("Menu", (10, 10))

        self.btn_load_1 = Button("Load", (500, 150))
        self.btn_del_1 = Button("Delete", (730, 150))

        self.btn_load_2 = Button("Load", (500, 250))
        self.btn_del_2 = Button("Delete", (730, 250))

        self.btn_load_3 = Button("Load", (500, 350))
        self.btn_del_3 = Button("Delete", (730, 350))

        self.btn_load_4 = Button("Load", (500, 450))
        self.btn_del_4 = Button("Delete", (730, 450))

        self.btn_load_5 = Button("Load", (500, 550))
        self.btn_del_5 = Button("Delete", (730, 550))

        self.btn_prev_page = Button("<", (540, 700), size=(40, 50))
        self.txt_page = Button(f"{self.page_info}", (590, 700), size=(100, 50))
        self.btn_next_page = Button(">", (700, 700), size=(40, 50))


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.btn_menu.rect.collidepoint(mouse_pos):
                    self.app.set_view(self.app.menu_view)

                if self.btn_load_1.rect.collidepoint(mouse_pos):
                    pass

                if self.btn_load_1.rect.collidepoint(mouse_pos):
                    pass

                if self.btn_prev_page.rect.collidepoint(mouse_pos):
                    self.page = max(self.page - 1, 1)
                    self.page_info = self.__format_page_text(self.page, self.last_page)
                    self.txt_page.set_text(self.page_info)

                if self.btn_next_page.rect.collidepoint(mouse_pos):
                    self.page = min(self.page + 1, self.last_page)
                    self.page_info = self.__format_page_text(self.page, self.last_page)
                    self.txt_page.set_text(self.page_info)


    def on_update(self):
        pass


    def on_render(self, screen):
        screen.fill("black")

        title = TITLE_FONT.render("Load games", True, "white")
        width, _ = title.get_rect().size
        screen.blit(title, (1280/2 - width/2, 50))

        self.btn_menu.draw(screen)

        

        self.btn_prev_page.draw(screen)
        self.txt_page.draw(screen)
        self.btn_next_page.draw(screen)

        # start and finish indices of the save files in the saves list
        # that are on the current page
        start = self.saves_per_page * (self.page - 1)
        finish = min(self.saves_per_page * (self.page), len(self.saves))

        for i in range(start, finish):
            ri = i % self.saves_per_page
            screen.blit(FONT.render(self.saves[i], True, "white"), (275, 165+100*ri))

            if ri == 0:
                self.btn_load_1.draw(screen)
                self.btn_del_1.draw(screen)

            elif ri == 1:
                self.btn_load_2.draw(screen)
                self.btn_del_2.draw(screen)

            elif ri == 2:
                self.btn_load_3.draw(screen)
                self.btn_del_3.draw(screen)

            elif ri == 3:
                self.btn_load_4.draw(screen)
                self.btn_del_4.draw(screen)

            elif ri == 4:
                self.btn_load_5.draw(screen)
                self.btn_del_5.draw(screen)
    
    def __format_page_text(self, current_page, last_page):
        return f"{current_page} / {last_page}"


