import logging
import random
from typing import List

from fool.card import Card, CardList

log = logging.getLogger(__name__)


class Hand(CardList):
    def take(self, cards: List[Card]) -> None:

        if not isinstance(cards, list) or not all(isinstance(card, Card) for card in cards):
            raise TypeError(f"Невозможно взять в руку: {cards}")

        self._validate_cards(cards)
        self.extend(cards)

    def play(self, i: int) -> Card:

        if not self:
            raise IndexError("Невозможно сыграть карту. Рука пустая.")

        if i < 0 or i > len(self) - 1:
            raise IndexError(
                f"Невозможно выбрать карту {i}. Возможные значения: [0 - {len(self) - 1}]."
            )

        return self.pop(i)


class Dump(CardList):
    def __call__(self, cards: List[Card]) -> None:
        self._validate_cards(cards)
        self.extend(cards)


class Deck(CardList):
    def __init__(self):
        self.trump: int

        cards = []
        for value in range(9):
            for suit in range(4):
                cards.append(Card(value, suit))

        self._validate_cards(cards)
        super().__init__(cards)

    def shuffle(self):
        random.shuffle(self)

    def deal(self, n: int):
        if not self:
            log.debug("Колода пустая.")
            return []

        result = []
        for _ in range(n):
            try:
                result.append(self.pop())
            except IndexError:
                break

        log.debug(f"Сдаётся карт: {len(result)} {CardList(result)}")
        return result

    def set_trump(self, trump: int) -> None:
        self.trump = trump
        super().set_trump(trump)

    def __str__(self) -> str:
        condition: str = ""
        if len(self) <= 6:
            condition = str(len(self))
        elif len(self) < 18:
            condition = "меньше половины"
        else:
            condition = "больше половины"
        log.debug(f"Козырь: {Card.TRUMP_ICONS[self.trump]}, осталось карт в колоде: {len(self)}")
        return f"Козырь: {Card.TRUMP_ICONS[self.trump]}, осталось карт в колоде: {condition}"
