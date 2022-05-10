"""Функции, реализующие простые тактики для атаки."""
import logging
import random
from collections import Counter
from typing import List, Optional

from fool.card import Card
from fool.deck import CardList, Dump
from fool.table import Table

log = logging.getLogger(__name__)


def legal_attacks(cards: List[Card], table: Table) -> List[Card]:
    """Составляет список карт, которые можно сыграть."""
    result = []

    log.debug("Достоиства карт на столе: %s", [str(value) for value in table.values])

    for card in cards:
        if card.value in table.values:
            result.append(card)

    if not result and not table.contents:
        result = cards

    log.debug("Возможные карты для атаки: %s", CardList(result))
    return result


def play_lowest_value(cards: List[Card], table: Table) -> Optional[Card]:
    """Сыграть наименьшую карту в руке."""

    def sort_key_func(card):
        return card.trump, card.value

    possible_moves = legal_attacks(cards, table)

    if possible_moves:
        card = sorted(possible_moves, key=sort_key_func)[0]
        log.debug("Наименьшая карта: %s", str(card))
        return card

    return None


def play_random_value(cards: List[Card], table: Table) -> Optional[Card]:
    """Сыграть случайную карту в руке."""
    possible_moves = legal_attacks(cards, table)

    if possible_moves:
        card = random.choice(possible_moves)
        log.debug("Случайная карта: %s", str(card))
        return card

    return None


def play_highest_value(cards: List[Card], table: Table) -> Optional[Card]:
    """Сыграть наибольшую карту в руке."""

    def sort_key_func(card):
        return card.trump, -card.value

    possible_moves = legal_attacks(cards, table)

    if possible_moves:
        card = sorted(possible_moves, key=sort_key_func)[0]
        log.debug("Наибольшая карта: %s", str(card))
        return card

    return None


def play_most_common_value(cards: List[Card], table: Table) -> Optional[Card]:
    """Сыграть карту с самым часто встречающимся достоинством."""
    possible_moves = legal_attacks(cards, table)

    values = Counter()
    for card in cards + table.attack_row:
        values.update({card.value: 1})

    for value, _ in values.most_common():
        for card in possible_moves:
            if card.value == value:
                return card

    return None


def play_least_common_suit(cards: List[Card], table: Table, dump: Dump) -> Optional[Card]:
    """Сыграть карту с наименее распространённой мастью."""
    possible_moves = legal_attacks(cards, table)

    suits = Counter()
    for card in dump + cards + table.defence_row:
        suits.update({card.suit: 1})

    for suit, _ in suits.most_common():
        for card in possible_moves:
            if card.suit == suit:
                return card

    return None
