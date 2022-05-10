import logging
import time

from fool.card import Card, CardList
from fool.deck import Deck, Dump, Hand
from fool.players import HumanPlayer, Players
from fool.table import Table

log = logging.getLogger(__name__)


class Game:
    def __init__(self, players: Players):

        self.players = Players(players)
        self.deck = Deck()
        self.deck.shuffle()
        self.dump = Dump([])
        self.table = Table()

        self.human = False
        if any(isinstance(player, HumanPlayer) for player in self.players):
            self.human = True

        for player in self.players:
            player.hand = Hand([])
            player.take(self.deck.deal(6))

        trump = self.decide_trump(self.deck, self.players)
        self.deck.set_trump(trump)
        self.players.set_trump(trump)

        n, smallest_trump = self.players.decide_turn_order()

        print(f"Игроков: {len(self.players)}")
        print(f"Козырь: {Card.TRUMP_ICONS[self.deck.trump]}")
        if smallest_trump is not None:
            print(f"{players[n]} делает первый ход: {smallest_trump}")
        else:
            print(f"{players[n]} делает первый ход")
        print()

    @classmethod
    def decide_trump(cls, deck: Deck, players: Players) -> int:
        if not deck:
            return players[-1].hand[-1].suit
        else:
            deck.append(deck.pop(0))
            return deck[-1].suit

    def play(self):

        turn = 0
        while True:

            if turn == 100:
                raise RuntimeError("Слишком долгая игра.")

            turn += 1
            print(f"Раунд {turn}:")
            print(self.deck)
            print(self.players.report_hands(self.human))

            attacker = self.players[0]
            attacker.attacker = True
            attacker.attack_finished = False

            defender = self.players[1]
            defender.defender = True
            defender.defence_failed = False

            attacks_allowed = len(defender.hand)
            if turn == 1:
                attacks_allowed = 5
            attacks_performed = 0
            while attacks_performed <= attacks_allowed:

                card_attack = attacker.attack(
                    self.table,
                    self.dump,
                    self.deck,
                    defender.hand,
                )

                if card_attack is not None:

                    print(f"{attacker} атакует {card_attack}")
                    self.table.process_attack(card_attack)
                    if self.human:
                        print(self.table)
                    attacks_performed += 1

                    if not defender.defence_failed:

                        card_defence = defender.defend(
                            self.table,
                            self.dump,
                            self.deck,
                            attacker.hand,
                        )

                        if card_defence is not None:
                            print(f"{defender} отбивается {card_defence}")
                            self.table.process_defence(card_defence)
                            if self.human:
                                print(self.table)
                        else:
                            print(f"{defender} не может отбить {card_attack}")
                            defender.defence_failed = True

                else:
                    print(f"{attacker} исчерпал все возможные атаки.")
                    break

            if not defender.defence_failed and self.table.resolved:
                print(f"{defender} успешно побил все карты.")
                self.dump(self.table.dump())

            else:
                print(f"{defender} берёт {Hand(self.table.contents)}")
                defender.take(self.table.dump())

            print(self.players.report_hands(self.human))

            if len(self.players) == 2:
                if self.deck:
                    pass
                elif not attacker.hand and not defender.hand:
                    print("Ничья")
                    return attacker, defender, True
                elif not attacker.hand and defender.hand:
                    print(f"{defender} проигрывает")
                    return attacker, defender, False
                elif attacker.hand and not defender.hand:
                    print(f"{attacker} проигрывает")
                    return defender, attacker, False

            if not self.deck:
                if not attacker.hand:
                    print(f"{attacker} выходит из игры.")
                    self.players.remove(attacker)

                if not defender.hand:
                    print(f"{defender} выходит из игры.")
                    self.players.remove(defender)

            else:
                message = self.players.take_cards(self.deck, self.human)
                print(message)
                print(self.players.report_hands(self.human))

            self.players.rotate()
            if defender.defence_failed and defender in self.players:
                self.players.rotate()

            print()

            if self.human:
                time.sleep(1)
