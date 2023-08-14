from Round import *


class GameManager:
    """
    A class to initialise and manage each game, before and between game rounds.

    Methods:
    play_game()
        Check if the number of players is selected, or if the game has been quit.
    handle_mouse_input(event)
        Process the event, registering when the selected mode is changed
        and when the user selects the number of players.
    play_new_round()
        Create a new round for the selected mode, and starts play.
    """
    def __init__(self):
        pygame.display.set_caption("Uno [2 - 4 Players]")
        pygame.display.set_icon(pygame.image.load(f"{PATH}yellow_star.png"))
        self.is_sudden_death = False
        self.welcome_screen = WelcomeScreen(self)
        self.current_screen = self.welcome_screen
        self.mouse_position = (0, 0)

        # Set up players
        self.number_of_players = 0
        self.user = None
        self.players = dict()
        self.player_points = dict()

    def play_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if isinstance(self.current_screen, WelcomeScreen):
                        if self.number_of_players != 0:
                            self.user = HumanPlayer()
                            self.players["Player 1"] = self.user
                            for player_id in range(2, self.number_of_players + 1):
                                self.players[f"Player {player_id}"] = ComputerPlayer(player_id)
                            for player in self.players.keys():
                                self.player_points[player] = 0
                            self.play_new_round()
                        elif pygame.mouse.get_focused() != 0:
                            self.handle_mouse_input(event)
                self.current_screen.draw_game()
                pygame.display.update()

    def handle_mouse_input(self, event):
        self.mouse_position = pygame.mouse.get_pos()
        if isinstance(self.current_screen, WelcomeScreen):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SELECT_MODE_BUTTON_RECT.collidepoint(self.mouse_position):
                    self.is_sudden_death = not self.is_sudden_death
                for button in CHOOSE_PLAYERS:
                    if button[1].collidepoint(self.mouse_position):
                        self.number_of_players = button[2]

    def play_new_round(self):
        if self.is_sudden_death:
            current_round = SuddenDeathRound(self)
        else:
            current_round = NormalRound(self)
        current_round.play_round()
