import pytest

from fool.card import Card, CardList


class TestInit:
    c1 = Card(0, 0, trump=False)
    c2 = Card(1, 2, trump=True)
    cl = CardList([c1, c2])

    def test_repr(self):
        assert repr(self.cl) == f"CardList([{self.c1!r}, {self.c2!r}])"

    def test_str(self):
        assert str(self.cl) == f"[{self.c1!s},{self.c2!s}]"

    def test_values(self):
        assert self.cl.values == {0, 1}

    def test_suits(self):
        assert self.cl.suits == {0, 2}

    def test_trumps(self):
        assert self.cl.trumps


class TestInitWrong:
    def test_duplicate_card(self):
        with pytest.raises(RuntimeError) as exc_info:
            _ = CardList([Card(0, 0), Card(0, 1), Card(0, 0)])
        print(exc_info.value)

    def test_two_trumps(self):
        with pytest.raises(RuntimeError) as exc_info:
            _ = CardList([Card(0, 0, trump=True), Card(0, 1), Card(0, 1, trump=True)])
        print(exc_info.value)


class TestSetTrump:

    c1 = Card(0, 0, trump=False)
    c2 = Card(1, 2, trump=False)
    cl = CardList([c1, c2])
    cl.set_trump(2)

    def test_regular(self):
        assert not self.cl[0].trump

    def test_trump(self):
        assert self.cl[1].trump

    def test_trumps(self):
        assert self.cl.trumps
