#!/usr/bin/env python3
from collections import Counter


# The next series of functions evaluates the hand...
# The straight flush needs to call methods that check for straight and flush
# but avoid calling is_straight, is_flush directly
def is_straight_flush(a_hand):
    return cards_all_same_suit(a_hand) and return_cards_rank_as_straight(a_hand)


# Same issue with a flush as we had with a straight - need a way to tell is_straight_flush
# that a hand is both straight and flush without calling those functions

def cards_all_same_suit(a_hand):
    # One step at a time: Extract the suit from the display hand
    suits = [a_card[1] for a_card in a_hand]
    # If the length of the Counter object is 1 then all the suits are the same
    return len(Counter(suits)) == 1


# For a flush, check if each hand has the same suit
# Use the Counter class to count how many of a given suit
# appears in the hand. If the count is 5, length of counter object is 1, a flush it it
def is_flush(a_hand):
    return cards_all_same_suit(a_hand) and not return_cards_rank_as_straight(a_hand)


# Need to be sure this 'straight' is not also a flush - else it would be a straight flush
def is_straight(a_hand):
    return return_cards_rank_as_straight(a_hand) and not cards_all_same_suit(a_hand)



def return_cards_rank_as_straight(a_hand):
    # Need to map character string ranks into numbers
    # There are oh-so-many ways to do this!

    # This will return a list of cards with the face cards
    # replaced by a number
    # If the hand has an Ace this function is called twice
    # once for Ace-low, once for Ace-high
    def generate_hand_with_mapped_picture_cards(map_picture_cards):
        # Map (change) picture cards to numerical equivalents
        # There's likely a more 'Pythonic' way to do this...
        pics_mapped_to_numbers = []
        for num_id_or_pic_card in ranks_maybe_with_face_cards:
            if num_id_or_pic_card not in map_picture_cards:
                pics_mapped_to_numbers.append(int(num_id_or_pic_card))
            else:
                pics_mapped_to_numbers.append(
                    map_picture_cards[num_id_or_pic_card])

        # Sort ranks....
        sorted_hand_by_rank = sorted(pics_mapped_to_numbers)
        # Check if this is a straight
        cards_are_straight = len(set(sorted_hand_by_rank)) == 5 and \
            sorted_hand_by_rank[4] - sorted_hand_by_rank[0] == 4

        return cards_are_straight

    # If we have an Ace we want two hands - one with the Ace low (1) the other with
    # Ace high (14).
    map_picture_cards_ace_high = {"Ace": 14,
                                  "King": 13, "Queen": 12, "Jack": 11}
    map_picture_cards_ace_low = {"Ace": 1, "King": 13, "Queen": 12, "Jack": 11}

    # Get the numbers on the cards may have picture cards
    ranks_maybe_with_face_cards = [a_card[0] for a_card in a_hand]
    # If hand has an Ace we call the above local function twice and save both mapped hands
    # Get the mapped cards, do sort, check ranges for both
    if "Ace" in ranks_maybe_with_face_cards:
        #
        high_cards_are_straight = generate_hand_with_mapped_picture_cards(
            map_picture_cards_ace_high)
        low_cards_are_straight = generate_hand_with_mapped_picture_cards(
            map_picture_cards_ace_low)

        return high_cards_are_straight or low_cards_are_straight

    else:
        # Doesn't matter which picture card map we pass to mapping function here
        return generate_hand_with_mapped_picture_cards(map_picture_cards_ace_low)


# The remaining hand types deal with frequencies of occurring ranks
# provides the distribution of ranks in the hand
def return_most_frequent_and_num_counter_elements(a_hand):
    # One step at a time: Extract the rank from the display hand
    rank = [a_card[0] for a_card in a_hand]
    count_a_hand = Counter(rank)
    most_frequent_card_count = count_a_hand.most_common()[0]

    return most_frequent_card_count[1], len(count_a_hand.most_common())


# If hand is 3-kind and counter length == 2
# then hand contains a three-kind and a pair
def is_full_house(a_hand):
    (most_frequent_card_count,
     len_count_object) = return_most_frequent_and_num_counter_elements(a_hand)
    return most_frequent_card_count == 3 and len_count_object == 2


# If hand is a pair and counter length == 3
# then hand contains a two pairs
def is_two_pairs(a_hand):
    (most_frequent_card_count,
     len_count_object) = return_most_frequent_and_num_counter_elements(a_hand)
    return most_frequent_card_count == 2 and len_count_object == 3


# See if there's a rank that occurs 4 times in the hand
def is_four_kind(a_hand):
    (most_frequent_card_count,
     len_count_object) = return_most_frequent_and_num_counter_elements(a_hand)
    return most_frequent_card_count == 4


# See if there's a rank that occurs 3 times in the hand
# For 3-kind we must check if there is a pair in the remaining cards - then it is a full house!
# Don't want the same hand to be a 3-kind and a full house!
def is_three_kind(a_hand):
    (most_frequent_card_count,
     len_count_object) = return_most_frequent_and_num_counter_elements(a_hand)

    return most_frequent_card_count == 3 and len_count_object != 2


# For pairs we want two occurring ranks and 4 distinct ranks in the counter
def is_pair(a_hand):
    (most_frequent_card_count,
     len_count_object) = return_most_frequent_and_num_counter_elements(a_hand)
    return most_frequent_card_count == 2 and len_count_object == 4
