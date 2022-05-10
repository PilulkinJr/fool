"""Имплементация карты и набора карт."""
import logging
from typing import List, Optional, Set

log = logging.getLogger(__name__)


class Card:
    """Карта."""

    VALUE_ICONS = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUIT_ICONS = ["♤", "♡", "♢", "♧"]
    TRUMP_ICONS = ["♠", "♥", "♦", "♣"]

    # NAMES = ["пики", "червы", "бубны", "крести"]

    def __init__(self, value: int, suit: int, trump: bool = False):
        """Карта.

        Parameters
        ----------
        value : int
            Достоиство карты.
        suit : int
            Масть карты.
        trump : bool, default = False
            Козырь.
        """
        self._trump: bool
        self._icon: str

        self._validate_value(value)
        self._value: int = value

        self._validate_suit(suit)
        self._suit: int = suit

        self.trump = trump

    @classmethod
    def _validate_value(cls, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value < 0 or value > len(cls.VALUE_ICONS) - 1:
            raise ValueError

    @property
    def value(self) -> int:
        """Достоиство карты."""
        return self._value

    @classmethod
    def _validate_suit(cls, suit: int) -> None:
        if not isinstance(suit, int):
            raise TypeError
        if suit < 0 or suit > len(cls.VALUE_ICONS) - 1:
            raise ValueError

    @property
    def suit(self) -> int:
        """Масть карты."""
        return self._suit

    @classmethod
    def _validate_trump(cls, trump: bool) -> None:
        if not isinstance(trump, bool):
            raise TypeError

    @property
    def trump(self) -> bool:
        """Козырная карта."""
        return self._trump

    @trump.setter
    def trump(self, trump: bool) -> None:
        self._validate_trump(trump)
        self._trump = trump
        if trump:
            self._icon = self.VALUE_ICONS[self._value].rjust(2) + self.TRUMP_ICONS[self._suit]
        else:
            self._icon = self.VALUE_ICONS[self._value].rjust(2) + self.SUIT_ICONS[self._suit]

    @property
    def icon(self) -> str:
        """Иконка карты."""
        return self._icon

    def __eq__(self, other) -> bool:
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.value, self.suit, self.trump) == (other.value, other.suit, other.trump)

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + f"value={self.value}, "
            + f"suit={self.suit}, "
            + f"trump={self.trump}"
            + ")"
        )

    def __str__(self) -> str:
        return self._icon


class CardList(list):
    def __init__(self, cards: List[Card]):
        self._validate_cards(cards)
        self.extend(cards)

    @classmethod
    def _validate_cards(cls, cards: List[Card]) -> None:
        for i, card_a in enumerate(cards):
            for _, card_b in enumerate(cards[i + 1 :]):
                if card_a == card_b:
                    raise RuntimeError(
                        f"{cards} содержит две одинаковые карты: {card_a} и {card_b}"
                    )
                if (card_a.trump and card_b.trump) and (card_a.suit != card_b.suit):
                    raise RuntimeError(
                        f"{cards} содержит два различных козыря: {card_a} и {card_b}"
                    )

    def __repr__(self) -> str:
        return self.__class__.__name__ + "([" + ", ".join(repr(card) for card in self) + "])"

    def __str__(self) -> str:
        return "[" + ",".join(str(card) for card in self) + "]"

    def set_trump(self, trump_suit: int) -> None:
        Card._validate_suit(trump_suit)
        for card in self:
            card.trump = card.suit == trump_suit

    @property
    def values(self) -> Set[int]:
        return {card.value for card in self}

    @property
    def suits(self) -> Set[int]:
        return {card.suit for card in self}

    @property
    def trumps(self) -> bool:
        return any(card.trump for card in self)
