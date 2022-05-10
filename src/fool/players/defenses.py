import logging
import random
from typing import List, Optional

from fool.card import Card
from fool.deck import CardList
from fool.table import Table

log = logging.getLogger(__name__)


def legal_defences(cards: List[Card], table: Table) -> List[Card]:
    """Формирует список возможных атак."""
    if not table.contents:
        raise RuntimeError

    result = []

    for card in cards:
        if table.is_defence_legal(card):
            result.append(card)

    log.debug("Возможные карты для защиты: %s", CardList(result))
    return result


def defend_by_lowest_value(cards: List[Card], table: Table) -> Optional[Card]:
    """Отбиться наименьшей возможной картой."""
    possible_moves = legal_defences(cards, table)

    def sort_key_func(card):
        return card.trump, card.value

    if possible_moves:
        card = sorted(possible_moves, key=sort_key_func)[0]
        log.debug("Наименьшая карта: %s", str(card))
        return card

    return None


def defend_by_random_value(cards: List[Card], table: Table) -> Optional[Card]:
    """Отбиться случайной картой."""
    possible_moves = legal_defences(cards, table)

    if possible_moves:
        card = random.choice(possible_moves)
        log.debug("Наименьшая карта: %s", str(card))
        return card

    return None


def defend_by_highest_value(cards: List[Card], table: Table) -> Optional[Card]:
    """Отбиться наименьшей возможной картой."""
    possible_moves = legal_defences(cards, table)

    def sort_key_func(card):
        return card.trump, -card.value

    if possible_moves:
        card = sorted(possible_moves, key=sort_key_func)[0]
        log.debug("Наибольшая карта: %s", str(card))
        return card

    return None
