from typing import List, Dict, Tuple, Union, Type
from pygame import sprite, Rect, Vector2
from .card import Card
from .player import Player
from .row import Row
import commons.enum as Commons

class Board():
    def __init__(self, width: float, height: float):
        self.cards: sprite.Group[Card] = sprite.Group()
        self.rows: sprite.Group[Row] = sprite.Group()
        self.rect: Rect = Rect(0, 0, width, height)

    def get_board_state(self) -> Dict[str, sprite.Group]:
        boardstate: Dict[str, Dict[int, Union[Tuple[Vector2, int], List[Tuple[Card, int]]]]] = {
            "cards": {card.id : (Vector2(card.rect.x, card.rect.y), card.location) for card in self.cards}, 
            "rows": {row.id: [(card, row.cards.index(card)) for card in row] for row in self.rows}
            }
        return boardstate
    
    def restore_board(self, boardstate: Dict[str, Dict[int, Union[Tuple[Vector2, int], List[Tuple[Card, int]]]]], deck: List[Card]) -> List[Card]:
        player_cards: List[Card] = deck
        self.cards.empty()
        for idx, data in boardstate["cards"].items():
            for card in deck:
                if card.id == idx:
                    card.set_position(data[0])
                    card.set_location(data[1])
                    card.get_played()
                    self.add_card(card)
                    player_cards.remove(card)
        
        self.rows.empty()
        for idx, data in boardstate["rows"].items():
            data.sort(key = lambda tupl: tupl[1])
            new_row = Row([item[0] for item in data], Vector2(data[0][0].rect.x, data[0][0].rect.y))
            new_row.align_cards()
            self.add_row(new_row)
        
        return player_cards
                    

    def get_row_with_card(self, card: Card) -> Union[Row, None]:
        for row in self.rows:
            if card in row.cards:
                return row
        return None
    
    def add_card(self, card: Card) -> None:
        if card not in self.cards:
            self.cards.add(card)
    
    def add_row(self, row: Row) -> None:
        if row not in self.rows:
            self.rows.add(row)
        for card in row.cards:
            self.add_card(card)
    
    def remove_from_all_rows(self, card: Card) -> None:
        for row in self.rows:
            if card in row.cards:
                row.cards.remove(card)
                if len(row.cards) == 0:
                    self.delete_row(row)
                else:
                    row.set_position(Vector2(row.cards[0].rect.x, row.cards[0].rect.y))
                    row.align_cards()
                

    def remove_from_board(self, card: Card, player: Player) -> None:
        self.remove_from_all_rows(card)
        if card in self.cards:
            self.cards.remove(card)
        card.location = Commons.LOCATIONS.HAND.value
        if card not in player.cards:
            player.cards.add(card)

    def delete_row(self, row: Row) -> None:
        if row in self.rows:
            self.rows.remove(row)