import logging
from typing import List, Set

from fool.card import Card

log = logging.getLogger(__name__)


class Table:
    def __init__(self):
        self.attack_row = []
        self.defence_row = []

    def is_attack_legal(self, attack_card: Card) -> bool:
        if not self.contents:
            return True
        if attack_card.value in self.values:
            return True
        return False

    def is_defence_legal(self, defence_card: Card) -> bool:
        if not self.attack_row:
            raise RuntimeError("Невозможно отбиться: нет карт с атакующей стороны.")
        attack_card = self.attack_row[-1]
        if not defence_card.trump and attack_card.trump:
            return False
        if defence_card.trump and not attack_card.trump:
            return True
        if (defence_card.suit == attack_card.suit) and (defence_card.value > attack_card.value):
            return True
        return False

    def process_attack(self, card: Card) -> None:
        log.debug(f"Попытка актаковать {card}")
        if not self.is_attack_legal(card):
            log.error(f"Нелегальная атака {card}")
            raise ValueError(f"Атака {card} запрещена.")
        self.attack_row.append(card)

    def process_defence(self, card: Card) -> None:
        log.debug(f"Попытка покрыть {self.attack_row[-1]} <- {card}")
        if not self.is_defence_legal(card):
            log.error(f"Неленальная защита {self.attack_row[-1]} <- {card}")
            raise ValueError(f"Защита {card} запрещена.")
        self.defence_row.append(card)

    def __repr__(self) -> str:
        attack = " ".join(map(str, self.attack_row))
        defence = " ".join(map(str, self.defence_row))
        return "\n".join(
            (
                "",
                "Атака",
                attack,
                defence,
                "Защита",
                "",
            )
        )

    def dump(self) -> List[Card]:
        result = []
        while self.attack_row:
            result.append(self.attack_row.pop())
        while self.defence_row:
            result.append(self.defence_row.pop())
        return result

    def resolved(self) -> bool:
        if len(self.attack_row) == len(self.defence_row):
            return all(a > d for a, d in zip(self.attack_row, self.defence_row))
        return False

    @property
    def contents(self) -> List[Card]:
        return self.attack_row + self.defence_row

    @property
    def values(self) -> Set[int]:
        return {card.value for card in self.contents}

    @property
    def suits(self) -> Set[int]:
        return {card.suit for card in self.contents}
