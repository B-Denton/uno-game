from Deck import *


class Player:
    """
    A class to represent a player in the game.

    Methods:
    swap_card(card_to_swap, stock_deck, discard_deck)
        Remove the card from the player's hand, place on bottom of the discard deck,
        and draw a new card from the stock deck.
    """
    def __init__(self):
        # Initialise Hand
        self.hand = Hand()

    def swap_card(self, card_to_swap, stock_deck, discard_deck):
        if isinstance(card_to_swap, NumberCard):
            for card in self.hand.cards_in_hand:
                if (card_to_swap.card_colour == card.card_colour) and \
                        (card_to_swap.card_type == card.card_type) and \
                        (card_to_swap.card_value == card.card_value):
                    self.hand.cards_in_hand.remove(card)
                    discard_deck.cards_in_deck.insert(0, card_to_swap)
                    check_stock_deck(stock_deck, discard_deck)
                    stock_deck.draw_card(self.hand)
                    pygame.time.wait(100)
                    break
        else:
            for card in self.hand.cards_in_hand:
                if (card_to_swap.card_colour == card.card_colour) and (card_to_swap.card_type == card.card_type):
                    self.hand.cards_in_hand.remove(card)
                    discard_deck.cards_in_deck.insert(0, card_to_swap)
                    check_stock_deck(stock_deck, discard_deck)
                    stock_deck.draw_card(self.hand)
                    pygame.time.wait(100)
                    break


class HumanPlayer(Player):
    """
    A class to represent the user in the game.

    Methods:
    update_display_parameters()
        Check the number of cards in hand, and update variables that are calculated from this number.
    draw_player_hand(screen)
        Draw the cards in the user's hand at the bottom of the given screen.
    get_card_positions()
        Calculate a list of what coordinates can be associated with which card, based on what has been
        drawn to the screen.
    """
    def __init__(self):
        super().__init__()
        self.player_id = 1
        # Static Player Hand Display Settings
        self.hand_display_width = 1050
        self.y_position = 552
        # Dynamic Player Hand Display Settings
        self.number_of_cards = len(self.hand.cards_in_hand)
        self.x_start_position = 150
        self.x_start_intervals = [((self.hand_display_width / self.number_of_cards) * n)
                                  for n in range(0, self.number_of_cards)]

    def __str__(self):
        return f"Player 1"

    def __repr__(self):
        return f"Player 1"

    def update_display_parameters(self):
        self.number_of_cards = len(self.hand.cards_in_hand)
        self.x_start_intervals = [(self.hand_display_width / self.number_of_cards) * n
                                  for n in range(0, self.number_of_cards)]

    def draw_player_hand(self, screen):
        self.update_display_parameters()
        for index, card in enumerate(self.hand.cards_in_hand):
            current_x_position = self.x_start_position + self.x_start_intervals[index]
            screen.blit(card.draw_card(), (current_x_position, self.y_position))

    def get_card_positions(self):
        self.update_display_parameters()
        card_parameters = []  # [Card, [x_start_position, y_start_position, x_end_position, y_end_position]]

        if len(self.hand.cards_in_hand) > 5:  # Overlapping cards in hand
            for index, card in enumerate(self.hand.cards_in_hand[:-1]):
                card_parameters.append([card, [self.x_start_position + self.x_start_intervals[index],
                                               self.y_position,
                                               self.x_start_position + self.x_start_intervals[index+1],
                                               self.y_position + CARD_HEIGHT]])
            card_parameters.append([self.hand.cards_in_hand[-1],
                                    [self.x_start_position + self.x_start_intervals[-1],
                                     self.y_position,
                                     self.x_start_position + self.x_start_intervals[-1] + CARD_WIDTH,
                                     self.y_position + CARD_HEIGHT]])
        else:
            for index, card in enumerate(self.hand.cards_in_hand):
                card_parameters.append([card, [self.x_start_position + self.x_start_intervals[index],
                                               self.y_position,
                                               self.x_start_position + self.x_start_intervals[index] + CARD_WIDTH,
                                               self.y_position + CARD_HEIGHT]])
        return card_parameters


class ComputerPlayer(Player):
    """
    A class to represent the computer-controlled players in the game.

    Methods:
    choose_card_to_swap()
        Choose a card to swap at the start of the turn, prioritising number cards.
    choose_card_to_player(discard_deck, turn_order)
        Choose a valid card to play, prioritising high-cost cards towards the end of the round,
        draw cards when the following player has a small hand size, and low-value cards otherwise.
    choose_colour_for_black_card()
        Choose a colour for a played wild card, prioritising the colour most frequent amongst the
        cards in their hand.
    """
    def __init__(self, player_id):
        super().__init__()
        self.player_id = player_id

    def __str__(self):
        return f"Player {self.player_id}"

    def __repr__(self):
        return f"Player {self.player_id}"

    def choose_card_to_swap(self):
        for card_number in range(9, -1, -1):
            for card in self.hand.cards_in_hand:
                if isinstance(card, NumberCard) and card.card_value == card_number:
                    return card
        return random.choice(self.hand.cards_in_hand)

    def choose_card_to_play(self, discard_deck, turn_order):
        turn_orders_number_of_cards = []
        for opponent_player in turn_order:
            turn_orders_number_of_cards.append(len(opponent_player.hand.cards_in_hand))
        # Ditch 50-point cards if a player may win soon, then 20-point cards:
        if any([len(opponent_player.hand.cards_in_hand) <= 1 for opponent_player in turn_order]):
            for card in self.hand.cards_in_hand:
                if card.is_match(discard_deck.cards_in_deck[-1]):
                    if isinstance(card, BlackCard):
                        return card
            for card in self.hand.cards_in_hand:
                if card.is_match(discard_deck.cards_in_deck[-1]):
                    if isinstance(card, SkipCard) or \
                            isinstance(card, ReverseCard) or \
                            isinstance(card, DrawTwoCard):
                        return card
        # If next player has small hand size, make them draw:
        if turn_orders_number_of_cards[1] < 3:
            for card in self.hand.cards_in_hand:
                if card.is_match(discard_deck.cards_in_deck[-1]):
                    if isinstance(card, DrawTwoCard) or isinstance(card, WildDrawCard):
                        return card
        # Get rid of number cards
        for card_number in range(9, -1, -1):
            for card in self.hand.cards_in_hand:
                if card.is_match(discard_deck.cards_in_deck[-1]):
                    if isinstance(card, NumberCard) and card.card_value == card_number:
                        return card
        # Play any possible match
        for card in self.hand.cards_in_hand:
            if card.is_match(discard_deck.cards_in_deck[-1]):
                return card
        # No matches in hand
        return None

    def choose_colour_for_black_card(self):
        # Choose from most common colours in hand.
        card_colours_in_hand = [card.card_colour for card in self.hand.cards_in_hand
                                if card.card_colour != 'black']
        return max(set(card_colours_in_hand), key=card_colours_in_hand.count,
                   default=random.choice(['red', 'yellow', 'blue', 'green']))
