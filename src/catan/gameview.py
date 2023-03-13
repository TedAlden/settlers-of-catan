import pygame
from .board import Board
from .type import ActionType


class GameView:

    def __init__(self):
        # testing board saving/loading always works
        b = Board.make_random()
        Board.save_to_file(b, "board.json")
        self.board = Board.load_from_file("board.json")

        self.selected = []
        self.action = ActionType.PLACE_ROAD


    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                mouse_pos = pygame.mouse.get_pos()
                for settlement in self.board.settlements:
                    if settlement.rect.collidepoint(mouse_pos):
                        self._on_click_settlement(event, settlement)

                for terrain in self.board.terrain_tiles.values():
                    if terrain.rect.collidepoint(mouse_pos):
                        self._on_click_terrain(event, terrain)


    def on_update(self):
        pass


    def on_render(self, screen):
        screen.fill("#65cee0")

        for terrain_tile in self.board.terrain_tiles.values():
            terrain_tile.draw(screen)

        for node1, node2 in self.board.roads:
            pygame.draw.line(screen, "red", node1.get_pos(), node2.get_pos(), width=20)

        for settlement in self.board.settlements:
            if settlement.owner is not None:
                settlement.draw(screen)

            else:
                colour = "red" if settlement.selected else "#cccccc"
                pygame.draw.circle(screen, colour, settlement.get_pos(), settlement.radius)
    

    def _on_click_settlement(self, event, settlement):
        if self.action == ActionType.PLACE_ROAD:
            # select first settlement
            if len(self.selected) == 0:
                self.selected.append(settlement)
                settlement.selected = True

            elif len(self.selected) == 1:
                # select second settlement
                if settlement not in self.selected \
                        and settlement in self.board.get_surrounding_nodes(self.selected[0]):

                    self.selected.append(settlement)
                    if not self.board.has_road(*self.selected):
                        self.board.add_road(*self.selected)
                    # deselect settlements when road successfully placed
                    self.selected[0].selected = False
                    self.selected[1].selected = False
                    self.selected.clear()

                # deselect the first settlement
                elif settlement == self.selected[0]:
                    self.selected[0].selected = False
                    self.selected.clear()

        elif self.action == ActionType.PLACE_SETTLEMENT:    
            pass
    

    def _on_click_terrain(self, event, terrain):
        if self.action == ActionType.PLACE_ROBBER:
            pass
