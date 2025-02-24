from typing import List, Dict, Tuple, Union, Type
import random
import commons.enum as Commons
from pygame import sprite, Vector2
from .board import Board
from .card import Card
from .player import Player
from .row import Row

class CPU(Player):
    counter = 0
    def __init__(self) -> None:
        super().__init__("CPU"+str(self.counter), True)
        self.id: int = self.counter
        CPU.counter += 1

        self.available_cards: sprite.Group[Card] = self.cards

    def get_available_cards(self, cards: sprite.Group) -> sprite.Group:
        self.available_cards = sprite.Group(self.cards.sprites() + cards.sprites())
        return self.available_cards

    def simple_addition(self, board: Board) -> List[Tuple[Row, Card, int]]:
        played_cards: List[Tuple[Row, Card, int]] = []
        for card in self.cards:
            possible_rows = [row for row in board.rows if 
                             (card.number not in row.numbers and card.colour in row.colours and row.type == Commons.ROWTYPES.NUMBER.value) or 
                             (card.number in row.numbers and card.colour not in row.colours and row.type == Commons.ROWTYPES.COLOUR.value)
                            ]
            for row in possible_rows:
                idx = 0
                if len(row.cards) == 0:
                    continue
                if row.type == Commons.ROWTYPES.NUMBER.value:
                    while idx < len(row.cards) and card.number > row.cards[idx].number:
                        idx += 1
                if not row.validate_if_added(card, idx):
                    continue
                played_cards.append((row, card, idx))
        for triplet in played_cards:
            row, card, idx = triplet
            card.get_played()
            row.add_card(card, idx)
            board.add_card(card)
            self.available_cards.remove(card)
            self.cards.remove(card)
        return played_cards
    
    def find_30(self, board: Board) -> List[Tuple[Row, Card, int]]:
        played_cards: List[Tuple[Row, Card, int]] = []
        colours = [card.colour for card in self.cards]
        numbers = [card.number for card in self.cards]
        possible_colours = [colour for colour in set(colours) if colour != "white" and colours.count(colour) + colours.count("white") >= 3]
        possible_numbers = [number for number in set(numbers) if number != 0 and numbers.count(number) + numbers.count(0) >= 3]
        for card in self.cards:
            played_only_cards = [triplet[1] for triplet in played_cards]
            if card in played_only_cards:
                continue
            if card.number not in possible_numbers and card.colour not in possible_colours:
                continue
            elif card.number in possible_numbers:   # card can be added to a colour row
                considered_cards = [other for other in self.cards if (other.number == card.number or other.number == 0) and other not in played_only_cards]
                considered_cards_colours = [other.colour for other in self.cards]
                if (len(set(considered_cards_colours)) > 1 and considered_cards_colours.count("white") == 0) or (len(set(considered_cards_colours)) > 2):
                    continue
                if len(considered_cards) < 3:   # This list also has the card we are currently looking at
                    continue
                row = Row(considered_cards, Vector2(card.rect.x, card.rect.y))
                if not row.validate_row():
                    continue
                for c in considered_cards:
                    played_cards.append((row, c, row.cards.index(c)))
            else:   # card can be added to a number row
                considered_cards = [other for other in self.cards if (other.colour == card.colour or other.colour == "white") and other not in played_only_cards]
                if len(considered_cards) < 3:
                    continue
                considered_cards.sort(key = lambda c: c.number)
                row = Row(considered_cards, Vector2(card.rect.x, card.rect.y))
                if not row.validate_row():
                    continue
                for c in considered_cards:
                    played_cards.append((row, c, row.cards.index(c)))

        if sum(triplet[1].number for triplet in played_cards) < 30:
            return []

        for triplet in played_cards:
            row, card, idx = triplet
            card.get_played()
            if row not in board.rows:
                board.add_row(row)
            self.available_cards.remove(card)
            self.cards.remove(card)

        return played_cards