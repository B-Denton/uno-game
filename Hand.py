from Card import *


class Hand:
    """
    A class to represent the cards in a player's hand.

    Methods:
    pull_starting_hand(stock_deck)
        Move seven cards from the stock deck to the player's hand, for the start of a round.
    play_card(card, stock_deck, discard_deck, turn_order)
        Move the card from the player's hand to the discard deck, and manage the special effects for
        reverse cards, skip cards, draw two cards, and wild draw cards.
    """
    def __init__(self, cards_in_hand=None):
        if cards_in_hand is None:
            self.cards_in_hand = []
        else:
            self.cards_in_hand = cards_in_hand

    def pull_starting_hand(self, stock_deck):
        self.cards_in_hand = []
        for _ in range(7):
            self.cards_in_hand.append(stock_deck.cards_in_deck.pop(0))

    def play_card(self, card, stock_deck, discard_deck, turn_order):
        if isinstance(card, ReverseCard):
            turn_order.append(turn_order.pop(0))
            turn_order.reverse()
        if isinstance(card, SkipCard):
            turn_order.append(turn_order.pop(0))
        if isinstance(card, DrawTwoCard):
            for _ in range(2):
                check_stock_deck(stock_deck, discard_deck)
                stock_deck.draw_card(turn_order[1].hand)
        if isinstance(card, WildDrawCard):
            for _ in range(4):
                check_stock_deck(stock_deck, discard_deck)
                stock_deck.draw_card(turn_order[1].hand)
        discard_deck.cards_in_deck.append(card)
        if isinstance(card, NumberCard):
            for card_in_hand in self.cards_in_hand:
                if (card.card_colour == card_in_hand.card_colour) and \
                            (card.card_type == card_in_hand.card_type) and \
                            (card.card_value == card_in_hand.card_value):
                    self.cards_in_hand.remove(card_in_hand)
                    break
        else:
            for card_in_hand in self.cards_in_hand:
                if (card.card_colour == card_in_hand.card_colour) and \
                            (card.card_type == card_in_hand.card_type):
                    self.cards_in_hand.remove(card_in_hand)
                    break
