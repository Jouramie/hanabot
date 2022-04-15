from typing import List
import random
from simulator.game.card import Suit, Card, Rank


class DeckGenerator:

    def GenerateDeck(self, suits: List[Suit]) -> List[Card]:
        deck = []
        for suit in suits:
            deck.append(Card(suit, Rank.ONE))
            deck.append(Card(suit, Rank.ONE))
            deck.append(Card(suit, Rank.ONE))

            deck.append(Card(suit, Rank.TWO))
            deck.append(Card(suit, Rank.TWO))

            deck.append(Card(suit, Rank.THREE))
            deck.append(Card(suit, Rank.THREE))

            deck.append(Card(suit, Rank.FOUR))
            deck.append(Card(suit, Rank.FOUR))

            deck.append(Card(suit, Rank.FIVE))

        random.shuffle(deck)
        return deck
