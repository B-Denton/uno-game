from Logbook import *
from Player import *
from Screen import *
import sys


class Round:
    """
    A class to represent a single round in the game.

    Methods:
    next_turn()
        Move the current player to the end of the turn order, and set relevant instructions for the user.
    get_current_player
        Return the first player in the turn order.
    check_mouseover_card
        Return the card that the mouse is currently hovered over, if any.
    swap_mouseover_card
        Select the card being hovered over to swap, and move onto the main phase of the turn.
    handle_computer_player_turn(computer_player)
        Swap a card at the start of the turn, then try to play a card. Handles the effect of swap hand cards
        and wild cards that are played.
    handle_unresolved_black_card()
        Monitor if the player has selected a colour for their played wild card, and set the chosen colour if so.
    handle_unresolved_swap_card()
        Monitor if the player has selected a player to swap hands with, after a swap hands card has been played,
        and swaps the players' hands if so.
    handle_mouse_input(event)
        Monitor for mouse clicks, and call the correct function to handle the click depending on the mouse position
        and turn state.
    play_round()
        Check if a win condition has been reached, and end the game if so. If no winner has been found, continue
        to process game events.
    """
    def __init__(self, game_manager):
        self.game_manager = game_manager
        # Display Parameters
        self.game_screen = None
        self.current_screen = None
        self.win_screen = None

        # New Round Parameters
        self.mouse_position = (0, 0)
        self.logbook = Logbook()
        self.logbook.add_entry(f"- A new game begins!")
        self.is_swap_card_phase = True
        self.player_instructions = "Swap a card!"
        self.unresolved_black_card = False
        self.unresolved_drawn_card = False
        self.unresolved_swap_hands_card = False

        # Card Parameters
        self.mouseover_card = None
        self.stock_deck = StockDeck(generate_all_cards())
        self.discard_deck = DiscardDeck()

        # Set up players:
        self.game_manager.user.hand.pull_starting_hand(self.stock_deck)
        for player_id in game_manager.players.keys():
            self.game_manager.players[player_id].hand.pull_starting_hand(self.stock_deck)
            self.logbook.add_entry(f"- {player_id} joins the game.")

        # Organise Turns
        self.turn_order = list(self.game_manager.players.values())

        # Flip a non-black card onto discard for game start
        while isinstance(self.stock_deck.cards_in_deck[0], BlackCard):
            self.stock_deck.cards_in_deck.append(self.stock_deck.cards_in_deck.pop(0))
        self.discard_deck.cards_in_deck.append(self.stock_deck.cards_in_deck.pop(0))

    def add_delay(self):
        pass

    def next_turn(self):
        self.turn_order.append(self.turn_order.pop(0))
        if isinstance(self.get_current_player(), HumanPlayer):
            self.player_instructions = "Swap a Card"
            self.is_swap_card_phase = True
        else:
            self.player_instructions = "Waiting..."

    def get_current_player(self):
        return self.turn_order[0]

    def check_mouseover_card(self):
        card_positions = self.game_manager.user.get_card_positions()
        for card in card_positions:
            if (card[1][0] < self.mouse_position[0] < card[1][2]) \
                    and (card[1][1] < self.mouse_position[1] < card[1][3]):
                return card[0]
        else:
            return None

    def swap_mouseover_card(self):
        self.game_manager.user.swap_card(self.mouseover_card, self.stock_deck, self.discard_deck)
        self.logbook.add_entry(f"- You swapped a {self.mouseover_card}")
        self.logbook.add_entry(f"  and drew a {self.game_manager.user.hand.cards_in_hand[-1]}.")
        self.player_instructions = "Play a card, or draw."
        self.is_swap_card_phase = False

    def check_for_winner(self):
        pass

    def no_card_played_by_computer(self, computer_player):
        pass

    def handle_computer_player_turn(self, computer_player):
        # Select card to swap, prioritising high number cards.
        card_to_swap = computer_player.choose_card_to_swap()
        computer_player.swap_card(card_to_swap, self.stock_deck, self.discard_deck)
        # Play a card
        card_to_play = computer_player.choose_card_to_play(self.discard_deck, self.turn_order)
        if card_to_play is not None:
            if isinstance(card_to_play, BlackCard):
                card_to_play.card_colour = computer_player.choose_colour_for_black_card()
                check_stock_deck(self.stock_deck, self.discard_deck)
                computer_player.hand.play_card(card_to_play, self.stock_deck, self.discard_deck, self.turn_order)
                self.logbook.add_entry(f"- {repr(computer_player)} played a {card_to_play}")
                self.logbook.add_entry(f"  and chose {card_to_play.card_colour}.")
                self.add_delay()
                self.next_turn()
            elif isinstance(card_to_play, SwapHandsCard):
                if len(computer_player.hand.cards_in_hand) == 1:
                    self.logbook.add_entry(f"- {repr(computer_player)} played a {card_to_play} ")
                    self.add_delay()
                    self.next_turn()
                else:
                    # Choose from player with the smallest hand size.
                    computer_player.hand.play_card(card_to_play, self.stock_deck, self.discard_deck, self.turn_order)
                    minimum_hand_size = 0
                    minimum_hand_player = None
                    for player in self.turn_order:
                        if (minimum_hand_size == 0 or len(player.hand.cards_in_hand) < minimum_hand_size) and \
                                computer_player != player:
                            minimum_hand_size = len(player.hand.cards_in_hand)
                            minimum_hand_player = player
                    computer_player.hand.cards_in_hand, minimum_hand_player.hand.cards_in_hand = \
                        minimum_hand_player.hand.cards_in_hand, computer_player.hand.cards_in_hand
                    self.logbook.add_entry(f"- {repr(computer_player)} swapped hands with ")
                    self.logbook.add_entry(f"  {repr(minimum_hand_player)}.")
                    self.add_delay()
                    self.next_turn()
            else:
                check_stock_deck(self.stock_deck, self.discard_deck)
                computer_player.hand.play_card(card_to_play, self.stock_deck, self.discard_deck, self.turn_order)
                self.logbook.add_entry(f"- {repr(computer_player)} played a {card_to_play}.")
                self.add_delay()
                self.next_turn()
        else:
            self.no_card_played_by_computer(computer_player)

    def handle_unresolved_drawn_card(self):
        pass

    def handle_unresolved_black_card(self):
        for button in CHOOSE_COLOUR:
            if button[1].collidepoint(self.mouse_position):
                self.discard_deck.cards_in_deck[-1].card_colour = button[3]
                self.unresolved_black_card = False
                self.logbook.add_entry(f"- You played a {self.discard_deck.cards_in_deck[-1]}")
                self.logbook.add_entry(f"  and chose {button[3]}.")
                self.next_turn()

    def handle_unresolved_swap_card(self):
        for button in SELECT_PLAYER:
            player = self.game_manager.players.get(button[2])
            if player in self.turn_order:
                if button[1].collidepoint(self.mouse_position):
                    self.game_manager.user.hand.cards_in_hand, \
                        self.game_manager.players[button[2]].hand.cards_in_hand = \
                        self.game_manager.players[button[2]].hand.cards_in_hand, \
                        self.game_manager.user.hand.cards_in_hand
                    self.unresolved_swap_hands_card = False
                    self.logbook.add_entry(f"- You swapped your hand with")
                    self.logbook.add_entry(f"  {repr(self.game_manager.players[button[2]])}")
                    self.next_turn()

    def handle_special_round_button(self):
        pass

    def handle_mouse_input(self, event):
        self.mouse_position = pygame.mouse.get_pos()
        self.mouseover_card = self.check_mouseover_card()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if isinstance(self.current_screen, WinScreen):
                if NEW_ROUND_BUTTON_RECT.collidepoint(self.mouse_position):
                    self.game_manager.play_new_round()
            else:
                if self.unresolved_drawn_card:  # If user just drew a playable card:
                    self.handle_unresolved_drawn_card()
                elif self.unresolved_black_card:  # If top black card has unset colour:
                    self.handle_unresolved_black_card()
                elif self.unresolved_swap_hands_card:  # If target player not chosen for a Hand Swap:
                    self.handle_unresolved_swap_card()
                else:
                    if self.is_swap_card_phase:
                        if self.mouseover_card is not None:
                            self.swap_mouseover_card()
                    else:
                        if SPECIAL_ROUND_BUTTON_RECT.collidepoint(self.mouse_position):  # User chooses to draw
                            self.handle_special_round_button()
                        else:
                            if self.mouseover_card is not None:
                                if isinstance(self.mouseover_card, BlackCard):
                                    self.game_manager.user.hand.play_card(self.mouseover_card, self.stock_deck,
                                                                          self.discard_deck, self.turn_order)
                                    self.unresolved_black_card = True
                                else:
                                    # noinspection PyUnresolvedReferences
                                    if self.mouseover_card.is_match(self.discard_deck.cards_in_deck[-1]):
                                        if isinstance(self.mouseover_card, SwapHandsCard):
                                            self.game_manager.user.hand.play_card(self.mouseover_card, self.stock_deck,
                                                                                  self.discard_deck, self.turn_order)
                                            self.player_instructions = "Select a Player"
                                            self.unresolved_swap_hands_card = True
                                        else:
                                            self.game_manager.user.hand.play_card(self.mouseover_card, self.stock_deck,
                                                                                  self.discard_deck, self.turn_order)
                                            self.logbook.add_entry(f"- You played a {self.mouseover_card}")
                                            self.next_turn()

    def play_round(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if isinstance(self.current_screen, WinScreen):
                        if pygame.mouse.get_focused() != 0:
                            self.handle_mouse_input(event)
                    else:
                        self.check_for_winner()
                        if isinstance(self.current_screen, WinScreen):
                            self.current_screen.draw_game()
                            pygame.display.update()
                            pygame.time.wait(100)
                            pass
                        else:
                            self.current_screen.draw_log()
                            check_stock_deck(self.stock_deck, self.discard_deck)
                            if isinstance(self.get_current_player(), ComputerPlayer):
                                self.handle_computer_player_turn(self.get_current_player())
                            else:
                                if pygame.mouse.get_focused() != 0:
                                    self.handle_mouse_input(event)
                    self.current_screen.draw_game()
                    pygame.display.update()
        pygame.quit()
        sys.exit()


class NormalRound(Round):
    """
    A class to represent a single round in the game, with Sudden Death Mode turned off.

    Methods:
    add_delay()
        Slow the game between computer player turns, and clear all mouse events.
    check_for_winner()
        Check if any player has reached a hand size of zero,
        and calculate the points they win for the round if so.
    handle_unresolved_drawn_card()
        Monitor if a player has selected whether they want to play or keep a drawn card.
    handle_special_round_button()
        Monitor if the player chooses to draw a card during their turn, instead of playing a card.
    no_card_played_by_computer()
        Make the computer draw a card, if they have no valid play in hand.
    """
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # Display Parameters
        self.game_screen = NormalGameScreen(self)
        self.current_screen = self.game_screen
        self.win_screen = None

    def add_delay(self):
        pygame.time.wait(1000)
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"code": ""}))

    def check_for_winner(self):
        def sum_round_points():
            round_points = 0
            for add_player in self.game_manager.players.keys():
                round_points += sum([card.card_score for card in
                                     self.game_manager.players[add_player].hand.cards_in_hand])
            return round_points
        # Check for win condition
        for player in self.game_manager.players.keys():
            if len(self.game_manager.players[player].hand.cards_in_hand) == 0:
                self.game_manager.player_points[player] += sum_round_points()
                self.win_screen = WinScreen(self.game_manager.players[player], self.game_manager)
                self.current_screen = self.win_screen
                break

    def handle_unresolved_drawn_card(self):
        if PLAY_BUTTON_RECT.collidepoint(self.mouse_position):
            card_drawn = self.game_manager.user.hand.cards_in_hand[-1]
            self.game_manager.user.hand.play_card(card_drawn, self.stock_deck,
                                                  self.discard_deck, self.turn_order)
            if isinstance(card_drawn, BlackCard):
                self.unresolved_black_card = True
                self.unresolved_drawn_card = False
            elif isinstance(card_drawn, SwapHandsCard):
                self.unresolved_swap_hands_card = True
                self.unresolved_drawn_card = False
            else:
                self.unresolved_drawn_card = False
                self.logbook.add_entry(f"- You played the {card_drawn}.")
                self.next_turn()
        if KEEP_BUTTON_RECT.collidepoint(self.mouse_position):
            card_drawn = self.game_manager.user.hand.cards_in_hand[-1]
            self.logbook.add_entry(f"- You kept the {card_drawn}.")
            self.unresolved_drawn_card = False
            self.next_turn()

    def handle_special_round_button(self):
        self.stock_deck.draw_card(self.game_manager.user.hand)
        card_drawn = self.game_manager.user.hand.cards_in_hand[-1]
        self.logbook.add_entry(f"- You drew a {card_drawn}.")
        if card_drawn.is_match(self.discard_deck.cards_in_deck[-1]):
            self.unresolved_drawn_card = True
            self.player_instructions = "Play or keep?"
        else:
            self.next_turn()

    def no_card_played_by_computer(self, computer_player):
        check_stock_deck(self.stock_deck, self.discard_deck)
        self.stock_deck.draw_card(computer_player.hand)
        self.logbook.add_entry(f"- {repr(computer_player)} drew a card.")
        self.add_delay()
        self.next_turn()


class SuddenDeathRound(Round):
    """
    A class to represent a single round in the game, with Sudden Death Mode turned on.

    Methods:
    add_delay()
        Slow the game between computer player turns, and clear all mouse events.
    check_for_winner()
        Check if any player has reached a hand size of zero or if only one player is left actively playing,
        and calculate the points they win for the round if so.
    handle_special_round_button()
        Monitor if the player chooses to forfeit during their turn, instead of playing a card.
    no_card_played_by_computer()
        Make the computer forfeit if they have no valid play in hand.
    """
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # Display Parameters
        self.game_screen = SuddenDeathGameScreen(self)
        self.current_screen = self.game_screen
        self.win_screen = None
        self.logbook.add_entry(f"- [SUDDEN DEATH MODE ACTIVATED] -")
        self.has_forfeit = dict()
        for player in self.game_manager.players.keys():
            self.has_forfeit[player] = False

    def add_delay(self):
        if all([isinstance(player, ComputerPlayer) for player in self.turn_order]):
            pygame.time.wait(300)
        else:
            pygame.time.wait(1000)
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"code": ""}))

    def check_for_winner(self):
        def sum_round_points():
            round_points = 0
            for add_player in self.game_manager.players.keys():
                round_points += sum([card.card_score for card in
                                     self.game_manager.players[add_player].hand.cards_in_hand])
            return round_points
        # Check for win condition
        winning_player = None
        if len(self.turn_order) <= 1:
            winning_player = self.turn_order[0]
        else:
            for player in self.game_manager.players.keys():
                if len(self.game_manager.players[player].hand.cards_in_hand) == 0:
                    winning_player = self.game_manager.players[player]
                    break
        if winning_player is not None:
            self.game_manager.player_points[repr(winning_player)] += sum_round_points()
            self.win_screen = WinScreen(self.game_manager.players[repr(winning_player)], self.game_manager)
            self.current_screen = self.win_screen

    def handle_unresolved_drawn_card(self):
        pass

    def handle_special_round_button(self):
        self.has_forfeit['Player 1'] = True
        self.turn_order.pop(0)
        self.logbook.add_entry(f"- Player 1 forfeited the game.")
        self.player_instructions = "Forfeited"
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"code": ""}))

    def no_card_played_by_computer(self, computer_player):
        self.has_forfeit[repr(computer_player)] = True
        self.turn_order.pop(0)
        self.logbook.add_entry(f"- {computer_player} forfeited the game.")
        self.add_delay()
        self.is_swap_card_phase = True
