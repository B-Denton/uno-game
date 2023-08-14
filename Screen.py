from Player import *

welcome_background_texture = pygame.image.load(f"{PATH}welcome_background.png")
background_texture = pygame.image.load(f"{PATH}normal_background.png")
win_background_texture = pygame.image.load(f"{PATH}win_background.png")
win_screen_texture = pygame.image.load(f"{PATH}win_screen.png")


class Screen:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def draw_log(self):
        pass


class WelcomeScreen(Screen):
    """
    A class to represent the Welcome Screen when the player first opens the game.

    Methods:
    draw_game()
        Draw the background, as well as buttons to select the mode and number of players.
    """
    def __init__(self, game_manager):
        super().__init__()
        self.number_of_players = 0
        self.game_manager = game_manager

    def draw_game(self):
        self.screen.blit(welcome_background_texture, (0, 0))
        if self.game_manager.is_sudden_death:
            select_mode_button = SELECT_MODE_OFF_BUTTON
        else:
            select_mode_button = SELECT_MODE_ON_BUTTON
        pygame.draw.rect(self.screen, WHITE, SELECT_MODE_BUTTON_RECT)
        self.screen.blit(select_mode_button, (SELECT_MODE_BUTTON_X_POSITION, SELECT_MODE_BUTTON_Y_POSITION))
        for index, button in enumerate(CHOOSE_PLAYERS):
            pygame.draw.rect(self.screen, WHITE, button[1])
            self.screen.blit(button[0], (PLAYERS_BUTTON_X_POSITIONS[index], PLAYERS_BUTTON_Y_POSITION))


class GameScreen(Screen):
    """
    A class to represent the Game Screen when the player is playing a round of the game.

    Methods:
    draw_log()
        Draw the logbook to the screen.
    draw_game()
        Draw game components, such as the visual assets, player statuses, the user's hand, the stock deck
        and the discard deck.
    """
    def __init__(self, game_round):
        super().__init__()
        self.game_round = game_round

    def draw_log(self):
        logbook_x_position = 1070
        logbook_y_position = 154
        self.screen.blit(SMALL_FONT.render("Log:", True, BLACK), (logbook_x_position, logbook_y_position))
        last_lines = self.game_round.logbook.get_last_lines(10)
        for line_index, line in enumerate(last_lines):
            last_lines_text = TINY_FONT.render(line, True, BLACK)
            self.screen.blit(last_lines_text, (logbook_x_position, logbook_y_position + 45 + (line_index * 30)))

    def draw_player_status(self, active_player):
        pass

    def draw_round_special_button(self):
        pass

    def draw_game(self):
        def draw_hovered_card():
            if self.game_round.mouseover_card is not None:
                self.screen.blit(self.game_round.mouseover_card.draw_card(), (x_position, y_position))

        active_player = self.game_round.get_current_player()
        x_position = 810
        y_position = 232

        # Always Displayed features
        self.screen.blit(background_texture, (0, 0))
        self.game_round.game_manager.user.draw_player_hand(self.screen)
        self.game_round.stock_deck.draw_deck(self.screen)
        self.game_round.discard_deck.draw_deck(self.screen)
        self.draw_player_status(active_player)
        self.draw_log()
        player_instructions_text = SMALL_FONT.render(self.game_round.player_instructions.ljust(20), True, BLACK)
        self.screen.blit(player_instructions_text, (x_position - 75, y_position - 78))

        # State-Specific features
        if not isinstance(active_player, ComputerPlayer):
            if self.game_round.unresolved_drawn_card:
                pygame.draw.rect(self.screen, WHITE, PLAY_BUTTON_RECT)
                self.screen.blit(PLAY_BUTTON, (PLAY_BUTTON_X_POSITION, PLAY_BUTTON_Y_POSITION))
                pygame.draw.rect(self.screen, WHITE, KEEP_BUTTON_RECT)
                self.screen.blit(KEEP_BUTTON, (PLAY_BUTTON_X_POSITION, KEEP_BUTTON_Y_POSITION))
            elif self.game_round.unresolved_black_card:
                for index, button in enumerate(CHOOSE_COLOUR):
                    pygame.draw.rect(self.screen, button[2], button[1])
                    self.screen.blit(button[0], (COLOUR_BUTTON_X_POSITION,
                                                 COLOUR_BUTTON_Y_POSITIONS[index]))
            elif self.game_round.unresolved_swap_hands_card:
                for index, button in enumerate(SELECT_PLAYER):
                    player = self.game_round.game_manager.players.get(button[2])
                    if player in self.game_round.turn_order:
                        pygame.draw.rect(self.screen, WHITE, button[1])
                        self.screen.blit(button[0], (SELECT_PLAYER_BUTTON_X_POSITION,
                                                     SELECT_PLAYER_BUTTON_Y_POSITIONS[index]))
            else:
                if not self.game_round.is_swap_card_phase:
                    self.draw_round_special_button()
                draw_hovered_card()


class NormalGameScreen(GameScreen):
    """
    A class to represent the Game Screen when the player is playing a round of the game,
    with Sudden Death Mode turned off.

    Methods:
    draw_round_special_button()
        Draw the 'Draw Card' button to the screen.
    draw_player_status()
        Draw the player names at the top of the screen, alongside their hand size and who is playing.
    """
    def __init__(self, game_round):
        super().__init__(game_round)

    def draw_round_special_button(self):
        pygame.draw.rect(self.screen, WHITE, SPECIAL_ROUND_BUTTON_RECT)
        self.screen.blit(STOCK_DECK_DRAW_BUTTON, (SPECIAL_ROUND_BUTTON_X_POSITION, SPECIAL_ROUND_BUTTON_Y_POSITION))

    def draw_player_status(self, active_player):
        x_start_position = 100
        y_start_position = 32
        for player_id in range(1, 5):
            player_name = f"Player {player_id}"
            if isinstance(self.game_round.game_manager.players.get(player_name), HumanPlayer):
                first_line = f"You"
            else:
                first_line = player_name
            if self.game_round.game_manager.players.get(player_name) is not None:
                cards_in_hand_count = len(self.game_round.game_manager.players[player_name].hand.cards_in_hand)
                second_line = f"Cards in hand: {cards_in_hand_count}"
                if self.game_round.game_manager.players.get(player_name) == active_player:
                    text_colour = GREEN
                else:
                    text_colour = BLACK
            else:
                text_colour = GREY
                second_line = f"Player Inactive"
            first_line_text = LARGE_FONT.render(first_line.ljust(40-len(first_line)), True, text_colour)
            second_line_text = SMALL_FONT.render(second_line.ljust(40 - len(second_line)), True, text_colour)
            self.screen.blit(first_line_text, (x_start_position + (330 * (player_id-1)), y_start_position))
            self.screen.blit(second_line_text, (x_start_position + (330 * (player_id-1)), y_start_position + 50))


class SuddenDeathGameScreen(GameScreen):
    """
    A class to represent the Game Screen when the player is playing a round of the game,
    with Sudden Death Mode turned on.

    Methods:
    draw_round_special_button()
        Draw the 'Forfeit' button to the screen.
    draw_player_status()
        Draw the player names at the top of the screen, alongside their hand size and who is actively playing.
    """
    def __init__(self, game_round):
        super().__init__(game_round)

    def draw_round_special_button(self):
        pygame.draw.rect(self.screen, WHITE, SPECIAL_ROUND_BUTTON_RECT)
        self.screen.blit(FORFEIT_BUTTON, (SPECIAL_ROUND_BUTTON_X_POSITION, SPECIAL_ROUND_BUTTON_Y_POSITION))

    def draw_player_status(self, active_player):
        x_start_position = 100
        y_start_position = 32
        for player_id in range(1, 5):
            player_name = f"Player {player_id}"
            if isinstance(self.game_round.game_manager.players.get(player_name), HumanPlayer):
                first_line = f"You"
            else:
                first_line = player_name
            if self.game_round.game_manager.players.get(player_name) is not None:
                if not self.game_round.has_forfeit.get(player_name):
                    cards_in_hand_count = len(self.game_round.game_manager.players[player_name].hand.cards_in_hand)
                    second_line = f"Cards in hand: {cards_in_hand_count}"
                    if self.game_round.game_manager.players.get(player_name) == active_player:
                        text_colour = GREEN
                    else:
                        text_colour = BLACK
                else:
                    text_colour = RED
                    second_line = "Forfeited"
            else:
                text_colour = GREY
                second_line = "Player Inactive"
            first_line_text = LARGE_FONT.render(first_line.ljust(40-len(first_line)), True, text_colour)
            second_line_text = SMALL_FONT.render(second_line.ljust(40 - len(second_line)), True, text_colour)
            self.screen.blit(first_line_text, (x_start_position + (330 * (player_id-1)), y_start_position))
            self.screen.blit(second_line_text, (x_start_position + (330 * (player_id-1)), y_start_position + 50))


class WinScreen(Screen):
    """
    A class to represent the Win Screen displayed after a round has been won.

    Methods:
    draw_player_status()
        Draw the player names at the top of the screen, alongside their score for the previous round
        and their points collected for the overall game.
    draw_game()
        Draw game components, such as player statuses, who won the round, and a button to play another round.
    """
    def __init__(self, winning_player, game_manager):
        super().__init__()
        self.winning_player = winning_player
        self.game_manager = game_manager

    def draw_player_status(self):
        x_start_position = 100
        y_start_position = 42
        for player_id in range(1, 5):
            player_name = f"Player {player_id}"
            if isinstance(self.game_manager.players.get(player_name), HumanPlayer):
                first_line = f"You "
            else:
                first_line = player_name
            if self.game_manager.players.get(player_name) is not None:
                cards_in_hand = self.game_manager.players.get(player_name).hand.cards_in_hand
                second_line = f"Round Score: {sum([card.card_score for card in cards_in_hand])}"
                text_colour = BLACK
                third_line = f"Total Points: {self.game_manager.player_points.get(player_name)}"
            else:
                text_colour = GREY
                second_line = f"Player Inactive"
                third_line = ""
            first_line_text = LARGE_FONT.render(first_line.ljust(40 - len(first_line)), True, text_colour)
            second_line_text = SMALL_FONT.render(second_line.ljust(40 - len(second_line)), True, text_colour)
            third_line_text = SMALL_FONT.render(third_line.ljust(40 - len(third_line)), True, text_colour)
            self.screen.blit(first_line_text, (x_start_position + (330 * (player_id - 1)), y_start_position))
            self.screen.blit(second_line_text, (x_start_position + (330 * (player_id - 1)), y_start_position + 50))
            self.screen.blit(third_line_text, (x_start_position + (330 * (player_id - 1)), y_start_position + 80))

    def draw_game(self):
        self.screen.blit(win_background_texture, (0, 0))
        self.screen.blit(win_screen_texture, (200, 250))
        pygame.draw.rect(self.screen, WHITE, NEW_ROUND_BUTTON_RECT)
        self.screen.blit(NEW_ROUND_BUTTON, (NEW_ROUND_BUTTON_X_POSITION, NEW_ROUND_BUTTON_Y_POSITION))
        self.draw_player_status()
        winning_player_message = 'You won!'.center(16) if self.winning_player.player_id == 1 \
            else 'Player ' + str(self.winning_player.player_id) + ' won!'
        congratulations_text = WINNING_FONT.render(winning_player_message, True, BLACK)
        self.screen.blit(congratulations_text, (253, 325))
