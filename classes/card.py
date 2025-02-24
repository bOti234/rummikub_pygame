from typing import List, Dict, Tuple, Union, Type
from .errors import CardError
import commons.enum as Commons
from pygame import Surface, sprite, draw, Rect, font, Vector2

class Card(sprite.Sprite):
    counter = 0
    def __init__(self, colour: str, number: int, is_joker: bool = False, location: int = Commons.LOCATIONS.DECK.value, is_hover_outline_card: bool = False, position: Vector2 = Vector2(0, 0)):
        sprite.Sprite.__init__(self)
        self.id = self.counter
        Card.counter += 1

        self.location: int = location
        self.rect: None = None
        self.position: Vector2 = position
        self.rect: Rect = Rect(self.position.x, self.position.y, 50, 70)
        self.moving: bool = False
        self.hovered: bool = False
        self.hovered_side: int = Commons.HOVERED.NONE.value
        self.is_hover_outline_card: bool = is_hover_outline_card
        self.held_position: Union[None, Vector2] = None
        self.is_joker: bool = is_joker
        if self.is_joker:
            self.valid: bool = True
            self.colour: str = "white"
            self.number: int = 0
        else:
            self.valid: bool = self.validate_card(colour, number)
            self.colour: str = colour
            self.number: int = number

    def __str__(self):  # TODO: remove id
        if self.is_joker:
            return "joker id "+str(self.id)
        return self.colour+" "+str(self.number)+" id "+str(self.id)
    
    def __repr__(self):
        return self.__str__()

    def validate_card(self, colour: str, number: int) -> bool:
        if colour not in Commons.COLOURS.NAMES.value:
            return False
        if number > 13 or number < 0:
            return False
        return True
    
    def validate_colour(self, colour: str) -> bool:
        if colour not in Commons.COLOURS.NAMES.value:
            return False
        return True
    
    def validate_number(self, number: int) -> bool:
        if number > 13 or number < 0:
            return False
        return True
    
    def set_colour(self, new_colour: str) -> None:
        if not self.validate_colour(new_colour):
            raise CardError.ColourError()
        if not self.is_joker:
            raise CardError.JokerError()
        self.colour = new_colour
        return None

    def set_number(self, new_number: int) -> None:
        if not self.validate_number(new_number):
            raise CardError.NumberError()
        if not self.is_joker:
            raise CardError.JokerError()
        self.number = new_number
        return None
    
    def set_location(self, location: int = Commons.LOCATIONS.DECK.value) -> None:
        if location in Commons.LOCATIONS.LOCATIONS.value:
            self.location = location

    def mimic(self, colour: str, number: int) -> None:
        self.set_colour(colour)
        self.set_number(number)

    def unmask(self) -> None:
        if not self.is_joker:
            raise CardError.JokerError()
        self.colour = "white"
        self.number = 0

    def return_to_hand(self) -> None:
        if self.location == Commons.LOCATIONS.BOARD.value:
            self.location =  Commons.LOCATIONS.HAND.value
        if self.is_joker:
            self.unmask()

    def get_drawn(self) -> None:
        if self.location == Commons.LOCATIONS.DECK.value:
            self.location =  Commons.LOCATIONS.HAND.value

    def get_played(self) -> None:
        if self.location == Commons.LOCATIONS.HAND.value:
            self.location =  Commons.LOCATIONS.BOARD.value

    def set_moving(self, moving: bool) -> None:
        self.moving = moving

    def set_held_position(self, position: Union[None, Vector2] = None) -> None:
        self.held_position = position

    def set_position(self, position: Vector2 = Vector2(0, 0)) -> None:
        self.position = position
        self.rect.x = position.x
        self.rect.y = position.y

    def set_hovered(self, hover_side: int = Commons.HOVERED.NONE.value) -> None:
        if hover_side == Commons.HOVERED.NONE.value:
            self.hovered = False
            self.hovered_side = Commons.HOVERED.NONE.value
        else:
            self.hovered = True
            self.hovered_side = hover_side

    def blit(self, screen: Surface) -> None:
        if self.is_hover_outline_card:
            draw.rect(screen, "orange", self.rect, 3, 5)
        else:
            colour: str = "black" if self.is_joker else self.colour
            draw.rect(screen, "darkgray", self.rect, 0, 5)
            draw.rect(screen, colour, self.rect, 3, 5)
            draw.rect(screen, "black", self.rect, 1, 5)

            f = font.Font(None, 30)
            if self.is_joker:
                draw.circle(screen, "black", self.rect.center, 20, 2)
            if self.number != 0 and self.colour:
                text = f.render(str(self.number), False, self.colour)
                screen.blit(text, (self.rect.centerx - text.get_rect().width/2, self.rect.centery - text.get_rect().height/2))