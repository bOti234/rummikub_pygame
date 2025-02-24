from typing import List, Dict, Tuple, Union, Type
import random
from pygame import sprite
from .card import Card

class Player():
    counter = 0
    def __init__(self, name: str = "", is_cpu: bool = False) -> None:
        self.id: int = self.counter
        Player.counter += 1
        
        self.name: str = name
        self.cards: sprite.Group[Card] = sprite.Group()
        self.is_cpu: bool = is_cpu
        self.has_played_30: bool = False

    def has_card(self, colour: str, number: int, joker: bool = False) -> Union[Card | None]:
        if joker:
            for card in self.cards:
                if card.is_joker():
                    return card
        else:
            for card in self.cards:
                if card.colour == colour and card.number == number:
                    return card
        return None
                
    def has_card_id(self, id: int) -> Union[Card | None]:
        for card in self.cards:
            if card.id == id:
                return card
        return None
    
    def add_card(self, card: Card) -> None:
        if card not in self.cards:
            self.cards.add(card)

    def remove_card(self, card: Card) -> None:
        if card in self.cards:
            self.cards.remove(card)

    def draw_card(self, deck: sprite.Group) -> sprite.Group:
        if len(deck) == 0:
            return deck
        card: Card = random.choice(deck.sprites())
        self.cards.add(card)
        card.get_drawn()
        deck.remove(card)
        return deck
    
    def align_hand(self, screen_height) -> None:
        for n, card in enumerate(self.cards):
            card.rect.x = 40 + n * (10 + card.rect.width)
            card.rect.y = screen_height * 3 / 4 + 10

    def game_start(self, deck: sprite.Group, starting_cards_number: int = 14) -> sprite.Group:
        for _ in range(starting_cards_number):
            card: Card = random.choice(deck.sprites())
            self.cards.add(card)
            card.get_drawn()
            deck.remove(card)
        return deck