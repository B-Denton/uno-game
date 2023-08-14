from Hand import *
from Globals import *


def generate_all_cards():
    """Return a list of all the cards in a new deck."""
    list_of_cards = []
    for card_colour in ["red", "yellow", "green", "blue"]:
        for card_number in range(0, 10):
            list_of_cards.append(NumberCard(card_colour, card_number))
            list_of_cards.append(NumberCard(card_colour, card_number))
        for card_type in [SkipCard, ReverseCard, DrawTwoCard, SwapHandsCard]:
            list_of_cards.append(card_type(card_colour))
            list_of_cards.append(card_type(card_colour))
    for _ in range(0, 4):
        list_of_cards.append(WildCard())
        list_of_cards.append(WildDrawCard())
    random.shuffle(list_of_cards)
    return list_of_cards


class Deck:
    """A class used to represent a deck of cards."""
    def __init__(self, cards_in_deck=None):
        if cards_in_deck is None:
            self.cards_in_deck = []
        else:
            self.cards_in_deck = cards_in_deck


class StockDeck(Deck):
    """
    A class used to represent the stock deck that players draw cards from.

    Methods:
    draw_deck(screen)
        Draw a visual representation of the stock deck to the given screen.
    draw_card(hand):
        Move the card at the 'top' of the stock deck into the given hand.
    """
    def __init__(self, cards_in_deck=None):
        if cards_in_deck is None:
            cards_in_deck = []
        super().__init__(cards_in_deck)

    def draw_deck(self, screen):
        def draw_card_back():
            return CARD_TEXTURES["back_cover"]
        # Set parameters
        number_of_cards = len(self.cards_in_deck)
        x_position = 150
        y_position = 242
        # Draw number of cards
        number_of_cards_text = SMALL_FONT.render(f"Draw pile: {number_of_cards} "
                                                 f"Card{'s' if number_of_cards > 1 else ''}".ljust(20),
                                                 True, (0, 0, 0), )
        screen.blit(number_of_cards_text, (x_position - 80, y_position - 88))
        # Draw deck visual
        if number_of_cards > 13:
            y_start_position = y_position
            for index in range(13, -1, -1):
                y_start_position -= 3
                screen.blit(draw_card_back(), (x_position, y_start_position))
        else:
            y_start_position = y_position
            for index in range(number_of_cards, -1, -1):
                y_start_position -= 3
                screen.blit(draw_card_back(), (x_position, y_start_position))

    def draw_card(self, hand):
        drawn_card = self.cards_in_deck.pop(0)
        hand.cards_in_hand.append(drawn_card)


class DiscardDeck(Deck):
    """
    A class used to represent the discard deck that players play cards onto.

    Methods:
    draw_deck(screen)
        Draws a visual representation of the discard deck to the given screen.
    """
    def __init__(self, cards_in_deck=None):
        if cards_in_deck is None:
            cards_in_deck = []
        super().__init__(cards_in_deck)

    def draw_deck(self, screen):
        # Set parameters
        number_of_cards = len(self.cards_in_deck)
        x_position = 480
        y_position = 242
        # Draw number of cards
        number_of_cards_text = SMALL_FONT.render(f"Discard pile: {number_of_cards} "
                                                 f"Card{'s' if number_of_cards > 1 else ''}".ljust(20),
                                                 True, (0, 0, 0), )
        screen.blit(number_of_cards_text, (x_position - 80, y_position - 88))
        # Draw deck visual
        if number_of_cards > 13:
            y_start_position = y_position
            for index in range(13, -1, -1):
                y_start_position -= 3
                screen.blit(self.cards_in_deck[-1 - index].draw_card(), (x_position, y_start_position))
            if isinstance(self.cards_in_deck[-1], BlackCard):
                if ALL_FLAGS.get(self.cards_in_deck[-1].card_colour) is not None:
                    screen.blit(ALL_FLAGS.get(self.cards_in_deck[-1].card_colour),
                                ((x_position + 125), (y_start_position + 10)))
        else:
            y_start_position = y_position
            for index in range(number_of_cards-1, -1, -1):
                y_start_position -= 3
                screen.blit(self.cards_in_deck[-1 - index].draw_card(), (x_position, y_start_position))
            if isinstance(self.cards_in_deck[-1], BlackCard):
                if ALL_FLAGS.get(self.cards_in_deck[-1].card_colour) is not None:
                    screen.blit(ALL_FLAGS.get(self.cards_in_deck[-1].card_colour),
                                ((x_position + 125), (y_start_position + 10)))
