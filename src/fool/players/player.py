import collections
import logging
import random
from typing import List, Optional

from fool.card import Card, CardList
from fool.deck import Deck, Dump, Hand
from fool.table import Table

log = logging.getLogger(__name__)


class Player:
    """Базовый класс для игрока."""

    def __init__(self, name: Optional[str] = None):

        self.name = name or self.__class__.__name__

        self.hand = Hand([])

        self.attacker = False
        self.attack_finished = False

        self.defender = False
        self.defence_failed = False

        self.rating = 1000

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"(name={self.name})"

    def __str__(self) -> str:
        return self.name

    def play(self, i: int) -> Optional[Card]:
        try:
            card = self.hand.play(i)
            log.debug("%s играет карту %s", self, card)
            return card
        except IndexError as exc_info:
            log.exception("Невозможно сыграть карту.", exc_info=exc_info)
            raise

    def take(self, cards: List[Card]) -> None:
        log.debug(f"{self} берёт {len(cards)} карт.")
        self.hand.take(cards)

    def set_trump(self, trump: int):
        self.hand.set_trump(trump)

    def expected_rating(self, opponent):
        return 1 / (1 + 10 ** ((opponent.rating - self.rating) / 400))

    def attack(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        raise NotImplementedError()

    def defence(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        raise NotImplementedError()


class Players(collections.deque):
    def __init__(self, players=None):
        if players is not None:
            self.extend(players)

        self.winners = {}

    def set_trump(self, trump: int) -> None:
        for player in self:
            player.set_trump(trump)

    def decide_turn_order(self):
        def sort_key(card):
            return not card.trump, card.value

        candidates = []
        for i, player in enumerate(self):
            card = sorted(player.hand, key=sort_key)[0]
            if card.trump:
                candidates.append((i, card))

        n = 0
        smallest = None
        if not candidates:
            n = random.randint(0, len(self) - 1)
            log.debug("Первый игрок выбран случайно.")
            return n, None
        else:
            n, smallest = sorted(candidates, key=lambda item: sort_key(item[1]))[0]
            log.debug(f"Наименьший козырь: {smallest}")
        self.rotate(-n)
        log.debug(f"{self[0]} делает первый ход")

        return n, smallest

    def take_cards(self, deck: Deck, human: bool = False) -> str:
        report = []
        for player in self:
            row = f"{player} получает карты из колоды: "
            n_cards = 6 - len(player.hand)
            log.debug(f"{player} нужно {n_cards} карт до полной руки.")
            if n_cards > 0 and deck:
                cards_dealt = deck.deal(n_cards)
                if isinstance(player, HumanPlayer) or not human:
                    row += str(CardList(cards_dealt))
                else:
                    row += str(len(cards_dealt))
                if not player.defence_failed:
                    player.take(cards_dealt)
            report.append(row)
        return "\n".join(report)

    def report_hands(self, human: bool = False) -> str:
        rows = []
        for player in self:
            row = player.name + f" карт: {len(player.hand)} "
            if human:
                if isinstance(player, HumanPlayer):
                    row += str(player.hand)
            else:
                row += str(player.hand)
            rows.append(row)
        return "\n".join(rows)


class HumanPlayer(Player):
    """Игрок-человек."""

    @property
    def cards_available(self):
        return ", ".join(f"{str(card).strip()}" for _, card in enumerate(self.hand))

    def valid_pick(self, pick: str):

        try:
            i = int(pick)
        except ValueError:
            # print(f"Не понимаю: {pick}")
            return False

        if i < 1 or i > len(self.hand):
            # print(f"Невозможно выбрать карту {i}.")
            return False

        return True

    def prompt(self, defence: bool = False) -> str:
        message = ""
        if defence:
            message = "Выберите карту для защиты"
        else:
            message = "Выберите карту для атаки"
        rows = []
        for i in range(len(self.hand) // 6 + 1):
            row = " ".join(str(card) for card in self.hand[6 * i : 6 * (i + 1)])
            rows.append(row)
        return "\n".join((message, *rows))

    def attack(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        while True:
            pick = input(f"{self.prompt()}\n(Enter для окончания атаки): ")
            if not pick:
                if not table.contents:
                    continue
                else:
                    return None
            if self.valid_pick(pick):
                i = int(pick) - 1
                if not table.contents or (self.hand[i].value in table.values):
                    return self.hand.play(i)
                else:
                    print("Запрещённый ход.")
                    continue

    def defend(self, table: Table, dump: Dump, deck: Deck, opponent_hand: Hand):
        while True:
            pick = input(f"{self.prompt(defence=True)}\n(Enter для окончания защиты): ")
            if not pick:
                return None
            if self.valid_pick(pick):
                i = int(pick) - 1
                card = self.hand[i]
                if table.is_defence_legal(card):
                    return self.play(i)
                else:
                    print("Неверный ход.")
            else:
                continue
