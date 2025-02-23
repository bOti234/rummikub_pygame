from typing import List, Dict, Tuple, Union, Type
from .card import Card
import commons.enum as Commons
from .errors import RowError
from pygame import Surface, sprite, draw, Rect, Vector2

class Row(sprite.Sprite):
    counter = 0
    def __init__(self, cards: List[Card], position: Vector2 = Vector2(0, 0)):
        '''
        cards: An already ordered list of cards in the row. The first element of the list is the leftmost card in the row. Jokers already inherited the card's colour and number they suppose to mimic.\n
        '''
        sprite.Sprite.__init__(self)
        self.id = self.counter
        Row.counter += 1

        self.position: Vector2 = position
        self.valid: bool = self.validate_row(cards)
        self.type: Union[int, None] = self.get_row_type(cards)
        self.cards: List[Card] = cards
        self.rect: Rect = self.calculate_rect(self.position.x, self.position.y)
        self.moving: bool = False

    def __iter__(self):
        return iter(self.cards)
    
    def __len__(self):
        return len(self.cards)

    def get_card_idx(self, card: Card) -> int:
        # if card not in self.cards:    # TODO: custom error for this as well
        #     return -1
        return self.cards.index(card)

    def add_card(self, card: Card, idx: int = 0) -> None:
        if card not in self.cards:
            self.cards.insert(idx, card)
        self.valid = self.validate_row(self.cards)

    def remove_card(self, card: Card) -> None:
        if card in self.cards:
            self.cards.remove(card)
        self.valid = self.validate_row(self.cards)

    def set_position(self, position: Vector2 = Vector2(0, 0)) -> None:
        self.position = position
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def add_hover_outlines(self) -> None:
        self.remove_hover_outlines()
        id_list: List[Tuple[int, int]] = []
        for idx in range(len(self.cards)):
            idxs_after = [item[0] for item in id_list]
            if self.cards[idx].hovered_side == Commons.HOVERED.LEFT.value:
                if idx in idxs_after:
                    continue
                id_list.append((idx, idx + len(id_list)))
            if self.cards[idx].hovered_side == Commons.HOVERED.RIGHT.value:
                if idx + 1 in idxs_after:
                    continue
                id_list.append((idx + 1, idx + len(id_list) + 1))

        for item in id_list:
            hover_card = Card("red", -1, False, Commons.LOCATIONS.BOARD.value, True)
            self.cards.insert(item[1], hover_card)

        self.align_cards()
    
    def remove_hover_outlines(self) -> None:
        new_cards_list: List[Card] = []
        for card in self.cards:
            if not card.is_hover_outline_card:
                new_cards_list.append(card)
        self.cards = new_cards_list


    def validate_row(self, cards: Union[List[Card], None] = None) -> bool:
        cards = cards if cards else self.cards
        if len(cards) < 3:
            return False
        try:
            self.set_jokers(cards)
        except RowError as e:
            print(e)
            return False
        colours_list = [card.colour for card in cards if not card.is_hover_outline_card]
        numbers_list = [card.number for card in cards if not card.is_hover_outline_card]
        if len(set(colours_list)) > 4:
            return False
        if len(set(colours_list)) == 1:  # number type
            for i in range(1, len(numbers_list)):
                if numbers_list[i] != numbers_list[i - 1] + 1:   # If the numbers are not in ascending order
                    if numbers_list[i] != 1 or numbers_list[i - 1] != 13:   # Cards can loop back at 13-1...
                        return False
        elif len(set(numbers_list)) == 1:   # colour type
            if len(set(colours_list)) != len(colours_list): # If there are duplicates in the list, meaning two colours are the same
                return False
        else:
            return False    # Tpye missmatch
        return True
    
    def set_jokers(self, cards: List[Card]):
        not_jokers = [card for card in cards if not card.is_joker]
        if len(not_jokers) == 0:
            return
        jokers = [card for card in cards if card.is_joker]
        if len(jokers) == len(cards):
            raise RowError.AllJokers()
        colours_list = [card.colour for card in cards if not card.is_hover_outline_card and not card.is_joker]
        numbers_list = [card.number for card in cards if not card.is_hover_outline_card and not card.is_joker]
        if len(set(colours_list)) == 1:     # number type
            for n, card in enumerate(cards):
                if not card.is_joker:
                    continue
                if n == 0:
                    k = 1
                    while n+k < len(cards) and cards[n+k].is_joker:
                        k += 1
                    if n+k == len(cards):
                        raise RowError.AllJokers()
                    card.mimic(cards[n+k].colour, cards[n+k].number - k)
                else:
                    card.mimic(cards[n-1].colour, cards[n-1].number + 1)
        elif len(set(numbers_list)) == 1:   # colour type
            available_colours = [colour for colour in Commons.COLOURS.NAMES.value if colour not in colours_list]
            for card in jokers:
                if len(available_colours) == 0:
                    raise RowError.UnfitJoker()
                if not card.is_joker:
                    continue
                card.mimic(available_colours[0], not_jokers[0].number)
                available_colours.pop(0)
                
                
    
    def set_valid(self, valid: bool = False) -> None:
        self.valid = valid

    def align_cards(self) -> None:
        for n, card in enumerate(self.cards):
            if card.moving:
                continue
            card.rect.x = self.rect.x + n * (10 + card.rect.width)
            card.rect.y = self.rect.y
        self.rect = self.calculate_rect(self.rect.x, self.rect.y)

    def calculate_rect(self, x: float, y: float) -> Rect:
        return Rect(x, y, sum(card.rect.width for card in self.cards) + (len(self.cards) - 1) * 10, max(card.rect.height for card in self.cards))
    
    def get_row_type(self, cards: List[Card]) -> Union[int, None]:
        colours_list = [card.colour for card in cards]
        numbers_list = [card.number for card in cards]
        if len(set(colours_list)) == 1:     # number type
            return Commons.ROWTYPES.NUMBER.value
        elif len(set(numbers_list)) == 1:   # colour type
            return Commons.ROWTYPES.COLOUR.value
        return None
    
    def set_moving(self, moving: bool) -> None:
        self.moving = moving
        for card in self.cards:
            card.set_moving(moving)
    
    def blit(self, screen: Surface) -> None:
        self.validate_row()
        self.add_hover_outlines()
        outer_rect = Rect(self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10)
        valid_colour = "green" if self.valid else "red"
        valid_rect = Rect(outer_rect.x + 3 , outer_rect.y + 3, outer_rect.width, outer_rect.height)
        draw.rect(screen, valid_colour, valid_rect, 6, 5)
        draw.rect(screen, "gray", outer_rect, 0, 5)
        draw.rect(screen, "black", outer_rect, 3, 5)
        

        for card in self.cards:
            card.blit(screen)
        self.remove_hover_outlines()