from typing import List, Dict, Tuple, Union, Type
import random, pygame, os
from pygame.locals import *
from pygame import sprite, mouse, Surface, Vector2
import pygame.locals
from .board import Board
from .button import Button
from .card import Card
from .cpu import CPU
from .player import Player
from .row import Row
from.settings import Settings
import commons.enum as Commons

class Game():
    singleton_instance = None

    def __init__(self, players: List[Union[Player, CPU]], gamemode: str, screen_width: int, screen_height: int):
        self.settings: Settings = Settings(
			fps = 60,
            gamemode = gamemode,
			screen_width = screen_width,
			screen_height = screen_height,
			game_size = 40
			)
        
        self.players: List[Union[Player, CPU]] = players
        self.winners: List[Union[Player, CPU]] = []
        self.previous_player_idx: int = None
        self.current_player: Union[Player, CPU] = None
        self.this_round_played_cards: sprite.Group[Card] = None
        self.this_round_returned_cards: sprite.Group[Card] = None
        self.deck: sprite.Group[Card] = self.generate_deck()
        self.board: Board = Board(self.settings.screen_width, self.settings.screen_height * 3 / 4 - 50)
        self.previous_boardstate: Dict[str, Dict[int, Union[Tuple[Vector2, int], List[Tuple[Vector2, int]]]]] = None
        self.screen: Surface = None

        self.holding_card: bool = False
        self.held_card: Union[None, Card] = None

        self.buttons: sprite.Group[Button] = self.generate_buttons()

        if not pygame.get_init():
            self.pygame_bootstrap()

    @staticmethod	# This is a really cool decorator and I should've used it more in this project
    def get_instance():       # Setting and returning the Game instance
        if Game.singleton_instance is None:
            Game.singleton_instance = Game()
		
        return Game.singleton_instance
    
    def remove_instance():    # Resetting the Game instance (for fixtures)
        Game.singleton_instance = None

    def generate_deck(self) -> sprite.Group:
        deck: sprite.Group[Card] = sprite.Group()
        for number in range(1, 14):
            for colour in Commons.COLOURS.NAMES.value:
                card1 = Card(colour, number, False, Commons.LOCATIONS.DECK.value)
                card2 = Card(colour, number, False, Commons.LOCATIONS.DECK.value)
                deck.add([card1, card2])
        deck.add([
            Card("white", 0, True, Commons.LOCATIONS.DECK.value),     # "black" and 1 gets replaced by None
            Card("white", 0, True, Commons.LOCATIONS.DECK.value),
        ])
        return deck
    
    def generate_buttons(self) -> sprite.Group:
        buttons: sprite.Group[Button] = sprite.Group()
        button1 = Button('end_turn_button', "lime", "End Turn", Commons.BUTTONTYPES.ENDTURN.value, 40, 150, 80, 
                        Vector2(self.settings.screen_width - 250, self.settings.screen_height * 3 / 4 - 100))
        
        button2 = Button('restore_button', "cyan", "Restore", Commons.BUTTONTYPES.RESTORE.value, 30, 100, 50, 
                        Vector2(self.settings.screen_width - 225, self.settings.screen_height * 3 / 4 + self.settings.screen_height * 1 / 5 - 80))
        
        buttons.add(button1, button2)
        return buttons
    
    def pygame_bootstrap(self) -> None:
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.HWSURFACE)

        self.sizeratio_x = self.settings.screen_width / self.settings.fullscreen_width
        self.sizeratio_y = self.settings.screen_height / self.settings.fullscreen_height
        x = (self.settings.fullscreen_width - self.settings.screen_width) // 2
        y = (self.settings.fullscreen_height - self.settings.screen_height) // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
        pygame.display.set_caption("Rummikub")

        self.time = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    def start(self):
        self.show_buttons(Commons.BUTTONTYPES.INGAME_BUTTONS.value)
        for player in self.players:
            self.deck = player.game_start(self.deck, 14)
            player.align_hand(self.settings.screen_height)
        self.current_player = random.choice(self.players)
        self.this_round_played_cards = sprite.Group()
        self.this_round_returned_cards = sprite.Group()
        self.start_turn()
        
    def next_turn(self) -> None:
        if self.current_player is None and self.previous_player_idx:
            player_id = self.previous_player_idx - 2 if len(self.players) >= self.previous_player_idx - 1 else self.previous_player_idx - 1
        else:
            player_id = self.players.index(self.current_player)
        next_player_id = 0 if player_id + 1 >= len(self.players) else player_id + 1
        self.current_player = self.players[next_player_id]
        self.this_round_played_cards = sprite.Group()
        self.this_round_returned_cards = sprite.Group()
        self.start_turn()

    def start_turn(self) -> None:
        print("Starting turn of "+self.current_player.name+"...")
        self.current_player.align_hand(self.settings.screen_height)
        self.previous_boardstate = self.board.get_board_state()
        if self.current_player.is_cpu:
            self.calculate_cpu_turn()
        else:
            self.turn_in_progress()

    def end_turn(self) -> None:
        if len(self.current_player.cards) == 0:
            self.winners.append(self.current_player)
            self.previous_player_idx = self.players.index(self.current_player)
            self.players.remove(self.current_player)
            self.current_player = None
            if len(self.players) == 0:
                return self.end_game()
        elif len(self.this_round_played_cards) == 0 and len(self.this_round_returned_cards) == 0:
            self.deck = self.current_player.draw_card(self.deck)
        if self.current_player and not self.current_player.has_played_30:
            self.current_player.has_played_30 = True
        self.next_turn()

    def end_game(self) -> None:
        print("Winners are:\n")
        for n in range(1, len(self.winners) + 1):
            print(str(n)+". "+self.winners[n].name)
        pygame.quit()

    def calculate_cpu_turn(self) -> None:
        if isinstance(self.current_player, CPU):
            played_cards = self.current_player.simple_addition(self.board) if self.current_player.has_played_30 else self.current_player.find_30(self.board)
            for triplet in played_cards:
                row, card, idx = triplet
                self.play_card(card)
            self.board.move_rows_inside(self.settings.screen_width, self.settings.screen_height)
            self.end_turn()

    def turn_in_progress(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.MOUSEBUTTONUP and event.button == BUTTON_LEFT:
                    self.check_button_hitboxes(buttonup = True)
            self.draw_background()
            self.draw_hand()
            self.draw_board()
            self.draw_buttons()

            self.check_valid_rows()
            if not self.current_player.has_played_30:
                self.check_first_round()

            self.check_card_hitboxes()

            pygame.display.flip() # flip() the display to put your work on self.screen

            self.calculate_cooldowns()

            self.dt = self.clock.tick(self.settings.fps) / 1000 # self.dt is delta time in seconds since last frame
            self.time += self.dt
             # Call end_turn() at one point

    def show_buttons(self, buttontypes: List[int]) -> None:
        for button in self.buttons:
            if button.type in buttontypes:
                button.set_shown(True)

    def draw_background(self) -> None:
        self.screen.fill("white")

    def draw_hand(self) -> None:
        handBox = pygame.Rect(30, self.settings.screen_height * 3 / 4, self.settings.screen_width - 60, self.settings.screen_height * 1 / 5)
        pygame.draw.rect(self.screen, "grey", handBox, 5, 5, 10, 10, 5, 5)
        for card in self.current_player.cards:
            card.blit(self.screen)
    
    def draw_board(self) -> None:
        for row in self.board.rows:
            row.blit(self.screen)

    def draw_buttons(self) -> None:
        for button in self.buttons:
            button.blit(self.screen)

    def check_first_round(self) -> None:
        valid = True
        if self.check_valid_rows():
            if sum(card.number for card in self.this_round_played_cards) < 30:
                for row in self.board.rows:
                    for card in self.this_round_played_cards:
                        if card in row:
                            row.set_valid(False)
                            valid = False
                            break
        else:
            valid = False
        for button in self.buttons:
            if button.type == Commons.BUTTONTYPES.ENDTURN.value:
                button.set_can_be_clicked(valid)
                break
        return valid

    def check_valid_rows(self) -> bool:
        valid = True
        for row in self.board.rows:
            row.valid = row.validate_row()
            if not row.valid:
                valid = False
                break
        for button in self.buttons:
            if button.type == Commons.BUTTONTYPES.ENDTURN.value:
                button.set_can_be_clicked(valid)
                break
        return valid
    
    def check_returned_cards(self) -> bool:
        if len(self.this_round_returned_cards) == 0:
            return True
        return False

    def check_card_hitboxes(self) -> None:
        mouseX, mouseY = mouse.get_pos()
        pressed = mouse.get_pressed()
        if pressed[0] and self.holding_card:    # When a card is being held (excluding the moment of releasing the card)
            self.held_card.blit(self.screen)    # redraw held card so it appears on top of everything
            self.move_card(self.held_card)
            self.check_card_card_hitbox(self.held_card)
        elif not pressed[0] and self.holding_card:  # When a card is released
            if self.held_card.rect.colliderect(self.board.rect):
                self.play_card(self.held_card)
            else:
                self.return_card_to_hand(self.held_card)
            hitbox_check_card = self.held_card
            self.put_down_card(self.held_card)
            self.check_card_card_hitbox(hitbox_check_card)
        else:   # When no card is currently being held (including the moment of releasing the card)
            for card in self.current_player.cards.sprites() + self.board.cards.sprites():
                if card.rect.collidepoint(mouseX, mouseY):  # When a card is hovered with the mouse
                    if pressed[0]:  # When the card is being picked up
                        self.pick_up_card(card, mouseX, mouseY)
                        self.move_card(self.held_card)
                        self.check_card_card_hitbox(self.held_card)

    def check_card_card_hitbox(self, card: Card) -> None:
        for other in self.board.cards:
            if card == other:   # other card is the same card
                other.set_hovered(Commons.HOVERED.NONE.value)
                continue
            if other.location != Commons.LOCATIONS.BOARD.value: # other card is not on board
                other.set_hovered(Commons.HOVERED.NONE.value)
                continue
            calculated_rect = pygame.Rect(other.rect.x - other.rect.width - 10, other.rect.y, other.rect.width*3/2 + 20, other.rect.height
                                          ) if other.hovered_side == Commons.HOVERED.LEFT.value else other.rect
            calculated_rect = pygame.Rect(other.rect.x, other.rect.y, other.rect.width*3/2 + 20, other.rect.height
                                          ) if other.hovered_side == Commons.HOVERED.RIGHT.value else calculated_rect
            if not card.rect.colliderect(calculated_rect):   # other card is not colliding with the card
                other.set_hovered(Commons.HOVERED.NONE.value)
                continue
            row = self.board.get_row_with_card(other)
            if self.holding_card and self.held_card == card:
                self.board.remove_from_all_rows(card)
                other_right_rect = pygame.Rect(other.rect.x + other.rect.width/2, other.rect.y, other.rect.width*3/2, other.rect.height)
                card_left_rect = pygame.Rect(card.rect.x, card.rect.y, card.rect.width/2, card.rect.height)
                if other_right_rect.colliderect(card_left_rect):    # Show outline on right side
                    other.set_hovered(Commons.HOVERED.RIGHT.value)
                else:
                    other.set_hovered(Commons.HOVERED.LEFT.value)
            else:   # Card is released -> They merge into a row
                if row: # other already in row. Card will be removed from all rows before the merge anyway
                    self.board.remove_from_all_rows(card)
                    idx = row.get_card_idx(other)
                    if other.hovered_side == Commons.HOVERED.RIGHT.value:
                        idx += 1
                    row.add_card(card, idx)
                else:   # new row needs to be created
                    self.board.remove_from_all_rows(card)
                    cards: List[Card] = [other]
                    if other.hovered_side == Commons.HOVERED.RIGHT.value:
                        position = Vector2(other.rect.x, other.rect.y)
                        cards.append(card)
                    else:
                        position = Vector2(card.rect.x, card.rect.y)
                        cards.insert(0, card)
                    row = Row(cards, position)
                    self.board.add_row(row)
                other.set_hovered(Commons.HOVERED.NONE.value)
                row.align_cards()
                row.valid = row.validate_row()

    def check_button_hitboxes(self, buttonup: bool = False) -> None:
        mouseX, mouseY = mouse.get_pos()
        if not buttonup or self.holding_card:
            return
        for button in self.buttons:
            if button.type == Commons.BUTTONTYPES.ENDTURN.value:
                for card in self.board.cards:
                        if card.is_joker:
                            print(card.colour, card.number)
            if not button.is_shown:
                continue
            if not button.can_be_clicked:
                continue
            if button.is_clicked:
                continue
            if not button.rect.collidepoint(mouseX, mouseY):
                continue
            button.set_on_cooldown()
            if button.type == Commons.BUTTONTYPES.RESTORE.value:
                self.restore_gamestate()
            elif button.type == Commons.BUTTONTYPES.ENDTURN.value:
                if self.check_valid_rows() and self.check_returned_cards():
                    self.end_turn()

    def restore_gamestate(self) -> None:
        available_cards = self.board.cards.sprites() + self.current_player.cards.sprites()
        player_cards = self.board.restore_board(self.previous_boardstate, available_cards)
        for card in self.current_player.cards:
            if card in self.board.cards:
                self.play_card(card)
                self.current_player.remove_card(card)
        for card in player_cards:
            self.return_card_to_hand(card)
            self.current_player.add_card(card)
        self.current_player.align_hand(self.settings.screen_height)

    def pick_up_card(self, card: Card, mouseX: int, mouseY: int) -> None:
        if self.holding_card:
            return
        card.set_moving(True)
        self.holding_card = True
        self.held_card = card
        card.set_held_position(Vector2(mouseX, mouseY))

    def put_down_card(self, card: Card) -> None:
        if not self.holding_card:
            return
        card.set_moving(False)
        self.holding_card = False
        self.held_card = None
        card.set_held_position()
        if card.location == Commons.LOCATIONS.BOARD.value:
            row = self.board.get_row_with_card(card)
            if row is None:
                row = Row([card], Vector2(card.rect.x, card.rect.y))
                self.board.add_row(row)
            elif not row.rect.colliderect(card.rect):   # card is outside of row -> creates a new row for the card
                self.board.remove_from_all_rows(card)
                row = Row([card], Vector2(card.rect.x, card.rect.y))
                self.board.add_row(row)
            self.current_player.remove_card(card)
        elif card.location == Commons.LOCATIONS.HAND.value:
            self.board.remove_from_board(card, self.current_player)
            self.current_player.add_card(card)

    def move_card(self, card: Card) -> None:
        if not self.holding_card or self.held_card != card:
            return
        mouseX, mouseY = mouse.get_pos()
        diffX = mouseX - card.held_position.x
        diffY = mouseY - card.held_position.y
        card.set_position(Vector2(card.rect.x + diffX, card.rect.y + diffY))
        card.set_held_position(Vector2(mouseX, mouseY))

    def calculate_cooldowns(self) -> None:
        for button in self.buttons:
            if button.cooldown_current > 0:
                button.cooldown_current -= self.dt
                if button.cooldown_current <= 0:
                    button.is_clicked = False
                    button.cooldown_current = 0

    def play_card(self, card: Card) -> None:
        card.get_played()
        if card not in self.this_round_returned_cards and card not in self.this_round_played_cards:
            self.this_round_played_cards.add(card)
        if card in self.this_round_returned_cards:
            self.this_round_returned_cards.remove(card)

    def return_card_to_hand(self, card: Card) -> None:
        card.return_to_hand()
        if card not in self.this_round_returned_cards and card not in self.this_round_played_cards:
            self.this_round_played_cards.add(card)
        if card in self.this_round_played_cards:
            self.this_round_played_cards.remove(card)