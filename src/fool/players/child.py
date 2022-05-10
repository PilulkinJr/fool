import logging

from fool.deck import Deck, Dump, Hand
from fool.players.attacks import play_highest_value, play_lowest_value
from fool.players.defenses import defend_by_highest_value, defend_by_lowest_value
from fool.players.player import Player
from fool.table import Table

log = logging.getLogger(__name__)


class Child(Player):
    def attack(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        card = play_lowest_value(self.hand, table)
        if card is None:
            return None
        return self.play(self.hand.index(card))

    def defend(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        card = defend_by_lowest_value(self.hand, table)
        if card is None:
            return None
        return self.play(self.hand.index(card))


class Adult(Player):
    def attack(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        card = play_highest_value(self.hand, table)
        if card is None:
            return None
        return self.play(self.hand.index(card))

    def defend(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        card = defend_by_highest_value(self.hand, table)
        if card is None:
            return None
        return self.play(self.hand.index(card))
