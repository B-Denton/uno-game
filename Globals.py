import os
import pygame
import random
pygame.init()

# Card Parameters
CARD_HEIGHT, CARD_WIDTH = 250, 175

# Screen Parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 850

# Colours
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (199, 18, 11)
GREEN = (103, 172, 66)
YELLOW = (244, 212, 49)
BLUE = (3, 87, 157)

# Pathname to assets folder
PATH = f"{os.path.dirname(os.path.realpath(__file__))}//textures//"

# Font styles
TINY_FONT = pygame.font.Font(f"{PATH}tahomabd.TTF", 13)
SMALL_FONT = pygame.font.Font(f"{PATH}tahomabd.TTF", 24)
MEDIUM_FONT = pygame.font.Font(f"{PATH}BRLNSDB.TTF", 32)
LARGE_FONT = pygame.font.Font(f"{PATH}BRLNSDB.TTF", 50)
WINNING_FONT = pygame.font.Font(f"{PATH}BRLNSDB.TTF", 150)

# Card Texture Images
CARD_TEXTURES = {"back_cover": pygame.image.load(f"{PATH}back_cover.png"),
                 "black_wild": pygame.image.load(f"{PATH}black_wild.png"),
                 "black_wild_draw": pygame.image.load(f"{PATH}black_wild_draw.png")}
for colour in ['red', 'blue', 'green', 'yellow']:
    CARD_TEXTURES[f"{colour}_draw_two"] = pygame.image.load(f"{PATH}{colour}_draw_two.png")
    CARD_TEXTURES[f"{colour}_reverse"] = pygame.image.load(f"{PATH}{colour}_reverse.png")
    CARD_TEXTURES[f"{colour}_skip"] = pygame.image.load(f"{PATH}{colour}_skip.png")
    CARD_TEXTURES[f"{colour}_swap_hands"] = pygame.image.load(f"{PATH}{colour}_swap_hands.png")
    for number in range(0, 10):
        CARD_TEXTURES[f"{colour}_{number}"] = pygame.image.load(f"{PATH}{colour}_{number}.png")

# Flag Texture Images, for indicating the colour of a played wild card.
ALL_FLAGS = {
    "red": pygame.image.load(f"{PATH}red_flag.png"),
    "green": pygame.image.load(f"{PATH}green_flag.png"),
    "yellow": pygame.image.load(f"{PATH}yellow_flag.png"),
    "blue": pygame.image.load(f"{PATH}blue_flag.png")
}

# Number of Player Button Parameters
PLAYERS_BUTTON_X_POSITIONS = [200, 550, 900]
PLAYERS_BUTTON_Y_POSITION = 650
TWO_PLAYERS_BUTTON = pygame.image.load(f"{PATH}2_players_button.png")
TWO_PLAYERS_BUTTON_RECT = TWO_PLAYERS_BUTTON.get_rect(x=PLAYERS_BUTTON_X_POSITIONS[0],
                                                      y=PLAYERS_BUTTON_Y_POSITION)
THREE_PLAYERS_BUTTON = pygame.image.load(f"{PATH}3_players_button.png")
THREE_PLAYERS_BUTTON_RECT = TWO_PLAYERS_BUTTON.get_rect(x=PLAYERS_BUTTON_X_POSITIONS[1],
                                                        y=PLAYERS_BUTTON_Y_POSITION)
FOUR_PLAYERS_BUTTON = pygame.image.load(f"{PATH}4_players_button.png")
FOUR_PLAYERS_BUTTON_RECT = TWO_PLAYERS_BUTTON.get_rect(x=PLAYERS_BUTTON_X_POSITIONS[2],
                                                       y=PLAYERS_BUTTON_Y_POSITION)
CHOOSE_PLAYERS = [
    [TWO_PLAYERS_BUTTON, TWO_PLAYERS_BUTTON_RECT, 2],
    [THREE_PLAYERS_BUTTON, THREE_PLAYERS_BUTTON_RECT, 3],
    [FOUR_PLAYERS_BUTTON, FOUR_PLAYERS_BUTTON_RECT, 4]
]

# Select Mode Button Parameters
SELECT_MODE_BUTTON_X_POSITION = 400
SELECT_MODE_BUTTON_Y_POSITION = 450
SELECT_MODE_ON_BUTTON = pygame.image.load(f"{PATH}sudden_death_on_button.png")
SELECT_MODE_OFF_BUTTON = pygame.image.load(f"{PATH}sudden_death_off_button.png")
SELECT_MODE_BUTTON_RECT = SELECT_MODE_ON_BUTTON.get_rect(x=SELECT_MODE_BUTTON_X_POSITION,
                                                         y=SELECT_MODE_BUTTON_Y_POSITION)

# Select Player Button Parameters
SELECT_PLAYER_BUTTON_X_POSITION = 767
SELECT_PLAYER_BUTTON_Y_POSITIONS = [247, 329, 411]
SELECT_PLAYER_2_BUTTON = pygame.image.load(f"{PATH}player_2_select_button.png")
SELECT_PLAYER_2_BUTTON_RECT = SELECT_PLAYER_2_BUTTON.get_rect(x=SELECT_PLAYER_BUTTON_X_POSITION,
                                                              y=SELECT_PLAYER_BUTTON_Y_POSITIONS[0])
SELECT_PLAYER_3_BUTTON = pygame.image.load(f"{PATH}player_3_select_button.png")
SELECT_PLAYER_3_BUTTON_RECT = SELECT_PLAYER_3_BUTTON.get_rect(x=SELECT_PLAYER_BUTTON_X_POSITION,
                                                              y=SELECT_PLAYER_BUTTON_Y_POSITIONS[1])
SELECT_PLAYER_4_BUTTON = pygame.image.load(f"{PATH}player_4_select_button.png")
SELECT_PLAYER_4_BUTTON_RECT = SELECT_PLAYER_4_BUTTON.get_rect(x=SELECT_PLAYER_BUTTON_X_POSITION,
                                                              y=SELECT_PLAYER_BUTTON_Y_POSITIONS[2])
SELECT_PLAYER = [
    [SELECT_PLAYER_2_BUTTON, SELECT_PLAYER_2_BUTTON_RECT, 'Player 2'],
    [SELECT_PLAYER_3_BUTTON, SELECT_PLAYER_3_BUTTON_RECT, 'Player 3'],
    [SELECT_PLAYER_4_BUTTON, SELECT_PLAYER_4_BUTTON_RECT, 'Player 4']
]

# Colour Select Button Parameters
COLOUR_BUTTON_X_POSITION = 780
COLOUR_BUTTON_Y_POSITIONS = [237, 299, 361, 423]
RED_BUTTON = pygame.image.load(f"{PATH}red_button.png")
RED_BUTTON_RECT = RED_BUTTON.get_rect(x=COLOUR_BUTTON_X_POSITION,
                                      y=COLOUR_BUTTON_Y_POSITIONS[0])
GREEN_BUTTON = pygame.image.load(f"{PATH}green_button.png")
GREEN_BUTTON_RECT = GREEN_BUTTON.get_rect(x=COLOUR_BUTTON_X_POSITION,
                                          y=COLOUR_BUTTON_Y_POSITIONS[1])
YELLOW_BUTTON = pygame.image.load(f"{PATH}yellow_button.png")
YELLOW_BUTTON_RECT = YELLOW_BUTTON.get_rect(x=COLOUR_BUTTON_X_POSITION,
                                            y=COLOUR_BUTTON_Y_POSITIONS[2])
BLUE_BUTTON = pygame.image.load(f"{PATH}blue_button.png")
BLUE_BUTTON_RECT = BLUE_BUTTON.get_rect(x=COLOUR_BUTTON_X_POSITION,
                                        y=COLOUR_BUTTON_Y_POSITIONS[3])
CHOOSE_COLOUR = [
    [RED_BUTTON, RED_BUTTON_RECT, RED, "red"],
    [GREEN_BUTTON, GREEN_BUTTON_RECT, GREEN, "green"],
    [YELLOW_BUTTON, YELLOW_BUTTON_RECT, YELLOW, "yellow"],
    [BLUE_BUTTON, BLUE_BUTTON_RECT, BLUE, "blue"]
]

# Special Round Button Parameters
SPECIAL_ROUND_BUTTON_X_POSITION = 730
SPECIAL_ROUND_BUTTON_Y_POSITION = 232
STOCK_DECK_DRAW_BUTTON = pygame.image.load(f"{PATH}draw_card_button.png")
FORFEIT_BUTTON = pygame.image.load(f"{PATH}forfeit_button.png")
SPECIAL_ROUND_BUTTON_RECT = STOCK_DECK_DRAW_BUTTON.get_rect(x=SPECIAL_ROUND_BUTTON_X_POSITION,
                                                            y=SPECIAL_ROUND_BUTTON_Y_POSITION)
# Play or Keep Button Parameters
PLAY_BUTTON_X_POSITION = 780
PLAY_BUTTON_Y_POSITION = 284
KEEP_BUTTON_Y_POSITION = 366
PLAY_BUTTON = pygame.image.load(f"{PATH}play_button.png")
PLAY_BUTTON_RECT = PLAY_BUTTON.get_rect(x=PLAY_BUTTON_X_POSITION,
                                        y=PLAY_BUTTON_Y_POSITION)
KEEP_BUTTON = pygame.image.load(f"{PATH}keep_button.png")
KEEP_BUTTON_RECT = KEEP_BUTTON.get_rect(x=PLAY_BUTTON_X_POSITION,
                                        y=KEEP_BUTTON_Y_POSITION)

# New Round Button Parameters
NEW_ROUND_BUTTON_X_POSITION = 550
NEW_ROUND_BUTTON_Y_POSITION = 550
NEW_ROUND_BUTTON = pygame.image.load(f"{PATH}play_new_round_button.png")
NEW_ROUND_BUTTON_RECT = NEW_ROUND_BUTTON.get_rect(x=NEW_ROUND_BUTTON_X_POSITION,
                                                  y=NEW_ROUND_BUTTON_Y_POSITION)


# Global Functions
def check_stock_deck(stock_deck, discard_deck):
    """
    Check if the stock deck is empty. If it is, shuffle the discard deck back into the stock deck pile,
    reset all black cards, and reveal one non-black card.
    """
    if len(stock_deck.cards_in_deck) == 0:
        stock_deck.cards_in_deck = discard_deck.cards_in_deck
        discard_deck.cards_in_deck = []
        random.shuffle(stock_deck.cards_in_deck)
        for card in stock_deck.cards_in_deck:
            if card.card_type in ('wild', 'wild_draw'):
                card.card_colour = 'black'
        while stock_deck.cards_in_deck[0].card_type in ('wild', 'wild_draw'):
            stock_deck.cards_in_deck.append(stock_deck.cards_in_deck.pop(0))
        discard_deck.cards_in_deck.append(stock_deck.cards_in_deck.pop(0))
