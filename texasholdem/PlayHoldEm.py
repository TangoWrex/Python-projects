#!/usr/bin/env python3
"""PlayHoldEm Game.

Texas holdem is a 1 vs 1-8 computer player game.
the game randomly generates your cards. you're able to to bet
1 - 1000. at the end of the game all cards are shown and a winner
is returned
"""

from RankTheHand import is_straight, is_flush, is_straight_flush
from RankTheHand import is_full_house, is_two_pairs
from RankTheHand import is_pair, is_three_kind, is_four_kind
from itertools import product, combinations
from validator import enter_valid_character, enter_integer_in_range
from random import sample, randint


def gen_player_hand(the_deck, number_of_cards):
    """Gen_player_hand.

    Generates Players Hand
    the number of cards are how many cards are to be returned
    those cards are removed to only be used once.
    """
    a_hand = sample(the_deck, number_of_cards)

    for a_card in the_deck:
        if a_card in a_hand:
            the_deck.remove(a_card)
    # Ok - the list (the_deck) is changed
    return a_hand


def generate_the_flop(the_deck):
    """generate_the_flop.

    Generates 3 cards

    These are the first three community cards
    """
    the_flop_card = gen_player_hand(the_deck, 3)
    # the_flop = sample(the_deck, 3)
    return the_flop_card


def generate_a_card(the_deck):
    """generate_a_card.

    Generates 1 card. the 2nd and third round.
    """
    the_river_card = gen_player_hand(the_deck, 1)
    return the_river_card


def generate_deck():
    """generate_deck.

    This function creates the deck
    """
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank = ["Ace", "King", "Queen", "Jack"]
    # Remember - extends does not return anything - changes the list
    # in place so we need a list to start with
    rank.extend([str(rank_num) for rank_num in range(2, 11)])
    # Use the product function to generate the display card combinations
    display_cards = product(rank, suits)
    # Want the_deck as an indexable structure - a generator is not useful here
    return list(display_cards)


# Create num_players.
def create_players(the_deck, num_players):
    """create_players.

    a dictionary of players are created and given 2 cards,
    $1000. the amount of players is input by the user.
    """
    all_players = [{'name': f"Player_{int(player_num)}", 'amount_left': 1_000,
                    'player_hand': gen_player_hand(the_deck, 2),
                    'still_playing': True}
                   for player_num in range(1, num_players)]
    return all_players


# This function changes the pot by adding a player's bet,
# adjusts the amount hte player has left after the bet
# and prints the player name, bet amount, the pot amount
# and how much the player has left
def handle_a_bet(a_player, amount_to_bet, the_pot):
    """handle_a_bet.

    Player 1s bet is handlded here and counted in the pot
    """
    # Add amount to pot...deduct from a_player
    # Remember that players HAVE TO bet what you bet above
    amount_bet = enter_integer_in_range(f"Whats your bet {a_player['name']}?"
                                        f"(between {amount_to_bet} \
and {a_player['amount_left']})",
                                        amount_to_bet, a_player['amount_left'])
    # Change amount player has left - subtract bet amount from existing amount
    the_pot += amount_bet
    a_player['amount_left'] = a_player['amount_left'] - amount_bet

    print(f"{a_player['name']} bets {amount_bet}. The pot is at {the_pot}\
{a_player['name']} has \
${a_player['amount_left']} left")
    return the_pot, amount_bet


def handle_other_bets(a_player, amount_bet, the_pot):
    """handle_other_bets.

    This function brings amount_bet from player 1 and applied that to the
    rest of the players
    """
    # this pot is used to for the rest of the players
    the_pot += amount_bet
    a_player['amount_left'] = a_player['amount_left'] - amount_bet
    print(f"{a_player['name']} bets {amount_bet}. The pot is \
at {the_pot} {a_player['name']} has \
${a_player['amount_left']} left")
    return the_pot, amount_bet


def the_hand_is_a(player_hand):
    """the_hand_is_a.

    the hand is uses the rankthehand.py file to rank each hand
    """
    hand = {is_full_house: ("full house", 8),
            is_straight_flush: ("straight flush", 10),
            is_straight: ("straight", 6),
            is_four_kind: ("four of a kind", 9),
            is_two_pairs: ("two pairs", 4),
            is_flush: ("flush", 7),
            is_three_kind: ("three kind", 5),
            is_pair: ("pair", 3)}

    # Call the hand evaluation functions in succession;
    #  order really doesn't matter
    # - each hand is one and only one type
    for i, t in hand.items():
        if i(player_hand):
            return t
    # If we get here the hand has no real rank
    # Use 'Nothing' as the rank and 0 as the relative rank
    return ("Nothing", 0)


# Determine the best hand the player has out of the 5-7
# cards available in the hand
def the_players_best_hand(player_hand):
    """the_players_best_hand.

    We take all possible combinations of the players hand and run it
    against rankthehand.py.
    we then sort the tuple
    """
    # create a list of tuples containing a tuple
    # representing hand rank and the hand
    hand_tuple = [(the_hand_is_a(hand), hand)
                  for hand in combinations(player_hand, r=5)]

    # SORT the structure 'hand_by_type' by the NUMBER paired with the string
    # description of the hand type.
    # After the sort, return the first element
    # Depending on how you chose the numbers, you may have to sort in reverse
    hand_tuple.sort(key=lambda sort: sort[0][1], reverse=True)
    # We want the first one - not concerned if there's
    # several hands of the same
    # rank just return one of the best ones
    return hand_tuple[0]


# Want to return a list of structures that contain the player
# and the player's best hand
def return_all_players_best_hand(player_list):
    """return_all_players_best_hand.

    we iterate through each players best hand.
    each players hand is ran through the players best hand
    and the highest value is returned to pick_a_winner
    """
    return [(i, the_players_best_hand(i["player_hand"])) for i in player_list]


# Pick the highest hand
# Consider ONLY the rank - if there are two players with a pair,
# DO NOT determine who has the higher pair.
# Same for all ranks
#
# def pick_a_winner(rank):
#     """pick_a_winner.


#     """
#     # Sort the hand ranks contained in the argument passed to this function.

#     # Return the first element of the structure passed to this function

#     # Use a lambda to sort on the appropriate item.
#     # The appropriate item depends on the particulars
#     # of the argument passed to this function
#     # (pick_a_winner) which is the structure
#     # returned by function 'return_all_players_best_hand'
#     print("unknown")


def main():
    # Much of this is the same as the lab from lesson 9
    num_players = enter_integer_in_range(
        "Enter a number between 2 and 9, inclusive, for # players ", 2, 9)
    # Generate the deck
    the_deck = generate_deck()
    # Create the players
    # Each player gets TWO cards.....
    player_list = create_players(the_deck, num_players+1)
    # When you bet, the other players get to match your bet or fold (no raises)
    # the_flop = generate_the_flop(the_deck)
    # print(the_flop)
    the_pot = 0
    # Might as well...a bit easier to read
    you = player_list[0]
    print(f"Your hole cards: {you['player_hand']}")

    # # This will be flop, turn, river
    # # Create an empty list to hold the community cards
    community_cards = []
    if community_cards == []:
        print("No community cards are shown: ")

    # # The round is valid if there is an active player and
    # the river was displayed and bet on
    # # IOW, after the river is shown, a round of betting
    #  ensues. After that, the
    # # valid_bidding_round flag is False
    valid_bidding_round = True
    # # AND... need to keep track of active players
    # # If everyone folds, you win!
    everyone_folded = False

    # # The 'enter_valid_character' function in validator.py has a keyword
    # # parm that by default ignores case
    # # Hence, the use of "in 'Bb'" in the while loop
    # # Code a loop that will execute when the following condition is True:
    # # 1 - There is at least one active player
    # # 2 - This is a valid bidding round

    number_of_players = len(player_list)
    the_round = 1
    msg = "Do you bet or fold (B or F)?"
    while not everyone_folded and valid_bidding_round is True and \
            (player_1_action :=
             enter_valid_character(msg, ('B', 'F'))) != 'F' and the_round < 4:
        # Change flag - reset to False if there's a player that hasn't folded
        everyone_folded = True
        # Player_1 bets. Let's get the amount of the bet...
        the_pot, amount_bet = handle_a_bet(
            you, 1, the_pot)

        # Blank line to make outputs a bit easier to swallow
        print()

        # Now let's see what other players are gonna do
        # Other players may randomly play or fold
        # Let's weigh their actions toward fold
        # Remember - you are player_1 and your action was already tended to
        for player_idx in player_list[1:]:
            # if a_player.still_playing:
            if player_idx['still_playing']:
                player_wanna_bet = randint(1, 100) < 75
                if player_wanna_bet:
                    # Remember the _ means 'dont care' - we
                    # need only keep the bet amount
                    # for player_1 since other players must match it
                    the_pot, amount_bet = handle_other_bets(
                        player_idx, amount_bet, the_pot)
                    # Still got a live one!
                    everyone_folded = False

                else:
                    print(f"{player_idx['name']} folds")
                    # Take player out of the game....
                    player_idx['still_playing'] = False

        if len(community_cards) == 5:
            valid_bidding_round = False
        else:

            if the_round == 1:
                print("The Flop is shown")
                the_flop_cards = generate_the_flop(the_deck)
                for card in the_flop_cards:
                    community_cards.append(card)
                print(community_cards)
                the_round += 1

            elif the_round == 2:
                print("The Turn is shown:")
                the_turn_cards = generate_a_card(the_deck)
                for card in the_turn_cards:
                    community_cards.append(card)
                print(community_cards)
                the_round += 1

            elif the_round == 3:
                print("The river is shown:")
                the_river_cards = generate_a_card(the_deck)
                for card in the_river_cards:
                    community_cards.append(card)
                print(community_cards)
                the_round += 1

        # if you dont have any money left to bet the handle bet
        # function won't work
        # so you must break out of the loop
        if(you['amount_left'] == 0 and not everyone_folded):
            # get out of the while loop because you dont have any money left
            print("\nYou ran out of money so you must fold!\n")
            break

    # Well... if we get here because everyone folded, then you win!
    # If not, you folded and lost
    if(player_list[0]['still_playing'] is False and not everyone_folded):
        print(
            f"You win! The pot is {the_pot} and you have"
            f"{player_list[0]['amount_left'] + the_pot}")
    elif everyone_folded:
        print(f"You folded! You have {player_list[0]['amount_left']} left")

    else:
        print(f'these are community cards {community_cards}')
        active_players = []
        for active_player in range(0, number_of_players):
            if player_list[active_player]['still_playing']:
                active_players.append(player_list[active_player])

        for player in active_players:
            for card in community_cards:
                player['player_hand'].append(card)
            print(
                f"player{player['name']} has a hand of \
{player['player_hand']}")

        # Get the player's best hand from the 7 cards by name
        player_rank_and_best_hand = return_all_players_best_hand(
            active_players)

        # Print each player's name, best hand and rank of best hand
        # Items in the below print statements in the loop are
        # contained in the structure
        # player_rank_and_best_hand
        for hand_info in player_rank_and_best_hand:
            print(
                f"Player {hand_info[0]['name']} has a hand of \
{hand_info[0]['player_hand']}")
            print(f"Player {hand_info[0]['name']}'s best hand is\
{hand_info[1][1]} \n which is a {hand_info[1][0][0]}\n")
        # Pick and display the winning hand
        # No loop here - this is info for one player, right?
        # Items in the below print statements contained in the structure
        # player_and_winning_rank


if __name__ == "__main__":
    main()
