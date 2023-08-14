from Globals import *


class Card:
    """
    A class used to represent a playing card. Classes inheriting from this represent cards of a specific card type.

    Methods:
    is_match(top_card)
        Compare the card to the given top_card,
        returning True if they match according to Uno rules for that card type, and False if they do not.
    draw_card()
        Return the image that should be drawn to the screen to represent the card.
    """
    def __init__(self, card_colour, card_type):
        self.card_colour, self.card_type = card_colour, card_type
        self.card_texture = CARD_TEXTURES[f"{card_colour}_{card_type}"]
        self.back_cover = CARD_TEXTURES["back_cover"]

    def is_match(self, top_card):
        pass

    def draw_card(self):
        return self.card_texture


class NumberCard(Card):
    def __init__(self, card_colour, card_value):
        super().__init__(card_colour, card_value)
        self.card_type = "number"
        self.card_value = card_value
        self.card_colour, self.card_value = card_colour, card_value
        self.card_texture = CARD_TEXTURES[f"{card_colour}_{str(card_value)}"]
        self.back_cover = CARD_TEXTURES["back_cover"]
        self.card_score = card_value

    def __str__(self):
        return f"{self.card_colour.title()} {str(self.card_value)} Card"

    def is_match(self, top_card):
        return (self.card_colour == top_card.card_colour) or (isinstance(top_card, NumberCard)
                                                              and self.card_value == top_card.card_value)


class DrawTwoCard(Card):
    def __init__(self, card_colour):
        super().__init__(card_colour, "draw_two")
        self.card_score = 20

    def __str__(self):
        return f"{self.card_colour.title()} Draw Card"

    def is_match(self, top_card):
        return (self.card_colour == top_card.card_colour) or isinstance(top_card, DrawTwoCard)


class ReverseCard(Card):
    def __init__(self, card_colour):
        super().__init__(card_colour, "reverse")
        self.card_score = 20

    def __str__(self):
        return f"{self.card_colour.title()} Reverse Card"

    def is_match(self, top_card):
        return (self.card_colour == top_card.card_colour) or isinstance(top_card, ReverseCard)


class SkipCard(Card):
    def __init__(self, card_colour):
        super().__init__(card_colour, "skip")
        self.card_score = 20

    def __str__(self):
        return f"{self.card_colour.title()} Skip Card"

    def is_match(self, top_card):
        return (self.card_colour == top_card.card_colour) or isinstance(top_card, SkipCard)


class SwapHandsCard(Card):
    def __init__(self, card_colour):
        super().__init__(card_colour, "swap_hands")
        self.card_score = 30

    def __str__(self):
        return f"{self.card_colour.title()} Swap Hands Card"

    def is_match(self, top_card):
        return self.card_colour == top_card.card_colour or isinstance(top_card, SwapHandsCard)


class BlackCard(Card):
    def __init__(self, card_colour, card_type):
        super().__init__(card_colour, card_type)
        self.card_score = 50


class WildCard(BlackCard):
    def __init__(self):
        super().__init__("black", "wild")

    def __str__(self):
        return f"Wild Card"

    def is_match(self, top_card):
        return True


class WildDrawCard(BlackCard):
    def __init__(self):
        super().__init__("black", "wild_draw")

    def __str__(self):
        return f"Wild Draw Card"

    def is_match(self, top_card):
        return True
