import pytest

from fool.card import Card


class TestInit:

    card = Card(1, 1, trump=False)

    def test_value(self):
        assert self.card.value == 1

    def test_suit(self):
        assert self.card.suit == 1

    def test_trump(self):
        assert not self.card.trump

    def test_icon(self):
        assert self.card.icon == " 7♡"

    def test_repr(self):
        assert repr(self.card) == "Card(value=1, suit=1, trump=False)"

    def test_str(self):
        assert str(self.card) == " 7♡"


class TestInitTrump:

    card = Card(2, 2, trump=True)

    def test_value(self):
        assert self.card.value == 2

    def test_suit(self):
        assert self.card.suit == 2

    def test_trump(self):
        assert self.card.trump

    def test_icon(self):
        assert self.card.icon == " 8♦"

    def test_repr(self):
        assert repr(self.card) == "Card(value=2, suit=2, trump=True)"

    def test_str(self):
        assert str(self.card) == " 8♦"


class TestSetTrump:

    card = Card(3, 2, trump=False)
    card.trump = True

    def test_value(self):
        assert self.card.value == 3

    def test_suit(self):
        assert self.card.suit == 2

    def test_trump(self):
        assert self.card.trump

    def test_icon(self):
        assert self.card.icon == " 9♦"

    def test_repr(self):
        assert repr(self.card) == "Card(value=3, suit=2, trump=True)"

    def test_str(self):
        assert str(self.card) == " 9♦"


class TestInitWrong:
    def test_wrong_value_type(self):
        with pytest.raises(TypeError) as exc_info:
            self.card = Card("J", 1)
        print(exc_info.value)

    def test_wrong_value_value(self):
        with pytest.raises(ValueError) as exc_info:
            self.card = Card(11, 1)
        print(exc_info.value)

    def test_wrong_suit_type(self):
        with pytest.raises(TypeError) as exc_info:
            self.card = Card(1, "♦")
        print(exc_info.value)

    def test_wrong_suit_value(self):
        with pytest.raises(ValueError) as exc_info:
            self.card = Card(1, 7)
        print(exc_info.value)

    def test_wrong_trump_type(self):
        with pytest.raises(TypeError) as exc_info:
            self.card = Card(1, 1, trump=1)
        print(exc_info.value)


class TestEq:
    def test_eq(self):
        assert Card(1, 1, trump=False) == Card(1, 1, trump=False)

    def test_ne_trump(self):
        assert Card(1, 1, trump=False) != Card(1, 1, trump=True)

    def test_ne_value(self):
        assert Card(2, 1, trump=False) != Card(1, 1, trump=False)

    def test_ne_suit(self):
        assert Card(1, 2, trump=False) != Card(1, 1, trump=False)

    def test_ni(self):
        assert Card(1, 2, trump=False).__eq__((1, 2)) == NotImplemented
