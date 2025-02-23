from typing import List, Dict, Tuple, Union, Type
from pygame import Surface, sprite, draw, Rect, font, Vector2
import commons.enum as Commons

class Button(sprite.Sprite):
    counter = 0
    def __init__(self, name: str, colour: str, content: str, buttontype: int = Commons.BUTTONTYPES.MENU.value, fontsize: int = 40, width: int = 150, height: int = 50, position: Vector2 = Vector2(0, 0)):
        sprite.Sprite.__init__(self)
        self.id = self.counter
        Button.counter += 1

        self.name: str = name
        self.type: int = buttontype
        self.colour: str = colour
        self.content: str = content
        self.is_clicked: bool = False
        self.is_shown: bool = False
        self.can_be_clicked: bool = True
        self.cooldown_current: float = 0
        self.cooldown_max: float = 1    # in seconds

        self.rect: None = None
        self.position: Vector2 = position
        self.rect: Rect = Rect(self.position.x, self.position.y, width, height)
        self.fontsize: int = fontsize
        self.font: Union[font.Font, None] = None

    def toggle_clicked(self) -> None:
        self.is_clicked = not self.is_clicked

    def set_clicked(self, click: bool) -> None:
        self.is_clicked = click

    def set_can_be_clicked(self, click: bool) -> None:
        self.can_be_clicked = click

    def toggle_shown(self) -> None:
        self.is_shown = not self.is_shown

    def set_shown(self, show: bool) -> None:
        self.is_shown = show

    def set_fontsize(self, fontsize: int) -> None:
        if fontsize <= 0:
            return
        self.fontsize = fontsize

    def set_font(self, fontsize: int = 0) -> None:
        fontsize = self.fontsize if fontsize <= 0 else fontsize
        self.font: font.Font = font.Font(None, fontsize)

    def set_on_cooldown(self) -> None:
        self.set_clicked(True)
        self.cooldown_current = self.cooldown_max

    def blit(self, screen: Surface) -> None:
        if not self.is_shown:
            return
        self.set_font()
        colour = "orange" if self.is_clicked else self.colour
        colour = colour if self.can_be_clicked else "red"
        draw.rect(screen, colour, self.rect, 0, 5)
        draw.rect(screen, "black", self.rect, 3, 5)
        text = self.font.render(self.content, False, "black")
        screen.blit(text, (self.rect.centerx - text.get_rect().width/2, self.rect.centery - text.get_rect().height/2))